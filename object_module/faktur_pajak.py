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
        obj_res_company = self.pool.get('res.company')

        company_id = obj_res_company._company_default_get(cr, uid, 'res.partner', context=context)
        return company_id
        
    def default_faktur_pajak_date(self, cr, uid, context={}):
        return datetime.now().strftime('%Y-%m-%d')
        
    def default_created_time(self, cr, uid, context={}):
        return datetime.now().strftime('%Y-%m-%d')
        
    def default_created_user_id(self, cr, uid, context={}):
        return uid

    def function_amount_all(self, cr, uid, ids, name, args, context=None):
        #TODO: Tiket 11
        res = {}
        for faktur in self.browse(cr, uid, ids):
            res[faktur.id] = {
                                        'untaxed' : 0.0,
                                        'base' : 0.0,
                                        'amount_tax' : 0.0,
                                        }
        return res
    
            
    
    _columns =  {
                                'name' : fields.char(string='# Faktur Pajak', size=30, required=True, readonly=True),
                                'company_id' : fields.many2one(obj='res.company', string='Company', required=True),
                                'company_npwp' : fields.char(string='Company NPWP', size=30, required=True),
                                'partner_id' : fields.many2one(obj='res.partner', string='Partner', required=True),
                                'partner_npwp' : fields.char(string='Partner NPWP', size=30, required=True),
                                'signature_id' : fields.many2one(obj='res.users', string='Signature', readonly=True),
                                'discount' : fields.float(string='Discount', digits_compute=dp.get_precision('Account'), required=True),
                                'advance_payment' : fields.float(string='Amount Advance Payment', digits_compute=dp.get_precision('Account'), required=True),
                                'untaxed' : fields.function(fnct=function_amount_all, type='float', string='Untaxed', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'),
                                'base' : fields.function(fnct=function_amount_all, type='float', string='Base', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'),
                                'amount_tax' : fields.function(fnct=function_amount_all, string='Amount Tax', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'),
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
                
    _defaults = {
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
        obj_res_company = self.pool.get('res.company')

        value = {}
        domain = {}
        warning = {}
       
        if company_id:
            npwp = obj_res_company.browse(cr, uid, company_id).partner_id.npwp
            value.update({'company_npwp' : npwp})

        return {'value' : value, 'domain' : domain, 'warning' : warning}

    def onchange_partner_id(self, cr, uid, ids, partner_id):
        #TODO: Ticket #8

        obj_res_partner = self.pool.get('res.partner')

        value = {}
        domain = {}
        warning = {}

        if partner_id:
            npwp = obj_res_partner.browse(cr, uid, partner_id).npwp
            value.update({'partner_npwp' : npwp})
        
        return {'value' : value, 'domain' : domain, 'warning' : warning}
        
    def create_sequence(self, cr, uid, id):
        #TODO: Ticket #9
        
        obj_sequence = self.pool.get('ir.sequence')
        obj_company = self.pool.get('res.company')
        
        faktur_pajak = self.browse(cr, uid, [id])[0]
            
        sequence = obj_sequence.next_by_id(cr, uid, faktur_pajak.company_id.sequence_faktur_pajak.id)
        self.write(cr, uid, [id], {'name' : sequence})
            
        
        return True
        
    def select_sequence(self, cr, uid, id, faktur_pajak_sequence):
        """
        Parameter :
        faktur_pajak_sequence : char
        """
        #TODO: Ticket #10
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

            wkf_service.trg_validate(uid, 'pajak.faktur_pajak', id, 'button_cancel', cr)

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

        
        

faktur_pajak()

class faktur_pajak_line(osv.osv):
    _name = 'pajak.faktur_pajak_line'
    _description = 'Faktur Pajak Line'
    
    _columns =  {
                'name' : fields.char('Description', size=100, required=True),
                'product_id' : fields.many2one(obj='product.product', string='Product'),
                'faktur_pajak_id' : fields.many2one(obj='pajak.faktur_pajak', string='# Faktur Pajak'),
                'subtotal':fields.float(string='Subtotal', digits_compute=dp.get_precision('Account')),
                }   

faktur_pajak_line()

class faktur_pajak_ppnbm_line(osv.osv):
    _name = 'pajak.faktur_pajak_ppnbm_line'
    _description = 'Faktur Pajak PPNBm Line'
    
    _columns =  {
                                'ppnbm_rate' : fields.float(string='Rate', digits=(16,9), required=True),
                                'base' : fields.float(string='Base', digits_compute=dp.get_precision('Account'), required=True),
                                'ppnbm_amount' : fields.float(string='PPN Bm', digits_compute=dp.get_precision('Account'), required=True),
                                'faktur_pajak_id' : fields.many2one(obj='pajak.faktur_pajak', string='# Faktur Pajak'),
                }   

faktur_pajak_ppnbm_line()

class account_faktur_pajak_sequence(osv.osv):
    _name = 'pajak.faktur_pajak_sequence'
    _description = 'Faktur Pajak Sequence'
    
    _columns =  {
                'name' : fields.char('Name', size=30, readonly=True),
                'faktur_pajak_id' : fields.many2one(obj='pajak.faktur_pajak', string='# Faktur Pajak', readonly=True),
                }   
            

account_faktur_pajak_sequence()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
