# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import json
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
from odoo import fields, models, tools

class ReportMaro90(models.Model):
    _name = "report.macro90"
    _description = "Reporte Macro 90"
    _auto = False

    articulo = fields.Char("Articulo ", readonly=True)    #miguel
    existencia_kt = fields.Integer("Existencia KT ", readonly=True)  
    bonos_kt = fields.Char("Bonos KT ", readonly=True)  
    existencia_srzl = fields.Integer("Existencia SRZL ", readonly=True)  
    bonos_srzl = fields.Char("Bonos SRZL ", readonly=True)  
    transito_kt = fields.Integer("Transito KT ", readonly=True)      #miguel
    transito_real = fields.Integer("Transito Real ", readonly=True)  #miguel
    disponible_kt = fields.Integer("Disponible KT ", readonly=True)  #miguel
    ped_pendiente_kt = fields.Integer("Pedidos Pendientes KT", readonly=True)  
    pre_pedidos_pendientes_kt = fields.Integer("Pre Pedidos Pendienntes KT ", readonly=True)  
    autorizado_kt = fields.Char("Autorizado KT ", readonly=True)        
    ultimo_costo  = fields.Float("Ultimo Costo ", readonly=True)  
    precio_base = fields.Float("Precio Base", readonly=True)  
    costo_promedio = fields.Float("Costo Promedio ", readonly=True)  
    precio_base_al = fields.Float("Precio Base Al ", readonly=True)  
    ex_wh = fields.Integer("Existencia WH", readonly=True)
    ex_cubitt_albrook_tigre = fields.Integer("Existencia Cubitt Albrook", readonly=True)
    ex_mayor_panama = fields.Integer("Existencia Mayor Panama", readonly=True)
    ex_casio_albrook_carrusel = fields.Integer("Existencia Albrook Carrusel", readonly=True)
    ex_multiplaza = fields.Integer("Existencia Multiplaza ", readonly=True)
    ex_metromall = fields.Integer("Existencia Metromall", readonly=True)
    ex_albrook_pinguino = fields.Integer("Existencia Pinguino", readonly=True)
    ex_altaplaza_mall = fields.Integer("Existencia Altaplaza Mall", readonly=True)
    ex_los_andes_mall = fields.Integer("Existencia Los Andes  Mall", readonly=True)
    ex_westland_mall = fields.Integer("Existencia West", readonly=True)
    ex_basaidai = fields.Integer("Existencia Basaidai", readonly=True)  
    lista_precio_an = fields.Float("Lista de Precio AN", readonly=True)  
    lista_precio_cn = fields.Float("Lista de Precio CN", readonly=True)  
    lista_precio_do = fields.Float("Lista de Precio DO", readonly=True)  
    lista_precio_ds = fields.Float("Lista de Precio DS", readonly=True)  
    lista_precio_es = fields.Float("Lista de Precio ES ", readonly=True)  
    lista_precio_fk = fields.Float("Lista de Precio FK", readonly=True)  
    lista_precio_fr = fields.Float("Lista de Precio FR", readonly=True)  
    lista_precio_fv = fields.Float("Lista de Precio FV", readonly=True)  
    lista_precio_ms = fields.Float("Lista de Precio MS", readonly=True)  
    lista_precio_p_plus = fields.Float("Lista de Precio P+", readonly=True)  
    lista_precio_pa = fields.Float("Lista de Precio PA", readonly=True)  
    lista_precio_pb = fields.Float("Lista de Precio PB", readonly=True)  
    lista_precio_pr = fields.Float("Lista de Precio PR", readonly=True)  
    lista_precio_ta = fields.Float("Lista de Precio TA", readonly=True)  
    lista_precio_tm = fields.Float("Lista de Precio TM", readonly=True)  

    @property
    def _table_query(self):
        query = """
                SELECT pt.id                                                   AS id, 
                    pt.name::json->>'en_US'                                    AS articulo,
                    f_existencia_almacen(pt.id, '0101')                        AS existencia_kt,
                    'N'                                                        AS bonos_kt , /* por hacer*/
                    f_existencia_almacen(pt.id, '0102')                        AS existencia_srzl,
                    'N'                                                        AS bonos_srzl , /* por hacer*/
                    f_mercancia_en_transito_articulo(pt.id)                    AS transito_kt,  
                    f_get_transito_real_articulo('91', pt.id,'0101')           AS transito_real,
                    f_get_disponible(pt.id, '0101')                            AS disponible_kt,
                    f_get_saliente(pt.id, '0101')                              AS ped_pendiente_kt,
                    f_get_pre_pedidos_pendientes(pt.id)                        AS pre_pedidos_pendientes_kt, 
                    f_get_pedidos_autorizados(pt.id)                           AS autorizado_kt,       
                    f_get_valor_ultima_compra(pt.id)                           AS ultimo_costo,
                    f_pbase(pt.id)                                             AS precio_base,
                    f_pbase(pt.id)                                             AS costo_promedio,
                    f_pbase(pt.id)                                             AS precio_base_al,
                    f_existencia_almacen(pt.id, 'WH')                          AS ex_wh,
                    f_existencia_almacen(pt.id, '0505')                        AS ex_cubitt_albrook_tigre,
                    f_existencia_almacen(pt.id, '0808')                        AS ex_mayor_panama,
                    f_existencia_almacen(pt.id, '0909')                        AS ex_casio_albrook_carrusel,
                    f_existencia_almacen(pt.id, '1010')                        AS ex_multiplaza,
                    f_existencia_almacen(pt.id, '1111')                        AS ex_metromall,
                    f_existencia_almacen(pt.id, '1212')                        AS ex_albrook_pinguino,
                    f_existencia_almacen(pt.id, '1313')                        AS ex_altaplaza_mall,
                    f_existencia_almacen(pt.id, '1414')                        AS ex_los_andes_mall,
                    f_existencia_almacen(pt.id, '1515')                        AS ex_westland_mall,
                    f_existencia_almacen(pt.id, '2020')                        AS ex_basaidai,   
                    f_get_lista_precio_articulo('91',pt.id,'AN')               AS lista_precio_an,
                    f_get_lista_precio_articulo('91',pt.id,'CN')               AS lista_precio_cn,
                    f_get_lista_precio_articulo('91',pt.id,'DO')               AS lista_precio_do,
                    f_get_lista_precio_articulo('91',pt.id,'DS')               AS lista_precio_ds,
                    f_get_lista_precio_articulo('91',pt.id,'ES')               AS lista_precio_es,
                    f_get_lista_precio_articulo('91',pt.id,'FK')               AS lista_precio_fk,
                    f_get_lista_precio_articulo('91',pt.id,'FR')               AS lista_precio_fr,
                    f_get_lista_precio_articulo('91',pt.id,'FV')               AS lista_precio_fv,
                    f_get_lista_precio_articulo('91',pt.id,'MS')               AS lista_precio_ms,
                    f_get_lista_precio_articulo('91',pt.id,'P+')               AS lista_precio_p_plus,
                    f_get_lista_precio_articulo('91',pt.id,'PA')               AS lista_precio_pa,
                    f_get_lista_precio_articulo('91',pt.id,'PB')               AS lista_precio_pb,
                    f_get_lista_precio_articulo('91',pt.id,'PR')               AS lista_precio_pr,
                    f_get_lista_precio_articulo('91',pt.id,'TA')               AS lista_precio_ta,
                    f_get_lista_precio_articulo('91',pt.id,'TM')               AS lista_precio_tm
                from product_template pt	
                
            """
        return query
