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
from openerp.tools.translate import _

class formulir_1111_b2(osv.osv):
    _name = 'pajak.formulir_1111_b2'
    _description = 'Formulir 1111 B2'
    _inherit = ['mail.thread']
    
    def default_state(self, cr, uid, context={}):
        return 'draft'
        
    def default_name(self, cr, uid, context={}):
        return '/'
        
    def default_created_time(self, cr, uid, context={}):
        #TODO: Ticket #61
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    def default_created_user_id(self, cr, uid, context={}):
        return uid

    def function_amount_all(self, cr, uid, ids, name, args, context={}):
        #TODO: Ticket #70

        res = {}
        
        for formulir in self.browse(cr, uid, ids):
            total_dpp = 0.0
            total_ppn = 0.0
            total_ppnbm = 0.0
            if formulir.detail_ids:
                for detail in formulir.detail_ids:
                    total_dpp += detail.dpp
                    total_ppn += detail.ppn
                    total_ppnbm += detail.ppnbm
            res[id] =   {
                        'total_dpp' : total_dpp,
                        'total_ppn' : total_ppn,
                        'total_ppnbm' : total_ppnbm
                        }
        return res
    
    _columns =  {
                                'name' : fields.char(string='# SPT', size=30, required=True, readonly=True),
                                'company_id' : fields.many2one(string='Perusahaan', obj='res.company', required=True, readonly=True, states={'draft':[('readonly',False)]}), #TODO: Ticket #67
                                'nama_pkp' : fields.char(string='Nama PKP', size=255, required=True, readonly=True, states={'draft':[('readonly',False)]}), #TODO: Ticket #67
                                'npwp' : fields.char(string='NPWP', size=50, required=True, readonly=True, states={'draft':[('readonly',False)]}), #TODO: Ticket #67
                                'masa_pajak_id' : fields.many2one(string='Masa Pajak', obj='pajak.masa_pajak', required=True, readonly=True, states={'draft':[('readonly',False)]}), #TODO: Ticket #67
                                'pembetulan_ke' : fields.integer(string='Pembetulan Ke-', required=True, readonly=True, states={'draft':[('readonly',False)]}), #TODO: Ticket #67
                                'detail_ids' : fields.one2many(string='Detail', obj='pajak.detail_formulir_1111_b2', fields_id='formulir_id', readonly=True, states={'draft':[('readonly',False)]}), #TODO: Ticket #67
                                'total_dpp' : fields.function(string='Total DPP', fnct=function_amount_all, digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'),
                                'total_ppn' : fields.function(string='Total PPN', fnct=function_amount_all, digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'),
                                'total_ppnbm' : fields.function(string='Total PPnBM', fnct=function_amount_all, digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'),
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
                
    _defaults = {
                'name' : default_name,
                'state' : default_state,
                'created_time' : default_created_time,
                'created_user_id' : default_created_user_id,
                }

    def workflow_action_confirm(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.create_sequence(cr, uid, id):
                return False

            if not self.log_audit_tral(cr, uid, id, 'confirmed'):
                return False
        return True

    def workflow_action_approve(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.log_audit_trail(cr, uid, id, 'approved'):
                return False
        return True         
        
    def workflow_action_done(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.log_audit_trail(cr, uid, id, 'processed'):
                return False
        return True     
        
    def workflow_action_cancel(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.log_audit_trail(cr, uid, id, 'cancelled'):
                return False
        return True     
        
        
    def button_action_set_to_draft(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.delete_workflow_instance(cr, uid, id):
                return False

            if not self.create_workflow_instance(cr, uid, id):
                return False

            if not self.clear_log_audit(cr, uid, id):
                return False

            if not self.log_audit_audit(cr, uid, id, 'created'):
                return False
                
        return True

        
    def button_action_cancel(self, cr, uid, ids, context={}):
        wkf_service = netsvc.LocalService('workflow')
        for id in ids:
            if not self.delete_workflow_instance(cr, uid, id):
                return False

            if not self.create_workflow_instance(cr, uid, id):
                return False

            wkf_service.trg_validate(uid, 'pajak.formulir_1111_b2', id, 'button_cancel', cr)

        return True

    def write_cancel_description(self, cr, uid, id, reason):
        self.write(cr, uid, [id], {'cancelled_eason' : reason})
        return True

    def log_audit_trail(self, cr, uid, id, state):
        #TODO: Ticket #62
        if state not in ['created','confirmed','approved','processed','cancelled']:
            raise osv.except_osv(_('Peringatan!'),_('Error pada method log_audit'))
            return False
			
            state_dict = 	{
                            'created' : 'draft',
                            'confirmed' : 'confirm',
                            'approved' : 'approve',
                            'processed' : 'done',
                            'cancelled' : 'cancel'
                            }
                    
            val =	{
                    '%s_user_id' % (state) : uid ,
                    '%s_time' % (state) : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'state' : state_dict.get(state, False),
                    }
                                    
            self.write(cr, uid, [id], val)
        return True


    def delete_workflow_instance(self, cr, uid, id):
        #TODO: Ticket #63

        wkf_service = netsvc.LocalService('workflow')
        wkf_service.trg_delete(uid, 'pajak.formulir_1111_b2', id, cr)

        return True

    def create_workflow_instance(self, cr, uid, id):
        #TODO: Ticket #64

        wkf_service = netsvc.LocalService('workflow')
        wkf_service.trg_create(uid, 'pajak.formulir_1111_b2', id, cr)

        return True
            
    def onchange_company_id(self, cr, uid, ids, company_id):
        #TODO: Ticket #65
        obj_res_company = self.pool.get('res.company')

        value = {}
        domain = {}
        warning = {}
       
        if company_id:
            npwp = obj_res_company.browse(cr, uid, company_id).partner_id.npwp
            value.update({'npwp' : npwp})

        return {'value' : value, 'domain' : domain, 'warning' : warning}                    

    def create_sequence(cr, uid, id):
        #TODO: Ticket #66
        obj_sequence = self.pool.get('ir.sequence')
        obj_company = self.pool.get('res.company')
        
        formulir = self.browse(cr, uid, [id])[0]

        if formulir.name == '/':

            if formulir.company_id.sequence_formulir_1111_b2.id:
                sequence = obj_sequence.next_by_id(cr, uid, formulir.company_id.sequence_formulir_1111_b2.id)
                self.write(cr, uid, [id], {'name' : sequence})
            else:
                raise osv.except_osv(_('Peringatan'),_('Sequence Formulir 1111 B2 Belum Di-Set'))
                return False
        return True

formulir_1111_b2()

class detail_formulir_1111_b2(osv.osv):
    _name = 'pajak.detail_formulir_1111_b2'
    _description = 'Formulir 1111 B2'
    _columns =  {
                                'partner_id' : fields.many2one(string='Pembeli', obj='res.partner', required=True),
                                'npwp' : fields.char(string='NPWP/Nomor Paspor', size=50, required=True),
                                'dokumen_id' : fields.char(string='Kode dan Nomor Seri', size=255, required=True), #TODO:
                                'tanggal_dokumen' : fields.date(string='Tanggal Dokumen', required=True),
                                'dpp' : fields.float(string='DPP', digits_compute=dp.get_precision('Account')),
                                'ppn' : fields.float(string='PPN', digits_compute=dp.get_precision('Account')),
                                'ppnbm' : fields.float(string='PPnBM', digits_compute=dp.get_precision('Account')),
                                'dokumen_pengganti_id' : fields.char(string='Kode dan Nomor Seri Pengganti', size=255, required=True), #TODO:
                                'formulir_id' : fields.many2one(string='Formulir 1111 B2', obj='pajak.formulir_1111_b2'),
                                }
detail_formulir_1111_b2()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
