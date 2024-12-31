from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class BonoDetalle(models.Model):
    
   _name = 'kbono.detalle'
   _description = 'Bonos x Detalle de Articulo'
   
   company_id      = fields.Many2one('res.company', string='Compañia', default=lambda self: self.env.user.company_id, readonly=True)
   codigo_bono_id  = fields.Many2one('kbono.comisiones',string='ID del Bono', required=True)
   warehouse_id    = fields.Many2one('stock.warehouse' ,string='Almacen'      , required=True)
   product_id      = fields.Many2one('product.product' ,string='Producto'     , required=True)
   monto_bono      = fields.Float(string='Monto Bono')
   meta            = fields.Float(string='Meta')    
   monto_meta      = fields.Float(string='Monto Meta')    

class SaleOrder(models.Model):
    _inherit = 'kbono.detalle'

    def action_view_order_lines(self):
        self.ensure_one()
        return {
            'name': 'Líneas de la Orden',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line',
            'view_mode': 'tree',
            'domain': [('company_id', '=', self.id)],
            'context': dict(self._context, default_order_id=self.id)
        }