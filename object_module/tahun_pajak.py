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
from datetime import datetime
from dateutil.relativedelta import relativedelta


class tahun_pajak(osv.osv):
	_name = 'pajak.tahun_pajak'
	_description = 'Tahun Pajak'
		
	_columns = 	{
				'name' : fields.char(string='Tahun Pajak', size=30, required=True),
				'kode' : fields.char(string='Kode', size=10, required=True),
				'tanggal_mulai' : fields.date(string='Tanggal Mulai', required=True),
				'tanggal_akhir' : fields.date(string='Tanggal Akhir', required=True),
				'masa_pajak_ids' : fields.one2many(obj='pajak.masa_pajak', fields_id='tahun_pajak_id', string='Masa Pajak'),
				}
				
	def find(self, cr, uid, tanggal=None, context=None):
		obj_tahun_pajak = self.pool.get('pajak.tahun_pajak')
	
		if context is None : context = {}
		
		if not tanggal:
			tanggal = fields.date.context_today(self, cr, uid, context=context)
			
		kriteria = [('tanggal_mulai', '<=', tanggal),('tanggal_akhir','>=', tanggal)] 
		
		tahun_pajak_ids = obj_tahun_pajak.search(cr, uid, kriteria, context=context)
		if not tahun_pajak_ids:
			raise osv.except_osv('Peringatan', 'Tidak ada tahun pajak didefinisikan untuk tanggal %s' % (tanggal))
			
		return tahun_pajak_ids
		
	def buat_masa_pajak(self, cr, uid, ids, context=None):
		obj_masa_pajak = self.pool.get('pajak.masa_pajak')
		obj_tahun_pajak = self.pool.get('pajak.tahun_pajak')

		for tahun_pajak in obj_tahun_pajak.browse(cr, uid, ids, context=context):
			ds = datetime.strptime(tahun_pajak.tanggal_mulai, '%Y-%m-%d')
			sequence = 1
			while ds.strftime('%Y-%m-%d') < tahun_pajak.tanggal_akhir:
				de = ds + relativedelta(months=1, days=-1)

				if de.strftime('%Y-%m-%d') > tahun_pajak.tanggal_akhir:
				    de = datetime.strptime(tahun_pajak.tanggal_akhir, '%Y-%m-%d')
				    
				val =	{
						'name' : ds.strftime('%m/%Y'),
						'kode' : ds.strftime('%m/%Y'),
						'tanggal_mulai' : ds.strftime('%Y-%m-%d'),
						'tanggal_akhir' : de.strftime('%Y-%m-%d'),
						'tahun_pajak_id' : tahun_pajak.id,
						'sequence' : sequence,
						}
		
				obj_masa_pajak.create(cr, uid, val)

				ds = ds + relativedelta(months=1)
				sequence += 1
		return True						

tahun_pajak()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
