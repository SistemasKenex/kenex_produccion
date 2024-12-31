from odoo import api, fields, models, SUPERUSER_ID
import sys
import requests
import json
import logging
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from openerp import api

_logger = logging.getLogger(__name__)
logging.captureWarnings(True)

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    it_check_aprobar_empaque = fields.Boolean('(A.T)',store=True, dafault= False)
    it_check_aprobar_facturacion = fields.Boolean('(A.F)',store=True, dafault= False)
    it_check_aprobar_empaque_vendedor = fields.Boolean('(S.A.T )',store=True, dafault= False)
    it_check_aprobar_facturacion_vendedor = fields.Boolean('(S.A.F)',store=True, dafault= False)
    it_check_aprobar_pre_venta = fields.Boolean('(A.P.V)',store=True, dafault= False)
    it_check_solicitar_pre_venta = fields.Boolean('(S.P.V)',store=True, dafault= False)
    
    it_total_quantity = fields.Integer(string='(Total Cantidad)', store=True, readonly=True, compute='_amount_all')
    it_estado_en_wms = fields.Many2one('estados.wms' ,string=('(Estado en WMS)'))


   # Canal 1 = Solicitud para Trabajar
   # Canal 2 = Solicitud para Facturar
   # Canal 3 = Aprobacion para Trabajar
   # Canal 4 = Aprobacion para Facturar
   # Canal 5 = Administracion Bodega
   # Canal 6 = Administracion Trafico
   # Canal 7 = Administracion Aprobaciones
   # Canal 8 = Solicitar Pre-venta 
   # Canal 9 = Aprobacion de Pre-venta 
   

    def _send_email(self,subject,email_from,email_to,body_html):
        mail_values = {
        'subject': subject,
        'email_from': email_from,
        'email_to': email_to,
        'body_html': body_html,
        }
        msg = self.env['mail.mail'].create(mail_values)
        # Enviar el correo electrónico
        #msg.send()
        return

    def _send_channel_mail(self,canal_id,msg):
        self.env['mail.message'].create({
        'message_type': 'comment',
        'subtype_id': self.env.ref('mail.mt_comment').id,
        'model': 'mail.channel',
        'res_id': canal_id,
        'body': msg,
                })        
        return

    def _send_mail_channel_aprobar(self, correo_vendedor, msg, psubject, id_channel):
        mail_channel_member = self.env['mail.channel.member'].search([('channel_id', '=', id_channel)])
        for reg_mail_channel_member in mail_channel_member:
            channel_partner_id  = reg_mail_channel_member.partner_id.id                        
            res_partner = self.env['res.partner'].search([('id', '=', channel_partner_id)])
            for reg_partner in res_partner:
                correo_channel_member = res_partner.email
                subject     = psubject
                email_from  = correo_vendedor
                email_to    = correo_channel_member
                body_html   = msg
                email = self._send_email(subject,email_from,email_to,body_html)                    
        return

    @api.depends('order_line.price_total')
    def _amount_all(self):
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            it_total_total = sum(order_lines.mapped('product_uom_qty'))
            order.it_total_quantity = it_total_total


    @api.onchange('it_check_aprobar_empaque_vendedor')   
    def _on_change_it_check_aprobar_empaque_vendedor(self):
        if self.it_check_aprobar_empaque_vendedor and self.state == 'sale':   
            # Se busca el Nombre del Cliente
            cliente = self.partner_id.name
            cliente_id = self.partner_id.id
            
            # Se Obtiene el codigo del Vendedor  
            create_uid = self.create_uid.id
            
            # Se Buscan los datos del vendedor en la tabla res_users
            res_users = self.env['res.users'].search([('id', '=', create_uid)])
            for reg_users in res_users:
                correo_vendedor = reg_users.login
                partner_id      = reg_users.partner_id.id  
                
            # Se Buscan los datos del vendedor en la tabla res_partner    
            res_partner = self.env['res.partner'].search([('id', '=', partner_id)])
            for reg_partner in res_partner:
                vendedor  = res_partner.name 
                email     = res_partner.email
            
            # Se arma el mensaje
            msg = '<h4>'+'<em>'+ 'Estimado Colaborador.- ' + '</em>'+'</h4>'
            msg = msg + 'Se solicita  la autorizacion para la Preparación del Pedido: ' + '<strong>' + self.name +'</strong>' + '<br>' +'</br>'
            msg = msg + ' Cliente : ' + '<strong>' + str(cliente_id) + ' - '+ cliente  + '</strong>' +   '<br>' +'</br>'
            msg = msg + ' Vendedor: ' + '<strong>' + vendedor + '</strong>'  
                        
            # Se Buscan los datos del canal segun la tabla de equivalencia mail_channel canal aprobacion para Solicitar trabajo Vendedor
            mail_channel = self.env['mail.channel'].search([('it_channel_propio_id', '=', 1)])
            #raise  ValidationError(mail_channel) 
            for reg_mail_channel in mail_channel:
                channel_mail_id  = reg_mail_channel.id             

            # Se envia le mensaje al canal para solicitar aprobacion
            
            #raise  ValidationError(channel_mail_id) 
            #channel_mail = self._send_channel_mail(channel_mail_id,msg)

            # Se Buscan el ID del canal del Vendedor
            params  = {'partner_id': partner_id}
            query = ''' SELECT mcm.channel_id channel_id
                          FROM res_partner rp, 
                               mail_channel_member mcm,
                               mail_channel mc
                          WHERE rp.id               = mcm.partner_id	
                            AND mcm.partner_id      = %(partner_id)s
                            AND mcm.channel_id      = mc.id
                            AND substr(mc.name,1,7) = 'OdooBot'        
                    '''
            self.env.cr.execute(query,params)   
            channel_id  = list(channel[0] for channel in self.env.cr.fetchall()) 
            
            # Se envia mensaje al Vendedor
            channel_mail = self._send_channel_mail(channel_id[0],msg)
            
            # Se Buscan los datos del canal segun la tabla de equivalencia mail_channel Admin Aprobaciones
            mail_channel = self.env['mail.channel'].search([('it_channel_propio_id', '=', 7)])
            for reg_mail_channel in mail_channel:
                channel_mail_id  = reg_mail_channel.id                        
                        
            # Se envia le mensaje al canal de Aprobacion 
            channel_mail = self._send_channel_mail(channel_mail_id,msg)
            
            #
            # ENVIO DEL EMAIL SOLICITUD DE APROBACION PATA TRABAJO
            #
            subject_aprobacion = 'Solicitud de Aprobacion para facturacion del Pedido ' + self.name 
            correo_channel_aprobacion = self._send_mail_channel_aprobar(correo_vendedor,msg, subject_aprobacion,7)            
            return          

    @api.onchange('it_check_aprobar_facturacion_vendedor')   
    def _on_change_it_check_aprobar_facturacion_vendedor(self):
        if self.it_check_aprobar_facturacion_vendedor and self.state == 'sale':   
            # Se busca el Nombre del Cliente
            cliente = self.partner_id.name
            cliente_id = self.partner_id.id
            
            # Se Obtiene el codigo del Vendedor  
            create_uid = self.create_uid.id
            
            # Se Buscan los datos del vendedor en la tabla res_users
            res_users = self.env['res.users'].search([('id', '=', create_uid)])
            for reg_users in res_users:
                partner_id      = reg_users.partner_id.id  
                
            # Se Buscan los datos del vendedor en la tabla res_partner    
            res_partner = self.env['res.partner'].search([('id', '=', partner_id)])
            for reg_partner in res_partner:
                vendedor  = res_partner.name 
                correo_vendedor = res_partner.email
            
            # Se busca el monto del pedido
            monto_pedido = self.amount_total

            # Se busca la cantidad de piezas del pedido
            cantidad_pedido =  self._amount_all()

            # Se arma el mensaje
            msg = '<h4>'+'<em>'+ 'Estimado Colaborador.- ' + '</em>'+'</h4>'
            msg = msg + 'Se solicita  la autorizacion para la Facturacion del Pedido: ' + '<strong>' + self.name +'</strong>' + '<br>' +'</br>'
            msg = msg + ' Cliente : ' + '<strong>' + str(cliente_id) + ' - '+ cliente  + '</strong>' +   '<br>' +'</br>'
            msg = msg + ' Vendedor: ' + '<strong>' + vendedor + '</strong>'  +  '<br>' +'</br>'
            msg = msg + ' Monto del Pedido: ' + '<strong>' + str(monto_pedido) + '</strong>'  +  '<br>' +'</br>'
            msg = msg + ' Cantidad de piezas: ' + '<strong>' + str(cantidad_pedido) + '</strong>'  
                        
            # Se Buscan los datos del canal segun la tabla de equivalencia mail_channel canal aprobacion para Solicitar Facturacion Vendedor
            mail_channel = self.env['mail.channel'].search([('it_channel_propio_id', '=', 2)])
            for reg_mail_channel in mail_channel:
                channel_mail_id  = reg_mail_channel.id             
                
            # Se envia le mensaje al canal 
            canal_id = channel_mail_id
            channel_mail = self._send_channel_mail(canal_id,msg)

            # Se Buscan el ID del canal del Vendedor
            params  = {'partner_id': partner_id}
            query = ''' SELECT mcm.channel_id channel_id
                          FROM res_partner rp, 
                               mail_channel_member mcm,
                               mail_channel mc
                          WHERE rp.id               = mcm.partner_id	
                            AND mcm.partner_id      = %(partner_id)s
                            AND mcm.channel_id      = mc.id
                            AND substr(mc.name,1,7) = 'OdooBot'
            
                    '''
            self.env.cr.execute(query,params)   
            channel_id  = list(channel[0] for channel in self.env.cr.fetchall())
            
            # Se envia el mensaje al canal al Vendedor
            channel_mail = self._send_channel_mail(channel_id[0],msg)

            # Se Buscan los datos del canal segun la tabla de equivalencia mail_channel Admin Aprobaciones
            mail_channel = self.env['mail.channel'].search([('it_channel_propio_id', '=', 7)])
            for reg_mail_channel in mail_channel:
                channel_mail_id  = reg_mail_channel.id                        
                        
            # Se envia le mensaje al canal de Aprobacion
            channel_mail =  self._send_channel_mail(channel_mail_id,msg)  
            
            #
            # ENVIO DEL EMAIL SOLICITUD DE APROBACION PARA FACTURACION
            # DESDE EL VENDEDOR AL ENCARGADO DE APROBACIONES
            #
            subject_aprobacion = 'Solicitud de Aprobacion para facturacion del Pedido ' + self.name 
            correo_channel_aprobacion = self._send_mail_channel_aprobar(correo_vendedor,msg, subject_aprobacion,7)            
            return          

    @api.onchange('it_check_aprobar_empaque')   
    def _on_change_it_check_aprobar_empaque(self):
        if self.it_check_aprobar_empaque and self.state == 'sale':   
            # Se busca el Nombre del Cliente
            cliente = self.partner_id.name
            cliente_id = self.partner_id.id
            
            # Se Obtiene el codigo del Vendedor  
            create_uid = self.create_uid.id
            
            # Se Buscan los datos del vendedor en la tabla res_users
            res_users = self.env['res.users'].search([('id', '=', create_uid)])
            for reg_users in res_users:
                correo_vendedor = reg_users.login
                partner_id      = reg_users.partner_id.id  
                
            # Se Buscan los datos del vendedor en la tabla res_partner    
            res_partner = self.env['res.partner'].search([('id', '=', partner_id)])
            for reg_partner in res_partner:
                vendedor  = res_partner.name 
            
            # Se arma el mensaje
            msg = '<h4>'+'<em>'+ 'Estimado Colaborador.- ' + '</em>'+'</h4>'
            msg = msg + 'Se autoriza la Preparación del Pedido: ' + '<strong>' + self.name +'</strong>' + '<br>' +'</br>'
            msg = msg + ' Cliente : ' + '<strong>' + str(cliente_id) + ' - '+ cliente  + '</strong>' +   '<br>' +'</br>'
            msg = msg + ' Vendedor: ' + '<strong>' + vendedor + '</strong>'  
                        
            # Se Buscan los datos del canal segun la tabla de equivalencia mail_channel canal aprobacion para Solicitar trabajo Vendedor
            mail_channel = self.env['mail.channel'].search([('it_channel_propio_id', '=', 3)])
            for reg_mail_channel in mail_channel:
                channel_mail_id  = reg_mail_channel.id             
            #raise  ValidationError(channel_mail_id )                                 
            # Se envia le mensaje al canal 
            canal_id = channel_mail_id
            channel_mail = self._send_channel_mail(canal_id,msg)     

            # Se Buscan el ID del canal del Vendedor
            params  = {'partner_id': partner_id}
            query = ''' SELECT mcm.channel_id channel_id
                          FROM res_partner rp, 
                               mail_channel_member mcm,
                               mail_channel mc
                          WHERE rp.id               = mcm.partner_id	
                            AND mcm.partner_id      = %(partner_id)s
                            AND mcm.channel_id      = mc.id
                            AND substr(mc.name,1,7) = 'OdooBot'
            
                    '''
            self.env.cr.execute(query,params)   
            channel_id  = list(channel[0] for channel in self.env.cr.fetchall())
            #raise  ValidationError('canal vendedor :' + str(channel_id)) 
            
            # Se envia mensaje al Vendedor
            channel_mail = self._send_channel_mail(channel_id[0],msg)     
            
            # Se Buscan los datos del canal segun la tabla de equivalencia mail_channel Admin Aprobaciones
            mail_channel = self.env['mail.channel'].search([('it_channel_propio_id', '=', 7)])
            for reg_mail_channel in mail_channel:
                channel_mail_id  = reg_mail_channel.id                        
                        
            # Se envia le mensaje al canal 
            channel_mail = self._send_channel_mail(channel_mail_id,msg)      

            # Se Buscan los datos del canal segun la tabla de equivalencia mail_channel canal aprobacion para Trabajar Bodega
            mail_channel = self.env['mail.channel'].search([('it_channel_propio_id', '=', 5)])
            for reg_mail_channel in mail_channel:
                channel_mail_id  = reg_mail_channel.id             
            #raise  ValidationError(channel_mail_id )                                 
            # Se envia le mensaje al canal 
            channel_mail = self._send_channel_mail(channel_mail_id,msg)      

            # ENVIO DEL EMAIL SOLICITUD DE APROBACION PARA FACTURACION
            # DESDE EL VENDEDOR AL ENCARGADO DE APROBACIONES
            #
            subject_aprobacion = 'Solicitud de Autorizacion para trabajar el Pedido ' + self.name 
            correo_channel_aprobacion = self._send_mail_channel_aprobar(correo_vendedor,msg, subject_aprobacion,7)            

            # ENVIO DEL EMAIL SOLICITUD DE APROBACION PARA FACTURACION
            # DESDE EL VENDEDOR AL ENCARGADO DE BODEGA
            #
            subject_aprobacion = 'Solicitud de Autorizacion para trabajar el Pedido ' + self.name 
            correo_channel_aprobacion = self._send_mail_channel_aprobar(correo_vendedor,msg, subject_aprobacion,5)            

            return          

    @api.onchange('it_check_aprobar_facturacion')   
    def _on_change_it_check_aprobar_facturacion(self):
        if self.it_check_aprobar_facturacion and self.state == 'sale':   
            # Se busca el Nombre del Cliente
            cliente = self.partner_id.name
            cliente_id = self.partner_id.id
            
            # Se Obtiene el codigo del Vendedor  
            create_uid = self.create_uid.id
            
            # Se Buscan los datos del vendedor en la tabla res_users
            res_users = self.env['res.users'].search([('id', '=', create_uid)])
            for reg_users in res_users:
                correo_vendedor = reg_users.login
                partner_id      = reg_users.partner_id.id  
                
            # Se Buscan los datos del vendedor en la tabla res_partner    
            res_partner = self.env['res.partner'].search([('id', '=', partner_id)])
            for reg_partner in res_partner:
                vendedor  = res_partner.name 
            
            # Se arma el mensaje
            msg = '<h4>'+'<em>'+ 'Estimado Colaborador.- ' + '</em>'+'</h4>'
            msg = msg + 'Se autoriza la Preparación del Pedido: ' + '<strong>' + self.name +'</strong>' + '<br>' +'</br>'
            msg = msg + ' Cliente : ' + '<strong>' + str(cliente_id) + ' - '+ cliente  + '</strong>' +   '<br>' +'</br>'
            msg = msg + ' Vendedor: ' + '<strong>' + vendedor + '</strong>'  
                        
            # Se Buscan los datos del canal segun la tabla de equivalencia mail_channel canal aprobacion Facturacion
            mail_channel = self.env['mail.channel'].search([('it_channel_propio_id', '=', 5)])
            for reg_mail_channel in mail_channel:
                channel_mail_id  = reg_mail_channel.id             
            #raise  ValidationError(channel_mail_id )                                 
            # Se envia le mensaje al canal 
            channel_mail = self._send_channel_mail(channel_mail_id,msg)      
            
            # Se Buscan el ID del canal del Vendedor
            params  = {'partner_id': partner_id}
            query = ''' SELECT mcm.channel_id channel_id
                          FROM res_partner rp, 
                               mail_channel_member mcm,
                               mail_channel mc
                          WHERE rp.id               = mcm.partner_id	
                            AND mcm.partner_id      = %(partner_id)s
                            AND mcm.channel_id      = mc.id
                            AND substr(mc.name,1,7) = 'OdooBot'
                    '''
            self.env.cr.execute(query,params)   
            channel_id  = list(channel[0] for channel in self.env.cr.fetchall())
            
            # Se envia mensaje al Vendedor
            channel_mail = self._send_channel_mail(channel_id[0],msg)      
            
            # Se Buscan los datos del canal segun la tabla de equivalencia mail_channel Admin Aprobaciones
            mail_channel = self.env['mail.channel'].search([('it_channel_propio_id', '=', 7)])
            for reg_mail_channel in mail_channel:
                channel_mail_id  = reg_mail_channel.id                        
                        
            # Se envia le mensaje al canal 
            channel_mail = self._send_channel_mail(channel_mail_id,msg)      
            # Se Buscan los datos del canal segun la tabla de equivalencia mail_channel canal aprobacion para Facturacion Trafico
            mail_channel = self.env['mail.channel'].search([('it_channel_propio_id', '=', 6)])
            for reg_mail_channel in mail_channel:
                channel_mail_id  = reg_mail_channel.id             

            # Se envia le mensaje al canal 
            channel_mail = self._send_channel_mail(channel_mail_id,msg)      

            # ENVIO DEL EMAIL SOLICITUD DE APROBACION PARA FACTURACION
            # DESDE EL VENDEDOR AL ENCARGADO DE APROBACIONES
            #
            subject_aprobacion = 'Solicitud de Autorizacion para facturar el Pedido ' + self.name 
            correo_channel_aprobacion = self._send_mail_channel_aprobar(correo_vendedor,msg, subject_aprobacion,7) 

            # ENVIO DEL EMAIL SOLICITUD DE APROBACION PARA FACTURACION
            # DESDE EL VENDEDOR AL ENCARGADO DE TRAFICO
            #
            subject_aprobacion = 'Solicitud de Autorizacion para trabajar el Pedido ' + self.name 
            correo_channel_aprobacion = self._send_mail_channel_aprobar(correo_vendedor,msg, subject_aprobacion,6)
            return          

    # Funcion para mostrar los tipos de precios en Sale.Order
    def actions_funcion(self):
        # Obtener el ID del usuario conectado
        users_id = self. _uid 
        # Obtener el id  de las Lista de Precios asignadas al usuario
        params   = {'p_users_id': users_id  } 
        query = """ SELECT pricelist_id FROM product_res_user_rel where users_id =  %(p_users_id)s """
        self.env.cr.execute(query,params)
        lines_ids = list(line[0] for line in self.env.cr.fetchall())
        #res = {}
        #res['domain'] = {'it_product_pricelist_id': [('id', 'in', lines_ids)]}
        # 'domain': [('order_id', '=', self.documento)],
        #raise  ValidationError(lines_ids)
        self.ensure_one()
        return { 'name': 'Tipos de Precios',
                'type': 'ir.actions.act_window',
                'res_model': 'product.pricelist.item',
                'view_mode': 'tree,form', 
                'target': 'new',
                'context': {} ,
                'domain': [('pricelist_id', 'in' ,lines_ids )],
                'view' : [(self.env.ref('kenex.product_pricelist_item_tree_window5').id),'tree']
                }
# Funcion para mostrar el Reporte de refenecia
    def actions_funcion_refe(self):
        #raise  ValidationError('entre')
        #self.ensure_one()
        return { 'name': 'Reporte de Referencia',
                 'type': 'ir.actions.act_window',
                 'res_model': 'report.refe',
                 'view_mode': 'tree,form', 
                 'target': 'new',
                 'view' : [(self.env.ref('kenex.actions_report_refe').id),'tree']
                }

    # Cambio de Precio en tipos de Precios de la Linea     
    @api.onchange('pricelist_id')                       
    def _onchange_pricelist_id(self):
        #ID lista de Precios
        pricelist_id = self.pricelist_id
        # Obtener datos del producto
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            #order_lines.mapped('it_product_pricelist_id') = pricelist_id
            order_lines.it_product_pricelist_id = pricelist_id


    # Funcion para mostrar los tipos de precios de vendedores en Sale.Order        
    # def action_product_pricelist_item_sellers(self):
    #     # Se borra la tabla que contiene la lista d Precios
    #     self.env.cr.execute("DELETE FROM product_pricelist_item_sellers")   
        
    #     # Se crea la tabla con el Pivot entre articulos y listas de Precios
    #     query =  """
    #                 insert into product_pricelist_item_sellers 
    #                     SELECT *, NOW() as create_date, 'odoo' write_date 
    #                         FROM crosstab(
    #                             'SELECT ppi.product_tmpl_id   , 
    #                                     ppi.pricelist_id,
    #                                     min_quantity
    #                             FROM product_pricelist_item ppi,
    #                                 product_pricelist pp
    #                             where  pp.id  = ppi.pricelist_id
    #                             ORDER BY 1,2 ',
    #                             'SELECT DISTINCT  pricelist_id
    #                                 FROM product_pricelist_item 
    #                             ORDER BY 1'
    #                         ) AS ct ("Product_ID "  float , "Precio 1"  float , "Precio 2"  float , "Precio 3"  float , 
    #                                                     "Precio 4"  float , "Precio 5"  float , "Precio 6"  float ,
    #                                                     "Precio 7"  float , "Precio 8" float  , "Precio 9" float ,
    #                                                     "Precio 10" float , "Precio 11" float , "Precio 12" float,
    #                                                     "Precio 13"  float, "Precio 14"  float)
    #                 """               
    #     self.env.cr.execute(query)        
        
    #     # Se ejecuta la comnsulta para ser mostrada de la lista de precios
    #     query = """ SELECT  pp.product_id  as id,
    #                         pt.name::json->>'en_US' as name , 
    #                         pp.precio1   ,
    #                         pp.precio2   ,
    #                         pp.precio3   ,
    #                         pp.precio4   ,
    #                         pp.precio5   ,
    #                         pp.precio6   ,
    #                         pp.precio7   ,
    #                         pp.precio8   ,
    #                         pp.precio9   ,
    #                         pp.precio10  ,
    #                         pp.precio11  ,
    #                         pp.precio12  ,
    #                         pp.precio13  ,
    #                         pp.precio14  
    #                    FROM product_pricelist_item_sellers  pp,
    #                         product_template pt	       
    #                    WHERE pp.product_id = pt.id     
    #         """        
    #     self.env.cr.execute(query)
    #     lines_ids = list(line[0] for line in self.env.cr.fetchall())
    #     return{
    #         'name': 'Tipo de Pedido',
    #         'type'  : 'ir.actions.act_window',
    #         'view_type' : 'form',
    #         'view_mode' : 'tree',
    #         'res_model' : 'product.pricelist.item.sellers',  