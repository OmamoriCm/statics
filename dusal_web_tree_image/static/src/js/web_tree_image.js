openerp.dusal_web_tree_image = function (instance) {
    instance.web.list.Imagen = instance.web.list.Column.extend({
        format: function (row_data, options) {
            if (!row_data[this.id] || !row_data[this.id].value) {
                return '';
            }
            var value = row_data[this.id].value, src;
            if (this.type === 'binary') {
                if (value && value.substr(0, 10).indexOf(' ') === -1) {
                    src = "data:image/png;base64," + value;
                } else {
                    src = instance.session.url('/web/binary/image', {model: options.model, field: this.id, id: options.id});
                }
            } else {
                if (!/\//.test(row_data[this.id].value)) {
                    src = '/web/static/src/img/icons/' + row_data[this.id].value + '.png';
                } else {
                    src = row_data[this.id].value;
                }
            }
            return instance.web.qweb.render('ListView.row.imagen', {widget: this, src: src});
        }
    });
    instance.web.list.columns.add('field.image', 'instance.web.list.Imagen');
};
