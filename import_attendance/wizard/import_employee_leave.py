from openerp.osv import fields, osv
#from tools.translate import _
import StringIO
import cStringIO
import base64
import xlrd
import string
import calendar
import datetime
from calendar import monthrange

class attendance_import(osv.osv_memory):
    _inherit='attendance.import'
    
    def import_leave(self,cr,uid,ids,context=None):

        cur_obj = self.browse(cr,uid,ids)[0]
        file_data=cur_obj.file
        val=base64.decodestring(file_data)
        fp = StringIO.StringIO()
        fp.write(val)     
        wb = xlrd.open_workbook(file_contents=fp.getvalue())
        sheet=wb.sheet_by_index(1)
        #sheet1=wb.sheet_by_index(1)
        date_dict = {}
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
               date_dict[i] = datetime.datetime(year,month ,i,0,0,0)
               
        print "date_dict",date_dict       
        date_from = datetime.date(year, month, 1)
        date_to = datetime.date(year, month, to_date)
         
        #sheet.nrows
        for i in range(9,sheet.nrows):
           emp_code =sheet.row_values(i,0,sheet.ncols)[0]
           emp_name =sheet.row_values(i,0,sheet.ncols)[1]
           employee_id = self.pool.get('hr.employee').search(cr,uid,[('identification_id','=',emp_code)])
           if  employee_id:  
            employee_id = employee_id[0]
            #attendance_id = self.pool.get('hr.attendance.table').create(cr,uid,{'employee_id': employee_id,'date_from' : date_from,'date_to' : date_to})
            d =1
            holiday_list = []
            attendance_id = self.pool.get('hr.attendance.table').search(cr,uid,
                                                                        [('employee_id','=', employee_id),
                                                                         ('date_from','=', date_from),
                                                                         ('date_to','=',date_to )])
            print "emp_code",emp_code,emp_name
            for j in sheet.row_values(i,3,monthrange(year, month)[1]+2):
                print "date_dict[d]",date_dict[d]
                
                if j:
                  status_id  = self.pool.get('hr.holidays.status').search(cr, uid, [('leave_code','=',j)]) 
                  print status_id,"status_id"
                  if status_id:
                      holiday_ids = self.pool.get('hr.holidays').search(cr,uid,[('employee_id','=',employee_id),
                                                                  ('date_to','=',(date_dict[d]-datetime.timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')),
                                                                  ('holiday_status_id','=',status_id[0])])
                      print "holiday_ids",holiday_ids,date_dict[d],date_dict[d]+ datetime.timedelta(seconds=3600*24-1),emp_name
                      if holiday_ids:
                          leave_obj = self.pool.get('hr.holidays').browse(cr, uid, holiday_ids[0])
                          days = leave_obj.number_of_days_temp
                          
                          self.pool.get('hr.holidays').write(cr, uid, holiday_ids,{'date_to':date_dict[d]+ datetime.timedelta(seconds=3600*24-1),
                                                                                    'number_of_days_temp' : days +1},)
                                                                 
                      else:    
                          
                          dic = {
                                 'employee_id': employee_id,
                                 'date_from': date_dict[d],
                                 'date_to': date_dict[d]+ datetime.timedelta(seconds=3600*24-1)  ,
                                 'holiday_status_id': status_id[0],
                                 'number_of_days_temp' :1
                                 }
                          
                          holiday_id = self.pool.get('hr.holidays').create(cr, uid, dic)
                          print "holiday_id",holiday_id
                          holiday_list.append(holiday_id)
                      print "j",j    
                  if attendance_id:
                         att_line_id = self.pool.get('hr.attendance.table.line').search(cr ,uid,
                                                                              [('attendance_table','=',attendance_id[0]),
                                                                               ('date','=', date_dict[d])])
                         print "j",j    
                         dic = {}
                         if j == 'L': 
                             dic ={
                                   'absent_info':'L',
                                   'final_result':'PL' ,
                                   }
                         elif j == 'UL':
                             dic ={
                                   'absent_info':'UL',
                                   'final_result':'UL' ,
                                   }
                         elif j == 'OL':
                             dic ={
                                   'absent_info':'Work at other Location',
                                   'final_result':'P' ,
                                   }
                         elif j == 'CO':
                             dic ={
                                   'absent_info':'Compensatory Off',
                                   'final_result':'PL' ,
                                   }
                         elif j == 'MA':
                             dic ={
                                   'absent_info':'Mobile Attendance',
                                   'final_result':'P' ,
                                   }
                         elif j == 'WO':
                             line_obj = self.pool.get('hr.attendance.table.line').browse(cr, uid, att_line_id[0])
                             
                             dic ={
                                   'absent_info':'WO',
                                   'final_result':'WO' ,
                                   }
                             
                             if line_obj.attendance:
                                 dic['final_result'] = 'HH'
                                      
                         self.pool.get('hr.attendance.table.line').write(cr, uid, att_line_id, dic )
                             
                d += 1          
            self.pool.get('hr.holidays').holidays_validate(cr, uid, holiday_list)
            
            
                
            
                          
                          
                          
            

    