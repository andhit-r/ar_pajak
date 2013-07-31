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


class masa_pajak(osv.osv):
	_name = 'pajak.masa_pajak'
	_description = 'Masa Pajak'
	
	def default_state(self, cr, uid, context={}):
		return 'draft'

		
	_columns = 	{
				'name' : fields.char(string='Masa Pajak', size=30, required=True),
				'kode' : fields.char(string='Kode', size=30, required=True),
				'tahun_pajak_id' : fields.many2one(obj='pajak.tahun_pajak', string='Tahun Pajak', required=True),
				'tanggal_mulai' : fields.date(string='Tanggal Mulai', required=True),
				'tanggal_akhir' : fields.date(string='Tanggal Akhir', required=True),
				'sequence' : fields.integer(string='Urutan'),
				'state' : fields.selection(selection=[('draft','Draft'),('aktif','Aktif'),('selesai','Selesai')], string='Status', readonly=True),
				}
				
	_defaults =	{
				'state' : default_state,
				}
				
	def workflow_action_aktif(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'aktif'})
		return True
		
	def workflow_action_selesai(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'selesai'})
		return True		
				
	def find(self, cr, uid, tanggal=None, context=None):
		obj_masa_pajak = self.pool.get('pajak.masa_pajak')
	
		if context is None : context = {}
		
		if not tanggal:
			tanggal = fields.date.context_today(self, cr, uid, context=context)
			
		kriteria = [('tanggal_mulai', '<=', tanggal),('tanggal_akhir','>=', tanggal)] 
		
		masa_pajak_ids = obj_masa_pajak.search(cr, uid, kriteria, context=context)
		if not masa_pajak_ids:
			raise osv.except_osv('Peringatan', 'Tidak ada masa pajak didefinisikan untuk tanggal %s' % (tanggal))
			
		return masa_pajak_ids
		
	def masa_pajak_sebelum(self, cr, uid, masa_pajak_id, context=None):
		obj_masa_pajak = self.pool.get('pajak.masa_pajak')
		
		masa_pajak = obj_masa_pajak.browse(cr, uid, [masa_pajak_id])[0]
		
		kriteria = [('tahun_pajak_id.id', '=', masa_pajak.tahun_pajak_id.id), ('tanggal_mulai', '<', masa_pajak.tanggal_mulai)]
		
		masa_pajak_ids = obj_masa_pajak.search(cr, uid, kriteria)
		
		return masa_pajak_ids

masa_pajak()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
