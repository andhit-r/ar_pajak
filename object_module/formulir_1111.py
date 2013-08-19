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

class formulir_1111(osv.osv):
	_name = 'pajak.formulir_1111'
	_description = 'SPT Masa PPN'
	_inherit = ['mail.thread']
	
	def default_state(self, cr, uid, context={}):
		return 'draft'
		
	def default_name(self, cr, uid, context={}):
		return '/'
		
	def default_company_id(self, cr, uid, context={}):
		#TODO : Ticket #29
		return False
		
	def default_created_time(self, cr, uid, context={}):
		#TODO: Ticket #30
		return datetime.now().strftime('%Y-%m-%d')
		
	def default_created_user_id(self, cr, uid, context={}):
		return uid

	_columns = 	{
								'name' : fields.char(string='# SPT', size=30, required=True, readonly=True),
								'company_id' : fields.many2one(obj='res.company', string='Nama PKP', required=True),
								'company_npwp' : fields.char(string='NPWP', size=30, required=True),
                                'company_address' : fields.char(string='Alamat', size=255, required=True),
                                'masa_pajak_id' : fields.many2one(string='Masa Pajak', obj='pajak.masa_pajak', required=True),
                                'tahun_pajak_id' : fields.related('masa_pajak_id', 'tahun_pajak_id', string='Tahun Pajak', type='many2one', relation='pajak.tahun_pajak', store=True),
                                'telepon' : fields.char(string='Telepon', size=100),
                                'hp' : fields.char(string='HP', size=100),
                                'klu' : fields.char(string='KLU', size=100),
								'note' : fields.text(string='Note'),
                                'pembetulan_ke' : fields.integer(string='Pembetulan Ke'),
                                'wajib_ppnbm' : fields.boolean(string='Wajib PPnBM'),
                                # BAGIAN 1
                                'item1A1' : fields.float(string='1. Export', digits_compute=dp.get_precision('Account')),
                                'item1A2_dpp' : fields.float(string='2. Penyerahan yang PPN-nya harus dipungut sendiri', digits_compute=dp.get_precision('Account')),
                                'item1A2_ppn' : fields.float(string='2. Penyerahan yang PPN-nya harus dipungut sendiri', digits_compute=dp.get_precision('Account')),
                                'item1A3_dpp' : fields.float(string='3. Penyerahan yang PPN-nya dipungut oleh pemungut PPN', digits_compute=dp.get_precision('Account')),
                                'item1A3_ppn' : fields.float(string='3. Penyerahan yang PPN-nya dipungut oleh pemungut PPN', digits_compute=dp.get_precision('Account')),
                                'item1A4_dpp' : fields.float(string='4. Penyerahan yang PPN-nya tidak dipungut', digits_compute=dp.get_precision('Account')),
                                'item1A4_ppn' : fields.float(string='4. Penyerahan yang PPN-nya tidak dipungut', digits_compute=dp.get_precision('Account')),
                                'item1A5_dpp' : fields.float(string='4. Penyerahan yang dibebankan dari pengenaan PPN', digits_compute=dp.get_precision('Account')),
                                'item1A5_ppn' : fields.float(string='4. Penyerahan yang dibebankan dari pengenaan PPN', digits_compute=dp.get_precision('Account')),
                                'item_jumlah_1A' : fields.float(string='Jumlah (I.A.1 + I.A.2 + I.A.3 + I.A.4 + I.A.5', digits_compute=dp.get_precision('Account')),
                                'item1B' : fields.float(string='Tidak Terutang PPN', digits_compute=dp.get_precision('Account')),
                                'item1C' : fields.float(string='Jumlah Seluruh Penyerahan (I.A + I.B)', digits_compute=dp.get_precision('Account')),
                                # BAGIAN 2
                                'item2A' : fields.float(string='Pajak keluaran yang harus dipungut sendiri', digits_compute=dp.get_precision('Account')),
                                'item2B' : fields.float(string='PPN disetor dimuka dalam masa pajak yang sama', digits_compute=dp.get_precision('Account')),
                                'item2C' : fields.float(string='Pajak masukan yang dapat diperhitungkan', digits_compute=dp.get_precision('Account')),
                                'item2D' : fields.float(string='PPN kurang atau (lebih) bayar (II.A - II.B - II.C)', digits_compute=dp.get_precision('Account')),
                                'item2E' : fields.float(string='PPN kurang atau (lebih) bayar pada SPT yang dibetulkan', digits_compute=dp.get_precision('Account')),
                                'item2F' : fields.float(string='PPN kurang atau (lebih) bayar karena pembetulan (II.D - II.E)', digits_compute=dp.get_precision('Account')),
                                
                                # BAGIAN 3
                                'item3A' : fields.float(string='A. Jumlah Dasar Pengenaan Pajak', digits_compute=dp.get_precision('Account')),
                                'item3B' : fields.float(string='B. PPN Terutang', digits_compute=dp.get_precision('Account')),
                                'item3C_tanggal' : fields.date(string='C. Dilunasi Tanggal'),
                                'item3C_ntpn' : fields.char(string='NTPN', size=100),
                                
                                # BAGIAN 4
                                'item4A' : fields.float(string='A. PPN yang wajib dibayar kembali', digits_compute=dp.get_precision('Account')),
                                'item4B_tanggal' : fields.date(string='B. Dilunasi Tanggal'),
                                'item4B_ntpn' : fields.char(string='NTPN', size=100),                                
                                
                                # BAGIAN 5
                                'item5A' : fields.float(string='A. PPnBM yang harus dipungut kembali', digits_compute=dp.get_precision('Account')),
                                'item5B' : fields.float(string='B. PPnBM disetor dimuka dalam Masa Pajak yang sama', digits_compute=dp.get_precision('Account')),
                                'item5C' : fields.float(string='C. PPnBM kurang atau (lebih) bayar (V.A - V.B)', digits_compute=dp.get_precision('Account')),
                                'item5D' : fields.float(string='D. PPnBM kurang atau (lebih) bayar pada SPT yang dibetulkan', digits_compute=dp.get_precision('Account')),
                                'item5E' : fields.float(string='E. PPnBM kurang atau (lebih) bayar karena pembetulan (V.C - V.D)', digits_compute=dp.get_precision('Account')),
                                'item5F_tanggal' : fields.date(string='F. Dilunasi Tanggal'),
                                'item5F_ntpn' : fields.char(string='NTPN', size=100),                                       
                                
                                # BAGIAN 6
                                
                                
                                # PERNYATAAN
                                'kota_pernyataan' : fields.char(string='Kota', size=100, required=True),
                                'tanggal_pernyataan' : fields.date(string='Tanggal', required=True),
                                'pernyataan_user_id' : fields.many2one(string='Pengurus/Kuasa', obj='res.users', required=True),
                                'jenis_pengurus' : fields.selection(string='PKP/Kuasa', selection=[('pkp','PKP'),('kuasa','Kuasa')], required=True),
                                

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

                    wkf_service.trg_validate(uid, 'pajak.formulir_1111', id, 'button_cancel', cr)

                return True

        def log_audit_trail(self, cr, uid, id, event):
                #TODO: Ticket #31
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
                #TODO: Ticket #32
                wkf_service = netsvc.LocalService('workflow')

                wkf_service.trg_delete(uid, 'pajak.formulir_1111', id, cr)
                return True

        def create_workflow_instance(self, cr, uid, id):
                #TODO: Ticket #33
                wkf_service = netsvc.LocalService('workflow')

                wkf_service.trg_create(uid, 'pajak.formulir_1111', id, cr)
                return True

formulir_1111()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
