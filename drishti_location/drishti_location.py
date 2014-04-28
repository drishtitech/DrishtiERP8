import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import fields,osv
from openerp.tools.translate import _

##======================================================================
# Inherit res.users for adding location_id field
##======================================================================

class res_users(osv.osv):
      _inherit = 'res.users'
      _columns = {
                  #'location_view_id': fields.many2one('stock.location', 'User Location View', help="Select Location base on user permission"),
                   'loc_id': fields.many2one('stock.location', 'Location', help="Select Location base on user permission"),
                  'location_id': fields.many2one('stock.location', 'User Location', help="Select Location base on user permission"),
                  'src_loc_id': fields.many2one('stock.location', 'Source Location'),
                  'location_ids':fields.many2many('stock.location','stock_location_users_rel','user_id','lid','Allowed Locations'),                   
                 }

##==============================================================================
# Overrite existing search method in stock.location base on user assign location
##==============================================================================

class stock_location(osv.osv):
    _inherit = 'stock.location'
    
    _columns = {
                'beach' : fields.boolean('Beach Location'),
                'sequence_id': fields.many2one('ir.sequence', 'Sequence',),
                }
    
    def name_get(self, cr, uid, ids, context=None):
        # always return the full hierarchical name
        res = self._complete_name(cr, uid, ids, 'complete_name', None, context=context)
        return res.items()

    def _complete_name(self, cr, uid, ids, name, args, context=None):
        """ Forms complete name of location from parent location to child location.
        @return: Dictionary of values
        """
        res = {}
        for m in self.browse(cr, uid, ids, context=context):
            names = [m.name]
#             parent = m.location_id
#             while parent:
#                 names.append(parent.name)
#                 parent = parent.location_id
            res[m.id] = ' / '.join(reversed(names))
        return res
    
    
#     def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
#         if not args:
#             args = []
#         user_obj = self.pool.get('res.users').browse(cr, user, user, context)
#         #if context and (context.get('search_default_in_location111', False) or context.get('filter_locaion_id1', False)):
#         user_obj = self.pool.get('res.users').browse(cr, user, user, context)    
#         ids = self.search(cr, user, [('id', 'in', [l.id for l in user_obj.location_ids])]+ args, limit=limit, context=context)
#         #ids += self.search(cr, user, [('name', operator, name)]+ args, limit=limit, context=context)
#         return self.name_get(cr, user, ids, context)
#     
#     def name_get(self, cr, uid, ids, context=None):
#         if not ids:
#             return []
#         if isinstance(ids, (int, long)):
#                     ids = [ids]
#         reads = self.read(cr, uid, ids, ['name'], context=context)
#         res = []
#         for record in reads:
#             name = record['name']
#             
#             res.append((record['id'], name))
#         return res
      
#     def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
#       print "context4",context
#       user_obj = self.pool.get('res.users').browse(cr, uid, uid, context)
#       if context and (context.get('search_default_in_location111', False) or context.get('filter_locaion_id1', False)):
#           user_obj = self.pool.get('res.users').browse(cr, uid, uid, context)
#           print "test", [l.id for l in user_obj.location_ids]
#           if user_obj.location_ids:
#                 return super(stock_location, self).search(cr, uid, [('id', 'in', [l.id for l in user_obj.location_ids])], context=context)
#         
#             #return super(stock_location, self).search(cr, uid, [('id', '=', user_obj.location_id.id)], context=context)      
#       return super(stock_location, self).search(cr, uid, args, offset, limit, order, context, count)
               
class product_product(osv.osv):
       _inherit = 'product.product'
       
       def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
         print "context1",context
         if context is None:
            context = {}
         if  context and context.get('filter_locaion_id1', False):  
            user_obj = self.pool.get('res.users').browse(cr, uid, uid, context)
            if user_obj.location_id:  
                 location_ids = self.pool.get('stock.location').search(cr, uid, [('id', '=', user_obj.location_id.id)], context=context)
                 
                 context = {'location': location_ids}
                    
                 return super(product_product, self).search(cr, uid, args, offset=offset, limit=limit, order=order, context=context, count=False)
         print "context2",context      
         return super(product_product, self).search(cr, uid, args, offset=offset, limit=limit, order=order, context=context, count=False)              
        
        
      
