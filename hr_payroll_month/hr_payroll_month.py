import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta

from openerp import netsvc
from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

from openerp.tools.safe_eval import safe_eval as eval

class hr_payslip(osv.osv):

    _inherit = 'hr.payslip'

#     def get_worked_day_lines(self, cr, uid, contract_ids, date_from, date_to, context=None):
#         """
#         @param contract_ids: list of contract id
#         @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
#         """
#         def was_on_leave(employee_id, datetime_day, context=None):
#             res = False
#             day = datetime_day.strftime("%Y-%m-%d")
#             holiday_ids = self.pool.get('hr.holidays').search(cr, uid, [('state','=','validate'),('employee_id','=',employee_id),('type','=','remove'),('date_from','<=',day),('date_to','>=',day)])
#             if holiday_ids:
#                 res = self.pool.get('hr.holidays').browse(cr, uid, holiday_ids, context=context)[0].holiday_status_id.name
#             return res
# 
#         res = []
#         for contract in self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context):
#             if not contract.working_hours:
#                 #fill only if the contract as a working schedule linked
#                 continue
#             attendances = {
#                  'name': _("Normal Working Days paid at 100%"),
#                  'sequence': 1,
#                  'code': 'WORK100',
#                  'number_of_days': 0.0,
#                  'number_of_hours': 0.0,
#                  'contract_id': contract.id,
#             }
#             leaves = {}
#             day_from = datetime.strptime(date_from,"%Y-%m-%d")
#             day_to = datetime.strptime(date_to,"%Y-%m-%d")
#             nb_of_days = (day_to - day_from).days + 1
#             for day in range(0, nb_of_days):
#                 working_hours_on_day = self.pool.get('resource.calendar').working_hours_on_day(cr, uid, contract.working_hours, day_from + timedelta(days=day), context)
#                 if working_hours_on_day:
#                     #the employee had to work
#                     leave_type = was_on_leave(contract.employee_id.id, day_from + timedelta(days=day), context=context)
#                     if leave_type:
#                         #if he was on leave, fill the leaves dict
#                         if leave_type in leaves:
#                             leaves[leave_type]['number_of_days'] += 1.0
#                             leaves[leave_type]['number_of_hours'] += working_hours_on_day
#                         else:
#                             leaves[leave_type] = {
#                                 'name': leave_type,
#                                 'sequence': 5,
#                                 'code': leave_type,
#                                 'number_of_days': 1.0,
#                                 'number_of_hours': working_hours_on_day,
#                                 'contract_id': contract.id,
#                             }
#                     else:
#                         #add the input vals to tmp (increment if existing)
#                         attendances['number_of_days'] += 1.0
#                         attendances['number_of_hours'] += working_hours_on_day
#             leaves = [value for key,value in leaves.items()]
#             monthdays = {
#                  'name': _("Days in the Month"),
#                  'sequence': 10,
#                  'code': 'MONTHDAYS',
#                  'number_of_days': nb_of_days,
#                  'number_of_hours': 0.0,
#                  'contract_id': contract.id,
#             }
#             res += [attendances] + leaves + [monthdays]
#         return res
