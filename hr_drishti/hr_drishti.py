# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################git add -A


from openerp import addons
from datetime import datetime, timedelta
from dateutil import relativedelta
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
import time


class mail_compose_message(osv.osv):
    _inherit = "mail.compose.message"
    
    def send_mail1(self, cr, uid, ids, context=None):
        """ Process the wizard content and proceed with sending the related
            email(s), rendering any template patterns on the fly if needed. """
        if context is None:
            context = {}

        # clean the context (hint: mass mailing sets some default values that
        # could be wrongly interpreted by mail_mail)
        context.pop('default_email_to', None)
        context.pop('default_partner_ids', None)

        for wizard in self.browse(cr, uid, ids, context=context):
            print "wizard.composition_mode ",wizard.composition_mode 
            mass_mode = wizard.composition_mode in ('mass_mail', 'mass_post')
            active_model_pool = self.pool[wizard.model if wizard.model else 'mail.thread']
            if not hasattr(active_model_pool, 'message_post'):
                context['thread_model'] = wizard.model
                active_model_pool = self.pool['mail.thread']

            # wizard works in batch mode: [res_id] or active_ids or active_domain
            if mass_mode and wizard.use_active_domain and wizard.model:
                res_ids = self.pool[wizard.model].search(cr, uid, eval(wizard.active_domain), context=context)
            elif mass_mode and wizard.model and context.get('active_ids'):
                res_ids = context['active_ids']
            else:
                res_ids = [wizard.res_id]

            sliced_res_ids = [res_ids[i:i + self._batch_size] for i in range(0, len(res_ids), self._batch_size)]
            for res_ids in sliced_res_ids:
                all_mail_values = self.get_mail_values(cr, uid, wizard, res_ids, context=context)
                for res_id, mail_values in all_mail_values.iteritems():
                    
                        mail_id = self.pool['mail.mail'].create(cr, uid, mail_values, context=context)
                        self.pool['mail.mail'].send(cr,uid,[mail_id])

        return {'type': 'ir.actions.act_window_close'}
    



class res_partner_bank(osv.osv):
    _name = "res.partner.bank"
    _description = "Bank Details"
    _inherit = "res.partner.bank"
    _columns = {
        'bank_no': fields.many2one('hr.employee','Bank No.', size=124),
        }

res_partner_bank()


class res_bank(osv.osv):
    _name = "res.bank"
    _description = "Branch Details"
    _inherit = "res.bank"
    _columns = {
        'branch_name': fields.char('Branch name'),
        }

res_partner_bank()



class ir_attachment(osv.osv):
    _name = "ir.attachment"
    _description = "Attachments"
    _inherit = "ir.attachment"
    _columns = {
        'attachment_id': fields.many2one('hr.employee','Attachments', size=124),
        }

ir_attachment()



