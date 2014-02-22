import time
from openerp.osv import fields, osv
from datetime import datetime
from openerp import tools
from openerp.tools.translate import _

import time                            
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
import calendar
import openerp.addons.decimal_precision as dp

class hr_payslip_line(osv.osv):
    _name = "hr.payslip.line"
    _description = "Payslip Line"
    _inherit = "hr.payslip.line"
    
    def _calculate_total(self, cr, uid, ids, name, args, context):
        if not ids: return {}
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
           # res[line.id] = float(line.quantity) * line.amount * line.rate / 100
           x = float(line.quantity) * round(line.amount) * line.rate / 100
           res[line.id] = round(x)
        return res
    
    _columns = {
                'total': fields.function(_calculate_total, method=True, type='float', string='Total', digits_compute=dp.get_precision('Payroll'),store=True ),
                }


class leaves_calendar(osv.osv):
    _name = "leaves.calendar"
    _description = "Public Holidays"
    _columns = {
        'holiday_id':fields.many2one('holidays.calendar','Holidays Number', size=124),        
        'name': fields.char('Holiday Name', size=124, required=True),
        'date_from': fields.date('Date', size=124),
        'day': fields.selection([('0','Monday'),('1','Tuesday'),('2','Wednesday'),('3','Thursday'),('4','Friday'),('5','Saturday'),('6','Sunday')], 'Day of Week'),
        'description': fields.text('Description', size=124),
        'type':fields.selection([('even_sat', 'Even Saturday')],'Type'),
        
        }
    
    def onchange_date(self,cr,uid,ids,date_from):
        if date_from:
            from_dt = datetime.strptime(date_from, "%Y-%m-%d")
            a=from_dt.weekday()
            return {'value' : {'day':str(a)}}
        return {'value' : {'day':False}}
    
    
leaves_calendar()

class holidays_calendar(osv.osv):
    _name = "holidays.calendar"
    _description = "Holidays Calendar"
    _columns = {
        
        'name': fields.char('Holidays Calendar Name', size=124, required=True),
        'location':fields.selection([('Mumbai', 'Mumbai'),('Goa','Goa')],'Location'),
        'holidays_line':fields.one2many('leaves.calendar','holiday_id'," ", size=124),
         
        }
 
holidays_calendar()


class hr_holidays_payroll_code(osv.osv):
	_name = 'hr.holidays.payroll.code'
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
        'bonus_amount': fields.float('Bonus Amount', size=124) 
}
hr_contract()

class hr_attendance_table(osv.osv):
    _name='hr.attendance.table'
    _description = 'Attendance Table'
    _columns = {
        'date_from':fields.date('Date From'),
        'date_to':fields.date('Date To'),
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
                        date1= datetime.strptime(date,'%Y-%m-%d')
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
                            if j== 'P' and absent_info=='H': 
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
    'employee_id': fields.many2one('hr.employee', 'Employee', required=True),
    'date': fields.date('Day of the Month'),
	'attendance': fields.boolean('Absent/Present'),
	'absent_info': fields.char('Information', size=124),
	'final_result': fields.char('Result'),
    }
       
    def fetch_attendance_info(self,cr,uid,ids,context=None):
	 	for p in self.browse(cr, uid, ids,context=None):
						 leave_id=p.id
						 employee_id=p.employee_id.id
						 specific_date=p.date
						 attendance_status=p.attendance
						 absent_info=p.absent_info
						 aa = datetime.strptime(specific_date,"%Y-%m-%d")
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
						 	
						 		self.write(cr,uid,leave_id,{'final_result':'P'})
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
            
            old_slipline_ids = slip_line_pool.search(cr, uid, [('slip_id', '=', payslip.id)], context=context)

            if old_slipline_ids:
                slip_line_pool.unlink(cr, uid, old_slipline_ids, context=context)
            if payslip.contract_id:
                
                contract_ids = [payslip.contract_id.id]
            else:
                
                contract_ids = self.get_contract(cr, uid, payslip.employee_id, payslip.date_from, payslip.date_to, context=context)
            lines = [(0,0,line) for line in self.pool.get('hr.payslip').get_payslip_lines(cr, uid, contract_ids, payslip.id, context=context)]
            self.write(cr, uid, [payslip.id], {'line_ids': lines, 'number': number,}, context=context)
        return True
    
    
    

    def get_worked_day_lines(self, cr, uid, contract_ids, date_from, date_to, context=None):
       """
       @param contract_ids: list of contract id
       @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
       """
       print "testing"
       def was_on_leave(employee_id, datetime_day, context=None):
           res = False
           day = datetime_day.strftime("%Y-%m-%d")
           holiday_ids = self.pool.get('hr.holidays').search(cr, uid, [('state','=','validate'),('employee_id','=',employee_id),('type','=','remove'),('date_from','<=',day),('date_to','>=',day)])
           if holiday_ids:
               res = self.pool.get('hr.holidays').browse(cr, uid, holiday_ids, context=context)[0].holiday_status_id.name
           return res
       res = []
       
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
           day_from = datetime.strptime(date_from,"%Y-%m-%d")
           day_to = datetime.strptime(date_to,"%Y-%m-%d")
           nb_of_days = (day_to - day_from).days + 1
           attendance_line = self.pool.get('hr.attendance.table.line').search(cr, uid, [('employee_id','=',contract.employee_id.id),('date','>=',date_from),('date','<=',date_to)])
           
           leaves = {}
           
           for day in range(0, nb_of_days):
             if  not contract.employee_id.attendance: 
               att_id = self.pool.get('hr.attendance.table.line').search(cr, uid, [('employee_id','=',contract.employee_id.id),('date','=',day_from +timedelta(days=day))])
               for att_obj in self.pool.get('hr.attendance.table.line').browse(cr,uid, att_id):
                   if att_obj.attendance == True:
                       worked['number_of_days'] += 1.0
                       worked['number_of_hours'] += 8.0
                   if att_obj.attendance == True and att_obj.final_result == 'HH':
                       
                       P['number_of_days'] += 1.0
                       P['number_of_hours'] += 8.0
                   if att_obj.attendance == False and att_obj.absent_info == 'WO' and att_obj.final_result == 'HH':
                       
                       WO['number_of_days'] += 1.0
                       WO['number_of_hours'] += 8.0
                   if att_obj.attendance == False and att_obj.absent_info == 'Manual Attendance' and att_obj.final_result == 'HH':
                       
                       P['number_of_days'] += 1.0
                       P['number_of_hours'] += 8.0            
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
                    
                    leave_type = was_on_leave(contract.employee_id.id, day_from + timedelta(days=day), context=context)
                    if leave_type:
                        
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
               
               l = [salarydays,att_records['MONTHDAYS'], att_records['P'],  att_records['A'], att_records['PL'],  att_records['UL'],]  
       return l
   
    def get_payslip_lines(self, cr, uid, contract_ids, payslip_id, context):
        def _sum_salary_rule_category(localdict, category, amount):
            if category.parent_id:
                localdict = _sum_salary_rule_category(localdict, category.parent_id, amount)
            localdict['categories'].dict[category.code] = category.code in localdict['categories'].dict and localdict['categories'].dict[category.code] + amount or amount
            return localdict

        class BrowsableObject(object):
            def __init__(self, pool, cr, uid, employee_id, dict):
                self.pool = pool
                self.cr = cr
                self.uid = uid
                self.employee_id = employee_id
                self.dict = dict

            def __getattr__(self, attr):
                return attr in self.dict and self.dict.__getitem__(attr) or 0.0

        class InputLine(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""
            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = datetime.now().strftime('%Y-%m-%d')
                result = 0.0
                self.cr.execute("SELECT sum(amount) as sum\
                            FROM hr_payslip as hp, hr_payslip_input as pi \
                            WHERE hp.employee_id = %s AND hp.state = 'done' \
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s",
                           (self.employee_id, from_date, to_date, code))
                res = self.cr.fetchone()[0]
                return res or 0.0

        class WorkedDays(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""
            def _sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = datetime.now().strftime('%Y-%m-%d')
                result = 0.0
                self.cr.execute("SELECT sum(number_of_days) as number_of_days, sum(number_of_hours) as number_of_hours\
                            FROM hr_payslip as hp, hr_payslip_worked_days as pi \
                            WHERE hp.employee_id = %s AND hp.state = 'done'\
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s",
                           (self.employee_id, from_date, to_date, code))
                return self.cr.fetchone()

            def sum(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[0] or 0.0

            def sum_hours(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[1] or 0.0

        class Payslips(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = datetime.now().strftime('%Y-%m-%d')
                self.cr.execute("SELECT sum(case when hp.credit_note = False then (pl.total) else (-pl.total) end)\
                            FROM hr_payslip as hp, hr_payslip_line as pl \
                            WHERE hp.employee_id = %s AND hp.state = 'done' \
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id AND pl.code = %s",
                            (self.employee_id, from_date, to_date, code))
                res = self.cr.fetchone()
                return res and res[0] or 0.0

        #we keep a dict with the result because a value can be overwritten by another rule with the same code
        result_dict = {}
        rules = {}
        categories_dict = {}
        blacklist = []
        payslip_obj = self.pool.get('hr.payslip')
        inputs_obj = self.pool.get('hr.payslip.worked_days')
        obj_rule = self.pool.get('hr.salary.rule')
        payslip = payslip_obj.browse(cr, uid, payslip_id, context=context)
        worked_days = {}
        for worked_days_line in payslip.worked_days_line_ids:
            worked_days[worked_days_line.code] = worked_days_line
        inputs = {}
        for input_line in payslip.input_line_ids:
            inputs[input_line.code] = input_line

        categories_obj = BrowsableObject(self.pool, cr, uid, payslip.employee_id.id, categories_dict)
        input_obj = InputLine(self.pool, cr, uid, payslip.employee_id.id, inputs)
        worked_days_obj = WorkedDays(self.pool, cr, uid, payslip.employee_id.id, worked_days)
        payslip_obj = Payslips(self.pool, cr, uid, payslip.employee_id.id, payslip)
        rules_obj = BrowsableObject(self.pool, cr, uid, payslip.employee_id.id, rules)

        localdict = {'categories': categories_obj, 'rules': rules_obj, 'payslip': payslip_obj, 'worked_days': worked_days_obj, 'inputs': input_obj}
        #get the ids of the structures on the contracts and their parent id as well
        structure_ids = self.pool.get('hr.contract').get_all_structures(cr, uid, contract_ids, context=context)
        #get the rules of the structure and thier children
        rule_ids = self.pool.get('hr.payroll.structure').get_all_rules(cr, uid, structure_ids, context=context)
        #run the rules by sequence
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x:x[1])]

        for contract in self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context):
            employee = contract.employee_id
            localdict.update({'employee': employee, 'contract': contract})
            for rule in obj_rule.browse(cr, uid, sorted_rule_ids, context=context):
                key = rule.code + '-' + str(contract.id)
                localdict['result'] = None
                localdict['result_qty'] = 1.0
                #check if the rule can be applied
                if obj_rule.satisfy_condition(cr, uid, rule.id, localdict, context=context) and rule.id not in blacklist:
                    #compute the amount of the rule
                    amount, qty, rate = obj_rule.compute_rule(cr, uid, rule.id, localdict, context=context)
                    #check if there is already a rule computed with that code
                    previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                    #set/overwrite the amount computed for this rule in the localdict
                    tot_rule = round(amount) * qty * rate / 100.0
                    localdict[rule.code] = tot_rule
                    rules[rule.code] = rule
                    #sum the amount for its salary category
                    localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
                    #create/overwrite the rule in the temporary results
                    result_dict[key] = {
                        'salary_rule_id': rule.id,
                        'contract_id': contract.id,
                        'name': rule.name,
                        'code': rule.code,
                        'category_id': rule.category_id.id,
                        'sequence': rule.sequence,
                        'appears_on_payslip': rule.appears_on_payslip,
                        'condition_select': rule.condition_select,
                        'condition_python': rule.condition_python,
                        'condition_range': rule.condition_range,
                        'condition_range_min': rule.condition_range_min,
                        'condition_range_max': rule.condition_range_max,
                        'amount_select': rule.amount_select,
                        'amount_fix': rule.amount_fix,
                        'amount_python_compute': rule.amount_python_compute,
                        'amount_percentage': rule.amount_percentage,
                        'amount_percentage_base': rule.amount_percentage_base,
                        'register_id': rule.register_id.id,
                        'amount': round(amount),
                        'employee_id': contract.employee_id.id,
                        'quantity': qty,
                        'rate': rate,
                    }
                else:
                    #blacklist this rule and its children
                    blacklist += [id for id, seq in self.pool.get('hr.salary.rule')._recursive_search_of_rules(cr, uid, [rule], context=context)]

        result = [value for code, value in result_dict.items()]
        return result        
    
