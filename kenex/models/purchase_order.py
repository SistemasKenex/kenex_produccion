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

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    it_total_quantity = fields.Integer(string='(Total Cantidad)', store=True, readonly=True, compute='_amount_all')
    @api.depends('order_line.price_total')
    def _amount_all(self):
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            it_total_total = sum(order_lines.mapped('product_qty'))
            order.it_total_quantity = it_total_total
            #raise  ValidationError(it_total_total) 