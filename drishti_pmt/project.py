import openerp
from openerp import pooler, tools
from openerp.osv import fields,osv
from openerp.tools.translate import _
from datetime import datetime, date
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import time
from dateutil.relativedelta import relativedelta


class project_task(osv.osv):
    _inherit = "project.task"
    _columns = {
        
                 'task_priority': fields.selection([('0','Today-Critical'), ('1','Week-Critical'), ('2','Month-Critical'), ('3','Today-Not Critical'),('4','Week-Not Critical'),('5','Month-Not Critical') ], 'Task Priority',required=True),
                }
    _order = 'task_priority'
