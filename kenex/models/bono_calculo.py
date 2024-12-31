
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class BonoComisiones(models.Model):
    """
    Esta clase representa los detalles de los bonos de comisión calculados.
    Almacena información como la compañía, el identificador del documento 
    relacionado (opcional), la fecha del documento, el vendedor asociado al bono, 
    el producto (opcional), el almacén (opcional), el número de pedido (opcional), 
    el monto total del bono (requerido), la meta de ventas utilizada para el 
    cálculo (opcional), un campo para almacenar el cálculo del bono (opcional), 
    la descripción del bono (requerido), y el período del bono definido por la fecha 
    desde y fecha hasta (ambas requeridas).
    """
    _name = 'kbono.calculo'
    _description = 'Detalle Bonos Calculados'
    
    company_id     = fields.Many2one('res.company', string='Compañia', default=lambda self: self.env.user.company_id, readonly=True)
    documento      = fields.Char(string='Documento')
    fecha_orden    = fields.Date(string='Fecha Documento',required=True)
    vendedor       = fields.Many2one('res.users',string='Vendedor')
    producto       = fields.Many2one('product.product' ,string='Producto')
    almacen        = fields.Many2one('stock.warehouse' ,string='Almacen')
    pedido         = fields.Integer(string='Pedido')
    monto_bono     = fields.Float(string='Monto del Bono', required=True)
    meta           = fields.Float(string='Meta')
    calculo_bono   = fields.Integer(string='Calculo Bono')
    descripcion    = fields.Char(string='Descripcion del Bono', required=True)
    fechadesde     = fields.Date(string='Fecha Desde',required=True)
    fechahasta     = fields.Date(string='Fecha Desde',required=True)

    def action_view_order_lines(self):
        self.ensure_one()
        return {
            'name': 'Líneas de la Orden',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line',
            'view_mode': 'tree,form',
            'domain': [('order_id', '=', self.documento)],
            'context': dict(self._context, default_order_id=self.documento)
            }
        
    