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
    'depends' : [],
    'data' : [  'view/view_TahunPajak.xml',
                    'window_action/waction_TahunPajak.xml',
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
