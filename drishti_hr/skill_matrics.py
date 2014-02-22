import openerp
from openerp import pooler, tools
from openerp.osv import fields,osv
from openerp.tools.translate import _
from datetime import datetime, date
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import time
from dateutil.relativedelta import relativedelta


class employee_skill(osv.osv):
    _name ="employee.skill"
    _columns = {
                'name':fields.char('Skill Name',size=256),
                'description': fields.text('Description'),
                }
    
    
class employee_skill_line(osv.osv):
    _name = "employee.skill.line"
    
    _rec_name = "employee_id"
    _columns = {
                #'name': fields.char('Name'),
                'skill_id': fields.many2one('employee.skill','Employee Skill'),
                'employee_id': fields.many2one('hr.employee','Employee Name',required=True),

                 'skill_rate': fields.selection([('1','1'),('2','2'),('3','3'),('4','4'),
                                                ('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10')],'Rating'),
                'short_description': fields.char('Short Description',size=256),
                'notes': fields.text('Notes'),
                
                }    
    
    
    