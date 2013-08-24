# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP SA (<http://openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from osv import fields, osv
from tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
import decimal_precision as dp
import netsvc
from tools.translate import _
from datetime import datetime


class wizard_confirm_faktur_pajak(osv.osv_memory):
    _name = 'pajak.wizard_confirm_faktur_pajak'
    _description = 'Wizard Confirm Faktur Pajak'


    _columns =  {
                'select_sequence' : fields.boolean(string='Select Existing Sequence'),
                'sequence_id' : fields.many2one(string='Sequence', obj='pajak.faktur_pajak_sequence', domain=[('faktur_pajak_id','=',False)]),
                }

                
    def run_wizard(self, cr, uid, ids, context={}):
        #TODO: Ticket #112
# Jika select_sequence == False, maka jalankan method create_sequence
# Jika select_sequecen == True, maka jalankan method select_sequence dengan param faktur_pajak_sequence = sequence_id.name
# Kemudian trg_validate hingga draft -> confirm

        wkf_service = netsvc.LocalService("workflow")

        obj_wizard = self.pool.get('pajak.wizard_confirm_faktur_pajak')
        obj_faktur_pajak = self.pool.get('pajak.faktur_pajak')

        record_id = context and context.get('active_id', False) or False
        wizard = obj_wizard.browse(cr, uid, ids)[0]
        
        if wizard.select_sequence != True:
            obj_faktur_pajak.create_sequence(cr, uid, record_id)
            wkf_service.trg_validate(uid, 'pajak.faktur_pajak', record_id, 'button_confirm', cr)
        else:
            obj_faktur_pajak.select_sequence(cr, uid, wizard.sequence_id.id)
        return {}        
                
wizard_confirm_faktur_pajak()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
