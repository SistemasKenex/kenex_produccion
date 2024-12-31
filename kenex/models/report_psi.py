# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools

class ReportPsi(models.Model):
    _name = "report.psi"
    _description = "Reporte Psi"
    _auto = False

    articulo = fields.Char("Articulo", readonly=True)
    clase = fields.Char("Clase", readonly=True)
    ex_france_field = fields.Integer("Existencia France Field", readonly=True)
    transito = fields.Integer("Transito", readonly=True)
    f_ult_ec_wh = fields.Date("Ult. Entrada x Compra WH", readonly=True)
    f_ult_ec_kenex = fields.Date("Ult. Entrada x Compra Kenex", readonly=True)
    f_ult_ec_showroom_zl = fields.Date("Ult. Entrada x Compra ZL", readonly=True)
    f_ult_ec_cubbit_albrook_tigre = fields.Date("Ult. Entrada x Compra Cubitt Albrook Tigre", readonly=True)
    f_ult_ec_mayor_panama = fields.Date("Ult. Entrada x Compra Mayor Panama", readonly=True)
    f_ult_ec_casio_albrook_carrusel = fields.Date("Ult. Entrada x Compra Albrook Carrusel", readonly=True)
    f_ult_ec_multiplaza = fields.Date("Ult. Entrada x Compra Multi Plaza", readonly=True)
    f_ult_ec_metromall = fields.Date("Ult. Entrada x Compra Metro Mall", readonly=True)
    f_ult_ec_albrook_pinguino = fields.Date("Ult. Entrada x Compra Albrook Pinguino", readonly=True)
    f_ult_ec_altaplaza_mall = fields.Date("Ult. Entrada x Compra Alta Plaza Mall", readonly=True)
    f_ult_ec_los_andes_mall = fields.Date("Ult. Entrada x Compra Los Andes Plaza Mall", readonly=True)
    f_ult_ec_wesland_mall = fields.Date("Ult. Entrada x Compra Wesland Mall", readonly=True)
    f_ult_ec_basaidai = fields.Date("Ult. Entrada x Compra Wesland Mall", readonly=True)
    precio_base = fields.Float("Precio Base", readonly=True)
    ex_wh = fields.Integer("Existencia WH", readonly=True)
    ex_kenex = fields.Integer("Existencia Kenex", readonly=True)
    ex_showroom_zl = fields.Integer("Existencia Showroon ZL", readonly=True)
    ex_cubitt_albrook_tigre = fields.Integer("Existencia Albrook Tigre", readonly=True)
    ex_mayor_panama = fields.Integer("Existencia Mayor Panama", readonly=True)
    ex_casio_albrook_carrusel = fields.Integer("Existencia Albrook Carrusel", readonly=True)
    ex_multiplaza = fields.Integer("Existencia Multiplaza", readonly=True)
    ex_metromall = fields.Integer("Existencia Metro Mall", readonly=True)
    ex_albrook_pinguino = fields.Integer("Existencia Albrook Pinguino", readonly=True)
    ex_altaplaza_mall = fields.Integer("Existencia Alta Plaza", readonly=True)
    ex_los_andes_mall = fields.Integer("Existencia Los Andes Mall", readonly=True)
    ex_westland_mall = fields.Integer("Existencia Westland Mall", readonly=True)
    ex_basaidai = fields.Integer("Existencia Basaidai", readonly=True)   
    pedido = fields.Integer("Pedido", readonly=True)   
    ventas = fields.Integer("Ventas", readonly=True)   
    ex_mes6 = fields.Integer("Existencia Ultimos 6 Meses Anteriores", readonly=True)   
    ex_mes5 = fields.Integer("Existencia Ultimos 5 Meses Anteriores", readonly=True)   
    ex_mes4 = fields.Integer("Existencia Ultimos 4 Meses Anteriores", readonly=True)   
    ex_mes3 = fields.Integer("Existencia Ultimos 3 Meses Anteriores", readonly=True)   
    ex_mes2 = fields.Integer("Existencia Ultimos 2 Meses Anteriores", readonly=True)   
    ex_mes1 = fields.Integer("Existencia Ultimo Meses Anterior", readonly=True)   
    total = fields.Integer("Total Existencia Ultimos 6 Meses", readonly=True)   
    prom = fields.Integer("Promedio Ventas", readonly=True)   
    min = fields.Integer("Min", readonly=True)   

    @property
    def _table_query(self):
        query = """
        SELECT
            pt.id                                                  AS id,
            pt.company_id                                          AS cia,
            pt.name::json->>'en_US'                                   AS articulo,
            /*
            pt.default_code                                        AS articulo,
            */
            pc.complete_name                                       AS Clase,
            f_existencia_almacen(pt.id, '0101')                    AS ex_france_field,
            /*
            case
            when pt.x_studio_descontinuado = 'true' then 'ACTIVO'
            else
            'DESCONTINUADO'
            end Estado,
            */
            f_mercancia_en_transito_articulo(pt.id)                AS transito,
            --
            to_char(f_f_ult_ec_tienda(pt.id,'WH')   ,'YYYY-MM-DD') AS f_ult_ec_wh,
            to_char(f_f_ult_ec_tienda(pt.id,'0101') ,'YYYY-MM-DD') AS f_ult_ec_kenex,
            to_char(f_f_ult_ec_tienda(pt.id,'0102') ,'YYYY-MM-DD') AS f_ult_ec_showroom_zl,
            to_char(f_f_ult_ec_tienda(pt.id,'0505') ,'YYYY-MM-DD') AS f_ult_ec_cubbit_albrook_tigre,
            to_char(f_f_ult_ec_tienda(pt.id,'0808') ,'YYYY-MM-DD') AS f_ult_ec_mayor_panama,
            to_char(f_f_ult_ec_tienda(pt.id,'0909') ,'YYYY-MM-DD') AS f_ult_ec_casio_albrook_carrusel,
            to_char(f_f_ult_ec_tienda(pt.id,'1010') ,'YYYY-MM-DD') AS f_ult_ec_multiplaza,
            to_char(f_f_ult_ec_tienda(pt.id,'1111') ,'YYYY-MM-DD') AS f_ult_ec_metromall,
            to_char(f_f_ult_ec_tienda(pt.id,'1212') ,'YYYY-MM-DD') AS f_ult_ec_albrook_pinguino,
            to_char(f_f_ult_ec_tienda(pt.id,'1313') ,'YYYY-MM-DD') AS f_ult_ec_altaplaza_mall,
            to_char(f_f_ult_ec_tienda(pt.id,'1414') ,'YYYY-MM-DD') AS f_ult_ec_los_andes_mall,
            to_char(f_f_ult_ec_tienda(pt.id,'1515') ,'YYYY-MM-DD') AS f_ult_ec_wesland_mall,
            --
            to_char(f_f_ult_ec_tienda(pt.id,'2020') ,'YYYY-MM-DD') AS f_ult_ec_basaidai,
            f_pbase(pt.id)                                         AS precio_base,
            --
            f_existencia_almacen(pt.id, 'WH')                      AS ex_wh,
            f_existencia_almacen(pt.id, '0101')                    AS ex_kenex,
            f_existencia_almacen(pt.id, '0102')                    AS ex_showroom_zl,
            f_existencia_almacen(pt.id, '0505')                    AS ex_cubitt_albrook_tigre,
            f_existencia_almacen(pt.id, '0808')                    AS ex_mayor_panama,
            f_existencia_almacen(pt.id, '0909')                    AS ex_casio_albrook_carrusel,
            f_existencia_almacen(pt.id, '1010')                    AS ex_multiplaza,
            f_existencia_almacen(pt.id, '1111')                    AS ex_metromall,
            f_existencia_almacen(pt.id, '1212')                    AS ex_albrook_pinguino,
            f_existencia_almacen(pt.id, '1313')                    AS ex_altaplaza_mall,
            f_existencia_almacen(pt.id, '1414')                    AS ex_los_andes_mall,
            f_existencia_almacen(pt.id, '1515')                    AS ex_westland_mall,
            f_existencia_almacen(pt.id, '2020')                    AS ex_basaidai,
            f_cantidad_ventas_articulos(pt.id,'draft')             AS pedido,
            f_cantidad_ventas_articulos(pt.id,'sale' )             AS ventas,
        --
            f_existencia_almacen_mes(pt.id,'2024-08-31',6)         AS ex_mes6,
            f_existencia_almacen_mes(pt.id,'2024-08-31',5)         AS ex_mes5,
            f_existencia_almacen_mes(pt.id,'2024-08-31',4)         AS ex_mes4,
            f_existencia_almacen_mes(pt.id,'2024-08-31',3)         AS ex_mes3,
            f_existencia_almacen_mes(pt.id,'2024-08-31',2)         AS ex_mes2,
            f_existencia_almacen_mes(pt.id,'2024-08-31',1)         AS ex_mes1,
        --
            f_existencia_almacen_mes(pt.id,'2024-08-31',6)       +
            f_existencia_almacen_mes(pt.id,'2024-08-31',5)       +
            f_existencia_almacen_mes(pt.id,'2024-08-31',4)       +
            f_existencia_almacen_mes(pt.id,'2024-08-31',3)       +
            f_existencia_almacen_mes(pt.id,'2024-08-31',2)       +
            f_existencia_almacen_mes(pt.id,'2024-08-31',1)                     AS total,
            f_promedio_ventas(pt.id,'sale' )                      AS prom,
            f_promedio_ventas(pt.id,'sale') * 2                   AS min
        --
        FROM product_template pt,product_category pc
        where pt.categ_id    = pc.id
        
            """
        return query







