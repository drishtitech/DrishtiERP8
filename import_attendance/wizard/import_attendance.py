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
    
    
    def import_attendance1(self,cr,uid,ids,context=None):
 
        cur_obj = self.browse(cr,uid,ids)[0]
        file_data=cur_obj.file
        val=base64.decodestring(file_data)
        fp = StringIO.StringIO()
        fp.write(val)     
        wb = xlrd.open_workbook(file_contents=fp.getvalue())
        sheet=wb.sheet_by_index(0)
        date_dict = {}
        if cur_obj.location == '1':
            date_from1 = sheet.row_values(0,0,sheet.ncols)[3] 
            print "date_from1",date_from1
            from_date = int(date_from1[:2])
            month = int(date_from1[3:5])
            year = int(date_from1[6:10])
            date_from = datetime.date(year, month, 1)
            date_to = datetime.date(year, month, calendar.monthrange(year, month)[1])
            i = 0
            for p in range(1,calendar.monthrange(year, month)[1]+1):
                date_dict[p] = datetime.date(year,month ,p)
            while i < sheet.nrows:
                emp_code1 =sheet.row_values(i,0,sheet.ncols)[0]
                emp_name =sheet.row_values(i,0,sheet.ncols)[1]
                emp_code = '0'* (4-len(str(int(emp_code1)))) + str(int(emp_code1))
                employee_id = self.pool.get('hr.employee').search(cr,uid,[('identification_id','=',emp_code)])
            if not employee_id:
                i += calendar.monthrange(year, month)[1]
            else:
                employee_id = employee_id[0]
                emp_obj =   self.pool.get('hr.employee').browse(cr,uid,employee_id) 
                attendance_id = self.pool.get('hr.attendance.table').create(cr,uid,{'employee_id': employee_id,'date_from' : date_from,'date_to' : date_to})
                contract_ids = self.pool.get('hr.payslip').get_contract( cr, uid, emp_obj, date_from, date_to, context=None)
                if not contract_ids:
                        raise osv.except_osv(('Warning !'),_('The Contract does not exist!'))
                         
                contract_obj = self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context) and self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context)[0] or False 
                   
                for d in range(1,calendar.monthrange(year, month)[1]+1):
                    j = sheet.row_values(i,0,sheet.ncols)[7]
                    absent_info = ''
                    final_result = ''
                    if contract_obj:
                        search_for_weekly_off = self.pool.get('resource.calendar').working_hours_on_day(cr, uid, contract_obj.working_hours, date_dict[d], context)
                        search_for_even_saturday = self.pool.get('leaves.calendar').search(cr, uid, [('holiday_id','=',contract_obj.holidays_id.id),('date_from','=',date_dict[d]),('type','=','even_sat')])
                        search_for_holiday=self.pool.get('leaves.calendar').search(cr, uid, [('holiday_id','=',contract_obj.holidays_id.id),('date_from','=',date_dict[d]),('type','<>','even_sat')])
                        search_for_leave=self.pool.get('hr.holidays').search(cr, uid, [('employee_id','=',employee_id),('state','=','validate'),('type','=','remove'),('date_from','<=',date_dict[d].strftime('%Y-%m-%d')),('date_to','>=',date_dict[d].strftime('%Y-%m-%d'))])
                        if search_for_even_saturday:
                            search_for_weekly_off = 0.0
                        if search_for_leave:  
                                    absent_info = self.pool.get('hr.holidays').browse(cr, uid, search_for_leave, context=context)[0].holiday_status_id.payroll_code.name or self.pool.get('hr.holidays').browse(cr, uid, search_for_leave, context=context)[0].holiday_status_id.name
                                    if  absent_info == "Unpaid":
                                        absent_info = 'UL'
                                    else:
                                        absent_info = 'PL'
                        elif search_for_holiday:
                                absent_info = 'H'
                        elif not search_for_weekly_off:
                            absent_info = 'WO'
                    if absent_info:
                        if j== 'P' and absent_info=='H': #and attendance_status==True:
                            final_result = 'HH'                
                        else:
                                final_result = absent_info       
                    else:
                        if j== 'P':        
                                    final_result ='P'
                        else:
                                    final_result ='A'  
                    if j == 'P':
                        attendance_line_id = self.pool.get('hr.attendance.table.line').create(cr,uid,{'employee_id': employee_id,
                                'date' : date_dict[d],'attendance_table':attendance_id,
                                'attendance':True,'absent_info':absent_info,'final_result':final_result})
                    else:
                        attendance_line_id = self.pool.get('hr.attendance.table.line').create(cr,uid,{'employee_id': employee_id,
                                'date' : date_dict[d],'attendance_table':attendance_id,
                                'absent_info':absent_info,'final_result':final_result})   
                    i += 1
                         
        else:
                 
            date_from1 = sheet.row_values(5,0,sheet.ncols)[6] 
            date_to1 = sheet.row_values(5,0,sheet.ncols)[13] 
            from_date = 1 #int(date_from1[:2])
            month = 7 #int(date_from1[3:5])
            year = 2013 #int(date_from1[6:10])
            to_date = int(date_to1[:2])
              
            #last_date = monthrange(int(cur_obj.year), int(cur_obj.month))[1]
            #print "date123",date_from1,date_to1,int(cur_obj.year), int(cur_obj.month)
            #print "monthrange(int(cur_obj.year), int(cur_obj.month))",monthrange(int(cur_obj.year), int(cur_obj.month))
             
             
            for i in range(1,to_date+1):
                     
                date_dict[i] = datetime.date(year,month ,i)
            print "date_dict",date_dict       
            date_from = datetime.date(year, month, 1)
            date_to = datetime.date(year, month, to_date)
              
            #sheet.nrows
            for i in range(9,sheet.nrows):
                emp_code =sheet.row_values(i,0,sheet.ncols)[0]
                emp_name =sheet.row_values(i,0,sheet.ncols)[1]
                employee_id = self.pool.get('hr.employee').search(cr,uid,[('identification_id','=',emp_code)])
                if employee_id:
                    #employee_id = self.pool.get('hr.employee').create(cr,uid,{'identification_id': emp_code,'name':emp_name})
                    employee_id = employee_id[0]
                    emp_obj =   self.pool.get('hr.employee').browse(cr,uid,employee_id)
                    print emp_obj.id, "Employeeeeeeeeeeeee objjjjjjjjjjj" 
                      
                    attendance_id = self.pool.get('hr.attendance.table').create(cr,uid,{'employee_id': employee_id,'date_from' : date_from,'date_to' : date_to})
                    d =1
     
     ## end of code for emp. import
                 
                #Add Computation Attendance Code
                 
         
                    contract_ids = self.pool.get('hr.payslip').get_contract( cr, uid, emp_obj, date_from, date_to, context=None)
                    print contract_ids, "CONTRACT IDSSSSSSSSSSSS",emp_name,emp_code
                if  contract_ids:
                   # raise osv.except_osv(('Warning !'),_('The Contract does not exist!'))
#                     contract_id = self.pool.get('hr.contract').create(cr,uid,{'employee_id': employee_id,
#                                                                            'name':emp_name,
#                                                                            'wage':20000,
#                                                                            'struct_id': 1,
#                                                                            'working_hours': 1,
#                                                                             'date_start':date_from,
#                                                                             'holidays_id': 1    })
                    #contract_ids = [contract_id]
                    contract_obj = self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context) and self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context)[0] or False
                      
                    for j in sheet.row_values(i,2,monthrange(year, month)[1]+2):
                        absent_info = ''
                    final_result = ''
                    if contract_obj:
                        search_for_weekly_off = self.pool.get('resource.calendar').working_hours_on_day(cr, uid, contract_obj.working_hours, date_dict[d], context)
                          
                        search_for_even_saturday = self.pool.get('leaves.calendar').search(cr, uid, [('holiday_id','=',contract_obj.holidays_id.id),('date_from','=',date_dict[d]),('type','=','even_sat')])
                        search_for_holiday=self.pool.get('leaves.calendar').search(cr, uid, [('holiday_id','=',contract_obj.holidays_id.id),('date_from','=',date_dict[d]),('type','<>','even_sat')])
                        search_for_leave=self.pool.get('hr.holidays').search(cr, uid, [('employee_id','=',employee_id),('state','=','validate'),('type','=','remove'),('date_from','<=',date_dict[d].strftime('%Y-%m-%d')),('date_to','>=',date_dict[d].strftime('%Y-%m-%d'))])
                        #print search_for_leave, "SEARCHING FOR LEAVE"
                        #print "date_dict[d].strftime('%Y-%m-%d')",date_dict[d].strftime('%Y-%m-%d'),search_for_leave 
                        if search_for_even_saturday:
                            search_for_weekly_off = 0.0
                        print "date_dict[d]",date_dict[d],search_for_weekly_off,search_for_holiday,search_for_leave,search_for_even_saturday
                        if search_for_leave:  
                                absent_info = self.pool.get('hr.holidays').browse(cr, uid, search_for_leave, context=context)[0].holiday_status_id.payroll_code.name or self.pool.get('hr.holidays').browse(cr, uid, search_for_leave, context=context)[0].holiday_status_id.name
                                print absent_info, "ABSENT INFO"
                                if  absent_info == "Unpaid":
                                    absent_info = 'UL'
                                else:
                                    absent_info = 'PL'
                        elif search_for_holiday:
                                absent_info = 'H'
#                         elif not search_for_weekly_off:
#                             absent_info = 'WO'
                                  
                             
                    if absent_info:
                        if j== 'PP' and absent_info=='H': #and attendance_status==True:
                            final_result = 'HH'   
                        elif  j== 'PP' and absent_info == 'WO':
                            final_result = 'HH'         
                                      
                        else:
                            final_result = absent_info       
                    else:
                        if j== 'PP':        
                                final_result ='P'
                        else:
                                final_result ='A'  
                    if j == 'PP':
                        attendance_line_id = self.pool.get('hr.attendance.table.line').create(cr,uid,{'employee_id': employee_id,
                            'date' : date_dict[d],'attendance_table':attendance_id,
                            'attendance':True,'absent_info':absent_info,'final_result':final_result})
                    else:
                        attendance_line_id = self.pool.get('hr.attendance.table.line').create(cr,uid,{'employee_id': employee_id,
                              'date' : date_dict[d],'attendance_table':attendance_id,
                              'absent_info':absent_info,'final_result':final_result})
           
                    d +=1
                    
        return True
     
         
    


    def import_attendance(self,cr, uid, ids, context=None):
        attendance_obj = self.pool.get('hr.attendance.table')
        attendance_line_obj = self.pool.get('hr.attendance.table.line')
        employee_obj = self.pool.get('hr.employee')
        cur_obj = self.browse(cr,uid,ids)[0]
        file_data=cur_obj.file
        val=base64.decodestring(file_data)
        fp = StringIO.StringIO()
        fp.write(val)    
        
        wb = xlrd.open_workbook(file_contents=fp.getvalue())
        
   #* for i in range(0,6):

        final_result = ''
        date=cur_obj.date
        #for i in range(0):  
        sheet=wb.sheet_by_index(0)
        date_dict = {}
    # Bio Metric Attendance
   
   
        print'>>>>>>>>>>',date
        
        from time import strftime
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
                attendance_id = attendance_obj.search(cr, uid,[('employee_id','=',employee_id),('date_from','=',date_from),('date_to','=',date_to)])
                if not attendance_id:
                    attendance_id = attendance_obj.create(cr,uid,{'employee_id': employee_id,'date_from' : date_from,'date_to' : date_to})
                else:
                    attendance_id = attendance_id[0]
                d = 1
                for j in sheet.row_values(i,3,monthrange(year, month)[1]+3):
                    j=j.upper()
                    print'<<<<<<<<<<<<<<',j
                    
                    if j =='T' or j=='O' or j=='M' or j=='P':
                        final_result='P'
                    elif j=='L' or j=='C' :
                        final_result='PL'
                    elif j=='U':
                        final_result='UL'
                    elif j=='SL':
                        if 'SL'>= 3:
                            final_result='UL'
                    elif j=='W':
                        final_result='WO'
                    elif j=='A' or j=='':
                        final_result='A'
                    elif j=='H':
                        final_result='H' 
                   
                                       
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
        
  



