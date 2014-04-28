from openerp.osv import fields, osv

class add_fields_res_company(osv.Model):
    _name = 'res.company'
    _inherit = 'res.company'
    _columns = {
		'name_display': fields.related('partner_id', 'name_display', string='Company Display Name', size=128, required=True, store=True, type='char'),
    }

class add_fields_res_partner(osv.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'
	_columns = {
		'name_display': fields.char('Display Name', size=128),
	}
