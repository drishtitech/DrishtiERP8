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
        'name': fields.char('Holiday Name', size=124, required=True),
        'date_from': fields.date('Date', size=124,required=True),
        'day': fields.selection([('0','Monday'),('1','Tuesday'),('2','Wednesday'),('3','Thursday'),('4','Friday'),('5','Saturday'),('6','Sunday')], 'Day of Week',required=True),
        'description': fields.text('Description', size=124),
        'type':fields.selection([('even_sat', 'Even Saturday')],'Type'),
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
        'holiday_id': fields.many2one('leaves.calendar','Holidays ID', size=124),
        'name': fields.char('Holidays Calendar Name', size=124, required=True),
        'location':fields.selection([('Mumbai', 'Mumbai'),('Goa','Goa')],'Location'),
        'holidays_line':fields.many2many('leaves.calendar','holiday_calendar_name','holiday_id','calendar_id',"Holidays Number ", size=124),

 
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
