# -*- coding: utf-8 -*-

from odoo import models, fields, api


class kenex(models.Model):
    _name = 'kenex.kenex'
    _description = 'kenex.kenex'

    fecha_desde = fields.Date(string='Fecha Desde')
    fecha_hasta = fields.Date(string='Fecha Hasta')

    def ejecutar_reporte_pci(self):
        print ('hola mundo')

    def cancelar_reporte_pci(self):
        print ('hola mundo')          