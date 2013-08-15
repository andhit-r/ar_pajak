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




class formulir_1111_a2(osv.osv):
	_name = 'pajak.formulir_1111_a2'
	_description = 'Formulir 1111 A2'
	_inherit = ['mail.thread']
	
	def default_state(self, cr, uid, context={}):
		return 'draft'
		
	def default_name(self, cr, uid, context={}):
		return '/'
		
	def default_created_time(self, cr, uid, context={}):
		#TODO: Ticket #47
		return False
		

	def default_created_user_id(self, cr, uid, context={}):
        return uid
    
		
	    

	_columns = 	{
								'name' : fields.char(string='# Dokumen', size=30, required=True, readonly=True),
								'company_id' : fields.many2one(string='Perusahaan', obj='res.company', required=True),
								'nama_pkp' : fields.char(string='Nama PKP', size=255, required=True),
								'npwp' : fields.char(string='NPWP', size=50, required=True),
								'masa_pajak_id' : fields.many2one(string='Masa Pajak', obj='pajak.masa_pajak', required=True),
								'pembetulan_ke' : fields.integer(string='Pembetulan Ke-', required=True),
								'detail_ids' : fields.one2many(string='Detail', obj='pajak.detail_formulir_1111_a2', fields_id='formulir_id'),
                                'total_dpp' : fields.function(fnct=function_amount_all, string='Total DPP', type='float', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'),
                                'total_ppn' : fields.function(fnct=function_amount_all, string='Total PPN', type='float', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'),
                                'total_ppnbm' : fields.function(fnct=function_amount_all, string='Total PPnBM', type='float', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'),
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
		


		
	def button_action_set_to_draft(self, cr, uid, ids, context={}):
		for id in ids:
			if not self.delete_workflow_instance(self, cr, uid, id):
				return False

			if not self.create_workflow_instance(self, cr, uid, id):
				return False
				
		return True

		
        def button_action_cancel(self, cr, uid, ids, context={}):
                wkf_service = netsvc.LocalService('workflow')
                for id in ids:
                                if not self.delete_workflow_instance(self, cr, uid, id):
                                        return False

                                if not self.create_workflow_instance(self, cr, uid, id):
                                        return False

                                wkf_service.trg_validate(uid, 'pajak.formulir_1111_a2', id, 'button_cancel', cr)

                return True

        def log_audit_trail(self, cr, uid, id, event):
                #TODO: Ticket #12
                return True

        def delete_workflow_instance(self, cr, uid, id):
                #TODO: Ticket #13
                return True

        def create_workflow_instance(self, cr, uid, id):
                #TODO: Ticket #14
                return True
                
        def onchange_company_id(self, cr, uid, ids, comapny_id):
            value = {}
            domain = {}
            warning = {}
            
            return {'value' : value, 'domain' : domain, 'warning' : warning}                

		
		

formulir_1111_a2()

class detail_formulir_1111_a2(osv.osv):
    _name = 'pajak.detail_formulir_1111_a2'
    _description = 'Formulir 1111 A2'
    _columns =  {
                                'partner_id' : fields.many2one(string='Pembeli', obj='res.partner', required=True),
                                'npwp' : fields.char(string='NPWP/Nomor Paspor', size=50, required=True),
                                'dokumen_id' : fields.char(string='Kode dan Nomor Seri', size=255, required=True), #TODO:
                                'tanggal_dokumen' : fields.date(string='Tanggal Dokumen', required=True),
                                'dpp' : fields.float(string='DPP', digits_compute=dp.get_precision('Account')),
                                'ppn' : fields.float(string='PPN', digits_compute=dp.get_precision('Account')),
                                'ppnbm' : fields.float(string='PPnBM', digits_compute=dp.get_precision('Account')),
                                'dokumen_pengganti_id' : fields.char(string='Kode dan Nomor Seri Pengganti', size=255, required=True), #TODO:
                                'formulir_id' : fields.many2one(string='Formulir 1111 A2', obj='pajak.formulir_1111_a2'),
                                }
detail_formulir_1111_a2()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:autoindent
