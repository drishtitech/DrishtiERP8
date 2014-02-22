#!/usr/bin/env python
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

from openerp.report import report_sxw
from openerp.tools import amount_to_text_en
#from openerp.tools import amount_to_text
#from openerp.tools.amount_to_text import amount_to_text_in
#from openerp.tools.amount_to_text_in import amount_to_text
import time
from datetime import datetime
from drishti_hr.amount_to_text_in import amount_to_text
class payslip_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(payslip_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_payslip_lines': self.get_payslip_lines,
            'amount_to_text_en' : amount_to_text_en,
            'get_days' : self.get_days,
        })
        
    def get_days(self, obj):
        
        res1 = {'working_days' : 30, 'absent_days' :0.0}
        payslip = self.pool.get('hr.payslip')
        print "payslip.date_to",type(obj.date_to)
        to_date =  datetime.strptime(obj.date_to, '%Y-%m-%d').strftime('%d')
        res1['working_days'] =to_date
        for worked_line in obj.worked_days_line_ids:
            if worked_line.code == 'Unpaid':
                res1['absent_days'] += worked_line.number_of_days
                
        return res1     
    
    def get_payslip_lines(self, obj):
        payslip_line = self.pool.get('hr.payslip.line')
        res = []
        ids = []
        res1 = {'earn' :[],'ded' : [],'total_earn' : 0, 'total_ded' : 0, 'net_pay' : 0.0}
        total_ded = 0
        for id in range(len(obj)):
            if obj[id].appears_on_payslip == True:
                dic = {}
                if obj[id].category_id.code != 'DED'  and obj[id].category_id.code != 'NET' and obj[id].category_id.code != 'GROSS':
                    dic['code'] = obj[id].name
                    dic['amount'] = obj[id].total
                    dic['code1'] = ''
                    dic['amount1'] = ''
                    res1['earn'].append(dic)
                elif obj[id].category_id.code == 'DED' :
                    dic['code1'] = obj[id].name
                    dic['amount1'] = obj[id].total * -1
                    dic['code'] = ''
                    dic['amount'] = ''
                    total_ded += obj[id].total * -1
                    res1['ded'].append(dic) 
                elif obj[id].category_id.code == 'NET':
                    res1['net_pay'] = obj[id].total
                elif  obj[id].category_id.code == 'GROSS': 
                     res1['total_earn'] = obj[id].total
                     
                     
        for i in range(len(res1['ded'])):
            if i <= len(res1['earn']):
                res1['earn'][i]['code1']  =  res1['ded'][i]['code1']
                res1['earn'][i]['amount1']  =  res1['ded'][i]['amount1']
            else:
                 res1['earn'].append(res1['ded'])   
                 
                    
        res1['total_ded'] = total_ded 
        print "total_ded",total_ded       
        print "res1",res1,obj[0].employee_id.company_id.id
        
        res1['amount_in_word'] = amount_to_text(res1['net_pay'],'en', obj[0].employee_id.company_id.currency_id.name)    
           
        return [res1]
    
    def get_payslip_lines1(self, obj):
        payslip_line = self.pool.get('hr.payslip.line')
        res = []
        ids = []
        for id in range(len(obj)):
            if obj[id].appears_on_payslip == True:
                ids.append(obj[id].id)
        if ids:
            res = payslip_line.browse(self.cr, self.uid, ids)
            
        return res

report_sxw.report_sxw('report.payslip1', 'hr.payslip', 'drishti_hr/report/report_payslip.rml', parser=payslip_report)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
