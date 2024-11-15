# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import SUPERUSER_ID, api
from openupgradelib import openupgrade


def migrate_create_temp_table(cr):
    openupgrade.logged_query(
        cr,
        """
        CREATE TABLE temp_cancel_reason (
            old_id    integer,
            new_id    integer,
            name   varchar(40)
        )
        """,
    )


def migrate_update_module(cr):
    openupgrade.logged_query(
        cr,
        """
        UPDATE ir_module_module
        SET state='installed'
        WHERE name = 'base_cancel_reason' AND
        state='to install'
        """,
    )


def migrate_cancel_reason(env):
    obj_base_cancel_reason = env["base.cancel.reason"]
    query = """
        SELECT A.id, A.name
        FROM agreement_cancel_reason AS A
    """
    env.cr.execute(query)
    rows = env.cr.fetchall()
    for row in rows:
        criteria = [("name", "=", row[1])]
        check_data = obj_base_cancel_reason.search_count(criteria)

        if check_data == 0:
            new_id = obj_base_cancel_reason.create({"name": row[1]})
            openupgrade.logged_query(
                env.cr,
                """
                INSERT INTO temp_cancel_reason
                (old_id, new_id, name)
                VALUES (%s, %s, %s);
                """,
                (row[0], new_id.id, row[1]),
            )


def migrate_old_value(cr):
    openupgrade.logged_query(
        cr,
        """
        UPDATE agreement_agreement AS A
        SET	cancel_reason_id=B.new_id
        FROM temp_cancel_reason AS B
        WHERE A.old_cancel_reason_id=B.old_id
        """,
    )


def migrate_update_base_cancel_reason_config(env):
    config_id = env.ref("agreement_core.base_cancel_reason_config_agreement_agreement")
    query = """
        SELECT A.new_id
        FROM temp_cancel_reason AS A
    """
    env.cr.execute(query)
    rows = env.cr.fetchall()
    for row in rows:
        openupgrade.logged_query(
            env.cr,
            """
            INSERT INTO base_reason_config_rel
            (config_id, reason_id)
            VALUES (%s, %s);
            """,
            (config_id.id, row[0]),
        )


@openupgrade.migrate()
def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    migrate_update_module(cr)
    migrate_create_temp_table(cr)
    migrate_cancel_reason(env)
    migrate_old_value(cr)
    openupgrade.drop_columns(cr, [("agreement_agreement", "old_cancel_reason_id")])
    migrate_update_base_cancel_reason_config(env)
    if openupgrade.table_exists(env.cr, "agreement_cancel_reason"):
        openupgrade.logged_query(
            cr,
            """
            DROP TABLE agreement_cancel_reason CASCADE
            """,
        )
    if openupgrade.table_exists(env.cr, "temp_cancel_reason"):
        openupgrade.logged_query(
            cr,
            """
            DROP TABLE temp_cancel_reason
            """,
        )
