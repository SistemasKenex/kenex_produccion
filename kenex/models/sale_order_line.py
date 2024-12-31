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

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    it_country_id = fields.Many2one('res.country',string='(Pais de Origen)')
    it_product_pricelist_id = fields.Many2one('product.pricelist',string='(Tipo Precio)', store=True)
    it_check_value_sale = fields.Char(compute="_compute_it_check_value_sale", string='(+-=)', store=True)

    # Busca Lista de Precio Correspondiente para cada usuario.     
    @api.onchange('it_product_pricelist_id')                       
    def _get_users_pricelist_domain(self):
        # Obtener el ID del usuario conectado
        users_id = self. _uid 
        # Obtener el item  de las Lista de Precio para luego buscar el Valor
        params   = {'p_users_id': users_id  } 
        query = """ SELECT pricelist_id FROM product_res_user_rel where users_id =  %(p_users_id)s """
        self.env.cr.execute(query,params)
        lines_ids = list(line[0] for line in self.env.cr.fetchall())
        res = {}
        res['domain'] = {'it_product_pricelist_id': [('id', 'in', lines_ids)]}
        return res
        
        #raise  ValidationError(self.it_product_pricelist_id)   
            

    @api.depends('it_product_pricelist_id', 'price_unit')
    def _compute_it_check_value_sale(self):
        for record in self:
            if record.it_product_pricelist_id:
                params   = {'p_product_id': record.product_template_id.id,
                            'p_product_pricelist_id': record.it_product_pricelist_id.id,
                            'p_precio_venta': record.price_unit,
                            'p_order_id': self.order_id,
                            'p_pricelist_id':record.it_product_pricelist_id.id
                        } 
                query = """ SELECT * FROM f_get_precio_revision_pedidos( %(p_product_id)s ,	
                                                                        %(p_product_pricelist_id)s ,
                                                                        %(p_precio_venta)s )
                        """
                self.env.cr.execute(query,params)
                for line in self.env.cr.fetchone():
                    price = line
                    self.it_check_value_sale = price
                    #query = " UPDATE sale_order set pricelist_id = %(p_pricelist_id)s WHERE id = %(p_order_id)s "
                    #raise  ValidationError(self.order_id.id) 
                    #query = " UPDATE sale_order set pricelist_id = 1 WHERE id = 1 "
                    #self.env.cr.execute(query,params)
                    #raise  ValidationError(price) 
                    return
                
    #def _update_sale_order(cr, version):
     #   cr.execute(" UPDATE sale_order set pricelist_id = %(p_pricelist_id)s WHERE id = %(p_order_id)s ")
    
                
        #  raise  ValidationError('Entre en compute_it_check_value_sale')    

    
    # Busca el Precio en la Lista de Precio Correspondiente.
    @api.onchange('it_product_pricelist_id')            
    def _onchange_it_product_pricelist_id(self):
            # Obtener el ID del pruduct_list_id
            id_pricelist_id = self.it_product_pricelist_id.id                 
            # Obtener el ID del product_templete_id
            id_product      = self.product_template_id.id
            # Obtener el item  de las Lista de Precio para luego buscar el Valor
            pricelist_items = self.env['product.pricelist.item'].search([('pricelist_id', '=', id_pricelist_id), ('product_tmpl_id', '=', id_product)])
            for pricelist_item in pricelist_items:
                self.price_unit = pricelist_item.fixed_price  
                return
                #raise  ValidationError() 
                
    # validacion de Restriccion de producto y cantidad a restringuir.     
    @api.onchange('product_uom_qty')                       
    def _onchange_product_uom_qty(self):
        # Obtener datos del producto
        products = self.env['product.template'].search([("id", "=", self.product_template_id.id)])
        it_check_quantity = False
        for product in products:
            it_check_quantity = product.it_check_quantity
            it_block_quantity = product.it_block_quantity
        
        if it_check_quantity == True and self.product_uom_qty > 0 :
            if self.product_uom_qty > it_block_quantity :
                raise  ValidationError('La Cantidad del producto debe ser menor o igual a la permitida : ' + str(it_block_quantity)) 
        return