# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import Warning

class employee_agent(models.Model):
    _inherit = 'res.partner'

    employee = fields.Boolean(string="Employee")
    employee_id = fields.Many2one('hr.employee',string='Emp ID',ondelete='cascade')




class agent_override(models.Model):
	_inherit = 'hr.employee'

	is_agent = fields.Boolean(string="Agent")

	@api.model
	def create(self,vals):
		res = super(agent_override,self).create(vals)
		values_of_res_partner = {}
		values_of_res_partner['name'] = vals['name']
		values_of_res_partner['email'] = vals['work_email']
		values_of_res_partner['phone'] = vals['work_phone']
		values_of_res_partner['employee'] = True
		values_of_res_partner['agent'] = True
		if vals['is_agent'] == True:
			res1 = self.env['res.partner'].create(values_of_res_partner)
		return res


	@api.multi
	def write(self,vals,context=None):
		values_of_res_partner = {}
		res = super(agent_override, self).write(vals)
		def is_changed(name):
			return name in vals and self[name] != vals[name]

		def get_field(name,default=''):
			return vals.get(name,self[name]) or default


		current_id = get_field('id')
		values_of_res_partner['name'] = get_field('name')
		values_of_res_partner['email'] = get_field('work_email')
		values_of_res_partner['phone'] = get_field('work_phone')
		values_of_res_partner['employee'] = True
		values_of_res_partner['employee_id'] = current_id
		
		if is_changed('is_agent') or is_changed('name') or is_changed('work_email') or is_changed('work_phone'):
			current_partner = self.env['res.partner'].search([('employee_id','=',current_id)])
			if get_field('is_agent') == True and len(current_partner) < 1:
				values_of_res_partner['agent'] = True
				res1 = self.env['res.partner'].create(values_of_res_partner)
			else:
				partner_obj = self.env['res.partner'].browse(current_partner)
				partner_obj.name = "haha"


		return res
    	
		








   











