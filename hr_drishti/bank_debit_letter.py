
from openerp.osv import osv,fields

  

class employee_bank_debit_details(osv.osv):
    
    
    def _amount_total(self,cr,uid,ids,name,arg,context=None):
        res = {}
        if not ids: return {}
        amount = 0.0
        for val in self.browse(cr, uid, ids, context=context):
            for l in val.debit_account_ids:
                amount += l.amount
            
            res[val.id] =  amount
        return res

    
    
    _name = 'employee.bank.debit.details'
    _columns={
              
              'name':fields.char("Name",required=True),
              'date_from':fields.date('Date From',required=True), 
              'date_to':fields.date('Date To',required=True),
              'date':fields.date("Date"),
              'company_account_no':fields.char('Bank A/C No'),
              'company':fields.many2one('res.company','Company',required=True),
              'bank_id' : fields.many2one('res.bank','Bank',required=True),
              'debit_account_ids': fields.one2many('employee.bank.debit.details.line','debit_id', 'Employees'),
              'total': fields.function(_amount_total, string='Total',type='float')

              
                   }
    _defaults = {
        
        'date': fields.date.context_today,
        }
    def compute_sheet(self,cr,uid,ids,context=None):
        obj=self.browse(cr,uid,ids[0])
        employee_obj =self.pool.get('hr.employee')
        payslip_obj =self.pool.get('hr.payslip')
        employee_ids = employee_obj.search(cr ,uid, [('company_id','=', obj.company.id)])
        
        for val in employee_ids:

                payslip_ids = payslip_obj.search(cr ,uid, [('employee_id','=',val),('date_from','=',obj.date_from),('date_to','=',obj.date_to)])
                if payslip_ids:
                    payslip_line_ids = self.pool.get('hr.payslip.line').search(cr,uid,[('slip_id','in',payslip_ids),('code','=','NET')])
                    if payslip_line_ids:
                        amount = self.pool.get('hr.payslip.line').browse(cr,uid,payslip_line_ids[0]).amount
                        emp_amount = self.pool.get('employee.bank.debit.details.line').search(cr,uid,[('employee_id','=',val),('debit_id','=',obj.id)])
                        self.pool.get('employee.bank.debit.details.line').write(cr,uid,emp_amount,{'amount':amount})
                if not payslip_ids:
                        amount=0
                    
                        emp_amount = self.pool.get('employee.bank.debit.details.line').search(cr,uid,[('employee_id','=',val),('debit_id','=',obj.id)])

                        self.pool.get('employee.bank.debit.details.line').write(cr,uid,emp_amount,{'amount':amount})
        return True
                

    def onchange_company(self, cr, uid, ids, company,bank_id,context=None):
        res={}
        employee_list=[]
        count=1
        if company and bank_id:
            account_ids = self.pool.get('res.partner.bank').search(cr,uid,[('company_id','=',company)])
            if account_ids:
                accnt_number = self.pool.get('res.partner.bank').browse(cr,uid,account_ids[0]).acc_number
                res['company_account_no'] = accnt_number
            employee_ids = self.pool.get('hr.employee').search(cr,uid,[('company_id','=',company),('bank_field','=',bank_id)])
#             employee_name=ids and object.search(cr, uid, [('employee_id', '=', ids[0])], context=context) or False
                

            for val in employee_ids:
                bank_acc = self.pool.get('hr.employee').browse(cr,uid,val).acc_number
                
                if bank_acc:
                    employee_list.append((0,0,{'employee_id':val,'serial_no':count,'account_no':bank_acc}))
                count+=1
            res['debit_account_ids'] = employee_list
        return {'value':res}
    
   
class employee_bank_debit_details_line(osv.osv):
    _name = 'employee.bank.debit.details.line'
    _columns = {
                'serial_no':fields.char('Sr. No.',readonly=True),
                'debit_id':fields.many2one('employee.bank.debit.details',"Employee name"),
                'employee_id':fields.many2one('hr.employee','Employee',required=True,readonly=True),

                'account_no':fields.char('Account No',readonly=True),
                'amount':fields.float('Amount',readonly=True)
                }
   


    