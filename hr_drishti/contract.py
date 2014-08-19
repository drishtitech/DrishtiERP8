from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
from datetime import date
from datetime import timedelta
import calendar
import time

class hr_contract(osv.osv):
    _inherit = "hr.contract"
    _description = 'Employee Contract'
    
    def _gross_salary(self,cr,uid,ids, name, arg, context=None):
        res = {}
        
        for contract in self.browse(cr, uid, ids, context=context):
            
            
                res[contract.id] = contract.wage +contract.conveyance_allowence +contract.grade_pay + contract.hr_comp
        return res
    
    _columns = {
        'wage' : fields.float('Basic/Category Pay', required=True),
        'grade_pay': fields.float('Grade Pay'),
        'hr_comp' : fields.float('HR Compensatory'),
              
        'holidays_id' : fields.many2one('holidays.calendar','Holidays Calendar', size=124),
        'nutritional_allowance' : fields.integer('Nutritional Allowance', size=124),
        'attendance_incentive' : fields.integer('A.I. All', size=124),
        'da_lta_fa' : fields.integer('DA/LTA/FA', size=124),
        'special_allowance' : fields.integer('Special Allowance', size=124),
        'hra' : fields.integer('House Rent Allowance', size=124),
       
        'bonus_amount': fields.float('Bonus Amount', size=124),
        'current_date':fields.date('Current date'),
        'driver_salary':fields.boolean('Driver Salary'),
        'house_rent_allowance_metro_nonmetro':fields.float('House Rent Allowance(%)'),
        'supplementary_allowance':fields.float(' Supplementary Allowance '),
        'tds':fields.float('TDS'),
        'voluntary_provident_fund':fields.float('Voluntary Provident Fund (%)'),
        'medical_insurance':fields.float('Medical Insurance'),
        'cca_allowance':fields.float('CCA Allowance'),
        'office_wear_allowance':fields.float('Office Wear Allowance'),
        'medical_allowance':fields.float('Medical Allowance'),
        'over_time_allowence':fields.integer('Over Time',size=124),
        'conveyance_allowence':fields.float('Conveyance Allowance'),
        'provident_amount':fields.float('Provident Amount'),
        'e.s.i.s':fields.float('E.S.I.S'),
         'company_id': fields.related('employee_id', 'company_id', string='Company',store=True,type='many2one',relation="res.company",readonly=True),
         
         'emi_amount': fields.float('Loan EMI',),
         'mobile_deduction': fields.float('Mobile Deduction'),
         'tds_deduction': fields.float('TDS Deduction'),
         'arrers': fields.float('Arrers'),
        'gross_salary' : fields.function(
                                            _gross_salary,
                                            method=True,
                                            type='float',
                                            string="Gross Salary",
                                           
                                        ),
         
        }
     
    _defaults = {
        'current_date': lambda *a: time.strftime("%Y-%m-%d")
     }     
    
    def default_get(self, cr, uid, fields, context=None):
        res = super(hr_contract, self).default_get(cr, uid, fields, context=context)
        if context.get('active_id'):
            obj = self.browse(cr, uid, int(context['active_id']), context=context)
            current_date=datetime.datetime.strptime(obj.current_date,'%Y-%m-%d')
            previous_date=current_date + datetime.timedelta(days = -1)
            res.update({'name' : obj.name,'employee_id':obj.employee_id.id,'date_start':obj.current_date,'visa_expire' : obj.visa_expire,'permit_no':obj.permit_no,'visa_no':obj.visa_no,'house_rent_allowance_metro_nonmetro':obj.house_rent_allowance_metro_nonmetro,'supplementary_allowance':obj.supplementary_allowance,'tds':obj.tds,'voluntary_provident_fund':obj.voluntary_provident_fund,'medical_insurance':obj.medical_insurance,'advantages':obj.advantages,'notes':obj.notes,'nutritional_allowance':obj.nutritional_allowance,'attendance_incentive':obj.attendance_incentive,'da_lta_fa':obj.da_lta_fa,'special_allowance':obj.special_allowance,'bonus_amount':obj.bonus_amount,'hra':obj.hra,'schedule_pay':obj.schedule_pay,'struct_id':obj.struct_id.id,'working_hours':obj.working_hours.id, 'job_id':obj.job_id.id
                    })
            self.write(cr, uid, obj.id, {'date_end':str(previous_date)})
        return res   
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

