# -*- coding: utf-8 -*-
# Copyright 2018-2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class TileCategory(models.Model):
    _name = "tile.category"
    _description = "Tile Category"

    name = fields.Char(
        string="Category",
        required=True,
    )
    tile_ids = fields.Many2many(
        string="Dashboard Tiles",
        comodel_name="tile.tile",
        relation="rel_category_2_tile",
        column1="category_id",
        column2="tile_id",
    )
    group_ids = fields.Many2many(
        string="Groups",
        comodel_name="res.groups",
        relation="rel_category_2_group",
        column1="category_id",
        column2="group_id",
    )
    window_action_id = fields.Many2one(
        string="Window Action",
        comodel_name="ir.actions.act_window",
        readonly=True,
    )
    menu_id = fields.Many2one(
        string="Menu",
        comodel_name="ir.ui.menu",
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
        ],
        required=True,
        readonly=True,
        default="draft",
    )

    @api.multi
    def action_active(self):
        for categ in self:
            categ.write(categ._prepare_active_data())

    @api.multi
    def action_draft(self):
        for categ in self:
            categ.write(categ._prepare_draft_data())

    @api.multi
    def action_reload(self):
        for categ in self:
            categ.window_action_id.write(categ._prepare_waction_reload())
            categ.menu_id.write(categ._prepare_menu_reload())

    @api.multi
    def action_open_tile(self):
        self.ensure_one()
        xml_id = "web_dashboard_tile.action_tree_dashboard_tile"
        waction = self.env.ref(xml_id).read()[0]
        waction["domain"] = [
            ("id", "in", self.tile_ids.ids)
        ]
        return waction

    @api.multi
    def _prepare_active_data(self):
        self.ensure_one()
        window_action = self._create_window_action()
        menu = self._create_menu(window_action)
        return {
            "state": "active",
            "window_action_id": window_action.id,
            "menu_id": menu.id,
        }

    @api.multi
    def _prepare_draft_data(self):
        self.ensure_one()
        self.menu_id.unlink()
        self.window_action_id.unlink()
        return {
            "state": "draft",
            "window_action_id": False,
            "menu_id": False,
        }

    @api.multi
    def _create_window_action(self):
        self.ensure_one()
        obj_waction = self.env["ir.actions.act_window"]
        return obj_waction.create(self._prepare_window_action())

    @api.multi
    def _prepare_window_action(self):
        self.ensure_one()
        view = self.env.ref(
            "web_dashboard_tile.dashboard_tile_tile_kanban_view")
        return {
            "name": self.name,
            "type": "ir.actions.act_window",
            "res_model": "tile.tile",
            "view_type": "form",
            "view_mode": "kanban",
            "view_id": view.id,
            "domain": [
                ('id', 'in', self.tile_ids.ids),
                '|',
                ('user_id', '=', False),
                ('user_id', '=', self.env.user.id)]
        }

    @api.multi
    def _prepare_waction_reload(self):
        self.ensure_one()
        return {
            "name": self.name,
            "domain": [
                ('id', 'in', self.tile_ids.ids),
                '|',
                ('user_id', '=', False),
                ('user_id', '=', self.env.user.id)]
        }

    @api.multi
    def _create_menu(self, window_action):
        self.ensure_one()
        obj_menu = self.env["ir.ui.menu"]
        return obj_menu.create(self._prepare_menu(window_action))

    @api.multi
    def _prepare_menu(self, window_action):
        self.ensure_one()
        parent_menu = self.env.ref(
            "web_dashboard_tile_category.all_dashboard_menu")
        return {
            "name": self.name,
            "action": "ir.actions.act_window,%s" % window_action.id,
            "parent_id": parent_menu.id,
            "groups_id": [(6, 0, self.group_ids.ids)],
        }

    @api.multi
    def _prepare_menu_reload(self):
        self.ensure_one()
        return {
            "name": self.name,
            "groups_id": [(6, 0, self.group_ids.ids)],
        }
