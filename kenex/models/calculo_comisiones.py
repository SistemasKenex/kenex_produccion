 #-*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class kporcentaje_marca(models.Model):

    _name = 'kporcentaje.marca'
    _description = ' Porcentajes de Comisiones x Marca'

    company_id     = fields.Many2one('res.company', string='Compania', default=lambda self: self.env.user.company_id, readonly=True)
    marca_id       = fields.Many2one('product.attribute',string='Marca',required=True  )
    pricelist_id   = fields.Many2one('product.pricelist',string='Tipo de Precio',required=True  )
    porc_comision  = fields.Float(string='Porcentaje ',required=True) 
    ind_rep_comision = fields.Char(string='Paga Comision? ',required=True,default='S')    


class kcalculo_comisiones(models.Model):
    _name = 'kcalculo.comisiones'
    _description = 'Calculo de Comisiones'
    
    company    = fields.Many2one('res.company', string='Compania', default=lambda self: self.env.user.company_id, readonly=True)
    p_cia      = fields.Integer(string='Compania', default=lambda self: self.env.user.company_id, readonly=True)
    fechadesde = fields.Date(string='Fecha Desde',required=True)
    fechahasta = fields.Date(string='Fecha Hasta',required=True)
    


class DetalleComisiones(models.Model):
    _inherit = 'kcalculo.comisiones'
    _name = 'kdetalle.comisiones'
    _description = 'Detalle Calculo de Comisiones'

    company_id     = fields.Many2one('res.company', string='Compania', default=lambda self: self.env.user.company_id, readonly=True)
    order_id       = fields.Integer(string='Documento')  
    name           = fields.Char(string='Doc.del Pedido')
    date_order     = fields.Date(string='Fecha')
    vendedor_id    = fields.Many2one('res.users',string='Vendedor')
    cliente_id     = fields.Many2one('res.partner',string='Cliente')
    pricelist_id   = fields.Many2one('product.pricelist',string='Tipo de Precio')
    marca_id       = fields.Many2one('product.attribute',string='Marca')
    price_total    = fields.Float(string='Monto Total de la Venta')
    devolucion     = fields.Float(string='Monto Devolución')
    doc_orig_dev   = fields.Char(string='Doc.Origen Devolución')
    porcentaje     = fields.Float(string='Porcentaje')
    porc_comision  = fields.Float(string='Monto  Comision')    
    margen         = fields.Float(string='Margen')    
    porc_margen    = fields.Float(string='% Margen')    
    precio_base    = fields.Float(string='Costo')   
    bono_comision  = fields.Float(string=' Bono')   
    tot_bono_comision  = fields.Float(string='Comision + Bono')       
       
    def btn_calcular(self):
                
        cia     = self.p_cia
        fechad  = self.fechadesde
        fechah  = self.fechahasta
        params   = {'cia': cia,'fechad': fechad, 'fechah': fechah}
            
        query_del = " delete from kdetalle_comisiones where company_id =  %(cia)s AND date_order >=  %(fechad)s AND date_order <= %(fechah)s or date_order is null"
        self.env.cr.execute(query_del, params)
        #raise UserError(cia)
               
        query = " SELECT  f_comision_vendedores(%(cia)s, %(fechad)s, %(fechah)s) "
        self.env.cr.execute(query,params)
                
        query_nc = " SELECT f_comision_mayor_nc(%(cia)s, %(fechad)s, %(fechah)s) "
        self.env.cr.execute(query_nc,params)
        
        query1 = " SELECT  * from kdetalle_comisiones where company_id =  %(cia)s AND date_order >=  %(fechad)s AND date_order <= %(fechah)s order by date_order"

        self.env.cr.execute(query1, params)
        lines_ids = list(line[0] for line in self.env.cr.fetchall())

        return{
            'type'  : 'ir.actions.act_window',
            'name ' : 'Comisiones de Vendedores',
            'view_type' : 'form',
            'view_mode' : 'tree',
            'res_model' : 'kdetalle.comisiones',  
            'domain': [('id', 'in' ,lines_ids )],
        }

    def action_view_order_lines(self):
        self.ensure_one()
        return {
            'name': 'Líneas del Pedido',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line',
            'view_mode': 'tree,form',
            'domain': [('order_id', '=', self.order_id)],
            'context': dict(self._context, default_order_id=self.order_id)
            }
        
        
    def action_view_anulaciones(self):
        self.ensure_one()
        return {
            'name': 'Líneas de Anulaciones',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('invoice_origin', '=', self.name)],
            'context': dict(self._context, default_invoice_origin=self.name)
            }
        
    def action_view_order(self):
        self.ensure_one()
        return {
            'name': 'Pedido',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('id', '=', self.order_id)],
            'context': dict(self._context, default_id=self.order_id)
            }
        
        
