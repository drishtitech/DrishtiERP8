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

class hr_holidays(osv.osv):
    _name = "hr.holidays"
    _description = "HR Holidays"
    _inherit = "hr.holidays"
    _columns = {
        'serial_no': fields.char('Serial No.', size=124),
        'leave_allocation_date':fields.date('Request date',required=True),
        }
    
    _defaults = {
                 'leave_allocation_date': fields.datetime.now,
                 
                 }
    
    
    
    def action_email_send(self, cr, uid, ids, context=None):
     
        ctx = {}
        print "context['template_name']",context
        cur_obj = self.browse(cr,uid,ids[0])
        template_id = self.pool.get('email.template').search(cr,uid, [('name','=',context['template_name'])])
        if template_id:
            ctx.update({
                'default_model': 'hr.holidays',
                'default_res_id': ids[0],
                'default_use_template': bool(template_id[0]),
                'default_template_id': template_id[0],
                'default_composition_mode': 'comment',
              
            })
            hr_email_id = cur_obj.employee_id.company_id and cur_obj.employee_id.company_id.partner_id.id or False
            
            if context['type'] == 'confirm':
                email_id = cur_obj.employee_id.parent_id and cur_obj.employee_id.parent_id.user_id and cur_obj.employee_id.parent_id.user_id.partner_id.id or False
                partner_ids = [(6,0,[email_id])]
                author_id = cur_obj.employee_id.user_id.partner_id.id,
            else:
                email_id = cur_obj.employee_id.user_id and cur_obj.employee_id.user_id.partner_id.id
                partner_ids = [(6,0,[email_id])]
                author_id = cur_obj.employee_id.parent_id.user_id.partner_id.id
            ctx['default_email_cc'] =cur_obj.employee_id.company_id.partner_id.email
            message_id = self.pool.get('mail.compose.message').create(cr,uid,{'author_id' : author_id,'partner_ids': partner_ids ,'composition_mode': 'mass_mail'},context=ctx)
            self.pool.get('mail.compose.message').send_mail1(cr,uid,[message_id],ctx)
       
   
    def holidays_validate(self, cr, uid, ids, context=None):
        holiday_brw = self.browse(cr, uid, ids)[0]
       
        if holiday_brw.employee_id.user_id.id == uid:
            raise osv.except_osv(_('Warning!'),_("Employee cannot approve their own leaves"))
        res = super(hr_holidays, self).holidays_validate(cr, uid, ids,context)
        if not context:
            context = {}
        context['template_name'] = 'Leave Approve'
        context['type'] = 'approve'
        self.action_email_send(cr,uid,ids,context)
        return res
       
    def holidays_confirm(self, cr, uid, ids, context=None):
        res = super(hr_holidays, self).holidays_confirm(cr, uid, ids,context)
        if not context:
            context = {}
        context['template_name'] = 'Leave Request'
        context['type'] = 'confirm'
        self.action_email_send(cr,uid,ids,context)
       
        return res

    
    
    
hr_holidays()
