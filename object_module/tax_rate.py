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


class tax_rate(osv.osv):
    _name = 'pajak.tax_rate'
    _description = 'Tax Rate'

    _columns = {
        					'name': fields.date(string='Date', required=True, select=True),
        					'rate': fields.float(string='Rate', digits=(12,6), help='The rate of the currency to the currency of rate 1'),
        					'currency_id': fields.many2one(obj='res.currency', string='Currency', readonly=True),
        					'currency_rate_type_id': fields.many2one(obj='res.currency.rate.type', string='Currency Rate Type', help="Allow you to define your own currency rate types, like 'Average' or 'Year to Date'. Leave empty if you simply want to use the normal 'spot' rate type"),
    						}
    						
    _defaults = {
        					'name': lambda *a: time.strftime('%Y-%m-%d'),
    						}
    _order = 'name desc'

tax_rate()
	
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:



