openerp.ic_web_timesheet = function(instance) {
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;
    
    instance.hr_timesheet_sheet.WeeklyTimesheet.include({
    	init: function() {
			var res = this._super.apply(this, arguments);
			var self = this;
			self.hours_per_day = 8;
			var user_obj = new instance.web.Model('res.users');
			var company_obj = new instance.web.Model('res.company');
			user_obj.get_func('read')(self.session.uid, ['company_id']).then(function(res) {
				company_obj.get_func('read')(res['company_id'][0], ['timesheet_day_duration']).then(function(res) {
					self.hours_per_day = res['timesheet_day_duration'];
				});
			});			
		},
		initialize_content: function() {
            var self = this;
            if (self.setting)
                return;

            self.account_read_only = {};
            var accounts = _(self.get("sheets")).chain().map(function(el) {
            	// much simpler to use only the id in all cases
            	if (typeof(el.account_id) === "object")
            		el.account_id = el.account_id[0];
            	return el;
            }).groupBy("account_id").value();
            var account_ids = _.map(_.keys(accounts), function(el) { return el === "false" ? false : Number(el) });
			new instance.web.Model('account.analytic.account').get_func('read')(account_ids, ['ts_readonly']).then(function(res) {
				_.each(res, function(account) {
					self.account_read_only[account.id] = account.ts_readonly;
				});
			});
			return self._super.apply(this, arguments);
        },
    	display_data: function() {
    		var self = this;
    		self.week_pager_mode = self.dates.length > 7 ? true : false;
    		self.current_week = self.get_week();
    		
    		self.date_week = {};
    		self.week_day = {1: {days_count:[], working_days: 0}};
    		self.total_working_days = 0;
			var week = 1;
			_.each(_.range(self.dates.length), function(day_count) {
				var day = self.dates[day_count].getDay();
				self.date_week[self.dates[day_count]] = week;
				self.week_day[week].days_count.push(day_count);
				self.week_day[week].working_days += (day != 0 && day != 6) ? 1 : 0;
				self.total_working_days += (day != 0 && day != 6) ? 1 : 0;
				if (day == 0 && day_count != self.dates.length - 1) {
					week += 1;
					self.week_day[week] = {days_count:[], working_days: 0};
				}
			});
			self.total_weeks = week;
			
			self.add_day_before = 0;
			self.add_day_after = 0;
			if (self.dates.length) {
				var day = self.dates[0].getDay();
				day = day == 0 ? 7 : day;
				for (var i=1; i<day; i++) {
					self.add_day_before++;
				}
				day = self.dates[self.dates.length-1].getDay();
				day = day == 0 ? 7 : day;
				for (var i=day; i<7; i++) {
					self.add_day_after++;
				}
			}
			
			self.accounts_by_id = {};
			self.lines = {};
			_.each(self.accounts, function(account) {
				self.lines[account.account] = {};
				_.each(_.range(account.days.length), function(day_count) {
					var day = account.days[day_count];
					self.lines[account.account][day_count] = {};
					var description = '';
					var has_empty_line = false;
					_.each(day.lines, function(line) {
						if (line.unit_amount == 0 && line.amount == 0 && line.name === self.description_line) {
							has_empty_line = true;
						}
						if (line.name && line.name != self.description_line) {
							description += line.name + ' (' + line.unit_amount + ((line.product_uom_id && line.product_uom_id.length == 2) ? ' '+line.product_uom_id[1] : '') + ')\n';
						}
						self.lines[account.account][day_count][parseInt(line.id, 10)] = line;
					});
					if (description) {
						day.description = description;
					}
					if (!has_empty_line) {
						var tmp = _.extend(_.clone(account.account_defaults), {
                            name: self.description_line,
                            unit_amount: 0,
                            date: instance.web.date_to_str(day.day),
                            account_id: account.account,
                        });
						day.lines.unshift(tmp);
						self.lines[account.account][day_count][parseInt(tmp.id, 10)] = tmp;
					}
				});
				self.accounts_by_id[account.account] = account;
			});
			self._super.apply(self, arguments);
			self.set_boxes_onchange();
    		self.init_week_pager();
    		self.init_descriptions();
    		if (!self.get('effective_readonly')) {
    			self.init_amount_fields();    			
    		}
    	},
    	set_boxes_onchange: function() {
            var self = this;
            _.each(self.accounts, function(account) {
                _.each(_.range(account.days.length), function(day_count) {
                    if (!self.get('effective_readonly')) {
                        self.get_box(account, day_count).off('change').change(function() {
                            var num = $(this).val();
                            if (self.is_valid_value(num)){
                                num = (num == 0) ? 0 : Number(self.parse_client(num));
                            }
                            if (isNaN(num)) {
                                $(this).val(self.sum_box(account, day_count, true));
                            } 
                            else {
                            	var diff = num - self.sum_box(account, day_count);
                            	if (diff >= 0) {
                            		account.days[day_count].lines[0].unit_amount += diff;
                            	}
                            	else if (account.days[day_count].lines.length == 2 && num == 0) {
                            		account.days[day_count].lines.splice(1, 1);
                            	}
                            	else if (account.days[day_count].lines.length == 2) {
                            		account.days[day_count].lines[1].unit_amount += diff;
                            	}
                            	else {
                            		$(this).val(self.sum_box(account, day_count, true));
                            		var $dialog = new instance.web.Dialog(this, {
                        				title: _t('Warning'),
                        				buttons: [{
                        					text: _t("Ok"), 
                        					click: function() {
                        						this.parents('.modal').modal('hide');
                        					}
                        				}],
                        			}, $('<div/>').text(_t('To correct an already registered record, please use the "Details" tab.')))
                        			.open();
                            		return;
                            	}
                                
                                
                                var product = (account.days[day_count].lines[0].product_id instanceof Array) ? account.days[day_count].lines[0].product_id[0] : account.days[day_count].lines[0].product_id
                                var journal = (account.days[day_count].lines[0].journal_id instanceof Array) ? account.days[day_count].lines[0].journal_id[0] : account.days[day_count].lines[0].journal_id
                                self.defs.push(new instance.web.Model("hr.analytic.timesheet").call("on_change_unit_amount", [[], product, account.days[day_count].lines[0].unit_amount, false, false, journal]).then(function(res) {
                                    account.days[day_count].lines[0]['amount'] = res.value.amount || 0;
                                    self.display_totals();
                                    self.sync();
                                }));
                                if(!isNaN($(this).val())){
                                    $(this).val(self.sum_box(account, day_count, true));
                                }
                            }
                        });
                    }
                });
            });
        },
        display_totals: function() {
            var self = this;
			if (self.week_pager_mode) {
				var total_day = _.map(_.range(self.dates.length), function() { return 0 });
	            var super_total_week = 0;
	            var super_total_month = 0;
	            _.each(self.accounts, function(account) {
	                var account_total_week = 0;
	                var account_total_month = 0;
	                _.each(_.range(self.dates.length), function(day_count) {
	                	var sum = self.sum_box(account, day_count);
	                	var week = self.date_week[self.dates[day_count]];
	                	if (week == self.current_week) {
	                		account_total_week += sum;
	                		super_total_week += sum;
	                	}
	                	account_total_month += sum;
	                	super_total_month += sum;
	                	total_day[day_count] += sum;
	                });
	                self.get_total(account, 'week').html(account_total_week);
	                self.get_total(account, 'month').html(account_total_month);
	            });
	            var week_days_count = self.week_day[self.current_week].days_count;
	            _.each(_.range(week_days_count.length), function(i) {
	            	self.get_day_total(week_days_count[i]).html(total_day[week_days_count[i]]);
	            });
	            
	            var theoric_total_week = self.get_total_working_hours_in_week(self.current_week);
	            var theoric_total_month = self.get_total_working_hours_in_month();
	            
	            var color_week = (super_total_week < theoric_total_week) ? 'red' : 'green';
	            var super_total_week_str = '<span class="' + color_week + '">' + super_total_week  + ' / ' + theoric_total_week + '</span>'
	            var color_month = (super_total_month < theoric_total_month) ? 'red' : 'green';
	            var super_total_month_str = '<span class="' + color_month + '">' + super_total_month + ' / ' + theoric_total_month + '</span>'
	            
	            self.get_super_total('week').html(super_total_week_str);
	            self.get_super_total('month').html(super_total_month_str);
			}
			else {
				var res = this._super.apply(this, arguments);
			}
        },
        get_total: function(account, type) {
        	var selector = '[data-account-total="' + account.account + '"]';
        	if (type) {
        		selector += '.'+type;
        	}
            return this.$(selector);
        },
        get_super_total: function(type) {
        	var selector = '.oe_timesheet_weekly_supertotal';
        	if (type) {
        		selector += '.'+type;
        	}
            return this.$(selector);
        },
    	get_total_working_hours_in_month: function() {
			var self = this;
			return self.total_working_days * self.hours_per_day;
		},
		get_total_working_hours_in_week: function(week) {
			var self = this;
			return self.week_day[week].working_days * self.hours_per_day;
		},
		init_amount_fields: function () {
			var self = this;
			$('input.oe_timesheet_weekly_input').focus(function () {
				if (!self.get('effective_readonly')) {
					var account_id = $(this).attr('data-account');
					var day_count = $(this).attr('data-day-count');
					var account = self.accounts_by_id[account_id];
					if (account) {
						var count_lines = 0;
						_.each(account.days[day_count].lines, function (line) {
							if (line.amount) {
								count_lines++;
							}
						});
						if (count_lines > 0) {
							var position = $(this).offset();
							var width = $(this).width();
							self.show_description(account_id, day_count, position.left + width, position.top);
							$(this).attr('disabled', 'disabled');
						}
					}
				}
			});			
		},
		init_descriptions: function () {
			var self = this;
			$('i.oe_timesheet_description').click(function () {
				var account_id = $(this).attr('data-account-id');
				var day_count = $(this).attr('data-day-count');
				var position = $(this).offset();
				self.show_description(account_id, day_count, position.left, position.top);
			});
		},
		show_description: function(account_id, day_count, x, y) {
			var self = this;
			
			var account = self.accounts_by_id[account_id];
			if (account) {
				var readonly = self.account_read_only[account.account] || false;
				readonly = readonly || self.get('effective_readonly');
				$('div.oe_timesheet_description_div_outer').remove();
				var descriptions = [];
				_.each(account.days[day_count].lines, function (line) {
					desc = {
						name: (line.name && line.name != self.description_line) ? line.name : '',
						uom: ((line.product_uom_id && line.product_uom_id.length == 2) ? ' ' + line.product_uom_id[1] : ''),
						amount: line.unit_amount,
						hours: line.unit_amount ? self.format_client(line.unit_amount) : '',
						line_id: line.id,
						account_id: account.account,
					};
					descriptions.push(desc);
				});
				var html = QWeb.render("ic_web_timesheet.TsDescriptionDiv", {widget: self, descriptions: descriptions, day_count:day_count, readonly:readonly});
				var elem = $(html);
				elem.click(function(e) {
					self.hide_description();
				});
				elem.find('div.oe_timesheet_description_div').css({left: x + 'px', top: (y + 20) + 'px'}).click(function(e) {
					e.preventDefault();
					e.stopImmediatePropagation();
					e.stopPropagation();
					return false;
				});
				if (!self.get('effective_readonly')) {
					elem.find('input[name=amount]').change(function(e) {
						var account_id = parseInt($(this).attr('data-account-id'), 10);
						var account = self.accounts_by_id[account_id];
						var day_count = parseInt($(this).attr('data-day-count'), 10);
						var line_id = parseInt($(this).attr('data-line'), 10);
						var line = self.lines[account_id][day_count][line_id];
						var num = $(this).val();
                        if (self.is_valid_value(num)){
                            num = (num == 0) ? 0 : Number(self.parse_client(num));
                        }
                        if (isNaN(num)) {
                            $(this).val(line ? (line.unit_amount ? self.format_client(line.unit_amount) : '') : '');
                        }
                        else {
                            line.unit_amount = num;
                            var product = (line.product_id instanceof Array) ? line.product_id[0] : line.product_id;
                            var journal = (line.journal_id instanceof Array) ? line.journal_id[0] : line.journal_id;
                            self.defs.push(new instance.web.Model("hr.analytic.timesheet").call("on_change_unit_amount", [[], product, line.unit_amount, false, false, journal]).then(function(res) {
                                line['amount'] = res.value.amount || 0;
                                self.get_box(account, day_count).val(self.sum_box(account, day_count, true))
                                self.display_totals();
                                self.sync();
                            }));
                        }
					});
					elem.find('input[name=name]').change(function(e) {
						var account_id = parseInt($(this).attr('data-account-id'), 10);
						var account = self.accounts_by_id[account_id];
						var day_count = parseInt($(this).attr('data-day-count'), 10);
						var line_id = parseInt($(this).attr('data-line'), 10);
						var line = self.lines[account_id][day_count][line_id];
						line.name = $(this).val();
                        self.sync();
					});
				}
				$('body').append(elem);
			}
		},
		hide_description: function() {
			$('div.oe_timesheet_description_div_outer').remove();
		},
    	init_week_pager: function() {
			var self = this;
			$('#oe_timesheet_pager_prev').click(function() {
				if (self.current_week > 1) {
					self.current_week = parseInt(self.current_week, 10) - 1;
					self.pager_switch_week();
				}
			});
			$('#oe_timesheet_pager_next').click(function() {
				if (self.current_week < self.total_weeks) {
					self.current_week = parseInt(self.current_week, 10) + 1;
					self.pager_switch_week();
				}
			});
			self.pager_switch_week();
		},
		pager_switch_week: function() {
			var self = this;
			self.set_week(self.current_week);
			$('#oe_timesheet_pager_prev').css('visibility', self.current_week == 1 ? 'hidden' : 'visible');
			$('#oe_timesheet_pager_next').css('visibility', self.current_week == self.total_weeks ? 'hidden' : 'visible');
			$('#oe_timesheet_pager_week').text(_t('Week') + ' ' + self.current_week);
			self.$el.find('.week' + self.current_week).show();
			for (var i=1; i<=self.total_weeks; i++) {
				if (i != self.current_week) {
					self.$el.find('.week' + i).hide();
				}
			}
			self.display_totals();
		},
		get_ts_year_month: function () {
			var self = this;
    		var date = self.get("date_from");
    		if (!date) {
    			date = self.get("date_to");
    		}
    		if (!date) {
    			date = new Date();
    		}
    		var year = date.getFullYear();
    		var month = date.getMonth();
    		return [year, month];
		},
    	get_week: function () {
    		var self = this;
    		var year_month = self.get_ts_year_month();
    		var stored_week = self.get_stored_week(year_month[0], year_month[1]);
			return stored_week ? parseInt(stored_week, 10) : 1;
		},
		set_week: function (week) {
    		var self = this;
    		var year_month = self.get_ts_year_month();
    		self.store_week(year_month[0], year_month[1], week);
		},
		get_storage_key: function (year, month) {
			var self = this;
			month = month.toString();
			if (month.length == 1) {
				month = "0" + month;
			}
			return year.toString() + '-' + month;
		},
		get_stored_values: function () {
			var self = this;
			var pager = localStorage.getItem('oe_timesheet_pager');
			if (!pager) {
				pager = '{}';
			}
			pager = JSON.parse(pager);
			return pager;
		},
		get_stored_week: function (year, month) {
			var self = this;
			var pager = self.get_stored_values();
			key = self.get_storage_key(year, month);
			return pager[key];
		},
		store_week: function (year, month, week) {
			var self = this;
			var pager = self.get_stored_values();
			key = self.get_storage_key(year, month);
			pager[key] = week;
			localStorage.setItem('oe_timesheet_pager', JSON.stringify(pager));
		},
		go_to: function(event) {
            return false;
        },
		init_add_account: function() {
			var res = this._super.apply(this, arguments);
			this.$(".oe_timesheet_weekly_add_row td").find('span.oe_form_field_many2one > a.oe_m2o_cm_button').remove();
			return res;
		}
    });
}
