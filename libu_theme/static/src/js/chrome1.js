instance.web.WebClient1 = instance.web.Client.extend({
    init: function(parent, client_options) {
        this._super(parent);
        if (client_options) {
            _.extend(this.client_options, client_options);
        }
        this._current_state = null;
        this.menu_dm = new instance.web.DropMisordered();
        this.action_mutex = new $.Mutex();
        this.set('title_part', {"zopenerp": "SONIC"});
    },
});
