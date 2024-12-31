# -*- coding: utf-8 -*-
{
    'name': "Kenex",

    'summary': """
        Procesos Propios de Kenex  """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Kenextrading",
    'website': "https://www.yourcompany.com",
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','product','stock','sales_team', 'sale_management','purchase','point_of_sale',
                'contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security_aprobacion_show_group.xml',
        'security/security_solicitud_show_group.xml',
        'security/security_boton_show_vendedores.xml',
        'views/aprobar_pedido_vendedores_view.xml',
        'views/actions_report_refe.xml',
        #'views/pedidos_pedidos_view.xml',
        'views/product_pricelist_item_view.xml',
        'views/mail_channel_view_tree.xml',
        'views/mail_channel_view_form.xml',
        'views/product_template_view.xml',
        'views/product_brand_view.xml',
        'views/report_refe_view.xml',
        'views/templates.xml',
        'views/res_company.xml',
        'views/purchase_order_view.xml',
        'views/calculo_comisiones_view.xml',
        'views/bono_comisiones_view.xml',
        'views/bono_calculo_view.xml',
        'views/bono_detalle_view.xml',
        'views/report_pago_comisiones_view.xml',
        'views/report_macro90_view.xml',
        'views/sale_order_line_view.xml',
        'views/stock_picking_view.xml',
        'views/sale_order_view.xml',
        'views/purchase_order_line_view.xml',
        'views/account_move_view.xml',
        'views/action_view.xml',
        'views/menu_view.xml',
        'views/porcentaje_comisiones.xml',
        'views/calculo_comisiones_tienda.xml',
        'views/product_pricelist_search_view.xml',
        'views/report_refe_search_view.xml',
        'views/users_pricelist_view.xml',
        'views/product_pricelist_item_sellers_view.xml',
        'views/actions_sale_order.xml',
        'views/sale_order_hide.xml',
        'views/report_psi_view.xml',
        'views/aprobar_pre_pedidos_view.xml',
        'views/aprobacion_hide_view.xml',
        'views/solicitud_hide_view.xml',
        'views/boton_vendedores_hide_view.xml',
        'views/boton_enviar_hide_view.xml',
        'views/boton_confirmar_cotizacion_hide_view.xml',
        #'views/estados_wms_view.xml',
        #'views/crea_funcion.xml',
        #'views/assents.xml',
    ],
    # 'assets':{ 
    #     'point_of_sale.assets':[
    #         'kenex/static/src/js/models.js',
    #     ],      
    #     'web.assets_qweb':[
    #         'kenex/static/src/xml/**/*',
    #     ],        
    # },

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}