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


from osv import fields, osv
from datetime import date, datetime
import netsvc


class surat_setor_pajak(osv.osv):
    _name = 'pajak.surat_setor_pajak'
    _description = 'Surat Setor Pajak'
    _inherit = ['mail.thread']
    
    def default_name(self, cr, uid, context={}):
            return '/'
    
    def default_company_id(self, cr, uid, context={}):
            obj_user = self.pool.get('res.users')
    
            user = obj_user.browse(cr, uid, [uid])[0]
    
            return user.company_id and user.company_id.id or False
    
    def default_date_ssp(self, cr, uid, context={}):
            #TODO Ticket #22
            return datetime.now().strftime('%Y-%m-%d')
    
    def default_signature_ssp_id(self, cr, uid, context={}):
            #TODO  Ticket #23
            return uid
    
    def default_state(self, cr, uid, context={}):
            return 'draft'

    def function_amount_to_text(self, cr, uid, ids, name, args, context=None):
            #TODO Ticket #24
            res = {}
            amount_to_text = []
            obj_surat_setor_pajak = self.pool.get('pajak.surat_setor_pajak')
            obj_res_currency = self.pool.get('res.currency')

            for surat_setor_pajak in obj_surat_setor_pajak.browse(cr, uid, ids):
                try:
                    amount_to_text = obj_res_currency.terbilang(cr, uid, surat_setor_pajak.company_id.currency_id.id ,surat_setor_pajak.amount_spp)
                except:
                    amount_to_text = '-'
                res[surat_setor_pajak.id] = amount_to_text
            return res

    _columns = {
                            'name' : fields.char(string='# SSP', size=50, required=True, readonly=True),
                            'company_id' : fields.many2one(string='Company', obj='res.company', required=True),
                            'npwp' : fields.char(string='NPWP', size=50, required=True),
                            'partner_id' : fields.many2one(string='Nama NPWP', obj='res.partner', required=True),
                            #'npwp_address_id' : fields.many2one(string='Alamat NPWP', obj='res.partner.address', required=True),
                            'nop' : fields.char(string='NOP', size=100),
                            'nop_address' : fields.char(string='Alamat OP', size=255),
                            'akun_pajak_id' : fields.many2one(string='Kode Akun Pajak', obj='pajak.akun_pajak', required=True),
                            'jenis_setor_pajak_id' : fields.many2one(string='Kode Jenis Setoran', obj='pajak.jenis_setor_pajak', required=True),
                            'description' : fields.char(string='Uraian Pembayaran', size=255, required=True),
                            'masa_pajak_id' : fields.many2one(string='Masa Pajak', obj='pajak.masa_pajak', required=True),
                            'tahun_pajak_id' : fields.related('masa_pajak_id', 'tahun_pajak_id', type='many2one', relation='pajak.tahun_pajak', readonly=True, store=True, string='Tahun Pajak'),
                            'nomor_ketetapan' : fields.char(string='Nomor Ketetapan', size=50),
                            'amount_ssp' : fields.float(string='Jumlah Pembayaran', digits=(16,2), required=True),
                            'amount_to_text' : fields.function(fnct=function_amount_to_text, string='Terbilang', type='text', method=True, store=True),
                            'city_ssp' : fields.char(string='Kota Setor', size=100, required=True),
                            'date_ssp' : fields.date(string='Tanggal Setor', required=True),
                            'signature_ssp_id' : fields.many2one(string='SSP Signature', obj='res.users', required=True),
                            'state' : fields.selection(string='State', selection=[('draft','Draft'),('confirm','Waiting For Approval'),('approve','Ready To Process'),('done','Done'),('cancel','Cancel')], readonly=True),
                            #Audit Trail
                            'created_user_id' : fields.many2one(string='Created By', obj='res.users', readonly=True),
                            'created_time' : fields.datetime(string='Created Time', readonly=True),
                            'confirmed_user_id' : fields.many2one(string='Confirmed By', obj='res.users', readonly=True),
                            'confirmed_time' : fields.datetime(string='Confirmed Time', readonly=True),               
                            'approved_user_id' : fields.many2one(string='Approved By', obj='res.users', readonly=True),
                            'approved_time' : fields.datetime(string='Approved Time', readonly=True),                                        
                            'processed_user_id' : fields.many2one(string='Processed By', obj='res.users', readonly=True),
                            'processed_time' : fields.datetime(string='Done Time', readonly=True),                           
                            'cancelled_user_id' : fields.many2one(string='Cancelled By', obj='res.users', readonly=True),
                            'cancelled_time' : fields.datetime(string='Cancelled Time', readonly=True),
                            }
                            
    _defaults = {
                            'name' : default_name,
                            'company_id' : default_company_id,
                            'date_ssp' : default_date_ssp,
                            'signature_ssp_id' : default_signature_ssp_id,
                            'state' : default_state,
                            }
                            
    _order = 'name desc'
    
    def workflow_action_confirm(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.create_sequence(cr, uid, id):
                return False

            if not self.log_audit_trail(cr, uid, id, 'confirmed'):
                return False

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
            if not self.reset_audit_trail(cr, uid, id):
                return False
                    
            self.write(cr, uid, [id], {'state' : 'cancel'})
        return True     
        
    def button_action_cancel(self, cr, uid, ids, context={}):
        """
        Method that runs by Cancel button
        """
        
        for id in ids:
            if not self.delete_workflow_instance(cr, uid, id):
                return False
                    
            if not self.create_workflow_instance(cr, uid, id):
                return False    
                        
            wkf_service.trg_validate(uid, 'pajak.surat_setor_pajak', id, 'button_cancel', cr)
                        
        return True
        
    def button_action_set_to_draft(self, cr, uid, ids, context={}):
        """
        Method that runs by Set To Draft button
        """
        for id in ids:
            if not self.delete_workflow_instance(cr, uid, id):
                return False
                        
            if not self.create_workflow_instance(cr, uid, id):
                return False                
                        
            if not self.reset_audit_trail(cr, uid, id):
                return False

            if not self.log_audit_trail(cr, uid, id, 'created'):
                return False
                        
        return True     
        
    def write_cancel_description(self, cr, uid, id, reason):
        self.write(cr, uid, [id], {'cancelled_reason' : reason})
        return True

    def reset_audit_trail(self, cr, uid, id):
        #TODO Ticket #25

        val =   {
                    'created_user_id' : False,
                    'created_time' : False,     
                    'confirmed_user_id' : False,
                    'confirmed_time' : False,
                    'approved_user_id' : False,
                    'approved_time' : False,
                    'done_user_id' : False,
                    'done_time' : False,
                    }
                    
        self.write(cr, uid, [id], val)
        
        return True
            
    def delete_workflow_instance(self, cr, uid, id):
        #TODO Ticket #27

        wkf_service = netsvc.LocalService('workflow')
        wkf_service.trg_delete(uid, 'pajak.surat_setor_pajak', id, cr)

        return True
            
    def create_workflow_instance(self, cr, uid, id):
        #TODO Ticket #26

        wkf_service = netsvc.LocalService('workflow')
        wkf_service.trg_create(uid, 'pajak.surat_setor_pajak', id, cr)

        return True

    def create_sequence(self, cr, uid, id):
        #TODO: Ticket #122
        return True

    def log_audit_trail(self, cr, uid, id, state):
        #TODO: Ticket #123
        return True

    def clear_log_audit(self, cr, uid, id):
        #TODO: Ticket #124
        return True

    def write_cancel_description(self, cr, uid, id, reason):
        #TODO: Ticket #125
        return True


    
    def onchange_company_id(self, cr, uid, ids, company_id):
        #TODO 28
        obj_res_company = self.pool.get('res.company')

        value = {}
        domain = {}
        warning = {}
       
        if company_id:
            npwp = obj_res_company.browse(cr, uid, company_id).partner_id.npwp
            value.update({'npwp' : npwp})

        return {'value' : value, 'domain' : domain, 'warning' : warning}

surat_setor_pajak()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
    




