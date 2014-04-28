#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
    'name': 'Payroll Days in the Month',
    'version': '1.0',
    'category': 'Human Resources',
    'sequence': 38,
    'description': """
Add calculation for number of days in the month.
=======================

   
    """,
    'author':'Drishti Tech',
    'website':'http://www.drishtitech.com',
    'images': ['images/hr_company_contributions.jpeg','images/hr_salary_heads.jpeg','images/hr_salary_structure.jpeg','images/hr_employee_payslip.jpeg'],
    'depends': [
        'hr',
        'hr_payroll'],
    'data': ['hr_payroll_month_view.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
