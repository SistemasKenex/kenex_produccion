# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import json
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
from odoo import fields, models, tools

class PricelistSellers(models.Model):
    _name = 'pricelist.sellers'
    _description = 'Lista de Precio X Vendedor'
    
    
    it_partner_id = fields.Many2one('res.users', string='Usuario', default=lambda self: self.env.user.partner_id)
    it_pricelist_id = fields.Many2one('product.pricelist' , string='Lista de Precio')

    