openerp.web_track_export = function(instance) {
    var _t = instance.web._t;
    instance.web.Sidebar.include({
        add_items: function(section_code, items) {
            var self = this;
            var user_id = -1;
            
            $.ajaxSetup({async:false});
            var allowed_user_id = new instance.web.Model("track.export").call("can_export", [[]]).then(function(result){  
                user_id = result;
            });     
            $.ajaxSetup({async:true});
            
            if (this.session.uid == user_id) {
                this._super.apply(this, arguments);
            }
            else {
                var export_label = _t("Export");
                var new_items = items;
                if (section_code == 'other') {
                    new_items = [];
                    for (var i = 0; i < items.length; i++) {
                        if (items[i]['label'] != export_label) {
                            new_items.push(items[i]);
                        };
                    };
                };
                if (new_items.length > 0) {
                    this._super.call(this, section_code, new_items);
                };
            }            
        },

    });

    instance.web.DataExport.include({         
          on_click_export_data: function () {
                this._super.apply(this, arguments);             
                var self = this;
                var exported_obj_fields = this.$el.find('#fields_list option').map(function () {
                    return {name: self.records[this.value] || this.value,
                            label: this.textContent || this.innerText};
                }).get();
                export_log = new instance.web.Model("track.export").call("create_log_line", [[this.dataset.model, exported_obj_fields, this.ids_to_export], this.dataset.context]);
          },
    });

};
