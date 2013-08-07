# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
{
    'name' : 'AR - Indonesian Tax Module',
    'version' : '1.1',
    'author' : 'Andhitia Rama & Michael Viriyananda',
    'category' : 'Accounting & Finance',
    'description' : """
                            Indonesian tax module with no dependency to accounting module
    """,
    'website': 'http://andhitiarama.wordpress.com',
    'images' : [],
    'depends' : ['product', 'ar_base_amount_to_text'],
    'data' : [  
                    'security/ir.model.access.csv',
                    'security/data_Application.xml',
                    'security/data_GroupsFakturPajak.xml',
                    'security/data_GroupsFormulir1111A1.xml',
                    'security/data_GroupsFormulir1111A2.xml',
                    'security/data_GroupsFormulir1111B1.xml',
                    'security/data_GroupsFormulir1111B2.xml',
                    'workflow/workflow_FakturPajak.xml',
                    'workflow/workflow_SuratSetorPajak.xml',
                    'view/view_TahunPajak.xml',
                    'view/view_AkunPajak.xml',
                    'view/view_JenisSetorPajak.xml',
                    'view/view_FakturPajak.xml',
                    'view/view_ResCurrency.xml',
                    'view/view_SuratSetorPajak.xml',
                    'view/view_Formulir1111.xml',
                    'view/view_Formulir1111A1.xml',
                    'view/view_Formulir1111A2.xml',
                    'view/view_Formulir1111B1.xml',
                    'view/view_Formulir1111B2.xml',                                                                                
                    'window_action/waction_TahunPajak.xml',
                    'window_action/waction_AkunPajak.xml',
                    'window_action/waction_JenisSetorPajak.xml',
                    'window_action/waction_FakturPajak.xml',
                    'window_action/waction_Formulir1111.xml',
                    'window_action/waction_Formulir1111A1.xml',
                    'window_action/waction_Formulir1111A2.xml',
                    'window_action/waction_Formulir1111B1.xml',
                    'window_action/waction_Formulir1111B2.xml',
                    'window_action/waction_SuratSetorPajak.xml',
                    'menu/menu_Tax.xml'],
    'js' : [],
    'qweb' : [],
    'css' : [],
    'demo ': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
