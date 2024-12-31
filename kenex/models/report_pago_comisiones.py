# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools

class ReportPagoComisiones(models.Model):
    _name = "report.pago.comisiones"
    _description = "Reporte Pago de Comisiones"
    _auto = False


    documento   = fields.Integer("Documento", readonly=True)
    fecha       = fields.Date("Fecha", readonly=True)
    cliente     = fields.Char("Cliente", readonly=True)
    vendedor    = fields.Char("Vendedor", readonly=True)
    comision    = fields.Float("Comision", readonly=True)
    bono_comision    = fields.Float("Bono", readonly=True)
    tot_bono_comision    = fields.Float("Total Comision + Bono", readonly=True)
    ventas           = fields.Float("Total Ventas", readonly=True)
    
    @property
    def _table_query(self):
        query = """
        select id                            AS id,
               order_id                      AS documento,
               date_order                    AS fecha,
	           f_cliente(cliente_id)         AS cliente,
	           f_vendedor_order(order_id)    AS vendedor,
	           porc_comision                 AS comision,
               bono_comision                 AS bono_comision,
               tot_bono_comision             AS tot_bono_comision,
	           price_total                   AS ventas
        from kdetalle_comisiones
            """
        return query







