# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools
import sys
import requests
import json
import logging
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class ReportRefe(models.Model):
    _name = "report.refe"
    _description = "Referencia en Pedidos"
    _auto = False
    articulo            = fields.Char("Articulo", readonly=True)
    nro_pedido          = fields.Char("Pedido", readonly=True)
    fecha               = fields.Date("Fecha   ", readonly=True)
    cantidad            = fields.Integer("Cantidad", readonly=True)
    nombre_cliente      = fields.Char("Nombre del Cliente", readonly=True)
    precio              = fields.Float("Precio", readonly=True)
    pais                = fields.Char("Pais", readonly=True)
    estado_cotizacion   = fields.Char("Estado Cotizacion", readonly=True)
    estado_bodega       = fields.Char("Estado Bodega", readonly=True)
    vendedor            = fields.Char("Vendedor", readonly=True)

    @property
    def _table_query(self):
        query = """
        SELECT  
            sol.id                                               AS id,
            f_articulo(sol.product_id )                          AS articulo,
            so.name                                              AS nro_pedido,  
            to_char(so.date_order   ,'YYYY-MM-DD')               AS fecha ,   
            sol.product_uom_qty                                  AS cantidad,
            rp.name                                              AS nombre_cliente,
            sol.price_unit                                       AS precio,
            rc.id                                                AS pais,
            CASE 
                WHEN so.state = 'done'   THEN 'Hecho'
                WHEN so.state = 'sale'   THEN 'Orden de venta'
                WHEN so.state = 'sent'   THEN 'Cotización enviada'
                WHEN so.state = 'cancel' THEN 'Cancelada'
                WHEN so.state = 'draft'  THEN 'Borrador'
            END                                                  AS estado_cotizacion,
            CASE
                WHEN f_estado_bodega(so.id) = 'confirmed' THEN 'Confirmado'
                WHEN f_estado_bodega(so.id) = 'done'      THEN 'Hecho'
                WHEN f_estado_bodega(so.id) = 'assigned'  THEN 'Asignado'
                WHEN f_estado_bodega(so.id) = 'waiting'   THEN  'En Espera'
                WHEN f_estado_bodega(so.id) = 'draft'     THEN  'Borrador'
                WHEN f_estado_bodega(so.id) = 'cancel'    THEN  'Cancelado' 
            END                                               AS estado_bodega,    
            f_vendedor_order(so.id)                      AS vendedor
        FROM  
            res_partner AS rp,
            sale_order AS so,
            sale_order_line AS sol,
            res_country AS rc,
            res_users AS ru
        WHERE  rp.id           = so.partner_id
        AND so.id              = sol.order_id
        AND rp.country_id      = rc.id
        AND so.user_id         = ru.id
        AND so.user_id         = """+str(self.env.user.id)+"""
        order by 2   """ 
        return query