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
        sheet=wb.sheet_by_index(0)
        date_dict = {}
        # Bio Metric Attendance
        for i in range(1,28+1):
            date_dict[i] = datetime.date(2014,2 ,i)
        date_from = datetime.date(2014, 2, 1)
        date_to = datetime.date(2014, 2, 28)
            
        #sheet.nrows
        for i in range(2,sheet.nrows):
            emp_code =sheet.row_values(i,0,sheet.ncols)[1]
           
            employee_id = employee_obj.search(cr,uid,[('identification_id','=',emp_code)])
            if employee_id:
                employee_id = employee_id[0]
                attendance_id = attendance_obj.search(cr, uid,[('employee_id','=',employee_id),('date_from','=',date_from),('date_to','=',date_to)])
                if not attendance_id:
                    attendance_id = attendance_obj.create(cr,uid,{'employee_id': employee_id,'date_from' : date_from,'date_to' : date_to})
                else:
                    attendance_id = attendance_id[0]
                d = 1
                for j in sheet.row_values(i,5,monthrange(2014, 2)[1]+5):
                    att_line_id =attendance_line_obj.search(cr, uid, [('date', '=', date_dict[d]),
                                                         ('attendance_table','=',attendance_id)])
                    if att_line_id:
                        attendance_line_obj.write(cr, uid,att_line_id,{'employee_id': employee_id,
                          'date' : date_dict[d],'attendance_table':attendance_id,
                          'attendance':True,'absent_info':j,})
                    else:   
                        attendance_line_obj.create(cr,uid,{'employee_id': employee_id,
                          'date' : date_dict[d],'attendance_table':attendance_id,
                          'attendance':True,'absent_info':j,}) 
                    d +=1
        return True    
