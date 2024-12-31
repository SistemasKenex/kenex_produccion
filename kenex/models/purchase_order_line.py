from odoo import api, fields, models, SUPERUSER_ID
import sys
import requests
import json
import logging
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
#from openerp import exceptions

_logger = logging.getLogger(__name__)
logging.captureWarnings(True)

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    it_country_id = fields.Many2one('res.country',string='(Pais de Origen)')
    it_costo = fields.Float(string='(Costo)')
    
    
    @api.onchange('product_qty')            
    def _onchange_product_qty(self):
        if self.product_qty != 0:
            self.env['purchase.order'].it_total_quantity = 1000

            
    # Busca del  Costo de Producto.
    @api.onchange('product_id')            
    def _onchange_product_id(self):
        # Obtener el ID del producto
        id_product = self.product_id.id       
        if id_product:            
            # Obtener el Registro en Product Template
            product_item = self.env['product.product'].search([ ('id', '=', id_product)])                
            for product_items in product_item:
                id_product_template = product_item.product_tmpl_id.id  
                #raise  ValidationError(id_product_template) 
                params   = {'p_product_id': id_product_template } 
                query = " SELECT * FROM f_pbase( %(p_product_id)s)"
                self.env.cr.execute(query,params)
                for line in self.env.cr.fetchone():
                    price = line
                    self.it_costo = price
                    #raise  ValidationError(price) 
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    #raise  ValidationError(id_product_template)    