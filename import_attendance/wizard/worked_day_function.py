def get_worked_day_lines(self, cr, uid, contract_ids, date_from, date_to, context=None):
       """
       @param contract_ids: list of contract id
       @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
       """
       print "testing"
       print "gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg"
       def was_on_leave(employee_id, datetime_day, context=None):
           res = False
           day = datetime_day.strftime("%Y-%m-%d")
           holiday_ids = self.pool.get('hr.holidays').search(cr, uid, [('state','=','validate'),('employee_id','=',employee_id),('type','=','remove'),('date_from','<=',day),('date_to','>=',day)])
           if holiday_ids:
               res = self.pool.get('hr.holidays').browse(cr, uid, holiday_ids, context=context)[0].holiday_status_id.name
           return res
       res = []
       print "here"
       for contract in self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context):
           loan_id = self.pool.get('hr.employee.loan').search(cr, uid,[('employee_id','=',contract.employee_id.id),('state','=','progress')])
           if loan_id:
               line_id = self.pool.get('hr.employee.loan.line').search(cr, uid,[('emi_date','>=',date_from),('emi_date','<=',date_to),('loan_id','=',loan_id[0])])
               if line_id :
                   loan_line_obj = self.pool.get('hr.employee.loan.line').browse(cr, uid,line_id[0])
                   self.pool.get('hr.contract').write(cr,uid,contract.id,{'emi_amount':loan_line_obj.emi_amount})
                   print "loan_line_obj.emi_amount",loan_line_obj.emi_amount
               else:
                   self.pool.get('hr.contract').write(cr,uid,contract.id,{'emi_amount': 0.0})
                   
           if not contract.working_hours:
               continue
           P = {
                    'name': _("Normal Working Days paid at 100%"),
                         'sequence': 1,
                         'code': 'WORK100',
                         'number_of_days': 0.0,
                         'number_of_hours': 0.0,
                         'contract_id': contract.id,
               }
           WO = {
                         'name': _("Weekly Offs"),
                         'sequence': 3,
                         'code': 'weekly',
                         'number_of_days': 0.0,
                         'number_of_hours': 0.0,
                         'contract_id': contract.id,
                     
                     }
           A = {
                      'name': _("Days Marked as Absent"),
                         'sequence': 4,
                         'code': 'absent',
                         'number_of_days': 0.0,
                         'number_of_hours': 0.0,
                         'contract_id': contract.id,
                    
                    }
           worked = {
                         'name': _("Goa-Days on the Ground"),
                         'sequence': 2,
                         'code': 'WORK200',
                         'number_of_days': 0.0,
                         'number_of_hours': 0.0,
                         'contract_id': contract.id,
                         }
               
               
           PL = {
                         'name': _("Paid Leaves taken"),
                         'sequence': 5,
                         'code': 'pl',
                         'number_of_days': 0.0,
                         'number_of_hours': 0.0,
                         'contract_id': contract.id,
                     
                     }
           UL = {
                        'name': _("Unpaid Leaves taken"),
                         'sequence': 6,
                         'code': 'Unpaid',
                         'number_of_days': 0.0,
                         'number_of_hours': 0.0,
                         'contract_id': contract.id,
                     }
           H = {
                    'name': _("Paid Holidays"),
                         'sequence': 7,
                         'code': 'paid_holiday',
                         'number_of_days': 0.0,
                         'number_of_hours': 0.0,
                         'contract_id': contract.id,
                    }
           HH = {
                      'name': _("Worked on a Paid Holiday"),
                         'sequence': 8,
                         'code': 'worked_paid_holiday',
                         'number_of_days': 0.0,
                         'number_of_hours': 0.0,
                         'contract_id': contract.id,
                     }
           att_records = {
                            'P' :P,
                            'A' :A,
                            'worked':worked,
                            'WO':WO,
                            'PL':PL,
                            'UL':UL,
                            'H':H,
                            'HH':HH
                              }
           day_from = datetime.datetime.strptime(date_from,"%Y-%m-%d")
           day_to = datetime.datetime.strptime(date_to,"%Y-%m-%d")
           print day_from, day_to, "uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu"
           nb_of_days = (day_to - day_from).days + 1
           attendance_line = self.pool.get('hr.attendance.table.line').search(cr, uid, [('employee_id','=',contract.employee_id.id),('date','>=',date_from),('date','<=',date_to)])
           print "attendance_line========",attendance_line,len(attendance_line)
           leaves = {}
           
           for day in range(0, nb_of_days):
             if  not contract.employee_id.attendance: 
               att_id = self.pool.get('hr.attendance.table.line').search(cr, uid, [('employee_id','=',contract.employee_id.id),('date','=',day_from +timedelta(days=day))])
               print att_id, "ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt"
               for att_obj in self.pool.get('hr.attendance.table.line').browse(cr,uid, att_id):
                   print att_obj.attendance, "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
#                    if att_obj.attendance == True:
#                        print "77777777777777777777777777777777777777"
#                        worked['number_of_days'] += 1.0
#                        worked['number_of_hours'] += 8.0
                   print att_obj.final_result, "#################################################"
                   print att_records, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                   if att_obj.final_result in att_records:
                       att_records[att_obj.final_result]['number_of_days'] += 1.0
                       att_records[att_obj.final_result]['number_of_hours'] += 8.0
                   else:
                       att_records[att_obj.final_result] = {
                                                               'name': att_obj.final_result,
                                                               'sequence': 10,
                                                               'code': att_obj.final_result,
                                                               'number_of_days': 1.0,
                                                               'number_of_hours': 8.0,
                                                               'contract_id': contract.id,
                                                            }  
             else:
                working_hours_on_day = self.pool.get('resource.calendar').working_hours_on_day(cr, uid, contract.working_hours, day_from + timedelta(days=day), context)
                if working_hours_on_day:
                    #the employee had to work
                    leave_type = was_on_leave(contract.employee_id.id, day_from + timedelta(days=day), context=context)
                    if leave_type:
                        #if he was on leave, fill the leaves dict
                        if leave_type in leaves:
                            leaves[leave_type]['number_of_days'] += 1.0
                            leaves[leave_type]['number_of_hours'] += working_hours_on_day
                        else:
                            leaves[leave_type] = {
                                'name': leave_type,
                                'sequence': 5,
                                'code': leave_type,
                                'number_of_days': 1.0,
                                'number_of_hours': working_hours_on_day,
                                'contract_id': contract.id,
                            }
                    else:
                        #add the input vals to tmp (increment if existing)
                        att_records['P']['number_of_days'] += 1.0
                        att_records['P']['number_of_hours'] += working_hours_on_day          
           leaves = [value for key,value in leaves.items()]            
           monthdays = {
                     'name': _("Days in the Month"),
                     'sequence': 100,
                     'code': 'MONTHDAYS',
                     'number_of_days': calendar.monthrange(day_from.year, day_from.month)[1],
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                        } 
           att_records['MONTHDAYS']=monthdays
           salarydays = {
                         'name': _("Salary Days in the Month"),
                                     'sequence': 100,
                                     'code': 'SALARYDAYS',
                                     'number_of_days': nb_of_days,
                                     'number_of_hours': 0.0,
                                     'contract_id': contract.id,
                         }
           
            
           if  contract.employee_id.leave_allocation_type == 'goa':
               
               l = [salarydays,att_records['MONTHDAYS'], att_records['P'], att_records['worked'], att_records['A'], att_records['PL'], att_records['WO'], att_records['UL'], att_records['H'], att_records['HH'],]            
           else:
               
               l = [salarydays,att_records['MONTHDAYS'], att_records['P'], att_records['worked'], att_records['A'], att_records['PL'], att_records['WO'], att_records['UL'], att_records['H'], att_records['HH'],] 
                
                #l = [salarydays,att_records['MONTHDAYS'], att_records['P'],  att_records['A'], att_records['PL'],  att_records['UL'],]  
       return l         