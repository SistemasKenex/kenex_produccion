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

class RevisionPedidos(models.Model):
    _inherit = 'sale.order'

    it_check_value_sale = fields.Char(string='(+-=)')     
    