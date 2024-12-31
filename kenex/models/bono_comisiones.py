from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class BonoComisiones(models.Model):
    """
    Vista SQL que muestra información resumida de los bonos de comisión
    en un rango de fechas específico. No almacena datos directamente.
    """
    _name = 'kbono.comisiones'
    _description = 'Bonos x Rango de Fecha'
    #_auto = False
    company_id     = fields.Many2one('res.company', string='Compañia', default=lambda self: self.env.user.company_id, readonly=True)
    codigo_bono_id = fields.Integer(string='Codigo de Bono', required=True)
    descripcion    = fields.Char(string='Descripcion del Bono', required=True)
    fechadesde     = fields.Date(string='Fecha Desde',required=True)
    fechahasta     = fields.Date(string='Fecha Hasta',required=True)

class BonoArinbo(models.Model):
    """
    Modelo temporal para almacenar datos de bonos antes de insertarlos en las tablas definitivas.
    """

    _name = 'kbono.arinbo'
    _description = 'Modelo temporal para la importacion de kbono.comisiones y kbono.detalle'
    
    company_id     = fields.Many2one('res.company', string='Compañia',default=lambda self: self.env.user.company_id, readonly=True)
    codigo_bono_id = fields.Integer(string='Codigo de Bono', required=False)
    descripcion    = fields.Char(string='Descripcion del Bono', required=True)
    fechadesde     = fields.Date(string='Fecha Desde', required=True)
    fechahasta     = fields.Date(string='Fecha Hasta', required=True)  
    warehouse_id   = fields.Many2one('stock.warehouse' ,string='Almacen', required=True)
    product_id     = fields.Many2one('product.product' ,string='Producto', required=True)
    monto_bono     = fields.Float(string='Monto del Bono', required=True)
    meta           = fields.Float(string='Meta')
    monto_meta     = fields.Float(string='Monto Meta')
    
    """
        Genera registros de bonos y sus detalles a partir de los datos temporales en BonoArinbo.
        Ejecuta consultas SQL para insertar los datos en las tablas definitivas y elimina los registros temporales.
    """
    
    def btn_generar(self):
        cia      = self.company_id.id
        params  = {'cia': cia}
       
        
        # Inserta los datos de los bonos en la tabla kbono.comisiones
        query1 = " SELECT  f_insert_bono_comision(%(cia)s) "
        self.env.cr.execute(query1,params)
            
        # Inserta los detalles de los bonos en la tabla correspondiente
        query2 = " SELECT  f_insert_bono_detalle(%(cia)s) "
        self.env.cr.execute(query2,params)
        
        query3 = " DELETE from kbono_arinbo WHERE company_id = (%(cia)s) "
        self.env.cr.execute(query3,params)