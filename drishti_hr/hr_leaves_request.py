import openerp
from openerp import pooler, tools
from openerp.osv import fields,osv
from openerp.tools.translate import _
from datetime import datetime, date
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import time
from dateutil.relativedelta import relativedelta

class hr_employee(osv.osv):
    _inherit = "hr.employee"
 
    _columns = {
                'joining_date' : fields.date('Joining Date'),
                'leave_allocation_date' : fields.date('Leave allocation date'),
                'bonus_leave_date' : fields.date('Bonus Leave Date'),
                'leave_allocation_type' : fields.selection([('goa','Goa'),('mumbai','Mumbai'),('mumbai_h2o','Mumbai H2O')], 'Leave Allocation Base on')
                }
    
    _defaults = {
                'leave_allocation_date': fields.date.context_today,
                'joining_date' : fields.date.context_today,
                }
    
    
    def run_employee_leave(self, cr, uid, automatic=False, use_new_cursor=False, context=None): 
        emp_ids = self.search(cr, uid, [('leave_allocation_type','=','mumbai')])
        emp_obj = self.browse(cr, uid, emp_ids)
        hr_holiday_obj = self.pool.get('hr.holidays')
        for emp in emp_obj:
            
          if emp.leave_allocation_date == time.strftime("%Y-%m-%d"): 
            leaves_obj_dict = {
                'name' :   emp.name, #) % (employee_name,tools.ustr(ttyme.strftime('%B-%Y'))), 
                'state': 'draft',
                'type' : 'add',
                'user_id' :  uid,
                'holiday_type' : 'employee',
                'holiday_status_id': 1,
                'number_of_days_temp' : 5,
                'employee_id' : emp.id
                    }
            leave_id = hr_holiday_obj.create(cr, uid, leaves_obj_dict, context=context)
            hr_holiday_obj.holidays_validate(cr, uid,[leave_id])
            next_leave_date = date.today() + relativedelta(months=3)
            bonus_leave_date = emp.bonus_leave_date
            print "t"
            if not emp.bonus_leave_date: 
                bonus_leave_date = (datetime.strptime(emp.joining_date,'%Y-%m-%d') +relativedelta(days=240)).strftime("%Y-%m-%d")
            self.write(cr, uid, emp.id, {'leave_allocation_date': next_leave_date, 'bonus_leave_date': bonus_leave_date})
         # print "test",(datetime.strptime(emp.current_year_date,'%Y-%m-%d') +relativedelta(days=240))  
          if emp.bonus_leave_date == time.strftime("%Y-%m-%d"):
          
               leaves_obj_dict = {
                'name' :   emp.name + ' Bonus Leave', #) % (employee_name,tools.ustr(ttyme.strftime('%B-%Y'))), 
                'state': 'draft',
                'type' : 'add',
                'user_id' :  uid,
                'holiday_type' : 'employee',
                'holiday_status_id': 1,
                'number_of_days_temp' : 1,
                'employee_id' : emp.id
                    }
               leave_id = hr_holiday_obj.create(cr, uid, leaves_obj_dict, context=context)
               hr_holiday_obj.holidays_validate(cr, uid,[leave_id])
               bonus_leave_date = (datetime.strptime(emp.bonus_leave_date,'%Y-%m-%d') +relativedelta(months=12)).strftime("%Y-%m-%d")
               self.write(cr, uid, emp.id, { 'bonus_leave_date': bonus_leave_date})
               print "test1"
        return True
    
    
    
