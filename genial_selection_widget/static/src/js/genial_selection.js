(function() {

var instance = openerp;
var _t = instance.web._t,
   _lt = instance.web._lt;
var QWeb = instance.web.qweb;


instance.web.form.GenialSelection = instance.web.form.FieldMany2One.extend({
    init: function(field_manager, node) {
        this._super(field_manager, node);
        instance.web.form.CompletionFieldMixin.init.call(this);
        this.set({'value': false});
        this.display_value = {};
        this.display_value_backup = {};
        this.last_search = [];
        this.floating = false;
        this.current_display = null;
        this.is_started = false;
        this.ignore_focusout = false;
    },
    get_search_result: function(search_val) {
        var self = this;

        var dataset = new instance.web.DataSet(this, this.__parentedParent.fields.model_name.get('value'), self.build_context());
        this.last_query = search_val;
        var exclusion_domain = [], ids_blacklist = this.get_search_blacklist();
        if (!_(ids_blacklist).isEmpty()) {
            exclusion_domain.push(['id', 'not in', ids_blacklist]);
        }

        return this.orderer.add(dataset.name_search(
                search_val, new instance.web.CompoundDomain(self.build_domain(), exclusion_domain),
                'ilike', this.limit + 1, self.build_context())).then(function(data) {
            self.last_search = data;
            // possible selections for the m2o
            var values = _.map(data, function(x) {
                x[1] = x[1].split("\n")[0];
                return {
                    label: _.str.escapeHTML(x[1]),
                    value: x[1],
                    name: x[1],
                    id: x[0],
                };
            });

            // search more... if more results that max
            if (values.length > self.limit) {
                values = values.slice(0, self.limit);
                values.push({
                    label: _t("Искать ещё ..."),
                    action: function() {
                        dataset.name_search(search_val, self.build_domain(), 'ilike', 160).done(function(data) {
                            self._search_create_popup("search", data);
                        });
                    },
                    classname: 'oe_m2o_dropdown_option'
                });
            }
            // quick create
            var raw_result = _(data.result).map(function(x) {return x[1];});
            if (search_val.length > 0 && !_.include(raw_result, search_val) &&
                ! (self.options && (self.options.no_create || self.options.no_quick_create))) {
                values.push({
                    label: _.str.sprintf(_t('Создать "<strong>%s</strong>"'),
                        $('<span />').text(search_val).html()),
                    action: function() {
                        self._quick_create(search_val);
                    },
                    classname: 'oe_m2o_dropdown_option'
                });
            }
            // create...
            if (!(self.options && (self.options.no_create || self.options.no_create_edit))){
                values.push({
                    label: _t("Cоздать и изменить ..."),
                    action: function() {
                        self._search_create_popup("form", undefined, self._create_context(search_val));
                    },
                    classname: 'oe_m2o_dropdown_option'
                });
            }
            else if (values.length == 0)
                values.push({
                    label: _t("Нет результатов ..."),
                    action: function() {},
                    classname: 'oe_m2o_dropdown_option'
                });

            return values;
        });
    },
    render_editable: function() {
        var self = this;
        this.$input = this.$el.find("input");

        this.init_error_displayer();

        self.$input.on('focus', function() {
            self.hide_error_displayer();
        });

        this.$drop_down = this.$el.find(".oe_m2o_drop_down_button");
        this.$follow_button = $(".oe_m2o_cm_button", this.$el);

        this.$follow_button.click(function(ev) {
            ev.preventDefault();
            if (!self.get('value')) {
                self.focus();
                return;
            }
            var pop = new instance.web.form.FormOpenPopup(self);
            var context = self.build_context().eval();
            var model_obj = new instance.web.Model(self.__parentedParent.fields.model_name.get('value'));
            model_obj.call('get_formview_id', [self.get("value"), context]).then(function(view_id){
                pop.show_element(
                    self.__parentedParent.fields.model_name.get('value'),
                    self.get("value"),
                    self.build_context(),
                    {
                        title: _t("Open: ") + self.string,
                        view_id: view_id
                    }
                );
                pop.on('write_completed', self, function(){
                    self.display_value = {};
                    self.display_value_backup = {};
                    self.render_value();
                    self.focus();
                    self.trigger('changed_value');
                });
            });
        });

        // some behavior for input
        var input_changed = function() {
            if (self.current_display !== self.$input.val()) {
                self.current_display = self.$input.val();
                if (self.$input.val() === "") {
                    self.internal_set_value(false);
                    self.floating = false;
                } else {
                    self.floating = true;
                }
            }
        };
        this.$input.keydown(input_changed);
        this.$input.change(input_changed);
        this.$drop_down.click(function() {
            self.$input.focus();
            if (self.$input.autocomplete("widget").is(":visible")) {
                self.$input.autocomplete("close");
            } else {
                if (self.get("value") && ! self.floating) {
                    self.$input.autocomplete("search", "");
                } else {
                    self.$input.autocomplete("search");
                }
            }
        });

        // Autocomplete close on dialog content scroll
        var close_autocomplete = _.debounce(function() {
            if (self.$input.autocomplete("widget").is(":visible")) {
                self.$input.autocomplete("close");
            }
        }, 50);
        this.$input.closest(".modal .modal-content").on('scroll', this, close_autocomplete);

        self.ed_def = $.Deferred();
        self.uned_def = $.Deferred();
        var ed_delay = 200;
        var ed_duration = 15000;
        var anyoneLoosesFocus = function (e) {
            if (self.ignore_focusout) { return; }
            var used = false;
            if (self.floating) {
                if (self.last_search.length > 0) {
                    if (self.last_search[0][0] != self.get("value")) {
                        self.display_value = {};
                        self.display_value_backup = {};
                        self.display_value["" + self.last_search[0][0]] = self.last_search[0][1];
                        self.reinit_value(self.last_search[0][0]);
                        self.last_search = []
                    } else {
                        used = true;
                        self.render_value();
                    }
                } else {
                    used = true;
                }
                self.floating = false;
            }
            if (used && self.get("value") === false && ! self.no_ed && ! (self.options && (self.options.no_create || self.options.no_quick_create))) {
                self.ed_def.reject();
                self.uned_def.reject();
                self.ed_def = $.Deferred();
                self.ed_def.done(function() {
                    self.show_error_displayer();
                    ignore_blur = false;
                    self.trigger('focused');
                });
                ignore_blur = true;
                setTimeout(function() {
                    self.ed_def.resolve();
                    self.uned_def.reject();
                    self.uned_def = $.Deferred();
                    self.uned_def.done(function() {
                        self.hide_error_displayer();
                    });
                    setTimeout(function() {self.uned_def.resolve();}, ed_duration);
                }, ed_delay);
            } else {
                self.no_ed = false;
                self.ed_def.reject();
            }
        };
        var ignore_blur = false;
        this.$input.on({
            focusout: anyoneLoosesFocus,
            focus: function () { self.trigger('focused'); },
            autocompleteopen: function () { ignore_blur = true; },
            autocompleteclose: function () { setTimeout(function() {ignore_blur = false;},0); },
            blur: function () {
                // autocomplete open
                if (ignore_blur) { $(this).focus(); return; }
                if (_(self.getChildren()).any(function (child) {
                    return child instanceof instance.web.form.AbstractFormPopup;
                })) { return; }
                self.trigger('blurred');
            }
        });

        var isSelecting = false;
        // autocomplete
        this.$input.autocomplete({
            source: function(req, resp) {
                self.get_search_result(req.term).done(function(result) {
                    resp(result);
                });
            },
            select: function(event, ui) {
                isSelecting = true;
                var item = ui.item;
                if (item.id) {
                    self.display_value = {};
                    self.display_value_backup = {};
                    self.display_value["" + item.id] = item.name;
                    self.reinit_value(item.id);
                } else if (item.action) {
                    item.action();
                    // Cancel widget blurring, to avoid form blur event
                    self.trigger('focused');
                    return false;
                }
            },
            focus: function(e, ui) {
                e.preventDefault();
            },
            html: true,
            // disabled to solve a bug, but may cause others
            //close: anyoneLoosesFocus,
            minLength: 0,
            delay: 200,
        });
        var appendTo = this.$el.parents('.oe_view_manager_body, .modal-dialog').last();
        if (appendTo.length === 0){
            appendTo = '.oe_application > *';
        }
        this.$input.autocomplete({
            appendTo: appendTo
        });
        // set position for list of suggestions box
        this.$input.autocomplete( "option", "position", { my : "left top", at: "left bottom" } );
        this.$input.autocomplete("widget").openerpClass();
        // used to correct a bug when selecting an element by pushing 'enter' in an editable list
        this.$input.keyup(function(e) {
            if (e.which === 13) { // ENTER
                if (isSelecting)
                    e.stopPropagation();
            }
            isSelecting = false;
        });
        this.setupFocus(this.$follow_button);
    },
    render_value: function(no_recurse) {
        var self = this;
        if (! this.get("value")) {
            this.display_string("");
            return;
        }
        var display = this.display_value["" + this.get("value")];
        if (display) {
            this.display_string(display);
            return;
        }
        if (! no_recurse) {
            var dataset = new instance.web.DataSetStatic(this, this.__parentedParent.fields.model_name.get('value'), self.build_context());
            var def = this.alive(dataset.name_get([self.get("value")])).done(function(data) {
                if (!data[0]) {
                    self.do_warn(_t("Render"), _t("No value found for the field "+self.field.string+" for value "+self.get("value")));
                    return;
                }
                self.display_value["" + self.get("value")] = data[0][1];
                self.render_value(true);
            }).fail( function (data, event) {
                // avoid displaying crash errors as many2One should be name_get compliant
                event.preventDefault();
                self.display_value["" + self.get("value")] = self.display_value_backup["" + self.get("value")];
                self.render_value(true);
            });
            if (this.view && this.view.render_value_defs){
                this.view.render_value_defs.push(def);
            }
        }
    },
    display_string: function(str) {
        var self = this;
        if (!this.get("effective_readonly")) {
            this.$input.val(str.split("\n")[0]);
            this.current_display = this.$input.val();
            if (this.is_false()) {
                this.$('.oe_m2o_cm_button').css({'display':'none'});
            } else {
                this.$('.oe_m2o_cm_button').css({'display':'inline'});
            }
        } else {
            var lines = _.escape(str).split("\n");
            var link = "";
            var follow = "";
            link = lines[0];
            follow = _.rest(lines).join("<br />");
            if (follow)
                link += "<br />";
            var $link = this.$el.find('.oe_form_uri')
                 .unbind('click')
                 .html(link);
            if (! this.options.no_open)
                $link.click(function () {
                    var context = self.build_context().eval();
                    var model_obj = new instance.web.Model(this.__parentedParent.fields.model_name.get('value'));
                    model_obj.call('get_formview_action', [self.get("value"), context]).then(function(action){
                        self.do_action(action);
                    });
                    return false;
                 });
            $(".oe_form_m2o_follow", this.$el).html(follow);
        }
    },
    _quick_create: function(name) {
        var self = this;
        var slow_create = function () {
            self._search_create_popup("form", undefined, self._create_context(name));
        };
        if (self.options.quick_create === undefined || self.options.quick_create) {
            new instance.web.DataSet(this, this.__parentedParent.fields.model_name.get('value'), self.build_context())
                .name_create(name).done(function(data) {
                    if (!self.get('effective_readonly'))
                        self.add_id(data[0]);
                }).fail(function(error, event) {
                    event.preventDefault();
                    slow_create();
                });
        } else
            slow_create();
    },
    // all search/create popup handling
    _search_create_popup: function(view, ids, context) {
        var self = this;
        var pop = new instance.web.form.SelectCreatePopup(this);
        pop.select_element(
            self.__parentedParent.fields.model_name.get('value'),
            {
                title: (view === 'search' ? _t("Поиск: ") : _t("Создать: ")) + this.string,
                initial_ids: ids ? _.map(ids, function(x) {return x[0];}) : undefined,
                initial_view: view,
                disable_multiple_selection: true
            },
            self.build_domain(),
            new instance.web.CompoundContext(self.build_context(), context || {})
        );
        pop.on("elements_selected", self, function(element_ids) {
            self.add_id(element_ids[0]);
            self.focus();
        });
    },
});

instance.web.form.widgets = instance.web.form.widgets.extend({
    'genialSelection' : 'instance.web.form.GenialSelection',
})

})();