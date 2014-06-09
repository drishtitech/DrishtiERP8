from openerp import addons

from openerp.osv import fields, osv

class res_partner(osv.osv):
    _inherit = "res.partner"
    
    _columns = {
                 'property_account_payable': fields.property(
            type='many2one',
            relation='account.account',
            string="Account Payable",
            domain="[('type', 'in', ['payable','receivable'])]",
            help="This account will be used instead of the default one as the payable account for the current partner",
            required=True),
        'property_account_receivable': fields.property(
            type='many2one',
            relation='account.account',
            string="Account Receivable",
            domain="[('type', 'in', ['payable','receivable'])]",
            help="This account will be used instead of the default one as the receivable account for the current partner",
            required=True),
                }