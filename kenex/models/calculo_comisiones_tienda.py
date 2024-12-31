 #-*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class kcalculo_comisiones_tienda(models.Model):
    """
    Modelo que define el rango de fechas para el cálculo de comisiones de vendedores en tiendas.
    Este modelo no almacena datos, sino que sirve como punto de partida para iniciar los cálculos.
    """

    _name = 'kcalculo.comisiones.tienda'
    _description = 'Calculo de Comisiones Tienda'
    
    company    = fields.Many2one('res.company', string='Compania', default=lambda self: self.env.user.company_id, readonly=True)
    p_cia      = fields.Integer(string='Compania', default=lambda self: self.env.user.company_id, readonly=True)
    fechadesde = fields.Date(string='Fecha Desde',required=True)
    fechahasta = fields.Date(string='Fecha Hasta',required=True)


class DetalleComisionesTienda(models.Model):
    """
    Modelo que almacena los detalles de las comisiones calculadas para cada vendedor y tienda.
    Incluye información como el monto de ventas, descuentos, comisiones y otros datos relevantes.
    """

    _inherit = 'kcalculo.comisiones.tienda'
    _name = 'kdetalle.comisiones.tienda'
    _description = 'Detalle Calculo de Comisiones Tienda'

    company_id                 = fields.Many2one('res.company', string='Compania', default=lambda self: self.env.user.company_id, readonly=True)
    vendedor_id                = fields.Many2one('hr.employee',string='Vendedor')
    tienda_id                  = fields.Many2one('pos.config' ,string='Tienda')
    monto_factura              = fields.Float(string='Monto Facturas')
    monto_descuento            = fields.Float(string='Monto Del Descuentos')
    sub_total                  = fields.Float(string='Sub-Total Facturas')
    #total_factura              = fields.Float(string='Total Facturas')
    comision_descuento         = fields.Float(string='(A) Comision Sobre Descuentos')
    comision_ventas            = fields.Float(string='(B) Comision Ventas')
    bono                       = fields.Float(string='(C) Bono')
    monto_meta                 = fields.Float(string='(D) Monto Meta')
    comision_descuento_ventas  = fields.Float(string='A Pagar (A+B+C+D)')
    #comision_a_pagar           = fields.Float(string='A Pagar (A+B) -100')
    porc_comision              = fields.Float(string='Porcentaje Ventas')
    porc_descuento             = fields.Float(string='Porcentaje Descuento')
    periodo                    = fields.Char(string='Periodo')
 
    """
    Este método inicia el proceso de cálculo de comisiones para el rango de fechas especificado.
    1. Elimina los registros de comisiones existentes para el período seleccionado.
    2. Ejecuta la función `f_comision_vendedores_tienda` para realizar los cálculos.
    3. Muestra los resultados en una vista de lista.
    """
    
    def get_company_id(self):
        self.ensure_one()
        return self.env.company.id
    
    def btn_calcular(self):
        cia      = self.p_cia
        fechad   = self.fechadesde
        fechah   = self.fechahasta
        mesd     = self.fechadesde.month
        anod     = self.fechadesde.year
        mesanod  = str(mesd).zfill(2)+str(anod)
        mesh     = self.fechahasta.month
        anoh     = self.fechahasta.year
        mesanoh  = str(mesh).zfill(2)+str(anoh)
        params  = {'cia': cia,'fechad': fechad, 'fechah': fechah, 'mesanod': mesanod,'mesanoh': mesanoh}
        
        self.env.cr.execute("DELETE FROM kdetalle_comisiones_tienda WHERE company_id = %s AND periodo BETWEEN %s AND %s OR periodo IS NULL", (cia, mesanod, mesanoh))   
               
        query = " SELECT  f_comision_vendedores_tienda(%(cia)s, %(fechad)s, %(fechah)s) "
        self.env.cr.execute(query,params)
        
        query2 = " SELECT  f_bono_comision_tienda(%(cia)s, %(fechad)s, %(fechah)s) "
        self.env.cr.execute(query2,params)
        
        query3 = " SELECT  f_meta_comision_tienda(%(cia)s, %(fechad)s, %(fechah)s) "
        self.env.cr.execute(query3,params)
       
        self.env.cr.execute(" SELECT  *  from kdetalle_comisiones_tienda where company_id = %s and periodo Between %s and %s",(cia, mesanod, mesanoh))
        
        return {
            'name': 'Líneas del Pedido',
            'type': 'ir.actions.act_window',
            'res_model': 'pos.order',
            'view_mode': 'tree,form',
            'domain': [('date_order', '>=', self.fechadesde),
                       ('date_order', '<=', self.fechahasta)],
            'context': {'message': 'Tu acción se ha ejecutado con éxito!'}
            }
        
    def action_view_order_lines(self):
        self.ensure_one()
        return {
            'name': 'Líneas del Pedido',
            'type': 'ir.actions.act_window',
            'res_model': 'pos.order',
            'view_mode': 'tree,form',
            'domain': [('date_order', '>=', self.fechadesde),
                       ('date_order', '<=', self.fechahasta)],
            'context': {'message': 'Tu acción se ha ejecutado con éxito!'}
            }
        
       