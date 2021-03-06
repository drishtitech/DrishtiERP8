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
    "name": "Employee Data",
    "version": "1.1",
    "author": "OpenERP SA",
    "category": "Leads",
    "sequence": 12,
    'complexity': "easy",
    "website": "http://www.openerp.com",
    "description": """
Module for human resource management.
=====================================

You can manage:
    * Employees and hierarchies : You can define your employee with User and display hierarchies
    * HR Departments
    * HR Jobs
    """,
    'author': 'OpenERP SA',
    'website': 'http://www.openerp.com',
    #'images': ['images/hr_department.jpeg', 'images/hr_employee.jpeg','images/hr_job_position.jpeg'],
    'depends': ['base','crm','hr','hr_holidays','hr_payroll',],
    'init_xml': [],
    'update_xml': [
        
        #'institute_view.xml',
        'hr_drishti_view.xml',
        'security/hr_security.xml',
        'security/ir.model.access.csv',
        'attendance_view.xml',
        'hr_attendance_payroll_view.xml',
       # 'product_view.xml',
        'wizard/import_attendance_view.xml', 
        'hr_working_schedule_demo.xml',
        'employee_month_payroll_view.xml',
        'report_bank_debit_view.xml',
        'views/bank_debit_repor.xml',
        'views/goa_payslip.xml',
        'bank_debit_letter.xml',
        'skill_matrics_view.xml',
        'employee_increment_view.xml',
        'hr_employee_view.xml',
        'hr_payroll_report.xml',
       # 'attendance_sequence.xml',
        
    ],
   
    
    'installable': True,
    'application': True,
    'auto_install': False,
    #'certificate': '0086710558965',
    #"css": [ 'static/src/css/hr.css' ],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
