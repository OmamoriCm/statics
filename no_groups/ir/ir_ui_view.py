# -*- coding: utf-8 -*-

import copy
from lxml import etree
import openerp
from odoo import api, fields, models
from openerp.tools.translate import _


class View(models.Model):
    _inherit = 'ir.ui.view'

   
    def _apply_group(self, model, node, modifiers, fields):
        
        Model = self.env[model]

        if node.tag == 'field' and node.get('name') in Model._fields:
            field = Model._fields[node.get('name')]
            if field.groups and not self.user_has_groups(groups=field.groups):
                node.getparent().remove(node)
                fields.pop(node.get('name'), None)
                # no point processing view-level ``groups`` anymore, return
                return False
        if node.get('groups'):
            can_see = self.user_has_groups(groups=node.get('groups'))
            if not can_see:
                node.set('invisible', '1')
                modifiers['invisible'] = True
                if 'attrs' in node.attrib:
                    del node.attrib['attrs']    # avoid making field visible later
            del node.attrib['groups']
        # add the evaluation of our no_groups attribute
        elif node.get('no_groups'):
            cant_see = self.user_has_groups( groups=node.get('no_groups'))
            if cant_see:
                node.set('invisible', '1')
                modifiers['invisible'] = True
                if 'attrs' in node.attrib:
                    del(node.attrib['attrs']) #avoid making field visible later
            del(node.attrib['no_groups'])
        return True
    
    