import time
from openerp.osv import fields, osv

from openerp import tools
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from dateutil.relativedelta import relativedelta

from openerp import netsvc





class ops_request_product(osv.Model):
	_name = 'ops.request.product'
	_inherit = ['mail.thread', 'sale.order','purchase.order'] 

	_description = 'Request for Items'
	_columns = {
		'name': fields.char('Order Reference', size=64, required=True), #readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, select=True),
		'employee_id': fields.many2one('hr.employee', "Employee",  states={'draft':[('readonly',False)], 'confirm':[('readonly',False)]}),
		'user_id': fields.many2one('res.users', 'Requested by', track_visibility='onchange'), #states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, select=True
		# 'location_id': requested for "Warehouse ID/ Stock Location"
		'purchase_id': fields.many2one('purchase.order', 'purchase_id' , "Purchase Order"),
		'origin': fields.char('Source Document', size=64, help="Reference of the document that generated this sales order request."),
		'picking_ids': fields.one2many('stock.picking.out', 'sale_id', 'Related Picking', readonly=True, ),
		'date_request': fields.date('Date', required=True),#readonly=True, select=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}),
		'priority': fields.selection([
		('normal', 'Regular'),
		('high', 'High'),
		('critical', 'Critical'),], 'Priority', track_visibility='onchange'),
		'product_id': fields.many2one('product.product', 'Product', domain=[('purchase_ok', '=', True)], required=True),
		'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure'), required=True),
		'note': fields.text('Remarks'),
		'qty_avl_virtual': fields.related('product_id', 'virtual_available', string='Forecasted Quantity', readonly=True, type='float'),
		'qty_avl_actual': fields.related('product_id', 'qty_available', string='Quantity On Hand', readonly=True, type='float'),
		'state': fields.selection([('draft', 'New'),('cancelled', 'Refused'),('confirm', 'Waiting Approval'),('accepted', 'Approved'),    ('done', 'Done'),],
		     'Status', track_visibility='onchange')

	}

###   set some  field value as defaults 
	_defaults = {
		'date_request': lambda *args: time.strftime('%Y-%m-%d %H:%M:%S'),
		'priority' : 'normal',
		'user_id': lambda self, cr, uid, c: self.pool.get('res.users').browse(cr, uid, uid, c).id ,
## set name field automaticaly , get it frm function defined and prefix is updated in xml file ops_request_product_sequence.xml
		'name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'ops.request.product.sequence'),
	}
### function defined to alter the name sequence if duplicate request is done .
	def copy(self, cr, uid, id, default=None, context=None):
        	if not default:
                   default = {}
                default.update({


                 'name': self.pool.get('ir.sequence').get(cr, uid, 'ops.request.product.sequence'),
                })
                return super(ops_request_product, self).copy(cr, uid, id, default, context)

###
#	def _get_date_request(self, cr, uid, order, line, start_date, context=None):
#            date_request = datetime.strptime(start_date, DEFAULT_SERVER_DATE_FORMAT) + relativedelta(days=line.delay or 0.0)
#            date_request = (date_request - timedelta(days=order.company_id.security_lead)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
#            return date_request
###


	def expense_confirm(self, cr, uid, ids, context=None):
            for expense in self.browse(cr, uid, ids):
                if expense.employee_id and expense.employee_id.parent_id.user_id:
                     self.message_subscribe_users(cr, uid, [expense.id], user_ids=[expense.employee_id.parent_id.user_id.id])
            return self.write(cr, uid, ids, {'state': 'confirm', 'date_confirm': time.strftime('%Y-%m-%d')}, context=context)

	def expense_accept(self, cr, uid, ids, context=None):
            return self.write(cr, uid, ids, {'state': 'accepted',  'user_valid': uid}, context=context)

	def expense_canceled(self, cr, uid, ids, context=None):
            return self.write(cr, uid, ids, {'state': 'cancelled'}, context=context)

	def action_view_delivery(self, cr, uid, ids, context=None):
        
            mod_obj = self.pool.get('ir.model.data')
            act_obj = self.pool.get('ir.actions.act_window')

            result = mod_obj.get_object_reference(cr, uid, 'stock', 'action_picking_tree')
            id = result and result[1] or False
            result = act_obj.read(cr, uid, [id], context=context)[0]
            #compute the number of delivery orders to display
            pick_ids = []
            for so in self.browse(cr, uid, ids, context=context):
                pick_ids += [picking.id for picking in so.picking_ids]
            #choose the view_mode accordingly
            if len(pick_ids) > 1:
               result['domain'] = "[('id','in',["+','.join(map(str, pick_ids))+"])]"
            else:
                 res = mod_obj.get_object_reference(cr, uid, 'stock', 'view_picking_out_form')
                 result['views'] = [(res and res[1] or False, 'form')]
                 result['res_id'] = pick_ids and pick_ids[0] or False
            return result

	




class sale_shop(osv.osv):
	_inherit = "sale.shop"
	_columns = {
   		'warehouse_id': fields.many2one('stock.warehouse', 'Warehouse'),
	}

sale_shop()


class sale_order(osv.osv):
    _inherit = "sale.order"
    
    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'shipped': False,
            'picking_ids': [],
        })
        return super(sale_order, self).copy(cr, uid, id, default, context=context)


    def action_view_delivery(self, cr, uid, ids, context=None):
        '''
        This function returns an action that display existing delivery orders of given sales order ids. It can either be a in a list or in a form view, if there is only one delivery order to show.
        '''
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        result = mod_obj.get_object_reference(cr, uid, 'stock', 'action_picking_tree')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        #compute the number of delivery orders to display
        pick_ids = []
        for so in self.browse(cr, uid, ids, context=context):
            pick_ids += [picking.id for picking in so.picking_ids]
        #choose the view_mode accordingly
        if len(pick_ids) > 1:
            result['domain'] = "[('id','in',["+','.join(map(str, pick_ids))+"])]"
        else:
            res = mod_obj.get_object_reference(cr, uid, 'stock', 'view_picking_out_form')
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = pick_ids and pick_ids[0] or False
        return result

class stock_picking_out(osv.osv):
    _inherit = 'stock.picking.out'
    _columns = {
        'sale_id': fields.many2one('sale.order', 'Sale Order',
            ondelete='set null', select=True),
    }










