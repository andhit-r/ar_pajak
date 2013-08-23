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
        if context is None:
            context = {}
        res = {}
        if 'date' in context:
            date = context['date']
        else:
            date = time.strftime('%Y-%m-%d')
        date = date or time.strftime('%Y-%m-%d')
        # Convert False values to None ...
        currency_rate_type = context.get('currency_rate_type_id') or None
        # ... and use 'is NULL' instead of '= some-id'.
        operator = '=' if currency_rate_type else 'is'
        for id in ids:
            cr.execute("SELECT currency_id, rate FROM pajak_tax_rate WHERE currency_id = %s AND name <= %s AND currency_rate_type_id " + operator +" %s ORDER BY name desc LIMIT 1" ,(id, date, currency_rate_type))
            if cr.rowcount:
                id, rate = cr.fetchall()[0]
                res[id] = rate
            else:
                res[id] = 0
        return res

    _columns =	{
                'tax_rate_ids' : fields.one2many(string='Tax Rate', obj='pajak.tax_rate', fields_id='currency_id'),
                'tax_rate' : fields.function(fnct=function_tax_rate, string='Tax Rate', type='float', digits=(16,2)),
                }
                                                    
    def get_tax_conversion_rate(self, cr, uid, from_currency, to_currency, context=None):
        #TODO: Ticket #19
        if context is None:
            context = {}
        ctx = context.copy()
        ctx.update({'currency_rate_type_id': ctx.get('currency_rate_type_from')})
        from_currency = self.browse(cr, uid, from_currency.id, context=ctx)

        ctx.update({'currency_rate_type_id': ctx.get('currency_rate_type_to')})
        to_currency = self.browse(cr, uid, to_currency.id, context=ctx)

        if from_currency.rate == 0 or to_currency.rate == 0:
            date = context.get('date', time.strftime('%Y-%m-%d'))
            if from_currency.rate == 0:
                currency_symbol = from_currency.symbol
            else:
                currency_symbol = to_currency.symbol
            raise osv.except_osv(_('Error'), _('No rate found \n' \
                    'for the currency: %s \n' \
                    'at the date: %s') % (currency_symbol, date))
        return to_currency.tax_rate/from_currency.tax_rate							
            
    def compute_tax(self, cr, uid, from_currency_id, to_currency_id, from_amount, round=True, currency_rate_type_from=False, currency_rate_type_to=False, context=None):
        #TODO: Ticket #20
        if not context:
            context = {}
        if not from_currency_id:
            from_currency_id = to_currency_id
        if not to_currency_id:
            to_currency_id = from_currency_id
        xc = self.browse(cr, uid, [from_currency_id,to_currency_id], context=context)
        from_currency = (xc[0].id == from_currency_id and xc[0]) or xc[1]
        to_currency = (xc[0].id == to_currency_id and xc[0]) or xc[1]
        if (to_currency_id == from_currency_id) and (currency_rate_type_from == currency_rate_type_to):
            if round:
                return self.round(cr, uid, to_currency, from_amount)
            else:
                return from_amount
        else:
            context.update({'currency_rate_type_from': currency_rate_type_from, 'currency_rate_type_to': currency_rate_type_to})
            rate = self.get_tax_conversion_rate(cr, uid, from_currency, to_currency, context=context)
            if round:
                return self.round(cr, uid, to_currency, from_amount * rate)
            else:
                return from_amount * rate
res_currency()




