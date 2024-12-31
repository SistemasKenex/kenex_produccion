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

class EstadoWms(models.Model):
    _name = 'estados.wms'
    _description = 'Estado WMS'

    name = fields.Char(string='(Estado WMS)')