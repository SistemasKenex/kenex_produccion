from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class BonoComisiones(models.Model):
    _name = 'kporcentaje.comisiones'
    _description = 'Porcentaje de Comisiones x Meta y Tienda'

    company_id     = fields.Many2one('res.company', string='Compañia', default=lambda self: self.env.user.company_id, readonly=True)
    tienda_id      = fields.Many2one('pos.config' ,string='Tienda'      , required=True)
    monto_desde    = fields.Float(string='Monto Desde', required=True)
    monto_hasta    = fields.Float(string='Monto Hasta',required=True)
    porcentaje     = fields.Float(string='Porcentaje Comision',required=True)
    ind_porc_desc  = fields.Char(string='Aplica % al Decuento',required=True)
    porc_descuento = fields.Float(string='Porcentaje Sobre Descuento',required=True)

