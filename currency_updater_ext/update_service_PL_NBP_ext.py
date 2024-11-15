# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Hadron for business sp. z o.o. (http://www.hadron.eu.com)
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from .. import currency_rate_update
#f#rom .. currency_rate_update import services
from .. currency_rate_update.services.update_service_PL_NBP import PL_NBP_getter
from .. currency_rate_update.services.currency_getter import Currency_getter_factory
from .. currency_rate_update.model.currency_rate_update import supported_currency_array,\
        YAHOO_supported_currency_array,RO_BNR_supported_currency_array,CH_ADMIN_supported_currency_array,\
        CA_BOC_supported_currency_array,ECB_supported_currency_array,MX_BdM_supported_currency_array,\
        PL_NBP_supported_currency_array,supported_currecies
from .. currency_rate_update.model.currency_rate_update import _intervalTypes
import logging
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime, time
from dateutil.relativedelta import relativedelta

from openerp import models, fields, api, _
from openerp import exceptions

_logger = logging.getLogger(__name__)

if supported_currecies.has_key('PL_NBP_getter'):
    supported_currecies.pop('PL_NBP_getter')
    supported_currecies.update({'PL_NBP_getter_ext': PL_NBP_supported_currency_array})

class res_currency_rate(models.Model):
    _inherit = 'res.currency.rate'

    tablename = fields.Char(string='Table name')
    rate_date = fields.Datetime('Table Rate Date')
    

class Currency_rate_update_service(models.Model):
    _inherit = 'currency.rate.update.service'

    service = fields.Selection(
        [('CH_ADMIN_getter', 'Admin.ch'),
         ('ECB_getter', 'European Central Bank'),
         ('YAHOO_getter', 'Yahoo Finance'),
         # Added for polish rates
         ('PL_NBP_getter_ext', 'National Bank of Poland'),
         # Added for mexican rates
         ('MX_BdM_getter', 'Bank of Mexico'),
         # Bank of Canada is using RSS-CB
         # http://www.cbwiki.net/wiki/index.php/Specification_1.1
         # This RSS format is used by other national banks
         #  (Thailand, Malaysia, Mexico...)
         ('CA_BOC_getter', 'Bank of Canada - noon rates'),
         # Added for romanian rates
         ('RO_BNR_getter', 'National Bank of Romania')
         ],
        string="Webservice to use",
        required=True)

    @api.onchange('service')
    def _onchange_service(self):
        currency_list = ''
        if self.service:
            currencies = []
            currency_list = supported_currency_array
            company_id = False
            if self.company_id.multi_company_currency_enable:
                company_id = self.company_id.id
            currency_list = supported_currecies[self.service]
            if company_id:
                currencies = self.env['res.currency'].search(
                    [('name', 'in', currency_list),
                     '|', ('company_id', '=', company_id),
                     ('company_id', '=', False)])
            else:
                currencies = self.env['res.currency'].search(
                    [('name', 'in', currency_list),
                     ('company_id', '=', False)])
            self.currency_list = [(6, 0, [curr.id for curr in currencies])]

    @api.one
    def refresh_currency(self):
        """Refresh the currencies rates !!for all companies now"""
        _logger.info(
            'Starting to refresh currencies with service %s (company: %s)',
            self.service, self.company_id.name)
        factory = Currency_getter_factory()
        curr_obj = self.env['res.currency']
        rate_obj = self.env['res.currency.rate']
        company = self.company_id
        # The multi company currency can be set or no so we handle
        # The two case
        if company.auto_currency_up:
            main_currency = curr_obj.search(
                [('base', '=', True), ('company_id', '=', company.id)],
                limit=1)
            if not main_currency:
                # If we can not find a base currency for this company
                # we look for one with no company set
                main_currency = curr_obj.search(
                    [('base', '=', True), ('company_id', '=', False)],
                    limit=1)
            if not main_currency:
                raise exceptions.Warning(_('There is no base currency set!'))
            if main_currency.rate != 1:
                raise exceptions.Warning(_('Base currency rate should '
                                           'be 1.00!'))
            note = self.note or ''
            try:
                # We initalize the class that will handle the request
                # and return a dict of rate
                getter = factory.register(self.service)
                curr_to_fetch = map(lambda x: x.name,
                                    self.currency_to_update)
                res, log_info, tablename,rate_date = getter.get_updated_currency(
                    curr_to_fetch,
                    main_currency.name,
                    self.max_delta_days
                    )
                rate_name = \
                    fields.Datetime.to_string(datetime.utcnow().replace(
                        hour=0, minute=0, second=0, microsecond=0))
                rate_date = \
                    fields.Datetime.to_string(rate_date.replace(
                        hour=0, minute=0, second=0, microsecond=0))
                for curr in self.currency_to_update:
                    if curr.id == main_currency.id:
                        continue
                    do_create = True
                    for rate in curr.rate_ids:
                        if rate.name == rate_name:
                            rate.rate = res[curr.name]
                            rate.tablename = tablename
                            rate.rate_date = rate_date
                            do_create = False
                            break
                    if do_create:
                        vals = {
                            'currency_id': curr.id,
                            'rate': res[curr.name],
                            'name': rate_name,
                            'tablename': tablename,
                            'rate_date':rate_date
                        }
                        rate_obj.create(vals)
                        _logger.info(
                            'Updated currency %s via service %s',
                            curr.name, self.service)

                # Show the most recent note at the top
                msg = '%s \n%s currency updated. %s' % (
                    log_info or '',
                    fields.Datetime.to_string(datetime.today()),
                    note
                )
                self.write({'note': msg})
            except Exception as exc:
                error_msg = '\n%s ERROR : %s %s' % (
                    fields.Datetime.to_string(datetime.today()),
                    repr(exc),
                    note
                )
                _logger.error(repr(exc))
                self.write({'note': error_msg})
            if self._context.get('cron', False):
                midnight = time(0, 0)
                next_run = (datetime.combine(
                            fields.Date.from_string(self.next_run),
                            midnight) +
                            _intervalTypes[str(self.interval_type)]
                            (self.interval_number)).date()
                self.next_run = next_run

class PL_NBP_getter_ext(PL_NBP_getter):

    """Implementation of Currency_getter_factory interface
        for PL NBP service
        """
    def rate_retrieve(self, dom, ns, curr):
        """ Parse a dom node to retrieve
        currencies data"""
        res = {}
        xpath_rate_currency = ("/tabela_kursow/pozycja[kod_waluty='%s']/"
                               "kurs_sredni/text()") % (curr.upper())
        xpath_rate_ref = ("/tabela_kursow/pozycja[kod_waluty='%s']/"
                          "przelicznik/text()") % (curr.upper())
        res['rate_currency'] = float(
            dom.xpath(xpath_rate_currency, namespaces=ns)[0].replace(',', '.')
        )
        res['rate_ref'] = float(dom.xpath(xpath_rate_ref, namespaces=ns)[0])
        return res

    def get_updated_currency(self, currency_array, main_currency,
                             max_delta_days):
        """implementation of abstract method of Curreny_getter_interface"""
        # LastA.xml is always the most recent one
        url = 'http://www.nbp.pl/kursy/xml/LastA.xml'
        # We do not want to update the main currency
        if main_currency in currency_array:
            currency_array.remove(main_currency)
        # Move to new XML lib cf Launchpad bug #645263
        from lxml import etree
        _logger.debug("NBP.pl currency rate service : connecting...")
        rawfile = self.get_url(url)
        dom = etree.fromstring(rawfile)
        ns = {}  # Cool, there are no namespaces !
        _logger.debug("NBP.pl sent a valid XML file")
        rate_date = dom.xpath('/tabela_kursow/data_publikacji/text()',
                              namespaces=ns)[0]
        tablename = dom.xpath('/tabela_kursow/numer_tabeli/text()',
                              namespaces=ns)[0]
        rate_date_datetime = datetime.strptime(rate_date,
                                               DEFAULT_SERVER_DATE_FORMAT)
        self.check_rate_date(rate_date_datetime, max_delta_days)
        # We dynamically update supported currencies
        self.supported_currency_array = dom.xpath(
            '/tabela_kursow/pozycja/kod_waluty/text()',
            namespaces=ns
        )
        self.supported_currency_array.append('PLN')
        _logger.debug("Supported currencies = %s" %
                      self.supported_currency_array)
        self.validate_cur(main_currency)
        if main_currency != 'PLN':
            main_curr_data = self.rate_retrieve(dom, ns, main_currency)
            # 1 MAIN_CURRENCY = main_rate PLN
            main_rate = (main_curr_data['rate_currency'] /
                         main_curr_data['rate_ref'])
        for curr in currency_array:
            self.validate_cur(curr)
            if curr == 'PLN':
                rate = main_rate
            else:
                curr_data = self.rate_retrieve(dom, ns, curr)
                # 1 MAIN_CURRENCY = rate CURR
                if main_currency == 'PLN':
                    rate = curr_data['rate_ref'] / curr_data['rate_currency']
                else:
                    rate = (main_rate * curr_data['rate_ref'] /
                            curr_data['rate_currency'])
            self.updated_currency[curr] = rate
            _logger.debug("Rate retrieved : %s = %s %s" %
                          (main_currency, rate, curr))
        return self.updated_currency, self.log_info, tablename, rate_date_datetime


class Currency_getter_factory():
    """Factory pattern class that will return
    a currency getter class base on the name passed
    to the register method

    """
    def register(self, class_name):
        allowed = [
            'CH_ADMIN_getter',
            'PL_NBP_getter_ext',
            'ECB_getter',
            'GOOGLE_getter',
            'YAHOO_getter',
            'MX_BdM_getter',
            'CA_BOC_getter',
            'RO_BNR_getter',
        ]
        if class_name in allowed:
            exec "from .update_service_%s import %s" % \
                 (class_name.replace('_getter', ''), class_name)
            class_def = eval(class_name)
            return class_def()
        else:
            raise UnknowClassError
