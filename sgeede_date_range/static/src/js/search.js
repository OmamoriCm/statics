openerp.sgeede_date_range = function(instance){
	var instance = openerp;
	var QWeb = instance.web.qweb,
      	_t =  instance.web._t,
     	_lt = instance.web._lt;


    instance.web.SearchView.include({
    	build_search_data: function () {
        var domains = [], contexts = [], groupbys = [], errors = [];

        this.query.each(function (facet) {
            var field = facet.get('field');
            try {
        // function that send the domain to odoo ?
        // if between domain is used (that have Advanced category
        //and 2 arrays inside it), split and insert the domain one by one
                var domain = field.get_domain(facet);
                var attributes = facet.get('category')
                if (domain) {
                    //change starts here
                    if (attributes === "Advanced") {
                        if (domain[0].length === 2) {
                            for (i in domain) {
                                domains.push(domain[i])
                            }
                         } else {
                            domains.push(domain);
                         }

                    } else {
                    //changes ends here
                    domains.push(domain);
                    };
                }
                var context = field.get_context(facet);
                if (context) {
                    contexts.push(context);
                }
                var group_by = field.get_groupby(facet);
                if (group_by) {
                    groupbys.push.apply(groupbys, group_by);
                }
            } catch (e) {
                if (e instanceof instance.web.search.Invalid) {
                    errors.push(e);
                } else {
                    throw e;
                }
            }
        });
        return {
            domains: domains,
            contexts: contexts,
            groupbys: groupbys,
            errors: errors
        };
    },
    });

    instance.web.search.ExtendedSearchProposition.DateTime.include({
    	operators: [
        {value: "=", text: _lt("is equal to")},
        {value: "!=", text: _lt("is not equal to")},
        {value: ">", text: _lt("greater than")},
        {value: "<", text: _lt("less than")},
        {value: ">=", text: _lt("greater or equal than")},
        {value: "<=", text: _lt("less or equal than")},
        {value: "∃", text: _lt("is set")},
        {value: "∄", text: _lt("is not set")},
        {value: "between", text: _lt("between")}
    	],

        format_label: function (format, field, operator) {
            //use a custom label from toStringBetween for between operators
            // otherwise use the default functions
            var between_label = this.toStringBetween()
            if (operator.value === "between") {
                var label = _.str.sprintf(format, {
                field: field.string,
                operator: operator.label || operator.text,
                value: between_label
                });
            } else {
                var label = _.str.sprintf(format, {
                field: field.string,
                // According to spec, HTMLOptionElement#label should return
                // HTMLOptionElement#text when not defined/empty, but it does
                // not in older Webkit (between Safari 5.1.5 and Chrome 17) and
                // Gecko (pre Firefox 7) browsers, so we need a manual fallback
                // for those
                operator: operator.label || operator.text,
                value: this
                });
            }
            return label;
        },

        toStringBetween: function () {
        str = instance.web.format_value(this.get_value(), { type:"datetime" });
        if (this.datewidget2 && this.datewidget2.get_value()) {
                str += ' and ' + instance.web.format_value(this.datewidget2.get_value(), { type:"datetime" });
            }
        return str;
        //function that provide the label for between field
        },

        start: function() {
            var ready = this._super();
            this.datewidget2 = new (this.widget())(this);
            this.datewidget2.appendTo(this.$el);
            this.$el.find("span:not(:first-child)").hide();
            return ready;
            //function to create the 2nd date field
        }
    });

    instance.web.search.ExtendedSearchProposition.Field.include({
    	get_domain: function (field, operator) {
	        switch (operator.value) {
	        case '∃': return this.make_domain(field.name, '!=', false);
	        case '∄': return this.make_domain(field.name, '=', false);
	        case 'between': return [[field.name ,'>=',this.datewidget.get_value()],[field.name,'<=',this.datewidget2.get_value()]]
	        default: return this.make_domain(
	            field.name, operator.value, this.get_value());
	        }
	        // function that created the domain filter
    	},
    });

    instance.web.search.ExtendedSearchProposition.include({
    	operator_changed: function (e) {
	        var $value = this.$('.searchview_extended_prop_value');
	        switch ($(e.target).val()) {
	        case '∃':
	        case '∄':
	            $value.hide();
	            break;
            case 'between':
                $value.show();
                $value.find("span > span").show();
                break;
	        default:
	            $value.show();
                $value.find("span > span:not(:first-child)").hide();
                //hide the 2nd input field when not in between
	        }
	        // the component that hide the fields fields when switching filters, operators
    	},
    });

    instance.web.search.ExtendedSearchProposition.Date.include({
        toStringBetween: function () {
        str = instance.web.format_value(this.get_value(), { type:"date" });
        if (this.datewidget2 && this.datewidget2.get_value()) {
                str += ' and ' + instance.web.format_value(this.datewidget2.get_value(), { type:"date" });
            }
        return str;
        }
        //toStringBetween for Date field filter
    });
};