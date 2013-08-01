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

class res_currency(osv.osv):
	_name = 'res.currency'
	_inherit = 'res.currency'
	
	def function_tax_rate(self, cr, uid, ids, name, arg, context=None):
		#TODO: Ticket #18
		res = {}
		
		for id in ids:
			res[id] = 0.0
			
		return res

	_columns =	{
							'tax_rate_ids' : fields.one2many(string='Tax Rate', obj='pajak.tax_rate', fields_id='currency_id'),
							'tax_rate' : fields.function(fnct=function_tax_rate, string='Tax Rate', type='float', digits=(16,2)),
							}
							
	def get_tax_conversion_rate(self, cr, uid, from_currency, to_currency, context=None):
		#TODO: Ticket #19
		return True							
		
	def compute_tax(self, cr, uid, from_currency_id, to_currency_id, from_amount, round=True, currency_rate_type_from=False, currency_rate_type_to=False, context=None):
		#TODO: Ticket #20
		return True
res_currency()




