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

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    it_codigo_alterno = fields.Char(string='(Codigo Alterno)')
    it_descripcion_alterna_uno = fields.Char(string='(Descripcion Alterna Uno)')
    it_descripcion_alterna_dos = fields.Char(string='(Descripcion Alterna Dos)')
    it_descripcion_alterna_tres = fields.Char(string='(Descripcion Alterna Tres)')
    it_descripcion_alterna_cuatro = fields.Char(string='(Descripcion Alterna Cuatro)')

    it_use_hs_code = fields.Boolean(string='(Use_hs_code)')
    it_hs_code_custom = fields.Boolean(string='(Hs_code_custom)')
    it_caja = fields.Integer(string='(Nro. Cajas)')
    it_bultos = fields.Integer(string='(Nro. Bultos)')
    it_peso_bultos = fields.Integer(string='(Peso Bulto)')
    it_descontinuado = fields.Boolean(string='(Descontinuado)')
    it_height = fields.Float(string='(Height)')
    it_long = fields.Float(string='(Long)')
    it_width = fields.Float(string='(Width)')
    it_ind_serial = fields.Boolean(string='(Indicador Serial)')
    it_check_quantity = fields.Boolean(string='(Restringir Producto)')
    it_block_quantity = fields.Integer(string='(Cantidad a restringir)')
    it_brand_id = fields.Many2one('product.brand', string='(Marca)')
    it_product_type = fields.Selection(
        selection=[
            ('analogo', "Analogo"),
            ('digital', "Digital"),
            ('no aplica', "No Aplica"),
        ],
        string="Product Type",
        copy=False,
        index=True,
        default='analogo'
        )    
    
    @api.onchange('it_bultos')            
    def _onchange_it_bultos(self):
        if self.weight != 0:
            if self.it_bultos != 0:
               self.it_peso_bultos = self.weight * self.it_bultos
            else:
               # raise ValidationError('Numero de Bultos deben ser Mayor a Cero(0)')            
               print('prueba')
        else:    
            #raise ValidationError('Peso debe ser Mayor a Cero(0)')
            print('prueba')