# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools

class ReportKenexProduct(models.Model):
    _name = "report.comisiones"
    _description = "Reporte de Comisiones"
    _auto = False

    vendedor = fields.Char(string='Vendedor', readonly=True)

    @property
    def _table_query(self):
        query = """
             select vendedor_id vendedor
               from kporcentaje_marca
            """
        return query
