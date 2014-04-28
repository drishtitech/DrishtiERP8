import openerp
from openerp import pooler, tools
from openerp.osv import fields,osv
from openerp.tools.translate import _
from datetime import datetime, date
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import time
from dateutil.relativedelta import relativedelta
from datetime import timedelta

class employee_increment(osv.osv):
    _name = "employee.increment"
    
    _columns = {
                'name' : fields.char('Name',required=True),
                'appraisal_date': fields.date('Appraisal Effective Date',required=True), 
                'category_ids': fields.many2many('hr.employee.category', 'employee_appraisal_category_rel', 'emp_appraisal_id', 'category_id', 'Tags'),
                'increment_line' : fields.one2many('employee.increment.line','appraisal_id','Increment Line'),  
                'state': fields.selection([
                        ('draft', 'Draft'),
                        ('confirm','Confirm'),
                       
                        ('done', 'Done'),
                        ],'State'),                  
                }
    
    
    
    def appraisal_confirm(self, cr, uid, ids, context=None):
        context = context or {}
        for o in self.browse(cr, uid, ids):
            
            for line in o.increment_line:
               
                contract_ids = self.pool.get('hr.payslip').get_contract( cr, uid, line.employee_id, o.appraisal_date, o.appraisal_date, context=None)
                if contract_ids:
                    contract_obj = self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context)[0]
                    date_end = datetime.strptime(o.appraisal_date,"%Y-%m-%d") - timedelta(days=1)
                    self.pool.get('hr.contract').write(cr, uid, contract_obj.id,{'date_end': date_end})
                emp_dict = {
                            'name': line.employee_id.name,
                            'employee_id': line.employee_id.id,
                            'type_id' : contract_obj.type_id.id,
                            'wage': contract_obj.wage*(1+(line.appraisal/100)),
                            'struct_id': contract_obj.struct_id.id,
                            'date_statrt': o.appraisal_date,
                            'house_rent_allowance_metro_nonmetro': contract_obj.house_rent_allowance_metro_nonmetro,
                            'tds' : contract_obj.tds,
                            'working_hours': contract_obj.working_hours.id,
                            }
                self.pool.get('hr.contract').create(cr, uid, emp_dict   ) 
        return True
    _defaults = { 
        'state': 'draft',
        }
    
class employee_increment_line(osv.osv):
    _name ="employee.increment.line"
    _rec_name = "employee_id"
    _columns = {
                'employee_id': fields.many2one('hr.employee','Employee Name',required=True),
                'current_wages': fields.float('Current Wages'),
                'appraisal' : fields.float('Appraisal(%)'),
                'appraisal_id': fields.many2one('employee.increment','Appraisal ID'),
                }
    
    
    
    
    
    
    
        