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

class ResCompany(models.Model):
    _inherit = 'res.company'

    it_company_id = fields.Char('(ID Compañia NAF) ')