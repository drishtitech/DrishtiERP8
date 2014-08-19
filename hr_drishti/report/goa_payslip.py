import time
from openerp.osv import osv
from openerp.report import report_sxw
from operator import itemgetter
from amount_to_text_en import amount_to_text_in
from datetime import datetime

class employee_goa_payslip(report_sxw.rml_parse):
   
    def __init__(self, cr, uid, name, context=None):
        if context is None:
            context = {}
        super(employee_goa_payslip, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_days': self._get_days,
            'get_allowance' : self._get_allowance,
            'get_deduction' : self._get_deduction,
            'get_result': self._get_result,
             'amount_to_text_in' : amount_to_text_in,
             'get_record' : self._get_record,
            })
        
    def _get_record(self,objs):
        obj_list = []
        if len(objs)%2 == 0:
            for i in range(0,len(objs),2):
                obj_list.append((objs[i],objs[i+1]))
        else:
            for i in range(0,len(objs)-1,2):
                t = (objs[i],objs[i+1])
                obj_list.append(t)
            obj_list.append((objs[len(objs)-1],))
        return obj_list
    def _get_days(self, obj):
        res = {
               'monthDays' : 0,
               'presentDays' : 0,
               'weeklyOff' : 0,
               'leaveDays'     : 0,
               'absentDays' : 0,
               'paidDays' : 0,
               }
        for worked_line in obj.worked_days_line_ids:
            if worked_line.code == 'MONTHDAYS': 
                res['monthDays'] = worked_line.number_of_days  
            if worked_line.code == 'SALARYDAYS':
                res['paidDays'] += worked_line.number_of_days
            if worked_line.code == 'WORK200':
                res['presentDays'] += worked_line.number_of_days
        res['absentDays'] =   res['monthDays'] -  res['paidDays']
        print "testing",res        
        return res 
    def _get_allowance(self, obj):
        res = []
        for line in obj.line_ids:
            if line.category_id.name in ['Basic' ,'Allowance']:
                res.append((line.name,round(line.total,2),line.sequence))
        sorted(res,key=itemgetter(2))        
        return sorted(res,key=itemgetter(2))        
    def _get_deduction(self, obj):
        res = []
        for line in obj.line_ids:
            if line.category_id.name in ['Deduction']:
                res.append((line.name,round(line.total,2),line.sequence))
        sorted(res,key=itemgetter(2))        
        return sorted(res,key=itemgetter(2))  
    
    def _get_result(self, obj):
        res = {'grossEarning' :0, 'netSalary' :0}
        for line in obj.line_ids:
            if line.category_id.name == 'Gross':
                res['grossEarning'] = round(line.total,2)
            if line.category_id.name == 'Net':
                res['netSalary'] = round(line.total, 2)
        res['totalDed'] = res['grossEarning'] - res['netSalary']
        res['year'] = obj.date_from[:4] 
        print "obj.date_from",obj.date_from
        a = datetime.strptime(obj.date_from , '%Y-%m-%d')
        res['month'] =a.strftime("%B")  
        print "res",res    
        return res 
     
#     def _get_date(self,date):
#         print'=_get_date=======_get_date_get_date'
#         d = datetime.datetime.strptime(date, '%Y-%m-%d')
#         return d.strftime('%d-%m-%Y')


    
class report_employee_goa_payslip(osv.AbstractModel):
    _name = 'report.hr_drishti.report_employee_goa_payslip'
    _inherit = 'report.abstract_report'
    _template = 'hr_drishti.report_employee_goa_payslip'
    _wrapped_report_class = employee_goa_payslip