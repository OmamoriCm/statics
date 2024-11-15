from datetime import datetime

from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):  # pylint: disable=R8110
        super(Parser, self).__init__(cr, uid, name, context)
        self.context = context
        self.localcontext.update(
            {
                "get_terbilang": self._get_terbilang,
                "get_print_date": self._get_print_date,
                "get_bank_account": self._get_bank_account,
            }
        )

    def _get_bank_account(self, journal):
        result = False
        criteria = [("journal_id", "=", journal.id)]
        bank_acc_ids = self.pool.get("res.partner.bank").search(
            self.cr, self.uid, criteria
        )
        if len(bank_acc_ids) > 0:
            result = self.pool.get("res.partner.bank").browse(
                self.cr, self.uid, bank_acc_ids
            )[0]
        return result

    def _get_print_date(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def _get_terbilang(self, value):
        obj_amount2text = self.pool.get("base.amount_to_text")
        obj_res_lang = self.pool.get("res.lang")
        obj_res_currency = self.pool.get("res.currency")
        criteria_lang = [("code", "=", "en_US")]
        criteria_curr = [("name", "=", "IDR")]

        lang_id = obj_res_lang.search(self.cr, self.uid, criteria_lang)
        lang = obj_res_lang.browse(self.cr, self.uid, lang_id)

        currency_id = obj_res_currency.search(self.cr, self.uid, criteria_curr)
        currency = obj_res_currency.browse(self.cr, self.uid, currency_id)

        if currency:
            result = obj_amount2text.get(self.cr, self.uid, value, currency, lang)
        else:
            result = "-"
        return result
