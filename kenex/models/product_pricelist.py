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

class ProductPriceList(models.Model):
    _inherit = 'product.pricelist'

    it_search_articulo_id = fields.Many2one(comodel_name='product.template', string="(Search Producto)")

    def btn_search(self):
        self.ensure_one()
        pricelist_id =  self._origin.id   
        product_tmpl_id = self.it_search_articulo_id.id
        product_pricelist_item = self.env['product.pricelist.item'].search([('pricelist_id', '=', pricelist_id), ('product_tmpl_id','=',product_tmpl_id)])
        entre = False
        for reg_product_pricelist_item  in product_pricelist_item:
            entre = True

        lines_ids = list(line[0] for line in product_pricelist_item)    
        if entre == True:
            return{
                    'type'     : 'ir.actions.act_window',
                    'name'     : 'Detalle de Precio',
                    'view_type': 'form',
                    'view_mode': 'tree',
                    'res_model': 'product.pricelist.item',  
                    'context': {},
                    'domain': [('pricelist_id'    , '=', self._origin.id),
                                ('product_tmpl_id', '=', self.it_search_articulo_id.id)],
                    'target' :'new',
                }
            
    @api.onchange('it_search_articulo_id')   
    def on_change_it_search_articulo_id(self):
        pricelist_id =  self._origin.id   
        product_tmpl_id = self.it_search_articulo_id.id
        product_pricelist_item = self.env['product.pricelist.item'].search([('pricelist_id', '=', pricelist_id), ('product_tmpl_id','=',product_tmpl_id)])
        entre = False
        for reg_product_pricelist_item  in product_pricelist_item:
            entre = True
            
        if entre == False:
            return {
                    'warning': {
                                'title': "Error",
                                'message': "Articulo no existe para esta lista",
                            }
                        }