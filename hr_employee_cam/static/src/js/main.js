openerp.hr_employee_cam = function (instance, local) {
    
    local.CamWidget = instance.web.Widget.extend({
        template: 'CameraPreviewTemplate',
        init: function (parent) {
            this.parent = parent;
            this._super.apply(this, arguments);
            this.start();
        },
        start: function () {
            if (!this.check_media()) {
                instance.web.notification.do_warn('Media', 'Your browser not support media access');
            }

            var self = this;

            this.create_widget();
            this.open_stream().then(function (stream) {
                self.handle_stream(stream);
            }).catch(this.handle_stream_error);
        },
        check_media: function () {
            return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
        },
        create_widget: function () {
            this.renderElement();
            $('body').append(this.$el);
            this.video = this.$el.find('video').get(0);
            
            this.$el.on('shown.bs.modal', this, this.play_media);
            this.$el.on('hidden.bs.modal', this, this.close_media);
            this.defer = $.Deferred();
        },
        open_stream: function () {
            instance.web.blockUI();

            var constraints = _.defaults({
                video: true,
                audio: false
            });

            return navigator.mediaDevices.getUserMedia(constraints);
        },
        handle_stream: function (stream) {
            this.stream = stream;
            this.video.srcObject = stream;
            this.$el.modal('show');
        },
        handle_stream_error: function (error) {
            instance.web.unblockUI();
            instance.webclient.crashmanager.show_message(error);
        },
        handle_action: function (e) {
            var self = e.data;
            var $target = $(e.target);

            if (_.isEqual($target.data('action'), 'cancel')) {
                self.$el.modal('hide');
                return;
            }

            self.capture_image();
        },
        play_media: function (e) {
            var self = e.data;

            self.video.play();
            self.$el.find('button').on('click', self, self.handle_action);

            instance.web.unblockUI();
        },
        close_media: function (e) {
            var $target = $(e.target);
            var self = e.data;

            self.video.srcObject = null;
            _.each(self.stream.getTracks(), function (track) {
                track.stop();
            });

            if (_.isEqual($target.data('action'), 'cancel')) {
                self.defer.reject();
                return;
            }

            self.$el.remove();
        },
        capture_image: function () {
            var width = this.video.videoWidth;
            var height = this.video.videoHeight;
            
            var canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            canvas.getContext('2d').drawImage(this.video, 0, 0, width, height);

            this.defer.resolve(canvas.toDataURL());
            this.$el.modal('hide');
        },
        get_image: function () {
            return this.defer;
        }
    });

    if (instance.web && instance.web.FormView) {
        instance.web.FormView.include({
            on_click_cam: function () {
                var self = this;
                var widget = new local.CamWidget(this);

                widget.get_image().then(function (data) {
                    data = data.replace(/data:[a-zA-Z0-9]+\/[a-zA-Z0-9-.+]+.*,/, '');
                    self.set_values({
                        image_medium: data
                    });
                    self.save();
                });
            },
            start: function () {
                var self = this;
                self._super.apply(self, arguments);

                $.when(self.is_initialized).then(function () {
                    if (self.model !== 'hr.employee') {
                        return;
                    }
                    
                    self.sidebar.add_items('other', [
                        {
                            label: 'Tomar foto',
                            classname: 'oe_sidebar_action',
                            callback: self.on_click_cam
                        }
                    ]);
                });
            }
        });
    }
}
