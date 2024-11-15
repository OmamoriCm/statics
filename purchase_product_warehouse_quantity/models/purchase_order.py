# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Ascetic Business Solution <www.asceticbs.com>
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
#################################################################################

from openerp import api, fields, models, SUPERUSER_ID, _
from datetime import datetime, timedelta
import datetime
from datetime import datetime
from dateutil import relativedelta


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    warehouse_quantity = fields.Char('Stock Quantity per Warehouse')

    #For update the onchange of product
    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, state='draft', context=None):
        result = {}
        res = super(PurchaseOrderLine, self).onchange_product_id(cr, uid, ids, pricelist_id, product_id, qty, uom_id, partner_id, date_order, fiscal_position_id, date_planned, name, price_unit, state, context)
        if res.get('value',False):
            result = res['value']
        warehouse_quantity_text = ''
        quant_ids = self.pool.get('stock.quant').search(cr, SUPERUSER_ID, [('product_id','=',product_id),('reservation_id','=',None),('location_id.usage','=','internal')], context=context)
        t_warehouses = {}
        for quant in quant_ids:
            quant_obj = self.pool.get('stock.quant').browse(cr, SUPERUSER_ID, quant, context=context)
            if quant_obj.location_id:
                if quant_obj.location_id not in t_warehouses:
                    t_warehouses.update({quant_obj.location_id:0})
                t_warehouses[quant_obj.location_id] += quant_obj.qty

        tt_warehouses = {}
        for location in t_warehouses:
            location_obj = self.pool.get('stock.location').browse(cr, SUPERUSER_ID, location.id, context=context)
            warehouse = False
            location1 = location_obj
            while (not warehouse and location1):
                warehouse_id = self.pool.get('stock.warehouse').search(cr, SUPERUSER_ID, [('lot_stock_id','=',location1.id)], context=context)
                warehouse_obj_id = self.pool.get('stock.warehouse').browse(cr, SUPERUSER_ID, warehouse_id, context=context)
                if len(warehouse_obj_id) > 0:
                    warehouse = True
                else:
                    warehouse = False
                location1 = location1.location_id
            if warehouse_obj_id:
                if warehouse_obj_id.name not in tt_warehouses:
                    tt_warehouses.update({warehouse_obj_id.name:0})
                tt_warehouses[warehouse_obj_id.name] += t_warehouses[location]

        for item in tt_warehouses:
            if tt_warehouses[item] != 0:
                warehouse_quantity_text = warehouse_quantity_text + ' ** ' + item + ': ' + str(tt_warehouses[item])
        result['warehouse_quantity'] = warehouse_quantity_text
        return {'value': result}

