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

class res_company(osv.osv):
	_name = 'res.company'
	_inherit = 'res.company'

	_columns =	{
							'sequence_faktur_pajak' : fields.many2one(string="Sequence Faktur Pajak", obj="ir.sequence"),
							'sequence_formulir_1111_a1' : fields.many2one(string="Sequence Formulir 1111 A1", obj="ir.sequence"),
							'sequence_formulir_1111_a2' : fields.many2one(string="Sequence Formulir 1111 A2", obj="ir.sequence"),
							'sequence_formulir_1111_ab' : fields.many2one(string="Sequence Formulir 1111 AB", obj="ir.sequence"),
							'sequence_formulir_1111_b1' : fields.many2one(string="Sequence Formulir 1111 B1", obj="ir.sequence"),
							'sequence_formulir_1111_b2' : fields.many2one(string="Sequence Formulir 1111 B2", obj="ir.sequence"),
							'sequence_formulir_1111_b3' : fields.many2one(string="Sequence Formulir 1111 B3", obj="ir.sequence"),
							'sequence_nota_pembatalan' : fields.many2one(string="Sequence Nota Pembatalan", obj="ir.sequence"),
							'sequence_nota_retur' : fields.many2one(string="Sequence Nota Retur", obj="ir.sequence"),
							'faktur_pajak_signature_id' : fields.many2one(string="Faktur Pajak Signature", obj="res.users"),
							'nota_pembatalan_signature_id' : fields.many2one(string="Nota Pembatalan Signature", obj="res.users"),
							'nota_retur_signature_id' : fields.many2one(string="Nota Retur Signature", obj="res.users"),
							}
		
res_company()




