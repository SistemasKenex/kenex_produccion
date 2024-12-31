# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Kenex(http.Controller):
    @http.route('/kenex/kenex', auth='none')
    def index(self, **kw):
        return "Hello, world"
    
    
    @http.route('/kenex/authenticate', type="json", auth="none", methods=["POST"], csrf=False)
    def authenticate(self, db, login, password):
        """
        Autentica al usuario, actualiza el session_id y lo retorna.
        """
        try:
            # Intentar autenticación
            request.session.authenticate(db, login, password)

            # Si la autenticación es exitosa, obtener el session_id
            session_id = request.session.sid
            user_id = request.session.uid  # ID del usuario autenticado

            if user_id:
                return {
                    "status": "success",
                    "session_id": session_id,
                    "user_id": user_id,
                }
            else:
                return {
                    "status": "error",
                    "message": "Credenciales inválidas",
                }
        except Exception as e:
            return {
                "status": "error",
                "message": "Error al autenticar al usuario",
            }

#     @http.route('/kenex/kenex/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kenex.listing', {
#             'root': '/kenex/kenex',
#             'objects': http.request.env['kenex.kenex'].search([]),
#         })

#     @http.route('/kenex/kenex/objects/<model("kenex.kenex"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kenex.object', {
#             'object': obj
#         })
