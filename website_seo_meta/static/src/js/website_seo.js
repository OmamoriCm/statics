openerp.define('website.seo', function (require) {
'use strict';

var core = require('web.core');
var ajax = require('web.ajax');
var Class = require('web.Class');
var Dialog = require('web.Dialog');
var mixins = require('web.mixins');
var Model = require('web.Model');
var Widget = require('web.Widget');
var base = require('web_editor.base');
var website = require('website.website');

var _t = core._t;

var qweb = core.qweb;

ajax.loadXML('/website/static/src/xml/website.seo.xml', qweb);
// reworked header 
ajax.loadXML('/website_seo_meta/static/src/xml/header.xml', qweb);

    // This replaces \b, because accents(e.g. à, é) are not seen as word boundaries.
    // Javascript \b is not unicode aware, and words beginning or ending by accents won't match \b
    var WORD_SEPARATORS_REGEX = '([\\u2000-\\u206F\\u2E00-\\u2E7F\'!"#\\$%&\\(\\)\\*\\+,\\-\\.\\/:;<=>\\?¿¡@\\[\\]\\^_`\\{\\|\\}~\\s]+|^|$)';

function analyzeKeyword(htmlPage, keyword) {
    return  htmlPage.isInTitle(keyword) ? {
                title: 'label label-primary',
                description: "This keyword is used in the page title",
            } : htmlPage.isInDescription(keyword) ? {
                title: 'label label-info',
                description: "This keyword is used in the page description",
            } : htmlPage.isInBody(keyword) ? {
                title: 'label label-info',
                description: "This keyword is used in the page content."
            } : {
                title: 'label label-default',
                description: "This keyword is not used anywhere on the page."
            };
}

var Suggestion = Widget.extend({
    template: 'website.seo_suggestion',
    events: {
        'click .js_seo_suggestion': 'select',
    },
    init: function (parent, options) {
        this.root = options.root;
        this.keyword = options.keyword;
        this.language = options.language;
        this.htmlPage = options.page;
        this._super(parent);
    },
    start: function () {
        this.htmlPage.on('title-changed', this, this.renderElement);
        this.htmlPage.on('description-changed', this, this.renderElement);
    },
    analyze: function () {
        return analyzeKeyword(this.htmlPage, this.keyword);
    },
    highlight: function () {
        return this.analyze().title;
    },
    tooltip: function () {
        return this.analyze().description;
    },
    select: function () {
        this.trigger('selected', this.keyword);
    },
});

var SuggestionList = Widget.extend({
    template: 'website.seo_suggestion_list',
    init: function (parent, options) {
        this.root = options.root;
        this.language = options.language;
        this.htmlPage = options.page;
        this._super(parent);
    },
    start: function () {
        this.refresh();
    },
    refresh: function () {
        var self = this;
        self.$el.append(_t("Loading..."));
        var language = self.language || base.get_context().lang.toLowerCase();
        ajax.jsonRpc('/website/seo_suggest', 'call', {
            'keywords': self.root,
            'lang': language,
        }).then(function (keyword_list) {
            self.addSuggestions(JSON.parse(keyword_list));
        });
    },
    addSuggestions: function (keywords) {
        var self = this;
        self.$el.empty();
        // TODO Improve algorithm + Ajust based on custom user keywords
        var regex = new RegExp(self.root, "gi");
        var keywords = _.map(_.uniq(keywords), function (word) {
            return word.replace(regex, "").trim();
        });
        // TODO Order properly ?
        _.each(keywords, function (keyword) {
            if (keyword) {
                var suggestion = new Suggestion(self, {
                    root: self.root,
                    language: self.language,
                    keyword: keyword,
                    page: self.htmlPage,
                });
                suggestion.on('selected', self, function (word, language) {
                    self.trigger('selected', word, language);
                });
                suggestion.appendTo(self.$el);
            }
        });
     },
});

var Keyword = Widget.extend({
    template: 'website.seo_keyword',
    events: {
        'click a[data-action=remove-keyword]': 'destroy',
    },
    maxWordsPerKeyword: 4, // TODO Check
    init: function (parent, options) {
        this.keyword = options.word;
        this.language = options.language;
        this.htmlPage = options.page;
        this._super(parent);
    },
    start: function () {
        this.htmlPage.on('title-changed', this, this.updateLabel);
        this.htmlPage.on('description-changed', this, this.updateLabel);
        this.suggestionList = new SuggestionList(this, {
            root: this.keyword,
            language: this.language,
            page: this.htmlPage,
        });
        this.suggestionList.on('selected', this, function (word, language) {
            this.trigger('selected', word, language);
        });
        this.suggestionList.appendTo(this.$('.js_seo_keyword_suggestion'));
    },
    analyze: function () {
        return analyzeKeyword(this.htmlPage, this.keyword);
    },
    highlight: function () {
        return this.analyze().title;
    },
    tooltip: function () {
        return this.analyze().description;
    },
    updateLabel: function () {
        var cssClass = "oe_seo_keyword js_seo_keyword " + this.highlight();
        this.$(".js_seo_keyword").attr('class', cssClass);
        this.$(".js_seo_keyword").attr('title', this.tooltip());
    },
    destroy: function () {
        this.trigger('removed');
        this._super();
    },
});

var KeywordList = Widget.extend({
    template: 'website.seo_list',
    maxKeywords: 10,
    init: function (parent, options) {
        this.htmlPage = options.page;
        this._super(parent);
    },
    start: function () {
        var self = this;
        var existingKeywords = self.htmlPage.keywords();
        if (existingKeywords.length > 0) {
            _.each(existingKeywords, function (word) {
                self.add.call(self, word);
            });
        }
    },
    keywords: function () {
        var result = [];
        this.$('.js_seo_keyword').each(function () {
            result.push($(this).data('keyword'));
        });
        return result;
    },
    isFull: function () {
        return this.keywords().length >= this.maxKeywords;
    },
    exists: function (word) {
        return _.contains(this.keywords(), word);
    },
    add: function (candidate, language) {
        var self = this;
        // TODO Refine
        var word = candidate ? candidate.replace(/[,;.:<>]+/g, " ").replace(/ +/g, " ").trim().toLowerCase() : "";
        if (word && !self.isFull() && !self.exists(word)) {
            var keyword = new Keyword(self, {
                word: word,
                language: language,
                page: this.htmlPage,
            });
            keyword.on('removed', self, function () {
               self.trigger('list-not-full');
               self.trigger('removed', word);
            });
            keyword.on('selected', self, function (word, language) {
                self.trigger('selected', word, language);
            });
            keyword.appendTo(self.$el);
        }
        if (self.isFull()) {
            self.trigger('list-full');
        }
    },
});

var Image = Widget.extend({
    template: 'website.seo_image',
    init: function (parent, options) {
        this.src = options.src;
        this.alt = options.alt;
        this._super(parent);
    },
});

var ImageList = Widget.extend({
    init: function (parent, options) {
        this.htmlPage = options.page;
        this._super(parent);
    },
    start: function () {
        var self = this;
        this.htmlPage.images().each(function (index, image) {
            new Image(self, image).appendTo(self.$el);
        });
    },
    images: function () {
        var result = [];
        this.$('input').each(function () {
           var $input = $(this);
           result.push({
               src: $input.attr('src'),
               alt: $input.val(),
           });
        });
        return result;
    },
    add: function (image) {
        new Image(this, image).appendTo(this.$el);
    },
});

var Preview = Widget.extend({
    template: 'website.seo_preview',
    init: function (parent, options) {
        this.title = options.title.slice(0,options.googleSERPTitleSize);
            if (this.title != options.title) {
                this.title = this.title.concat("...");
            }
            
        if (options.url.indexOf("https") != 0) {
            this.url = options.url.slice(7,options.httpURLSize); // "http://" is 7
        } else {
            this.url = options.url.slice(0,options.httpsURLSize);
        }
        if (this.url != options.url) {
            this.url = this.url.concat("...");
        }
        this.description = options.description || "[ The description will be generated by Google unless you specify one. ]"; // .slice(0,options.googleSERPDescriptionSize)
        this.description = this.description.slice(0,options.googleSERPDescriptionSize)
        this._super(parent);
    },
});

var HtmlPage = Class.extend(mixins.PropertiesMixin, {
    url: function () {
        var url = window.location.href;
        var hashIndex = url.indexOf('#');
        return hashIndex >= 0 ? url.substring(0, hashIndex) : url;
    },
    title: function () {
        var $title = $('title'); // prepopulated, thus never empty
        return ($title.length > 0) && $title.text() && $title.text().trim();
    },
    changeTitle: function (title) {
        // TODO create tag if missing
        $('title').text(title);
        this.trigger('title-changed', title);
    },
    description: function () {
        var $description = $('meta[name=description]'); // in case 'description' is empty (would return false)
        return ($description.length > 0) && ($description.attr('content') && $description.attr('content').trim());
    },
    changeDescription: function (description) {
        // TODO create tag if missing
        $('meta[name=description]').attr('content', description);
        this.trigger('description-changed', description);
    },
    keywords: function () {
        var $keywords = $('meta[name=keywords]');
        var parsed = ($keywords.length > 0) && $keywords.attr('content') && $keywords.attr('content').split(",");
        return (parsed && parsed[0]) ? parsed: [];
    },
    changeKeywords: function (keywords) {
        // TODO create tag if missing
        $('meta[name=keywords]').attr('content', keywords.join(","));
        this.trigger('keywords-changed', keywords);
    },
    headers: function (tag) {
        return $('#wrap '+tag).map(function () {
            return $(this).text();
        });
    },
    images: function () {
        return $('#wrap img').map(function () {
            var $img = $(this);
            return  {
                src: $img.attr('src'),
                alt: $img.attr('alt'),
            };
        });
    },
    company: function () {
        return $('html').attr('data-oe-company-name');
    },
    bodyText: function () {
        return $('body').children().not('.js_seo_configuration').text();
    },
    isInBody: function (text) {
        return new RegExp(WORD_SEPARATORS_REGEX+text+WORD_SEPARATORS_REGEX, "gi").test(this.bodyText());
    },
    isInTitle: function (text) {
        return new RegExp(WORD_SEPARATORS_REGEX+text+WORD_SEPARATORS_REGEX, "gi").test(this.title());
    },
    isInDescription: function (text) {
        return new RegExp(WORD_SEPARATORS_REGEX+text+WORD_SEPARATORS_REGEX, "gi").test(this.description());
    },
});

var Tip = Widget.extend({
    template: 'website.seo_tip',
    events: {
        'closed.bs.alert': 'destroy',
    },
    init: function (parent, options) {
        this.message = options.message;
        // cf. http://getbootstrap.com/components/#alerts
        // success, info, warning or danger
        this.type = options.type || 'info';
        this._super(parent);
    },
});

var Configurator = Dialog.extend({
    template: 'website.seo_configuration',
    events: {
        'keyup input[name=seo_page_keywords]': 'confirmKeyword',
        'blur input[name=seo_page_title]': 'titleChanged',
        'blur textarea[name=seo_page_description]': 'descriptionChanged',
        'click button[data-action=add]': 'addKeyword',
    },
    canEditTitle: false,
    canEditDescription: false,
    canEditKeywords: false,
    canEditLanguage: false,
    maxTitleSize: 120, // limit for site name SERP is 600 pixel (~70 char.), but Title size is not limited
    maxDescriptionSize: 320,  // Google limit in november 2017
    googleSERPTitleSize: 70, // Bing is 40, Yandex ?
    googleSERPDescriptionSize: 165, // Google display in some cases
    httpURLSize: 78,
    httpsURLSize: 90,
    minTitleWord: 10,
    maxTitleWord: 12,

    init: function (parent, options) {
        options = options || {};
        _.defaults(options, {
            title: _t('Promote This Page'),
            subtitle: _t('Give this page more visibility in Google search results to attract more visitors.'),
            buttons: [
                {text: _t('Save'), classes: 'btn-primary', click: this.update},
                {text: _t('Discard'), close: true},
            ],
        });

        this._super(parent, options);
    },
    start: function () {
        var self = this;

        this.$modal.addClass('oe_seo_configuration js_seo_configuration');

        this.htmlPage = new HtmlPage();
        this.$('.js_seo_page_url').text(this.htmlPage.url());
        this.$('input[name=seo_page_title]').val(this.htmlPage.title());
        this.$('textarea[name=seo_page_description]').val(this.htmlPage.description());

        this.keywordList = new KeywordList(self, { page: this.htmlPage });
        this.keywordList.on('list-full', self, function () {
            self.$('input[name=seo_page_keywords]').attr({
                readonly: "readonly",
                placeholder: "Remove a keyword first"
            });
            self.$('button[data-action=add]').prop('disabled', true).addClass('disabled');
        });
        this.keywordList.on('list-not-full', self, function () {
            self.$('input[name=seo_page_keywords]').removeAttr('readonly').attr('placeholder', "");
            self.$('button[data-action=add]').prop('disabled', false).removeClass('disabled');
        });
        this.keywordList.on('selected', self, function (word, language) {
            self.keywordList.add(word, language);
        });
        this.keywordList.appendTo(this.$('.js_seo_keywords_list'));
        this.disableUnsavableFields();
        this.renderPreview();
        this.getLanguages();
    },
    getLanguages: function () {
        var self = this;
        ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'website',
            method: 'get_languages',
            args: [[base.get_context().website_id]],
            kwargs: {context: base.get_context()}
        }).then( function (data) {
            self.$('#language-box').html(core.qweb.render('Configurator.language_promote', {
                'language': data,
                'def_lang': base.get_context().lang
            }));
        });
    },
    disableUnsavableFields: function () {
        var self = this;
        this.loadMetaData().then(function (data) {
            self.canEditTitle = data && ('website_meta_title' in data);
            self.canEditDescription = data && ('website_meta_description' in data);
            self.canEditKeywords = data && ('website_meta_keywords' in data);
            if (!self.canEditTitle) {
                self.$('input[name=seo_page_title]').attr('disabled', true);
            }
            if (!self.canEditDescription) {
                self.$('textarea[name=seo_page_description]').attr('disabled', true);
            }
            if (!self.canEditTitle && !self.canEditDescription && !self.canEditKeywords) {
                self.$footer.find('button[data-action=update]').attr('disabled', true);
            }
        });
    },
    suggestImprovements: function () {
        var self = this;
        var tips = [];
        _.each(tips, function (tip) {
            displayTip(tip.message, tip.type);
        });

        function displayTip(message, type) {
            new Tip(self, {
               message: message,
               type: type,
            }).appendTo(self.$('.js_seo_tips'));
        }
    },
    confirmKeyword: function (e) {
        if (e.keyCode == 13) {
            this.addKeyword();
        }
    },
    addKeyword: function (word) {
        var $input = this.$('input[name=seo_page_keywords]');
        var $language = this.$('select[name=seo_page_language]');
        var keyword = _.isString(word) ? word : $input.val();
        var language = $language.val().toLowerCase();
        this.keywordList.add(keyword, language);
        $input.val("");
    },
    update: function () {
        var self = this;
        var data = {};
        if (this.canEditTitle) {
            data.website_meta_title = this.htmlPage.title();
        }
        if (this.canEditDescription) {
            data.website_meta_description = this.htmlPage.description();
        }
        if (this.canEditKeywords) {
            data.website_meta_keywords = this.keywordList.keywords().join(", ");
        }
        this.saveMetaData(data).then(function () {
           self.close();
        });
    },
    getMainObject: function () {
        var repr = $('html').data('main-object');
        var m = repr.match(/(.+)\((\d+),(.*)\)/);
        if (!m) {
            return null;
        } else {
            return {
                model: m[1],
                id: m[2]|0
            };
        }
    },
    loadMetaData: function () {
        var obj = this.getMainObject();
        var def = $.Deferred();
        if (!obj) {
            // return $.Deferred().reject(new Error("No main_object was found."));
            def.resolve(null);
        } else {
            var fields = ['website_meta_title', 'website_meta_description', 'website_meta_keywords'];
            var model = new Model(obj.model).call('read', [[obj.id], fields, base.get_context()]).then(function (data) {
                if (data.length) {
                    var meta = data[0];
                    meta.model = obj.model;
                    def.resolve(meta);
                } else {
                    def.resolve(null);
                }
            }).fail(function () {
                def.reject();
            });
        }
        return def;
    },
    saveMetaData: function (data) {
        var obj = this.getMainObject();
        if (!obj) {
            return $.Deferred().reject();
        } else {
            return new Model(obj.model).call('write', [[obj.id], data, base.get_context()]);
        }
    },
    titleChanged: function () {
        var self = this;
        _.defer(function () {
            var title = self.$('input[name=seo_page_title]').val();
            self.htmlPage.changeTitle(title);
            self.renderPreview();
        });
    },
    descriptionChanged: function () {
        var self = this;
        _.defer(function () {
            var description = self.$('textarea[name=seo_page_description]').val();
            self.htmlPage.changeDescription(description);
            self.renderPreview();
        });
    },
    renderPreview: function () {
        var preview = new Preview(this, {
            title: this.htmlPage.title(),
            description: this.htmlPage.description(),
            url: this.htmlPage.url(),
            httpURLSize: this.httpURLSize,             
            httpsURLSize: this.httpsURLSize,
            googleSERPTitleSize: this.googleSERPTitleSize,
            googleSERPDescriptionSize: this.googleSERPDescriptionSize,
        });
        var $preview = this.$('.js_seo_preview');
        $preview.empty();
        preview.appendTo($preview);
    },
    destroy: function () {
        this.htmlPage.changeKeywords(this.keywordList.keywords());
        this._super.apply(this, arguments);
    },
});

website.TopBar.include({
    start: function () {
        this.$el.on('click', 'a[data-action=promote-current-page]', function () {
            new Configurator(this).open();
        });
        return this._super();
    }
});

return {
    Configurator: Configurator,
};

});
