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

class nota_pembatalan(osv.osv):
    _name = 'pajak.nota_pembatalan'
    _description = 'Nota Pembatalan'
    _inherit = ['mail.thread']
    
    def default_state(self, cr, uid, context={}):
        return 'draft'
        
    def default_name(self, cr, uid, context={}):
        return '/'
        
    def default_company_id(self, cr, uid, context={}):
        #TODO : Ticket #99
        obj_res_company = self.pool.get('res.company')

        company_id = obj_res_company._company_default_get(cr, uid, 'res.partner', context=context)
        return company_id
        
    def default_nota_pembatalan_date(self, cr, uid, context={}):
        #TODO: Ticket #100
        return datetime.now().strftime('%Y-%m-%d')
        
    def default_created_time(self, cr, uid, context={}):
        #TODO: Ticket #101
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    def default_created_user_id(self, cr, uid, context={}):
        return uid

    def function_total_dikembalikan(self, cr, uid, ids, name, args, context=None):
        #TODO: Tiket 102
        res = {}

        for nota_pembatalan in self.browse(cr, uid, ids):
            total_dikembalikan = 0.0
            if nota_pembatalan.nota_pembatalan_line_ids:
                for line in nota_pembatalan.nota_pembatalan_line_ids:
                    total_dikembalikan += line.subtotal
            res[nota_pembatalan.id] = { 'total_dikembalikan' : total_dikembalikan }
        return res
    
        
    
    _columns =  {
                'name' : fields.char(string='# Nota Pembatalan', size=30, required=True, readonly=True),
                'company_id' : fields.many2one(obj='res.company', string='Company', required=True),
                'company_npwp' : fields.char(string='Company NPWP', size=30, required=True),
                'partner_id' : fields.many2one(obj='res.partner', string='Partner', required=True),
                'partner_npwp' : fields.char(string='Partner NPWP', size=30, required=True),
                'signature_id' : fields.many2one(obj='res.users', string='Signature', readonly=False, required=True),
                'nota_pembatalan_line_ids' : fields.one2many(obj='pajak.nota_pembatalan_line', fields_id='nota_pembatalan_id', string='Nota Pembatalan Line'),
                'total_dikembalikan' : fields.function(string='Jumlah Harga Jual BKP Dikembalikan', fnct=function_total_dikembalikan, digits_compute=dp.get_precision('Account'), method=True, store=True),
                'ppn_diminta' : fields.float(string='PPN Yang Diminta Kembali', digits_compute=dp.get_precision('Account'), required=True),
                'ppnbm_diminta' : fields.float(string='PPnBM Yang Diminta Kembali', digits_compute=dp.get_precision('Account'), required=True),
                'nota_pembatalan_date' : fields.date(string='Date', required=True),
                'faktur_pajak_id' : fields.many2one(string='Faktur Pajak', obj='pajak.faktur_pajak', required=True),
                'note' : fields.text(string='Note'),
                'state' : fields.selection([('draft','Draft'),('confirm','Waiting For Approval'),('approve','Ready To Process'),('done','Done'),('cancel','Cancel')], 'Status', readonly=True),
                #LOG AUDIT
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
                'company_id' : default_company_id,
                'nota_pembatalan_date' : default_nota_pembatalan_date,
                'state' : default_state,
                'created_time' : default_created_time,
                'created_user_id' : default_created_user_id,
                }

    def workflow_action_confirm(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.create_sequence(cr, uid, id):
                return True

            if not self.log_audit_trail(cr, uid, id, 'confirmed'):
                return True
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
                return True
        return True     
        
    def onchange_company_id(self, cr, uid, ids, company_id):
        #TODO: Ticket #103
        obj_res_company = self.pool.get('res.company')

        value = {}
        domain = {}
        warning = {}
       
        if company_id:
            npwp = obj_res_company.browse(cr, uid, company_id).partner_id.npwp
            signature_id = obj_res_company.browse(cr, uid, company_id).nota_pembatalan_signature_id.id
            value.update({'company_npwp' : npwp, 'signature_id' : signature_id})

        return {'value' : value, 'domain' : domain, 'warning' : warning}

    def onchange_partner_id(self, cr, uid, ids, partner_id):
        #TODO: Ticket #104
        obj_res_partner = self.pool.get('res.partner')

        value = {}
        domain = {}
        warning = {}

        if partner_id:
            npwp = obj_res_partner.browse(cr, uid, partner_id).npwp
            value.update({'partner_npwp' : npwp})
        
        return {'value' : value, 'domain' : domain, 'warning' : warning}
        
    def write_cancel_description(self, cr, uid, id, reason):
        self.write(cr, uid, [id], {'cancelled_reason' : reason})
        return True

    def create_sequence(self, cr, uid, id):
        #TODO: Ticket #105
        obj_sequence = self.pool.get('ir.sequence')
        obj_company = self.pool.get('res.company')
        
        nota_pembatalan = self.browse(cr, uid, [id])[0]

        if nota_pembatalan.name == '/':

            if nota_pembatalan.company_id.sequence_nota_pembatalan.id:
                sequence = obj_sequence.next_by_id(cr, uid, nota_pembatalan.company_id.sequence_nota_pembatalan.id)
                self.write(cr, uid, [id], {'name' : sequence})
            else:
                raise osv.except_osv(_('Peringatan'),_('Sequence Nota Pembatalan Belum Di-Set'))
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

            wkf_service.trg_validate(uid, 'pajak.nota_pembatalan', id, 'button_cancel', cr)

        return True

    def log_audit_trail(self, cr, uid, id, event):
        #TODO: Ticket #106
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
        #TODO: Ticket #107

        wkf_service = netsvc.LocalService('workflow')
        wkf_service.trg_delete(uid, 'pajak.nota_pembatalan', id, cr)

        return True

    def create_workflow_instance(self, cr, uid, id):
        #TODO: Ticket #108

        wkf_service = netsvc.LocalService('workflow')
        wkf_service.trg_create(uid, 'pajak.nota_pembatalan', id, cr)

        return True
    
    def clear_log_audit(self, cr, uid, id):
        #TODO: Ticket #109
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

nota_pembatalan()

class nota_pembatalan_line(osv.osv):
    _name = 'pajak.nota_pembatalan_line'
    _description = 'Nota Pembatalan Line'
   
    def function_subtotal(self, cr, uid, ids, name, args, context=None):
        #TODO: Ticket #
        res = {}
        for id in ids:
            res[id] = 0.0
        return res
    


    _columns =  {
                'name' : fields.char('Description', size=100, required=True),
                'product_id' : fields.many2one(obj='product.product', string='Product'),
                'quantity' : fields.float(string='Quantity', digits=(16,2)),
                'unit_price' : fields.float(string='Unit Price', digits_compute=dp.get_precision('Account'), required=True),
                'nota_pembatalan_id' : fields.many2one(obj='pajak.nota_pembatalan', string='# Nota Pembatalan', ondelete='cascade'),
                'subtotal':fields.function(string='Subtotal', fnct=function_subtotal, digits_compute=dp.get_precision('Account'), method=True, store=True),
                }   

    def onchange_product_id(self, cr, uid, ids, product_id):
        #TODO: Ticket #116
        value = {}
        domain = {}
        warning = {}

        obj_product = self.pool.get('product.product')

        kriteria = [('id', '=', product_id)]
        product_ids = obj_product.search(cr, uid, kriteria)

        if product_ids:
            product = obj_product.browse(cr, uid, product_ids)[0]
            value.update({'unit_price' : product.list_price, 'name' : product.name})
            
        return {'value' : value, 'domain' : domain, 'warning' : warning}

nota_pembatalan_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
