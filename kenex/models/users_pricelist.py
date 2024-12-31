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

class UserPricelist(models.Model):
    _inherit = 'res.users'
    
    it_pricelist_id = fields.Many2many( 
        'product.pricelist',       # related model 
        'product_res_user_rel',    # relation table name 
        'users_id',                # field for "this" record 
        'pricelist_id',            # field for "other" record 
        string='Tipos de Precios')