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
from dateutil.relativedelta import relativedelta
from openerp.osv import fields, osv
from openerp.tools.translate import _
import StringIO
import base64
import xlrd
import calendar
from calendar import monthrange
import datetime
from time import strftime

class attendance_import(osv.osv_memory):
    _name='attendance.import'
    
    
    def _previous_date(self,cr,uid,ids,context=None):
        datedefault=datetime.date.today() - relativedelta( months = 1 )
        b = datedefault.strftime("%Y-%m-%d %H:%M:%S")
        return b
    
    _columns={
              'file':fields.binary("File Path:"),
              'file_name':fields.char('File Name:'),
              'location':fields.selection([('1', 'Mumbai'), ('2', 'Goa')],'Location'),
              'date': fields.date('Date')             
               }
    
    _defaults={
               'date': _previous_date                                                                                                #lambda *a:time.strftime("%Y-%m-%d")
               }
    
    
    def import_deduction_goa(self,cr,uid,ids,context=None):
        dedution_obj = self.pool.get('employee.deduction')
        deduction_line_obj = self.pool.get('employee.deduction.line')
        employee_obj = self.pool.get('hr.employee')
        cur_obj = self.browse(cr,uid,ids)[0]
        file_data=cur_obj.file
        val=base64.decodestring(file_data)
        fp = StringIO.StringIO()
        fp.write(val)    
        wb = xlrd.open_workbook(file_contents=fp.getvalue())
        date=cur_obj.date
        sheet=wb.sheet_by_index(0)
        year = int(date[:4])
        month = int(date[5:7])   
        total_days= monthrange(year, month)[1]
        date_from = datetime.date(year,month, 1)
        date_to = datetime.date(year, month, total_days)
        deuction_id = dedution_obj.create(cr, uid,{'deduction_from_date' : date_from, 'deduction_to_date' : date_to })
        for i in range(1,sheet.nrows):
            emp_code =sheet.cell_value(i,1)
            employee_id = employee_obj.search(cr,uid,[('identification_id1','=',emp_code)])
            if employee_id:
                deduction_line_dic = {
                                       'deduction_id': deuction_id,
                                       'employee_id': employee_id[0],
                                       'mobile_deduction':sheet.cell_value(i,3),
                                       'loan_deduction':sheet.cell_value(i,4),
                                       'tds_deduction' : sheet.cell_value(i,5)
                                      }
                deduction_line_obj.create(cr, uid, deduction_line_dic)
        return True
    
    def import_attendance(self,cr, uid, ids, context=None):
        attendance_obj = self.pool.get('hr.attendance.table')
        attendance_line_obj = self.pool.get('hr.attendance.table.line')
        employee_obj = self.pool.get('hr.employee')
        holiday_obj = self.pool.get('hr.holiday')
        holiday_status_obj = self.pool.get('hr.holiday.status')
        cur_obj = self.browse(cr,uid,ids)[0]
        file_data=cur_obj.file
        val=base64.decodestring(file_data)
        fp = StringIO.StringIO()
        fp.write(val)    
        wb = xlrd.open_workbook(file_contents=fp.getvalue())
        final_result = ''
        date=cur_obj.date
        sheet=wb.sheet_by_index(0)
        date_dict = {}
    # Bio Metric Attendance
   
        """Code    Name
            P    PRESENT
            W    WEEKLY OFF
            L    PAID LEAVE
            A    ABSENT
            C    COMPANSATORY OFF
            SL    Sick Leave
            U    UNPAID LEAVE
            H    HOLIDAY
            WW    Worked on Weekly off
            WH    Worked on public holiday
            RH    Restricted holiday """

#         month = int(date[1:2])
#         year = int(date[6:10])

        year = int(date[:4])
        month = int(date[5:7])   
        dob_date = int(date[8:10])
        print'>>>>>>>>>>>>>>month,year',year,month
        total_days= monthrange(year, month)[1]
        for i in range(1,total_days+1):
            date_dict[i] = datetime.date(year,month,i)
        date_from = datetime.date(year,month, 1)
        date_to = datetime.date(year, month, total_days)
            
        #sheet.nrows
        for i in range(1,sheet.nrows):
            emp_code =sheet.row_values(i,0,sheet.ncols)[1]
        
            employee_id = employee_obj.search(cr,uid,[('identification_id1','=',emp_code)])
            print'<<<<<<<<<<<<<<<<<<<<<<',emp_code
            if employee_id:
                employee_id = employee_id[0]
                employee_dic = {
                                'employee_id' : employee_id,
                                'month_days'  : total_days,
                                'salary_days' : sheet.cell_value(i,total_days+16),
                                'attendance_days' : sheet.cell_value(i,total_days+5),
                                'holiday_attendance_days':0, #sheet.cell_value(i,total_days+5)
                                'date_from' : date_from,
                                'date_to' : date_to
                                }
                
                attendance_id = attendance_obj.search(cr, uid,[('employee_id','=',employee_id),('date_from','=',date_from),('date_to','=',date_to)])
                if not attendance_id:
                    attendance_id = attendance_obj.create(cr,uid,employee_dic)
                else:
                    attendance_id = attendance_id[0]
                d = 1
                #status_id = holiday_status_obj.search(cr, uid,[('name','=','Compensatory Days')])
                for j in sheet.row_values(i,5,monthrange(year, month)[1]+5):
                    j=j.upper()
                    print'<<<<<<<<<<<<<<',j
                    att_list = ['T','O','M','P', 'L','C', 'U','SU','SL','W','A','H','RH','']
                    if j not in att_list:
                        raise osv.except_osv(_('Warning!'), _('Please define Attendance from "%s but Employee Code %s Contain %s",') % (att_list, emp_code, j))
                    if j =='T' or j=='O' or j=='M' or j=='P':
                        final_result='P'
                    elif j=='L' or j=='C' :
                        final_result='PL'
                    elif j=='U':
                        final_result='UL'
                    elif j=='SU':
                        final_result='UL'
                    elif j =='SL':
                        final_result='PL'     
                    elif j=='W':
                        final_result='WO'
                    elif j=='A' or j=='':
                        final_result='A'
                    elif j=='H' or j == 'RH':
                        final_result='H'
                    
                    
#                     elif j=='WW' and status_id:
#                         final_result='P'
#                         holiday_id = holiday_obj.search(cr, uid,[('employee_id','=',employee_id),('leave_allocation_date','=',date_dict[d])])
#                         if not holiday_id:
#                             holiday_id = holiday_obj.create(cr, uid, {'name' : 'test','holiday_type' : 'employee',
#                                                       'leave_allocation_date' : date_dict[d],
#                                                       'holiday_status_id' : status_id[0],
#                                                       'employee_id' : employee_id,
#                                                       'number_of_days_temp' : 1})
#                     if j == 'C':
#                         holiday_obj.create(cr, uid, {'name' : 'test','holiday_type' : 'employee',
#                                                       'leave_allocation_date' : date_dict[d],
#                                                       'holiday_status_id' : status_id[0],
#                                                       'employee_id' : employee_id,
#                                                       'date_from' : False,
#                                                       'date_to' : False})
#                         
                   
                                       
                    att_line_id =attendance_line_obj.search(cr, uid, [('date', '=', date_dict[d]),
                                                         ('attendance_table','=',attendance_id)])
                    if att_line_id:
                        attendance_line_obj.write(cr, uid,att_line_id,{'employee_id': employee_id,
                          'date' : date_dict[d],'attendance_table':attendance_id,
                          'goa_drive_attendance':j,'final_result':final_result})
                    else:   
                        attendance_line_obj.create(cr,uid,{'employee_id': employee_id,
                          'date' : date_dict[d],'attendance_table':attendance_id,
                          'goa_drive_attendance':j,'final_result':final_result}) 
                     
                    d +=1
        #i+=1
        return True   


    
    def import_attendance_mumbai(self,cr,uid,ids,context=None):
        attendance_obj = self.pool.get('hr.attendance.table')
        attendance_line_obj = self.pool.get('hr.attendance.table.line')
        employee_obj = self.pool.get('hr.employee')
        import_obj = self.browse(cr,uid,ids)[0]
        file_data=import_obj.file
        val=base64.decodestring(file_data)
        fp = StringIO.StringIO()
        fp.write(val)    
        wb = xlrd.open_workbook(file_contents=fp.getvalue())
        sheet=wb.sheet_by_index(0)
        date_dict = {}
        date=import_obj.date
        year = int(date[:4])     
        month = int(date[5:7])
        total_days= monthrange(year, month)[1]
        for i in range(1,total_days+1):
            date_dict[i] = datetime.date(year,month,i)
        date_from = datetime.date(year,month, 1)
        date_to = datetime.date(year, month, total_days)
        row =0
        final_result=''
        while row < sheet.nrows:
            if sheet.cell_value(row,0) == 'Emp Code':
                emp_code = str(int(sheet.cell_value(row,2)))
                emp_code =emp_code[:len(emp_code)-11]
                emp_code = '0'* (4-len(str(int(emp_code)))) + str(int(emp_code))
                employee_id = employee_obj.search(cr,uid,[('identification_id1','=',emp_code)])
                if employee_id:
                    attendance_id = attendance_obj.create(cr,uid,{'employee_id': employee_id[0],'date_from' : date_from,'date_to' : date_to})
                    row +=5
                    for i in range(1,total_days+1):
                        
                        login_time = sheet.cell_value(row,5)
                        logout_time = sheet.cell_value(row,6)
                        print "row",row
                        status = sheet.cell_value(row,10)
                        if status=='P':
                            final_result='P'
                        elif status=='A' :
                            final_result ='A'
                            
                        att_line_id =attendance_line_obj.search(cr, uid, [('date', '=', date_dict[i]),
                                                      ('attendance_table','=',attendance_id)])
                        if att_line_id:
                            attendance_line_obj.write(cr, uid,att_line_id,{'final_result':final_result})
                        else:   
                            attendance_line_obj.create(cr,uid,{'employee_id': employee_id[0],
                                                   'date' : date_dict[i],'attendance_table':attendance_id,
                                                   'final_result':final_result,'login_time':login_time,'logout_time':logout_time}) 
                        row +=1
                            
                else:
                    row += total_days+5
            else:        
                row +=1
        return True
        
  



