# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class PosOrder(models.Model):
    _inherit = 'pos.order'

    return_picking_id = fields.Many2one(
        string=_('Return Picking'),
        comodel_name='stock.picking',
    )

    @api.multi
    def _get_order_lines_to_pick(self, lines):
        self.ensure_one()

        order_lines = self.env['pos.order.line']
        return_order_lines = self.env['pos.order.line']

        if lines:
            for line in lines:
                if line.product_id.type != 'service':
                    if line.qty >= 0:
                        order_lines |= line
                    else:
                        return_order_lines |= line

        return order_lines, return_order_lines

    @api.multi
    def _create_picking(self):
        self.ensure_one()

        picking_cls = self.env['stock.picking']
        partner_cls = self.env['res.partner']
        move_cls = self.env['stock.move']

        picking_id = picking_cls
        move_list = move_cls
        return_picking_id = picking_cls
        return_move_list = move_cls

        order_lines, return_order_lines = self._get_order_lines_to_pick(self.lines)

        addr = self.partner_id and self.partner_id.address_get(['delivery']) or {}

        if order_lines:
            picking_type = self.picking_type_id
            if picking_type:
                picking_id = picking_cls.create({
                    'origin': self.name,
                    'partner_id': addr.get('delivery', False),
                    'date_done': self.date_order,
                    'picking_type_id': picking_type.id,
                    'company_id': self.company_id.id,
                    'move_type': 'direct',
                    'note': self.note or "",
                    'invoice_state': 'none',
                })

                self.write({'picking_id': picking_id.id})

            location_id = self.location_id.id
            if self.partner_id:
                destination_id = self.partner_id.property_stock_customer.id
            elif picking_type:
                if not picking_type.default_location_dest_id:
                    raise ValidationError(_(
                        'Missing source or destination location for picking type %s. '
                        'Please configure those fields and try again.' % (picking_type.name,)
                    ))
                destination_id = picking_type.default_location_dest_id.id
            else:
                destination_id = partner_cls.default_get(['property_stock_customer'])['property_stock_customer']

            for line in order_lines:
                if line.product_id and line.product_id.type == 'service':
                    continue

                move_list |= move_cls.create({
                    'name': line.name,
                    'product_uom': line.product_id.uom_id.id,
                    'product_uos': line.product_id.uom_id.id,
                    'picking_id': picking_id.id,
                    'picking_type_id': picking_type.id,
                    'product_id': line.product_id.id,
                    'product_uos_qty': abs(line.qty),
                    'product_uom_qty': abs(line.qty),
                    'state': 'draft',
                    'location_id': location_id,
                    'location_dest_id': destination_id,
                })

        if return_order_lines:
            return_picking_type = self.session_id.config_id.return_picking_type_id
            if return_picking_type:
                return_picking_id = picking_cls.create({
                    'origin': self.name,
                    'partner_id': addr.get('delivery', False),
                    'date_done': self.date_order,
                    'picking_type_id': return_picking_type.id,
                    'company_id': self.company_id.id,
                    'move_type': 'direct',
                    'note': self.note or "",
                    'invoice_state': 'none',
                })
    
                self.write({'return_picking_id': return_picking_id.id})
                return_destination_id = return_picking_type.default_location_dest_id.id

            else:
                return_destination_id = self.location_id.id

            if self.partner_id:
                return_location_id = self.partner_id.property_stock_customer.id
            elif return_picking_type:
                if not return_picking_type.default_location_src_id:
                    raise ValidationError(_(
                        'Missing source or destination location for picking type %s. '
                        'Please configure those fields and try again.' % (
                            return_picking_type.name,)
                    ))
                return_location_id = return_picking_type.default_location_src_id.id
            else:
                return_location_id = partner_cls.default_get(['property_stock_customer'])['property_stock_customer']

            for line in return_order_lines:
                if line.product_id and line.product_id.type == 'service':
                    continue

                return_move_list |= move_cls.create({
                    'name': line.name,
                    'product_uom': line.product_id.uom_id.id,
                    'product_uos': line.product_id.uom_id.id,
                    'picking_id': return_picking_id.id,
                    'picking_type_id': return_picking_type.id,
                    'product_id': line.product_id.id,
                    'product_uos_qty': abs(line.qty),
                    'product_uom_qty': abs(line.qty),
                    'state': 'draft',
                    'location_id': return_location_id,
                    'location_dest_id': return_destination_id,
                })

        return picking_id, move_list, return_picking_id, return_move_list

    @api.multi
    def create_picking(self):
        for order in self:
            if all(t == 'service' for t in order.lines.mapped('product_id.type')):
                continue

            # otherwise create the picking for the pos order
            picking_id, move_list, return_picking_id, return_move_list = order._create_picking()

            if picking_id:
                picking_id.action_confirm()

                if order.session_id.config_id.auto_transfer_picking:
                    picking_id.force_assign()
                    picking_id.action_done()

            elif move_list:
                move_list.action_confirm()

                if order.session_id.config_id.auto_transfer_picking:
                    move_list.force_assign()
                    move_list.action_done()

            if return_picking_id:
                return_picking_id.action_confirm()

                if order.session_id.config_id.auto_transfer_picking:
                    return_picking_id.force_assign()
                    return_picking_id.action_done()

            elif return_move_list:
                return_move_list.action_confirm()

                if order.session_id.config_id.auto_transfer_picking:
                    return_move_list.force_assign()
                    return_move_list.action_done()

        return True
