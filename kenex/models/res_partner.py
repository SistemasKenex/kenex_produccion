from odoo import api, fields, models, SUPERUSER_ID
import sys
import requests
import json
import logging
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)
logging.captureWarnings(True)

class ResPartner(models.Model):
    #_name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'Res Partner'
    
    it_cedula_cliente_id = fields.Integer(string='(Cedula)')
    
def name_get(self):
    result = []    
    for rec in self:
        result.append (( rec.id, '%s - %s'%( rec.id, rec.name)))
        return result