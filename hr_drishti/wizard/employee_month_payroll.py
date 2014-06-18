from openerp.osv import fields,osv
import datetime
import StringIO
import cStringIO
import base64
import csv
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import xlwt
from xlwt import *

class employee_payroll_report(osv.osv_memory):
    _name='employee.payroll.report'
    
    def _previous_date(self,cr,uid,ids,context=None):
        datedefault=datetime.date.today() - relativedelta( months = 1 )
        b = datedefault.strftime("%Y-%m-%d %H:%M:%S")
        return b
    
    _columns={
              'date': fields.date('Payroll Month Date'), 
              'company_id':fields.many2one('res.company','Company'), 
             'journal_id' : fields.many2one('account.journal','Journal'),
             'category_id' : fields.many2one('hr.employee.category','Category'),
              'file_name':fields.binary('Report'),
              'name' : fields.char('Name')
              
              }
    _defaults={
                'date': _previous_date,
                'company_id': lambda self, cr, uid, ctx=None: self.pool.get('res.company')._company_default_get(cr, uid, 'employee.payroll.report', context=ctx),
               }
    
    def print_report(self,cr,uid,ids,context=None):
        
        
        obj=self.browse(cr,uid,ids[0])
        filename = 'Employee Payroll.xls'
        string = 'Payroll'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
        
        date_dict = {}
        date=obj.date
        year = int(date[:4])     
        month = int(date[5:7])
        total_days= monthrange(year, month)[1]
        for i in range(1,total_days+1):
            date_dict[i] = datetime.date(year,month,i)
        date_from = datetime.date(year,month, 1)
        date_to = datetime.date(year, month, total_days)
        
        
        employee_obj =self.pool.get('hr.employee')
        payslip_obj =self.pool.get('hr.payslip')
        payslip_line_obj =self.pool.get('hr.payslip.line')
        salary_rule_obj = self.pool.get('hr.salary.rule')
        
        if obj.category_id:
            employee_ids = employee_obj.search(cr ,uid, [('category','=', obj.category_id.id)])
        else:
            employee_ids = employee_obj.search(cr ,uid, [])
        print "employee_ids",employee_ids
        if employee_ids:
            domain = [('employee_id','in',employee_ids),('company_id','=',obj.company_id.id)]
            if obj.journal_id:
                domain.append(('journal_id','=',obj.journal_id.id))
               
              
            payslip_ids = payslip_obj.search(cr ,uid, domain)
            #print "payslip_ids", payslip_ids
            if payslip_ids:
                payslip_line_ids = payslip_line_obj.search(cr,uid,[('slip_id','in',payslip_ids)])
                cr.execute('SELECT DISTINCT(salary_rule_id) FROM hr_payslip_line WHERE slip_id in %s',(tuple(payslip_ids),))
                salary_rule_ids = map(lambda x: x[0], cr.fetchall())
                
                rule_list = salary_rule_obj.read(cr, uid, salary_rule_ids,['name','code','sequence'])
                newlist = sorted(rule_list, key=lambda k: k['sequence']) 
                print "rule_list",rule_list
                k= 3 
                dic = {}
                style = XFStyle()
                fnt = Font()
                fnt.colour_index = 0x36
                fnt.bold = True
                style.font = fnt
                worksheet.write(3,0,'S.No.',style)
                worksheet.write(3,1,'Employee Name',style)
                worksheet.write(3,2,'SLSG No.',style)
                
                for l in newlist:
                    print "list",l
                    dic[l['id']] = k
                    
                    worksheet.write(3,k,l['name'],style)
                    k +=1
    #             worksheet.write(3,7,'This Week',style)
    #             worksheet.write(4,2,previous_users)
    #             worksheet.write(4,7,current_user)
                j =4
                p=0
                seq =1
                print "dic",dic
                dic1 = {}
                for key in dic.keys():
                    dic1[key] = 0
                    
                for emp_id in employee_ids:
                    payslip_id = payslip_obj.search(cr ,uid, [('employee_id','=',emp_id),('id','in' ,payslip_ids)])
                    if payslip_id:
                        emp_obj = employee_obj.browse(cr,uid,emp_id)
                        worksheet.write(j,p,seq)
                        worksheet.write(j,p+1,emp_obj.name)
                        worksheet.write(j,p+2,emp_obj.identification_id1)
                        
                        payslip_brw = payslip_obj.browse(cr, uid,payslip_id)[0]
                        for line in payslip_brw.line_ids:
                                dic1[line.salary_rule_id.id] += line.total
                                if line.salary_rule_id.name in ['Gross','Net', 'CTC']:
                                    worksheet.write(j,dic[line.salary_rule_id.id],line.total,style)
                                else:
                                    worksheet.write(j,dic[line.salary_rule_id.id],line.total)
                        j +=1
                        seq +=1 
                worksheet.write(j,0,'Total')
                for key in dic.keys():
                    worksheet.write(j,dic[key],dic1[key],style)
                   
            #print "set",set(list1)
            fp = cStringIO.StringIO()
            wb.save(fp)
            out = base64.encodestring(fp.getvalue())
            self.write(cr,uid,ids,{'file_name':out,'name': filename})
            return {
                    'domain': ([('id', 'in', ids)]),
                        'view_type': 'form',
                        'view_mode': 'tree,form',
                        'res_model': 'employee.payroll.report',
                        'target':'current',
                        'nodestroy': True,
                        'type': 'ir.actions.act_window',
                        'name' : 'Payroll Report',
                        'res_id': ids
                    
                    
                    }