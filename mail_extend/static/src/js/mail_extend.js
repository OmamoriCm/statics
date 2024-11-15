openerp.mail_extend = function (instance) {
    var module   = instance.mail;
	
	module.Wall.include({
		bind_events: function(){
			var self = this;
			this._super();
			this.$(".cbc_mail_refresh").click(function (event) {
				var model = new instance.web.Model("fetchmail.server");
		        model.call("fetch_mails", {context: new instance.web.CompoundContext()}).then(function(result) {
                    if(self.root) {
	                    $('<span class="oe_mail-placeholder"/>').insertAfter(self.root.$el);
	                    self.root.destroy();
	                }
		            return self.message_render();
		        });
				
			});
			
        },
    });
    
};

