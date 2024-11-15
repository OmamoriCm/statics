# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

column_renames = {
    "agreement_agreement": [
        ("cancel_reason_id", "old_cancel_reason_id"),
    ],
}


def migrate_install_module(cr):
    openupgrade.logged_query(
        cr,
        """
        UPDATE ir_module_module
        SET state='to install'
        WHERE name = 'base_cancel_reason' AND
        state='uninstalled'
        """,
    )


@openupgrade.migrate()
def migrate(cr, version):
    openupgrade.rename_columns(cr, column_renames)
    migrate_install_module(cr)
