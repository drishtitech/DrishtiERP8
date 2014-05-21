from openerp.osv import fields, osv
from openerp.tools.translate import _

import datetime
from datetime import date
from datetime import timedelta
import calendar
import time

class leaves_calendar(osv.osv):
    _name = "leaves.calendar"
    _description = "Public Holidays"
    _columns = {
        'holiday_id':fields.many2one('holidays.calendar','Holidays Number', size=124),        
        'name': fields.char('Holiday Name', size=124, required=True),
        #'employee_id':fields.many2one('hr.employee','Employee', size=124),
        #'leave': fields.char('Holiday Name', size=124, required=True),
        'date_from': fields.date('Date', size=124),
        #'day': fields.selection([('monday', 'Monday'),('tuesday', 'Tuesday'),('wednesday', 'Wednesday'),('thursday', 'Thursday'),('friday', 'Friday'),('saturday', 'Saturday'),('sunday', 'Sunday')],'Type'),
        'day': fields.selection([('0','Monday'),('1','Tuesday'),('2','Wednesday'),('3','Thursday'),('4','Friday'),('5','Saturday'),('6','Sunday')], 'Day of Week'),
        'description': fields.text('Description', size=124),
        'type':fields.selection([('even_sat', 'Even Saturday')],'Type'),
        #'date_to': fields.date('End Date', size=124),
        #'calendar_line':fields.one2many('holiday.details','holiday_id'," ", size=124),
        #'location':fields.selection([('Mumbai', 'Mumbai'),('Goa','Goa')],'Location'),
        }
    
    def onchange_date(self,cr,uid,ids,date_from):
        if date_from:
            from_dt = datetime.datetime.strptime(date_from, "%Y-%m-%d")
            a=from_dt.weekday()
            return {'value' : {'day':str(a)}}
        return {'value' : {'day':False}}
    
    
leaves_calendar()

class holidays_calendar(osv.osv):
    _name = "holidays.calendar"
    _description = "Holidays Calendar"
    _columns = {
        #'holiday_id': fields.many2one('leaves.calendar','Holidays ID', size=124),
        'name': fields.char('Holidays Calendar Name', size=124, required=True),
        'location':fields.selection([('Mumbai', 'Mumbai'),('Goa','Goa')],'Location'),
        'holidays_line':fields.one2many('leaves.calendar','holiday_id'," ", size=124),
        #'leave': fields.char('Holiday Name', size=124, required=True),
#         'degree':fields.char('Degree', size=124),
#         'institute':fields.char('Institute', size=124),
#         'board': fields.char('University/Board', size=124),
#         'marks': fields.char('% Marks', size=124),
#         'year': fields.char('Year of Completion', size=124),
 
        }
 
holidays_calendar()


class hr_holidays_payroll_code(osv.osv):
    _name = "hr.holidays.payroll.code"
    _columns = {
		'name' : fields.char('Code'),
		'description' : fields.char('Description'),
}

class hr_holidays_status(osv.osv):
    _inherit = "hr.holidays.status"
    _columns = {
		'payroll_code' : fields.many2one('hr.holidays.payroll.code','Payroll Code'), 
        'leave_code' : fields.char('Leave Code', size=4),
}
    
class hr_contract(osv.osv):
    _inherit = "hr.contract"
    _description = 'Employee Contract'
    _columns = {
		'holidays_id' : fields.many2one('holidays.calendar','Holidays Calendar', size=124),
        'nutritional_allowance' : fields.integer('Nutritional Allowance', size=124),
        'attendance_incentive' : fields.integer('A.I. All', size=124),
        'da_lta_fa' : fields.integer('DA/LTA/FA', size=124),
        'special_allowance' : fields.integer('Special Allowance', size=124),
        'hra' : fields.integer('House Rent Allowance', size=124),
        'emi_amount': fields.integer('Loan EMI', size=124),
        'bonus_amount': fields.float('Bonus Amount', size=124),
        'current_date':fields.date('Current date'),
        #'date_start':fields.date('Start Date')
        'driver_salary':fields.boolean('Driver Salary'),
        'house_rent_allowance_metro_nonmetro':fields.float('House Rent Allowance(%)'),
        'supplementary_allowance':fields.float(' Supplementary Allowance '),
        'tds':fields.float('TDS'),
        'voluntary_provident_fund':fields.float('Voluntary Provident Fund (%)'),
        'medical_insurance':fields.float('Medical Insurance'),
        'over_time_allowence':fields.integer('Over Time',size=124)
        }
     
    _defaults = {
        'current_date': lambda *a: time.strftime("%Y-%m-%d")
     }
        
#     def onchange_emp(self, cr, uid, ids, employee_id, context=None):
#         if employee_id:
#             emp_id = self.pool.get('hr.employee').browse(cr, uid, employee_id, context)
#             function=emp_id.job_id.id
#         return {'value':{'job_id':function}} 
#     
    
    def default_get(self, cr, uid, fields, context=None):
        res = super(hr_contract, self).default_get(cr, uid, fields, context=context)
        if context.get('active_id'):
            obj = self.browse(cr, uid, int(context['active_id']), context=context)
            
            #a=str(obj.date_end)
            #date_start=str(obj.date_start)
            current_date=datetime.datetime.strptime(obj.current_date,'%Y-%m-%d')
            #a=datetime.datetime.strptime(str(obj.date_end),'%Y-%m-%d')
            #a=datetime.datetime.strptime(str(obj.date_end),'%Y-%m-%d').date()
            previous_date=current_date + datetime.timedelta(days = -1)
            print ">>>>>>>>>",previous_date,current_date, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            res.update({'name' : obj.name,'employee_id':obj.employee_id.id,'date_start':obj.current_date,'visa_expire' : obj.visa_expire,'permit_no':obj.permit_no,'visa_no':obj.visa_no,'house_rent_allowance_metro_nonmetro':obj.house_rent_allowance_metro_nonmetro,'supplementary_allowance':obj.supplementary_allowance,'tds':obj.tds,'voluntary_provident_fund':obj.voluntary_provident_fund,'medical_insurance':obj.medical_insurance,'advantages':obj.advantages,'notes':obj.notes,'nutritional_allowance':obj.nutritional_allowance,'attendance_incentive':obj.attendance_incentive,'da_lta_fa':obj.da_lta_fa,'special_allowance':obj.special_allowance,'bonus_amount':obj.bonus_amount,'hra':obj.hra,'schedule_pay':obj.schedule_pay,'struct_id':obj.struct_id.id,'working_hours':obj.working_hours.id, 'job_id':obj.job_id.id
                    })
            self.write(cr, uid, obj.id, {'date_end':str(previous_date)})
        return res
    
#     _defaults = {
#          
#         'date_end': lambda *a: datetime.date.today().strftime('%Y-%m-%d')
#         
#        }
    
    def new_contract(self,cr,uid,vals,context={}):
        
        res = {
                    
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'hr.contract',
                    'target':'current',
                    'nodestroy': True,
                    'type': 'ir.actions.act_window',
                    'name' : 'New Contract',
                    
                    }
        
        return res
    
    
hr_contract()


class hr_attendance_table(osv.osv):
    _name='hr.attendance.table'
    _description = 'Attendance Table'
    _columns = {
        'date_from':fields.date('Date From',required=True),
        'date_to':fields.date('Date To',required=True),
        'name':fields.char('Attendance Slip', size=124),
        'employee_id':fields.many2one('hr.employee', 'Employee', required=True), 
        'attendance_line':fields.one2many('hr.attendance.table.line','attendance_table','Attendance Lines', size=124),       
}
    _defaults={
         'name': lambda obj, cr, uid, context: '/',   
               }
    
    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'hr.attendance.table') or '/'
        return super(hr_attendance_table, self).create(cr, uid, vals, context=context)
    
    def recompute_attendance(self, cr, uid, ids, context=None):
        for attendance in self.browse(cr, uid, ids,context=None):
            contract_ids = self.pool.get('hr.payslip').get_contract( cr, uid, attendance.employee_id, attendance.date_from, attendance.date_to, context=None)
            contract_obj = self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context) and self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context)[0] or False
            for line in attendance.attendance_line:
                        date = line.date
                        date1= datetime.datetime.strptime(date,'%Y-%m-%d')
                        j ='A'
                        if line.attendance:
                            j= 'P'
                        
                        absent_info = ''
                        final_result = ''
                        
                        if contract_obj:
                            search_for_weekly_off = self.pool.get('resource.calendar').working_hours_on_day(cr, uid, contract_obj.working_hours, date1, context)
                            search_for_even_saturday = self.pool.get('leaves.calendar').search(cr, uid, [('holiday_id','=',contract_obj.holidays_id.id),('date_from','=',date1),('type','=','even_sat')])
                            search_for_holiday=self.pool.get('leaves.calendar').search(cr, uid, [('holiday_id','=',contract_obj.holidays_id.id),('date_from','=',date1),('type','<>','even_sat')])
                            search_for_leave=self.pool.get('hr.holidays').search(cr, uid, [('employee_id','=',attendance.employee_id.id),('state','=','validate'),('type','=','remove'),('date_from','<=',date),('date_to','>=',date)])
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
                            attendance_line_id = self.pool.get('hr.attendance.table.line').write(cr,uid,line.id,{
                                                                                                        
                                  
                                  'absent_info':absent_info,'final_result':final_result})
                        else:
                            self.pool.get('hr.attendance.table.line').write(cr,uid,line.id,{
                                
                                
                                  'absent_info':absent_info,'final_result':final_result})   
                        
                        
        
        return True
    
hr_attendance_table()


class hr_attendance_table_line(osv.osv):
    _name = 'hr.attendance.table.line'
    _description = 'Attendance Table'
    _columns = {
    'attendance_table':fields.many2one('hr.attendance.table','Attendance'),
	'name' : fields.char('Name'),
    'employee_id': fields.related('attendance_table', 'employee_id', string='Employee Id',store=True,type='many2one',relation="hr.employee",readonly=True),
   # 'employee_id':fields.related('attendance_table','employee_id',type='many2one','Employee Id'),
 #   'employee_id': fields.many2one('hr.employee', 'Employee', required=True),
    'date': fields.date('Attendance Date',required=True),
	'attendance': fields.boolean('Absent/Present'),
	'absent_info': fields.char('Holiday Information', size=124),
	'final_result': fields.selection([('P','P'),('A','A'),('PL','PL'),('WO','WO'),('UL','UL'),('H','H')],'Result'),
    
    #'final_result':fields.('Result'),
  'goa_drive_attendance':fields.selection([('C','C'),('U','U'),('L','L'),('W','W'),('T','T'),('O','O'),('M','M'),('P','P'),('A','A'),('H','H'),('SL','SL')],'HR Drive Attendance'),
    #'goa_drive_hr_attendance':fields.selection([('C','C'),('U','U'),('L','L'),('W','W'),('T','T'),('O','O'),('M','M'),('P','P'),('A','A'),('SL','SL'),('H','H')],'HR Drive Attendance'),

   'biometric_attendance':fields.selection([('P','P'),('A','A')],'Biometric Attendance'),
   'login_time':fields.char('Punch In'),
   'logout_time':fields.char('Punch Out')
   }
       
    def fetch_attendance_info(self,cr,uid,ids,context=None):
	 	for p in self.browse(cr, uid, ids,context=None):
						 leave_id=p.id
						 employee_id=p.employee_id.id
						 specific_date=p.date
						 attendance_status=p.attendance
						 absent_info=p.absent_info
						 aa = datetime.datetime.strptime(specific_date,"%Y-%m-%d")
						 contract_ids = self.pool.get('hr.payslip').get_contract( cr, uid, p.employee_id, specific_date, specific_date, context=None)
						 contract_obj = self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context) and self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context)[0] or False
						 if contract_obj:
						 	search_for_weekly_off = self.pool.get('resource.calendar').working_hours_on_day(cr, uid, contract_obj.working_hours, aa, context)
                        
						 search_for_holiday=self.pool.get('leaves.calendar').search(cr, uid, [('employee_id','=',employee_id),('date_from','=',specific_date)])
						
						 search_for_leave=self.pool.get('hr.holidays').search(cr, uid, [('employee_id','=',employee_id),('state','=','validate'),('type','=','remove'),('date_from','<=',specific_date),('date_to','>=',specific_date)])
									            
						 if search_for_leave:
						 	
						 	res = self.pool.get('hr.holidays').browse(cr, uid, search_for_leave, context=context)[0].holiday_status_id.payroll_code.name
						 	self.write(cr,uid,leave_id,{'absent_info':res}) 
									 			 						  
						 elif search_for_holiday:
							
							self.write(cr,uid,leave_id,{'absent_info':'H'})
							
						 elif not search_for_weekly_off:
						 	
						 	self.write(cr,uid,leave_id,{'absent_info':'WO'})
						 
						 
						 for q in self.browse(cr, uid, ids,context=None):
								absent_info_new=q.absent_info
							        	
						 if absent_info_new: 
						 	if attendance_status==True and absent_info_new=='H':
						 	
						 		self.write(cr,uid,leave_id,{'final_result':'HH'})
					 		else:
					 			self.write(cr,uid,leave_id,{'final_result':absent_info_new})
					 	 else:
					 		if attendance_status:
					 			self.write(cr,uid,leave_id,{'final_result':'P'})
					 		else:
					 			self.write(cr,uid,leave_id,{'final_result':'A'})	 
						 		  
		return True				 
 
class absent_info(osv.osv):
    _name = "absent.info"
    _description = "Absent Information"
    _columns = {
        'name':fields.char('Absent Information', size=124),

        }

absent_info()

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
    

class employee_allowance(osv.osv):
    
    _name ="employee.allowance"
    
    _columns = {
               
               'allowance_to_date':fields.date("Date To",required=True),
               'allowance_from_date':fields.date("Date From",required=True),
               'overtime_allowance_id':fields.one2many('employee.allowance.line','overtime_id','Employee allowance')
        
               }
    
    
class employee_allowance_line(osv.osv):
    
    _name ="employee.allowance.line"
    
    _columns = {
               'overtime_id':fields.many2one('employee.allowance','Employee Allowance'),
               'employee_id':fields.many2one('hr.employee', 'Employee',required=True),
               'overtime':fields.integer('Overtime',size=124),
               'mobile_advance':fields.integer('Advance',size=124),
               'arrears':fields.integer('Arrears',size=124)
               }
    
       
    
    
    
