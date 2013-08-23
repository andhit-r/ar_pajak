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

class formulir_1111_ab(osv.osv):
    _name = 'pajak.formulir_1111_ab'
    _description = 'Formulir 1111 AB'
    _inherit = ['mail.thread']
    
    def default_state(self, cr, uid, context={}):
        return 'draft'
        
    def default_name(self, cr, uid, context={}):
        return '/'
        
    def default_created_time(self, cr, uid, context={}):
        #TODO: Ticket #79
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    def default_created_user_id(self, cr, uid, context={}):
        return uid

    def function_amount_all(self, cr, uid, ids, name, args, context=None):
        #TODO: Ticket #81
        res = {}
        itemA1 = 0.00
        item1B1_dpp = 0.00
        item1B1_ppn = 0.00
        item1B1_ppnbm = 0.00
        item2A_dpp = 0.00
        item2A_ppn = 0.00
        item2A_ppnbm = 0.00
        item2B_dpp = 0.00
        item2B_ppn = 0.00
        item2B_ppnbm = 0.00
        item2C_dpp = 0.00
        item2C_ppn = 0.00
        item2C_ppnbm = 0.00

        for formulir in self.browse(cr, uid, ids):
            res[formulir.id] =   {
                        'itemA1' : 0.0, # Diambil dari formulir 1111 A.1
                        'item1B1_dpp' : 0.0, # Diambil dari formulir 1111 A.2
                        'item1B1_ppn' : 0.0, # Diambil dari formulir 1111 A.2
                        'item1B1_ppnbm' : 0.0, # Diambil dari formulir 1111 A.2
                        'item2A_dpp' : 0.0, # Diambil dari formulir 1111 B.1
                        'item2A_ppn' : 0.0, # Diambil dari formulir 1111 B.1
                        'item2A_ppnbm' : 0.0, # Diambil dari formulir 1111 B.1
                        'item2B_dpp' : 0.0, #Diambil dari formulir 1111 B.2
                        'item2B_ppn' : 0.0, # Diambil dari formulir 1111 B.2
                        'item2B_ppnbm' : 0.0, # Diambil dari formulir 1111 B.2
                        'item2C_dpp' : 0.0, # Diambil dari formulir 1111 B.3
                        'item2C_ppn' : 0.0, # Diambil dari formulir 1111 B.3
                        'item2C_ppnbm' : 0.0, # Diambil dari formulir 1111 B.3
                        }
        return res


    
    _columns =  {
                        'name' : fields.char(string='# SPT', size=30, required=True, readonly=True),
                        'company_id' : fields.many2one(string='Perusahaan', obj='res.company', required=True),
                        'nama_pkp' : fields.char(string='Nama PKP', size=100, required=True),
                        'npwp' : fields.char(string='NPWP', size=50, required=True),
                        'masa_pajak_id' : fields.many2one(string='Masa Pajak', obj='pajak.masa_pajak', required=True),
                        'pembetulan_ke' : fields.integer(string='Pembetulan Ke', required=True),
                        'item1A' : fields.function(fnct=function_amount_all, type='float', string='A. Ekspor BKP Berwujud/BKP Tidak Berwujud/JKP', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'), #TODO: Ticket #80
                        'item1B1_dpp' : fields.function(fnct=function_amount_all, type='float', string='1. Penyerahan Dalam Negeri dengan Faktur Pajak yang tidak ditanggung', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'), #TODO: Ticket #80
                        'item1B1_ppn' : fields.function(fnct=function_amount_all, type='float', string='1. Penyerahan Dalam Negeri dengan Faktur Pajak yang tidak ditanggung', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'), #TODO: Ticket #80
                        'item1B1_ppnbm' : fields.function(fnct=function_amount_all, type='float', string='1. Penyerahan Dalam Negeri dengan Faktur Pajak yang tidak ditanggung', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'), #TODO: Ticket #80
                        'item1B2_dpp' : fields.float(string='2. Penyerahan Dalam Negeri dengan Faktur Pajak yang ditanggung', digits_compute=dp.get_precision('Account')),
                        'item1B2_ppn' : fields.float(string='2. Penyerahan Dalam Negeri dengan Faktur Pajak yang ditanggung', digits_compute=dp.get_precision('Account')),
                        'item1B2_ppnbm' : fields.float(string='2. Penyerahan Dalam Negeri dengan Faktur Pajak yang ditanggung', digits_compute=dp.get_precision('Account')),
                        'item1C1_dpp' : fields.float(string='1. Penyerahan yang PPN atau PPN dan PPnBM-nya harus dipunggut sendiri', digits_compute=dp.get_precision('Account')),
                        'item1C1_ppn' : fields.float(string='1. Penyerahan yang PPN atau PPN dan PPnBM-nya harus dipunggut sendiri', digits_compute=dp.get_precision('Account')),
                        'item1C1_ppnbm' : fields.float(string='1. Penyerahan yang PPN atau PPN dan PPnBM-nya harus dipunggut sendiri', digits_compute=dp.get_precision('Account')),                         
                        'item1C2_dpp' : fields.float(string='2.Penyerahan yang PPN atau PPN dan PPnBM-nya harus dipunggut oleh pemungut PPN', digits_compute=dp.get_precision('Account')),
                        'item1C2_ppn' : fields.float(string='2.Penyerahan yang PPN atau PPN dan PPnBM-nya harus dipunggut oleh pemungut PPN', digits_compute=dp.get_precision('Account')),
                        'item1C2_ppnbm' : fields.float(string='2.Penyerahan yang PPN atau PPN dan PPnBM-nya harus dipunggut oleh pemungut PPN', digits_compute=dp.get_precision('Account')),
                        'item1C3_dpp' : fields.float(string='3.Penyerahan yang PPN atau PPN dan PPnBM-nya tidak dipunggut', digits_compute=dp.get_precision('Account')),
                        'item1C3_ppn' : fields.float(string='3.Penyerahan yang PPN atau PPN dan PPnBM-nya tidak dipunggut', digits_compute=dp.get_precision('Account')),
                        'item1C3_ppnbm' : fields.float(string='3.Penyerahan yang PPN atau PPN dan PPnBM-nya tidak dipunggut', digits_compute=dp.get_precision('Account')),                         
                        'item1C4_dpp' : fields.float(string='4. Penyerahan yang dibebaskan dari pengenaan PPN atau PPN dan PPnBM', digits_compute=dp.get_precision('Account')),
                        'item1C4_ppn' : fields.float(string='4. Penyerahan yang dibebaskan dari pengenaan PPN atau PPN dan PPnBM', digits_compute=dp.get_precision('Account')),
                        'item1C4_ppnbm' : fields.float(string='4. Penyerahan yang dibebaskan dari pengenaan PPN atau PPN dan PPnBM', digits_compute=dp.get_precision('Account')),                         
                        'item2A_dpp' : fields.function(fnct=function_amount_all, type='float', string='Item II.A', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'), #TODO: Ticket #80
                        'item2A_ppn' : fields.function(fnct=function_amount_all, type='float', string='Item II.A', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'), #TODO: Ticket #80
                        'item2A_ppnbm' : fields.function(fnct=function_amount_all, type='float', string='Item II.A', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'), #TODO: Ticket #80
                        'item2B_dpp' : fields.function(fnct=function_amount_all, type='float', string='Item II.B', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'), #TODO: Ticket #80
                        'item2B_ppn' : fields.function(fnct=function_amount_all, type='float', string='Item II.B', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'), #TODO: Ticket #80
                        'item2B_ppnbm' : fields.function(fnct=function_amount_all, type='float', string='Item II.B', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'), #TODO: Ticket #80
                        'item2C_dpp' : fields.function(fnct=function_amount_all, type='float', string='Item II.C', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'), #TODO: Ticket #80
                        'item2C_ppn' : fields.function(fnct=function_amount_all, type='float', string='Item II.C', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'), #TODO: Ticket #80
                        'item2C_ppnbm' : fields.function(fnct=function_amount_all, type='float', string='Item II.C', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'), #TODO: Ticket #80
                        'item2D_dpp' : fields.float(string='Item II.D', digits_compute=dp.get_precision('Account')),
                        'item2D_ppn' : fields.float(string='Item II.D', digits_compute=dp.get_precision('Account')),
                        'item2D_ppnbm' : fields.float(string='Item II.D', digits_compute=dp.get_precision('Account')),
                        'item3A' : fields.float(string='Item III.A', digits_compute=dp.get_precision('Account')),
                        'item3B1' : fields.float(string='Item III.B.1', digits_compute=dp.get_precision('Account')),
                        'item3B2' : fields.float(string='Item III.B.2', digits_compute=dp.get_precision('Account')),
                        'item3B3' : fields.float(string='Item III.B.3', digits_compute=dp.get_precision('Account')),
                        'item3B4' : fields.float(string='Item III.B.4', digits_compute=dp.get_precision('Account')),
                        'item3C' : fields.float(string='Item III.C', digits_compute=dp.get_precision('Account')),                      
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
            if not self.log_audit_trail(cr, uid, id, 'confirmed'):
                return False
        return True

    def workflow_action_approve(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.log_audit_trail(cr, uid, id, 'approved'):
                return False
        return True         
        
    def workflow_action_done(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.log_audit_trail(cr, uid, id, 'procced'):
                return False
        return True     
        
    def workflow_action_cancel(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.log_audit_trail(cr, uid, id, 'cancelled'):
                return False
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

            wkf_service.trg_validate(uid, 'pajak.formulir_1111_ab', id, 'button_cancel', cr)

            return True

    def log_audit_trail(self, cr, uid, id, event):
        #TODO: Ticket #82
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

    def clear_log_audit(self, cr, uid, id):
        #TODO: Ticket #83

        val =	{
                'created_user_id' : False,
                'created_time' : False,		
                'confirmed_user_id' : False,
                'confirmed_time' : False,
                'approved_user_id' : False,
                'approved_time' : False,
                'processed_user_id' : False,
                'processed_time' : False,
                'cancelled_user_id' : False,
                'cancelled_time' : False,
                }
			
        self.write(cr, uid, [id], val)

        return True
        

    def delete_workflow_instance(self, cr, uid, id):
        #TODO: Ticket #84

        wkf_service = netsvc.LocalService('workflow')
        wkf_service.trg_delete(uid, 'pajak.formulir_1111_ab', id, cr)

        return True

    def create_workflow_instance(self, cr, uid, id):
        #TODO: Ticket #85

        wkf_service = netsvc.LocalService('workflow')
        wkf_service.trg_create(uid, 'pajak.formulir_1111_ab', id, cr)

        return True

    def onchange_company_id(self, cr, uid, ids, company_id):
        #TODO: Ticket #86
        obj_res_company = self.pool.get('res.company')

        value = {}
        domain = {}
        warning = {}
    
        if company_id:
            npwp = obj_res_company.browse(cr, uid, company_id).partner_id.npwp
            value.update({'npwp' : npwp})

        return {'value' : value, 'domain' : domain, 'warning' : warning}

    def create_sequence(self, cr, uid, id):
        #TODO: Ticket #87
        obj_sequence = self.pool.get('ir.sequence')
        obj_res_company = self.pool.get('res.company')

        formulir_1111_ab = self.browse(cr, uid, [id])[0]

        if formulir_1111_ab.name == '/':
            if formulir_1111_ab.company_id.sequence_formulir_1111_ab.id:
                sequence = obj_sequence.next_by_id(cr, uid, formulir_1111_ab.company_id.sequence_formulir_1111_ab.id)
                self.write(cr, uid, [id], {'name' : sequence})
            else:
                raise osv.except_osv(_('Perigatan'),_('Sequence Formulir 1111 AB Belum Di-Set'))
                return False
        return True

formulir_1111_ab()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
