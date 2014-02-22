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
    'name': 'Allocate Leave request',
    'version': '1.1',
    'author': 'Amit Gupta',
    'category': 'HR',
    'sequence': 21,
    'website': 'http://www.drishtitech.com',
    'summary': 'Allocate 5 leaves after every three months',
    'description': """
         Employee leave Allocation
         """,
 
    'images': [
               ],
    'depends': ['base', 'hr','hr_payroll'],
    'data': [    
                 'hr_employee_view.xml',
                'hr_payroll_report.xml',
                'skill_matrics_view.xml',
                'employee_increment_view.xml',
                 
                 ],
    'demo': [],
    'test': [  
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'css': [  ],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
