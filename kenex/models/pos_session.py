
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

from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    #def get_pos_ui(self):
    #    return super(PosSession, self).get_pos_ui() + [self.env['res.partner']._fields['it_cedula_cliente_id']]


    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].append('it_cedula_cliente_id')
        return result

    # def get_partner_extra_fields(self):
    #     config_id = True
    #     if config_id:
    #             return ['it_cedula_cliente_id']  # Replace with your field names
    #     else:
    #             return []

    # def _loader_params_res_partner(self):
    #     #raise  ValidationError('ENTRE EN _LOADER_PARAMS_RES') 
    #     return {
    #     'search_params':{
    #         'fields':['it_cedula_cliente_id'],
            
    #     },    
            
    # }
    
    # def _get_pos_ui_res_partner(self,params):
    #     #raise  ValidationError('ENTRE EN _GET_POS_UI_RES') 
    #     return self.env['res.partner'].search_read(**params['search_params'])    