# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import Warning

class employee_agent(models.Model):
    _inherit = 'res.partner'

    employee = fields.Boolean(string="Employee")
    employee_id = fields.Many2one('hr.employee',string='Emp ID',ondelete='cascade')

    @api.multi
    def unlink(self):
    	# raise Warning(self)
    	# for emp in self:
    	# 	if emp.id
    	 # current_emp_id = int(self.employee_id.id)
    	 # res = super(employee_agent, self).unlink()
    	 # list_emp = self.env['hr.employee'].search([('id','in',[current_emp_id])])
    	 # if len(list_emp) > 0:
    	for line in self.ids:
    		list_emp = self.env['hr.employee'].search([('agent_id','=',line)], order='id desc', limit=1)
    		list_emp.unlink()
    	return super(employee_agent,self).unlink()

    @api.multi
    def write(self,vals):
    	res = super(employee_agent,self).write(vals)
    	emp_id = {}
    	values_of_emp = {}
    	is_rewrite = True if vals.get('is_rewrite') else False
    	recs = self.read(['employee', 'phone', 'email', 'name', 'employee_id'])
    	is_done = True if vals.get('is_done_creating', False) is True else False
    	employee_obj = self.env['hr.employee']
    	fields = self.fields_get()
    	# Values(VALS) in write will only be received when the field value is changed after saving(SAVE BUTTON)
    	# For every record in recs(calling READ function in SELF to get current field value/s or fields value/s after saving).
    	for record in recs:
    		# vals.get() function to know if field value 'employee' has been changed. 
    		if vals.get('employee', False):
    			# record('employee') to know if field value that has been changed is True. else False
    			if record['employee'] is True:
    				# record('employee_id') to know if record has already an Employee_id stored
    				if record['employee_id'] is False:
    					values_of_emp['name'] = record['name']
    					values_of_emp['work_email'] = record['email']
    					values_of_emp['work_phone'] = record['phone']
    					values_of_emp['is_agent'] = True
    					values_of_emp['is_done_creating'] = True
    					if is_done is False:
    						list_agent = self.search([('employee_id','=',False)], order='id desc', limit=1)
    						values_of_emp['agent_id'] = list_agent[0].id
    						res1 = employee_obj.create(values_of_emp)
    						list_emp = employee_obj.search([('agent_id','=',list_agent[0].id)], order='id desc', limit=1)
    						emp_id['employee_id'] = list_emp[0].id
    						res2 = self.search([('employee_id','=',self.employee_id.id)], order='id desc', limit=1).write(emp_id)
    				else:
    					if is_rewrite is False:
    						values_of_emp['is_rewrite'] = True
    						if vals.get('name'):
    							values_of_emp['name'] = record['name']
    						if vals.get('email'):
    							values_of_emp['work_email'] = record['email']
    						if vals.get('phone'):
    							values_of_emp['work_phone'] = record['phone']
    						res3 = employee_obj.search(['&',('id','=',self.employee_id.id),('agent_id','=',self.id)]).write(values_of_emp)
    				
    				# list_emp = employee_obj.search([('id','=',self.employee_id.id)], order='id desc', limit=1)
    				
    		elif vals.get('employee') is False:
    			list_emp = employee_obj.search([('agent_id','=',self.id)], order='id desc', limit=1)
    			emp_id['employee_id'] = False
    			# raise Warning(emp_id)
    			res2 = self.search([('employee_id','=',list_emp[0].id)], order='id desc', limit=1).write(emp_id)
    			res3 = employee_obj.search([('agent_id','=',self.id)], order='id desc', limit=1).unlink()
    		else:
    			if is_rewrite is False:
    				values_of_emp['is_rewrite'] = True
    				if vals.get('name'):
    					values_of_emp['name'] = record['name']
    				if vals.get('email'):
    					values_of_emp['work_email'] = record['email']
    				if vals.get('phone'):
    					values_of_emp['work_phone'] = record['phone']
    				res3 = employee_obj.search(['&',('id','=',self.employee_id.id),('agent_id','=',self.id)]).write(values_of_emp)
    	return res

    @api.model
    def create(self,vals):
		res = super(employee_agent,self).create(vals)
		emp = True if vals.get('employee') else False 
		emp_id = {}
		employee_obj = self.env['hr.employee']
		is_done = True if vals.get('is_done_creating', False) is True else False
		values_of_emp = {}
		if emp:
			if 'email' in vals:
				values_of_emp['work_email'] = vals['email']
			if 'phone' in vals:
				values_of_emp['work_phone'] = vals['phone']
			if 'agent' in vals:
				values_of_emp['is_agent'] = True
			values_of_emp['name'] = vals['name']
			values_of_emp['is_done_creating'] = True
			if vals['employee'] is True and is_done is False:
				list_agent = self.search([('employee_id','=',False)], order='id desc', limit=1)
				values_of_emp['agent_id'] = list_agent[0].id
				res1 = employee_obj.create(values_of_emp)
				list_emp = employee_obj.search([('agent_id','=',list_agent[0].id)], order='id desc', limit=1)
				emp_id['employee_id'] = list_emp[0].id
				res2 = self.search([('employee_id','=',self.employee_id.id)], order='id desc', limit=1).write(emp_id)
		return res

class agent_override(models.Model):
	_inherit = 'hr.employee'

	is_agent = fields.Boolean(string="Agent")
	agent_id = fields.Many2one('res_partner',string='Agent ID',ondelete='cascade')

	@api.multi
	def unlink(self):

		return super(agent_override, self).unlink()

	@api.model
	def create(self,vals):
		res = super(agent_override,self).create(vals)
		agent = True if vals.get('is_agent') else False 
		is_done = True if 'is_done_creating' in vals else False
		ag_id = {}
		values_of_res_partner = {} 
		if agent:
			if 'work_email' in vals:
				values_of_res_partner['email'] = vals['work_email']
			if 'work_phone' in vals:
				values_of_res_partner['phone'] = vals['work_phone']
			values_of_res_partner['name'] = vals['name']
			values_of_res_partner['employee'] = True
			values_of_res_partner['agent'] = True
			values_of_res_partner['is_done_creating'] = True
			if vals['is_agent'] == True and is_done == False:
				list_emp = self.search([('agent_id','=',False)], order='id desc', limit=1)
				values_of_res_partner['employee_id'] = list_emp[0].id
				res1 = self.env['res.partner'].create(values_of_res_partner)
				list_agent = self.env['res.partner'].search([('employee_id','=',list_emp[0].id)], order='id desc', limit=1)
				ag_id['agent_id'] = list_agent[0].id
				res2 = self.search([('agent_id','=',self.agent_id.id)], order='id desc', limit=1).write(ag_id)
		return res


	@api.multi
	def write(self,vals):
		values_for_emp = {}
		values_of_res_partner = {}
		res = super(agent_override, self).write(vals)
		ag_id = {}
		is_rewrite = True if vals.get('is_rewrite') else False
		is_done = True if vals.get('is_done_creating', False) is True else False
		res_partner_obj = self.env['res.partner']
		recs = self.read(['is_agent', 'work_phone', 'work_email', 'name', 'agent_id'])
		for record in recs:
			if vals.get('is_agent', False):
				if record['is_agent'] is True:
					if record['agent_id'] is False:
						values_of_res_partner['name'] = record['name']
						values_of_res_partner['email'] = record['work_email']
						values_of_res_partner['phone'] = record['work_phone']
						values_of_res_partner['employee'] = True
						values_of_res_partner['agent'] = True
						values_of_res_partner['is_done_creating'] = True
						if is_done is False:
							list_emp = self.env['hr.employee'].search([('agent_id','=',False)], order='id desc', limit=1)
							values_of_res_partner['employee_id'] = list_emp[0].id
							res1 = res_partner_obj.create(values_of_res_partner)
							list_agent = self.env['res.partner'].search([('employee_id','=',list_emp[0].id)], order='id desc', limit=1)
							ag_id['agent_id'] = list_agent[0].id
							res2 = self.search([('agent_id','=',self.agent_id.id)], order='id desc', limit=1).write(ag_id)
					else:
						if is_rewrite is False:
							values_of_res_partner['is_rewrite'] = True
							if vals.get('name'):
								values_of_res_partner['name'] = record['name']
							if vals.get('email'):
								values_of_res_partner['email'] = record['work_email']
							if vals.get('phone'):
								values_of_res_partner['phone'] = record['work_phone']
							res3 = res_partner_obj.search(['&',('employee_id','=',self.id),('id','=',self.agent_id.id)]).write(values_of_res_partner)
			elif vals.get('is_agent') is False:
				list_agent = self.env['res.partner'].search([('employee_id','=',self.id)], order='id desc', limit=1)
				ag_id['agent_id'] = False
				res4 = self.search([('agent_id','=',list_agent[0].id)], order='id desc', limit=1).write(ag_id)
				res5 = self.env['res.partner'].search([('employee_id','=',self.id)], order='id desc', limit=1).unlink()
				# 	# Unlink
				# if record['is_agent'] is False:
					
				# else:
			else:
				if is_rewrite is False:
					values_of_res_partner['is_rewrite'] = True
					if vals.get('name'):
						values_of_res_partner['name'] = record['name']
					if vals.get('email'):
						values_of_res_partner['email'] = record['work_email']
					if vals.get('phone'):
						values_of_res_partner['phone'] = record['work_phone']
					res3 = res_partner_obj.search(['&',('employee_id','=',self.id),('id','=',self.agent_id.id)]).write(values_of_res_partner)
		return res
    	
		








   











