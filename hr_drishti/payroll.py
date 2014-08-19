from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
from datetime import date
from datetime import timedelta
import calendar
import time

class hr_payslip(osv.osv):

    _inherit = 'hr.payslip'
    
    
    def compute_sheet(self, cr, uid, ids, context=None):
        slip_line_pool = self.pool.get('hr.payslip.line')
        sequence_obj = self.pool.get('ir.sequence')
        for payslip in self.browse(cr, uid, ids, context=context):
            
            
            loan_id = self.pool.get('hr.employee.loan').search(cr, uid,[('employee_id','=',payslip.employee_id.id),('state','=','progress')])
            if loan_id:
                line_id = self.pool.get('hr.employee.loan.line').search(cr, uid,[('emi_date','>=',payslip.date_from),('emi_date','<=',payslip.date_to),('loan_id','=',loan_id[0])])
                print "line_id",line_id
                if line_id :
                    self.pool.get('hr.employee.loan.line').write(cr, uid,line_id[0],{'payslip_id' :payslip.id }) 
                   
                      
            number = payslip.number or sequence_obj.get(cr, uid, 'salary.slip')
            #delete old payslip lines
            old_slipline_ids = slip_line_pool.search(cr, uid, [('slip_id', '=', payslip.id)], context=context)
#            old_slipline_ids
            if old_slipline_ids:
                slip_line_pool.unlink(cr, uid, old_slipline_ids, context=context)
            if payslip.contract_id:
                #set the list of contract for which the rules have to be applied
                contract_ids = [payslip.contract_id.id]
            else:
                #if we don't give the contract, then the rules to apply should be for all current contracts of the employee
                contract_ids = self.get_contract(cr, uid, payslip.employee_id, payslip.date_from, payslip.date_to, context=context)
            lines = [(0,0,line) for line in self.pool.get('hr.payslip').get_payslip_lines(cr, uid, contract_ids, payslip.id, context=context)]
            self.write(cr, uid, [payslip.id], {'line_ids': lines, 'number': number,}, context=context)
#             input_id=self.pool.get('hr.payslip.input').search(cr,uid,[('payslip_id','=',payslip.id),('code','=','OT')])
#             self.pool.get('hr.payslip.input').write(cr,uid,input_id,{'amount':payslip.contract_id.over_time_allowence})
#             
        return True
    
    
    

    def get_worked_day_lines(self, cr, uid, contract_ids, date_from, date_to, context=None):
        """
        @param contract_ids: list of contract id
        @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
        """
        loan_obj = self.pool.get('hr.employee.loan')
        loan_line_obj = self.pool.get('hr.employee.loan')
        dedtn_obj = self.pool.get('employee.deduction')
        dedtn_line_obj = self.pool.get('employee.deduction.line')
        def was_on_leave(employee_id, datetime_day, context=None):
            res = False
            day = datetime_day.strftime("%Y-%m-%d")
            holiday_ids = self.pool.get('hr.holidays').search(cr, uid, [('state','=','validate'),('employee_id','=',employee_id),('type','=','remove'),('date_from','<=',day),('date_to','>=',day)])
            if holiday_ids:
                res = self.pool.get('hr.holidays').browse(cr, uid, holiday_ids, context=context)[0].holiday_status_id.name
            return res
        res = []
      #  print "here",contract_ids
        for contract in self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context):
            print "test",contract.employee_id.identification_id1
            contract_dict = {
                             'emi_amount': 0.0,
                             'mobile_deduction' : 0.0,
                             'emi_amount' : 0.0,
                             'tds_deduction' : 0.0,
                             'arrers' :0.0,
                             }
            loan_id = loan_obj.search(cr, uid,[('employee_id','=',contract.employee_id.id),('state','=','progress')])
            
            if loan_id:
                line_id = loan_line_obj.search(cr, uid,[('emi_date','>=',date_from),('emi_date','<=',date_to),('loan_id','=',loan_id[0])])
                if line_id :
                    loan_line_obj = loan_line_obj.browse(cr, uid,line_id[0])
                    contract_dict['emi_amount'] = loan_line_obj.emi_amount
                    
            deduction_id = dedtn_obj.search(cr, uid,[('deduction_from_date','>=',date_from),('deduction_to_date','<=',date_to)])       
            if deduction_id:
                print "deduction_id",deduction_id,contract.employee_id.id
                dedtn_line_id = dedtn_line_obj.search(cr, uid, [('deduction_id','=',deduction_id[0]),('employee_id','=',contract.employee_id.id)])
                if  dedtn_line_id:
                    dedtn_line_obj = dedtn_line_obj.browse(cr, uid, dedtn_line_id[0])
                    contract_dict['mobile_deduction'] =  dedtn_line_obj.mobile_deduction
                    contract_dict['emi_amount'] =  dedtn_line_obj.loan_deduction
                    contract_dict['tds_deduction'] =  dedtn_line_obj.tds_deduction
                    contract_dict['arrers'] =  dedtn_line_obj.arrers             
                         
              
            self.pool.get('hr.contract').write(cr,uid,contract.id,contract_dict)    
                    
#             if not contract.working_hours:
#                 continue
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
            #print day_from, day_to, "uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu"
            nb_of_days = (day_to - day_from).days + 1
           
            attendance_line = self.pool.get('hr.attendance.table.line').search(cr, uid, [('employee_id','=',contract.employee_id.id),('date','>=',date_from),('date','<=',date_to)])
            #print "attendance_line========",attendance_line,len(attendance_line)
            leaves = {}
           
            for day in range(0, nb_of_days):
                if not contract.employee_id.attendance: 
                    att_id = self.pool.get('hr.attendance.table.line').search(cr, uid, [('employee_id','=',contract.employee_id.id),('date','=',day_from +timedelta(days=day))])
                    #print att_id, "ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt"
                    for att_obj in self.pool.get('hr.attendance.table.line').browse(cr,uid, att_id):
                       
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
                     'number_of_days':    calendar.monthrange(day_from.year, day_from.month)[1],
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
           
            emp_attend_id = self.pool.get('hr.attendance.table').search(cr, uid, [('employee_id','=',contract.employee_id.id),('date_from','=',date_from),('date_to','=',date_to)])
            work_days  = []
            #print "emp_attend_id",emp_attend_id
            if emp_attend_id:
                att_obj = self.pool.get('hr.attendance.table').browse(cr, uid,emp_attend_id[0])
                work_days.append( {
                         'name': _("Days in the Month"),
                         'sequence': 100,
                         'code': 'MONTHDAYS',
                         'number_of_days':    att_obj.month_days,
                         'number_of_hours': 0.0,
                         'contract_id': contract.id,
                            })
                work_days.append( {
                             'name': _("Salary Days in the Month"),
                                         'sequence': 100,
                                         'code': 'SALARYDAYS',
                                         'number_of_days': att_obj.salary_days,
                                         'number_of_hours': att_obj.overtime,
                                         'contract_id': contract.id,
                             })  
                work_days.append( {
                             'name': _("Goa-Days on the Ground"),
                             'sequence': 2,
                             'code': 'WORK200',
                             'number_of_days': att_obj.attendance_days,
                             'number_of_hours': 0.0,
                             'contract_id': contract.id,
                             } )
                work_days.append(
                                    {
                                  'name': _("Worked on a Paid Holiday"),
                                     'sequence': 8,
                                     'code': 'worked_paid_holiday',
                                     'number_of_days': att_obj.holiday_attendance_days,
                                     'number_of_hours': 0.0,
                                     'contract_id': contract.id,
                                 }
                                             
                                     )
                   
                l = work_days
            if not emp_attend_id and contract.employee_id.leave_allocation_type == 'goa':
               
                l = [salarydays,att_records['MONTHDAYS'], att_records['P'], att_records['worked'], att_records['A'], att_records['PL'], att_records['WO'], att_records['UL'], att_records['H'], att_records['HH'],]            
            elif not emp_attend_id:
               
                l = [salarydays,att_records['MONTHDAYS'], att_records['P'], att_records['worked'], att_records['A'], att_records['PL'], att_records['WO'], att_records['UL'], att_records['H'], att_records['HH'],] 
                
                #l = [salarydays,att_records['MONTHDAYS'], att_records['P'],  att_records['A'], att_records['PL'],  att_records['UL'],]  
       # print "work_days",l
        return l         
    
