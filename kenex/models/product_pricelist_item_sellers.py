from odoo import api, fields, models, SUPERUSER_ID
import sys
import requests
import json
import logging
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)
logging.captureWarnings(True)


class ProductPricelistItemSellers(models.Model):
    _name = 'product.pricelist.item.sellers'
    _description = 'Lista de Precios x Vendedor'
    
    product_id = fields.Many2one('product.product' , string='Producto')
    articulo   = fields.Char(string='Articulo')
    lista_precio_an = fields.Float("AN", readonly=True)  
    lista_precio_cn = fields.Float("CN", readonly=True)  
    lista_precio_do = fields.Float("DO", readonly=True)  
    lista_precio_ds = fields.Float("DS", readonly=True)  
    lista_precio_es = fields.Float("ES ", readonly=True)  
    lista_precio_fk = fields.Float("FK", readonly=True)  
    lista_precio_fr = fields.Float("FR", readonly=True)  
    lista_precio_fv = fields.Float("FV", readonly=True)  
    lista_precio_ms = fields.Float("MS", readonly=True)  
    lista_precio_p_plus = fields.Float("P+", readonly=True)  
    lista_precio_pa = fields.Float("PA", readonly=True)  
    lista_precio_pb = fields.Float("PB", readonly=True)  
    lista_precio_pr = fields.Float("PR", readonly=True)  
    lista_precio_ta = fields.Float("TA", readonly=True)  
    lista_precio_tm = fields.Float("TM", readonly=True)  
    
    @property
    def _table_query_pricelist(self):
        # Obtener el ID del usuario conectado
        users_id = self. _uid 
        params  = {'users_id': users_id}
        query = """
                SELECT pt.id                                      AS id, 
                    pt.name::json->>'en_US'                       AS articulo,
                    f_get_lista_precio_articulo('91',pt.id,'AN')  AS lista_precio_an,
                    f_get_lista_precio_articulo('91',pt.id,'CN')  AS lista_precio_cn,
                    f_get_lista_precio_articulo('91',pt.id,'DO')  AS lista_precio_do,
                    f_get_lista_precio_articulo('91',pt.id,'DS')  AS lista_precio_ds,
                    f_get_lista_precio_articulo('91',pt.id,'ES')  AS lista_precio_es,
                    f_get_lista_precio_articulo('91',pt.id,'FK')  AS lista_precio_fk,
                    f_get_lista_precio_articulo('91',pt.id,'FR')  AS lista_precio_fr,
                    f_get_lista_precio_articulo('91',pt.id,'FV')  AS lista_precio_fv,
                    f_get_lista_precio_articulo('91',pt.id,'MS')  AS lista_precio_ms,
                    f_get_lista_precio_articulo('91',pt.id,'P+')  AS lista_precio_p_plus,
                    f_get_lista_precio_articulo('91',pt.id,'PA')  AS lista_precio_pa,
                    f_get_lista_precio_articulo('91',pt.id,'PB')  AS lista_precio_pb,
                    f_get_lista_precio_articulo('91',pt.id,'PR')  AS lista_precio_pr,
                    f_get_lista_precio_articulo('91',pt.id,'TA')  AS lista_precio_ta,
                    f_get_lista_precio_articulo('91',pt.id,'TM')  AS lista_precio_tm
                from product_template pt	                
            """
        return query
