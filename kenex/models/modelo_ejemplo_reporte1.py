# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools

class ReportKenexProduct(models.Model):
    _name = "report.kenex.product"
    _description = "Reporte Kenex Ejemplo1"
    _auto = False

    create_date = fields.Datetime("Create Date", readonly=True)
    categ_id = fields.Integer(string='Categ ID', readonly=True)
    uom_id = fields.Integer(string='Uom Id', readonly=True)
    default_code = fields.Char(string='Default Code', readonly=True)
    list_price = fields.Float(string='List Price', readonly=True)

    @property
    def _table_query(self):
        query = """
             select po.product_tmpl_id id,
                    po.default_code,
                    pt.create_date,
                    pt.categ_id,
                    pt.uom_id ,
                    pt.list_price
               from product_template pt ,  
                    product_product po 
              where po.product_tmpl_id = pt.id
            """
        return query
