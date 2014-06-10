from openerp.osv import fields, osv
from openerp.tools.translate import _

import datetime
from datetime import date
from datetime import timedelta
import calendar
import time


class hr_attendance_table(osv.osv):
    _name='hr.attendance.table'
    _description = 'Attendance Table'
    _columns = {
        'date_from':fields.date('Date From',required=True),
        'date_to':fields.date('Date To',required=True),
        'name':fields.char('Attendance Slip', size=124),
        'employee_id':fields.many2one('hr.employee', 'Employee', required=True), 
        'month_days' :fields.float('Month Days',),
        'salary_days' : fields.float('Salary Days'),
        'attendance_days' : fields.float('Attendance Days'),
        'holiday_attendance_days' : fields.float('Holiday attendance Days'),
        'attendance_line':fields.one2many('hr.attendance.table.line','attendance_table','Attendance Lines', size=124),       
}
    _defaults={
         'name': lambda obj, cr, uid, context: '/',   
               }
    
    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'hr.attendance.table') or '/'
        return super(hr_attendance_table, self).create(cr, uid, vals, context=context)
    
#     def recompute_attendance(self, cr, uid, ids, context=None):
#         for attendance in self.browse(cr, uid, ids,context=None):
#             contract_ids = self.pool.get('hr.payslip').get_contract( cr, uid, attendance.employee_id, attendance.date_from, attendance.date_to, context=None)
#             contract_obj = self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context) and self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context)[0] or False
#             for line in attendance.attendance_line:
#                         date = line.date
#                         date1= datetime.datetime.strptime(date,'%Y-%m-%d')
#                         j ='A'
#                         if line.attendance:
#                             j= 'P'
#                         
#                         absent_info = ''
#                         final_result = ''
#                         
#                         if contract_obj:
#                             search_for_weekly_off = self.pool.get('resource.calendar').working_hours_on_day(cr, uid, contract_obj.working_hours, date1, context)
#                             search_for_even_saturday = self.pool.get('leaves.calendar').search(cr, uid, [('holiday_id','=',contract_obj.holidays_id.id),('date_from','=',date1),('type','=','even_sat')])
#                             search_for_holiday=self.pool.get('leaves.calendar').search(cr, uid, [('holiday_id','=',contract_obj.holidays_id.id),('date_from','=',date1),('type','<>','even_sat')])
#                             search_for_leave=self.pool.get('hr.holidays').search(cr, uid, [('employee_id','=',attendance.employee_id.id),('state','=','validate'),('type','=','remove'),('date_from','<=',date),('date_to','>=',date)])
#                             if search_for_even_saturday:
#                                 search_for_weekly_off = 0.0
#                             if search_for_leave:  
#                                     absent_info = self.pool.get('hr.holidays').browse(cr, uid, search_for_leave, context=context)[0].holiday_status_id.payroll_code.name or self.pool.get('hr.holidays').browse(cr, uid, search_for_leave, context=context)[0].holiday_status_id.name
#                                     if  absent_info == "Unpaid":
#                                         absent_info = 'UL'
#                                     else:
#                                         absent_info = 'PL'
#                             elif search_for_holiday:
#                                     absent_info = 'H'
#                             elif not search_for_weekly_off:
#                                 absent_info = 'WO'
#                         if absent_info:
#                             if j== 'P' and absent_info=='H': #and attendance_status==True:
#                                 final_result = 'HH'                
#                             else:
#                                 final_result = absent_info       
#                         else:
#                             if j== 'P':        
#                                     final_result ='P'
#                             else:
#                                     final_result ='A'  
#                         if j == 'P':
#                             attendance_line_id = self.pool.get('hr.attendance.table.line').write(cr,uid,line.id,{
#                                                                                                         
#                                   
#                                   'absent_info':absent_info,'final_result':final_result})
#                         else:
#                             self.pool.get('hr.attendance.table.line').write(cr,uid,line.id,{
#                                 
#                                 
#                                   'absent_info':absent_info,'final_result':final_result})   
#                         
#                         
#         
#         return True
    
hr_attendance_table()


class hr_attendance_table_line(osv.osv):
    _name = 'hr.attendance.table.line'
    _description = 'Attendance Table'
    _columns = {
    'attendance_table':fields.many2one('hr.attendance.table','Attendance'),
    'name' : fields.char('Name'),
    'employee_id': fields.related('attendance_table', 'employee_id', string='Employee Id',store=True,type='many2one',relation="hr.employee",readonly=True),
    'date': fields.date('Attendance Date',required=True),
    'attendance': fields.boolean('Absent/Present'),
    'absent_info': fields.char('Holiday Information', size=124),
    'final_result': fields.selection([('P','P'),('A','A'),('PL','PL'),('WO','WO'),('UL','UL'),('H','H')],'Result'),
  'goa_drive_attendance':fields.selection([('C','C'),('U','U'),('L','L'),('W','W'),('T','T'),('O','O'),('M','M'),('P','P'),('A','A'),('H','H'),('SL','SL'),('C/O','C/O'),('CO','C/O')],'HR Drive Attendance'),
   'biometric_attendance':fields.selection([('P','P'),('A','A')],'Biometric Attendance',readonly=True),
   'login_time':fields.char('Punch In',readonly=True),
   'logout_time':fields.char('Punch Out',readonly=True)
   }
       
#     def fetch_attendance_info(self,cr,uid,ids,context=None):
#          for p in self.browse(cr, uid, ids,context=None):
#                          leave_id=p.id
#                          employee_id=p.employee_id.id
#                          specific_date=p.date
#                          attendance_status=p.attendance
#                          absent_info=p.absent_info
#                          aa = datetime.datetime.strptime(specific_date,"%Y-%m-%d")
#                          contract_ids = self.pool.get('hr.payslip').get_contract( cr, uid, p.employee_id, specific_date, specific_date, context=None)
#                          contract_obj = self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context) and self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context)[0] or False
#                          if contract_obj:
#                              search_for_weekly_off = self.pool.get('resource.calendar').working_hours_on_day(cr, uid, contract_obj.working_hours, aa, context)
#                         
#                          search_for_holiday=self.pool.get('leaves.calendar').search(cr, uid, [('employee_id','=',employee_id),('date_from','=',specific_date)])
#                         
#                          search_for_leave=self.pool.get('hr.holidays').search(cr, uid, [('employee_id','=',employee_id),('state','=','validate'),('type','=','remove'),('date_from','<=',specific_date),('date_to','>=',specific_date)])
#                                                 
#                          if search_for_leave:
#                              
#                              res = self.pool.get('hr.holidays').browse(cr, uid, search_for_leave, context=context)[0].holiday_status_id.payroll_code.name
#                              self.write(cr,uid,leave_id,{'absent_info':res}) 
#                                                                             
#                          elif search_for_holiday:
#                             
#                             self.write(cr,uid,leave_id,{'absent_info':'H'})
#                             
#                          elif not search_for_weekly_off:
#                              
#                              self.write(cr,uid,leave_id,{'absent_info':'WO'})
#                          
#                          
#                          for q in self.browse(cr, uid, ids,context=None):
#                                 absent_info_new=q.absent_info
#                                         
#                          if absent_info_new: 
#                              if attendance_status==True and absent_info_new=='H':
#                              
#                                  self.write(cr,uid,leave_id,{'final_result':'HH'})
#                              else:
#                                  self.write(cr,uid,leave_id,{'final_result':absent_info_new})
#                          else:
#                              if attendance_status:
#                                  self.write(cr,uid,leave_id,{'final_result':'P'})
#                              else:
#                                  self.write(cr,uid,leave_id,{'final_result':'A'})     
#                                    
#          return True                 
 