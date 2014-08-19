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
import time
from openerp.osv import osv
from openerp.report import report_sxw
from num2words import num2words
import datetime

class bank_debit_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        if context is None:
            context = {}
        super(bank_debit_report, self).__init__(cr, uid, name, context=context)
        ids = context.get('active_ids')
        voucher_obj = self.pool['employee.bank.debit.details']
        docs = voucher_obj.browse(cr, uid, ids, context)
        self.localcontext.update({
            'time': time,
            'docs': docs,
            'get_date':self._get_date
            })
        self.context = context
        
    
 
    def _get_date(self,date):
        print'=_get_date=======_get_date_get_date'
        d = datetime.datetime.strptime(date, '%Y-%m-%d')
        return d.strftime('%d-%m-%Y')

        
class drishti_bank_debit_letter(osv.AbstractModel):
    _name = 'report.hr_drishti.drishti_bank_debit_letter'
    _inherit = 'report.abstract_report'
    _template = 'hr_drishti.drishti_bank_debit_letter1'
    _wrapped_report_class = bank_debit_report



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
   