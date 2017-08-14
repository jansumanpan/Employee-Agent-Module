# -*- coding: utf-8 -*-
from openerp import http

# class EmployeeAgent(http.Controller):
#     @http.route('/employee_agent/employee_agent/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_agent/employee_agent/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_agent.listing', {
#             'root': '/employee_agent/employee_agent',
#             'objects': http.request.env['employee_agent.employee_agent'].search([]),
#         })

#     @http.route('/employee_agent/employee_agent/objects/<model("employee_agent.employee_agent"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_agent.object', {
#             'object': obj
#         })