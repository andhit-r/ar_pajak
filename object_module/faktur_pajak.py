# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp.osv import fields, osv, orm
import openerp.addons.decimal_precision as dp
from openerp import netsvc
from openerp import pooler
from datetime import datetime

class faktur_pajak(osv.osv):
	_name = 'pajak.faktur_pajak'
	_description = 'Faktur Pajak'
	_inherit = ['mail.thread']
	
	def default_state(self, cr, uid, context={}):
		return 'draft'
		
	def default_name(self, cr, uid, context={}):
		return '/'
		
	def default_company_id(self, cr, uid, context={}):
		#TODO : Ticket #88
		return False
		
	def default_faktur_pajak_date(self, cr, uid, context={}):
		#TODO: Ticket #88
		return False
		
	def default_created_time(self, cr, uid, context={}):
		#TODO: Ticket #88
		return False
		
	def default_created_user_id(self, cr, uid, context={}):
		#TODO: Ticket #88
		return False
	
			
	
	_columns = 	{
								'name' : fields.char(string='# Faktur Pajak', size=30, required=True, readonly=True),
								'company_id' : fields.many2one(obj='res.company', string='Company', required=True),
								'company_npwp' : fields.char(string='Company NPWP', size=30, required=True),
								'partner_id' : fields.many2one(obj='res.partner', string='Partner', required=True),
								'partner_npwp' : fields.char(string='Partner NPWP', size=30, required=True),
								'signature_id' : fields.many2one(obj='res.users', string='Signature', readonly=True),
								'discount' : fields.float(string='Discount', digits_compute=dp.get_precision('Account'), required=True),
								'advance_payment' : fields.float(string='Amount Advance Payment', digits_compute=dp.get_precision('Account'), required=True),
								'untaxed' : fields.float(string='Untaxed', digits_compute=dp.get_precision('Account'), required=True),
								'base' : fields.float(string='Base', digits_compute=dp.get_precision('Account'), required=True),
								'amount_tax' : fields.float(string='Amount Tax', digits_compute=dp.get_precision('Account'), required=True),
								'faktur_pajak_line_ids' : fields.one2many(obj='pajak.faktur_pajak_line', fields_id='faktur_pajak_id', string='Faktur Pajak Line'),
								'faktur_pajak_line_ppnbm_ids' : fields.one2many(obj='pajak.faktur_pajak_ppnbm_line', fields_id='faktur_pajak_id', string='Faktur Pajak PPN Bm Line'),
								'faktur_pajak_date' : fields.date(string='Date', required=True),
								'note' : fields.text(string='Note'),
								'state' : fields.selection([('draft','Draft'),('confirm','Waiting For Approval'),('approve','Ready To Process'),('done','Done'),('cancel','Cancel')], 'Status', readonly=True),
								'created_time' : fields.datetime(string='Created Time', readonly=True),
								'created_user_id' : fields.many2one(string='Created By', obj='res.users', readonly=True),
								'confirmed_time' : fields.datetime(string='Confirmed Time', readonly=True),
								'confirmed_user_id' : fields.many2one(string='Confirmed By', obj='res.users', readonly=True),						
								'approved_time' : fields.datetime(string='Approved Time', readonly=True),
								'approved_user_id' : fields.many2one(string='Approved By', obj='res.users', readonly=True),		
								'processed_time' : fields.datetime(string='Processed Time', readonly=True),
								'processed_user_id' : fields.many2one(string='Process By', obj='res.users', readonly=True),				
								'cancelled_time' : fields.datetime(string='Processed Time', readonly=True),
								'cancelled_user_id' : fields.many2one(string='Process By', obj='res.users', readonly=True),																								
								'cancelled_reason' : fields.text(string='Cancelled Reason', readonly=True),
								}	
				
	_defaults =	{
							'name' : default_name,
							'company_id' : default_company_id,
							'faktur_pajak_date' : default_faktur_pajak_date,
							'state' : default_state,
							'created_time' : default_created_time,
							'created_user_id' : default_created_user_id,
							}

	def workflow_action_confirm(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'confirm'})
		return True

	def workflow_action_approve(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'approve'})
		return True			
		
	def workflow_action_done(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'done'})
		return True		
		
	def workflow_action_cancel(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'cancel'})
		return True		
		
	def onchange_company_id(self, cr, uid, ids, company_id):
		#TODO: Ticket #88
		value = {}
		domain = {}
		warning = {}
		
		return {'value' : value, 'domain' : domain, 'warning' : warning}
		
	def create_sequence(self, cr, uid, id):
		#TODO: Ticket #88
		return True
		
	def select_sequence(self, cr, uid, id, faktur_pajak_sequence):
		"""
		Parameter :
		faktur_pajak_sequence : char
		"""
		#TODO: Ticket #88
		return True
		
	def onchange_partner_id(self, cr, uid, ids, partner_id):
		#TODO: Ticket #88
		value = {}
		domain = {}
		warning = {}
		
		return {'value' : value, 'domain' : domain, 'warning' : warning}		
		
	def button_action_set_to_draft(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.set_to_draft(self, cr, uid, id):
				return False
				
		return True
		
	def set_to_draft(self, cr, uid, id):
		#TODO: Ticket #88
		return True
		
		

faktur_pajak()

class faktur_pajak_line(osv.osv):
	_name = 'pajak.faktur_pajak_line'
	_description = 'Faktur Pajak Line'
	
	_columns = 	{
				'name' : fields.char('Description', size=100, required=True),
				'product_id' : fields.many2one(obj='product.product', string='Product'),
				'faktur_pajak_id' : fields.many2one(obj='pajak.faktur_pajak', string='# Faktur Pajak'),
				'subtotal':fields.float(string='Subtotal', digits_compute=dp.get_precision('Account')),
				}	

faktur_pajak_line()

class faktur_pajak_ppnbm_line(osv.osv):
	_name = 'pajak.faktur_pajak_ppnbm_line'
	_description = 'Faktur Pajak PPNBm Line'
	
	_columns = 	{
								'ppnbm_rate' : fields.float(string='Rate', digits=(16,9), required=True),
								'base' : fields.float(string='Base', digits_compute=dp.get_precision('Account'), required=True),
								'ppnbm_amount' : fields.float(string='PPN Bm', digits_compute=dp.get_precision('Account'), required=True),
								'faktur_pajak_id' : fields.many2one(obj='pajak.faktur_pajak', string='# Faktur Pajak'),
				}	

faktur_pajak_ppnbm_line()

class account_faktur_pajak_sequence(osv.osv):
	_name = 'pajak.faktur_pajak_sequence'
	_description = 'Faktur Pajak Sequence'
	
	_columns = 	{
				'name' : fields.char('Name', size=30, readonly=True),
				'faktur_pajak_id' : fields.many2one(obj='pajak.faktur_pajak', string='# Faktur Pajak', readonly=True),
				}	
			

account_faktur_pajak_sequence()
