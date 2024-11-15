(function() {
var instance = openerp;
var _t = instance.web._t;

// this only works after we leave the edited field

$(window).on('beforeunload', function () {
    if (window.document.getElementsByClassName('oe_form_dirty').length) {
        return _t("Warning, the record has been modified, your changes will be discarded.\n\nAre you sure you want to leave this page ?");
    }
})

})();
