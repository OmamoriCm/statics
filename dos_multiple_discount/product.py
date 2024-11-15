from openerp.osv import osv, fields, expression
import openerp.addons.decimal_precision as dp

class product_template(osv.osv):
    
    def _show_discount_product(self, cr, uid, ids, name, args, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = ''
            if line.customer_discount_ids:
                partners = []
                for disc in line.customer_discount_ids:
                    wheres = []
                    if disc.discount_ids:
                        for disc_line in disc.discount_ids:
                            #print "============",disc_line.name
                            wheres.append(str(disc_line.name)+'%')
                    #[disc.name.name]+wheres
                    partners.append([str(disc.name.name)]+wheres)
                part = []
                for p in partners:
                    partner = ",".join(p)
                    part.append(partner)
                res[line.id] = ",".join(part)
        return res

    _inherit = "product.template"
    _description = "Product Template"    
    _columns = {
        'show_discount_product': fields.function(_show_discount_product, string='Discount Multiple', type='char', readonly=True),
        'customer_discount_ids': fields.one2many('product.customer.discount', 'product_tmpl_id', 'Customer Discount'),
    }
    
class product_customer_discount(osv.osv):
    
    def _show_discount(self, cr, uid, ids, name, args, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = {
                'show_discount': '',
                #'member_discount': 0.0,
            }
            price = line.product_tmpl_id.standard_price
            if line.discount_ids:
                wheres = []
                for disc in line.discount_ids:
                    price = price + (price * (disc.name / 100.0))
                    wheres.append(str(disc.name)+'%')
                if len(wheres) == 1:
                    res[line.id]['show_discount'] = "".join(wheres)
                else:
                    res[line.id]['show_discount'] = ", ".join(wheres)
                #res[line.id]['member_discount'] = price
        return res
    
    _name = "product.customer.discount"
    _description = "Information about a discount multiple to customer"
    
    _columns = {
        'product_tmpl_id' : fields.many2one('product.template', 'Product Template', required=True, ondelete='cascade', select=True, oldname='product_id'),
        'name' : fields.many2one('res.partner.group', 'Partner Groups', required=True, help="Groups customer of discount"),
        'show_discount': fields.function(_show_discount, string='Discount %', type='char', readonly=True, multi='sums'),
        #'member_discount': fields.function(_show_discount, string='Member Price', type='float', readonly=True, multi='sums'),
        'discount_ids': fields.one2many('discount.multiple', 'product_customer_id','Discount Multiple', required=True, help="The discount multiple for customer groups"),
    }
        
class discount_multiple(osv.osv):
    _name = "discount.multiple"
    _description = "Information about a discount multiple to customer"

    _columns = {
        'product_customer_id' : fields.many2one('product.customer.discount', 'Discount Customer', required=False),
        'name' : fields.float('Discount', required=True, help="Assigns the priority to the list of discount customer."),
        'sequence': fields.integer('Sequence', help="The discount information for customer"),
    }
    
#     _sql_constraints = [
#         ('sequence_uniq', 'unique (product_customer_id, sequence)', 'Sequence of discount multiple for customer should be unique!')
#     ]
    