# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2012 Tiny SPRL (<http://tiny.be>).
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
    'name': 'Multi Branch Rights',
    'author': 'Drishti Tech',
    'version': '1.0',
    'depends': ['base',],
    'category' : 'Tools',
    'summary': 'Enable rights management for handling multiple branches of the same company',
    'description': """
The Multi Department Rights module takes the concept of Multi-Comapnies in OpenERP and expands the same to enable management of Multiple departments
    """,
    'data': ['multi_branch_view.xml',],
    'images': [],
    'demo': [],
    'installable': True,
    'application' : True,
    'certificate' : '',
}
