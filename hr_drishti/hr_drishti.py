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
##############################################################################

#from osv import fields, osv
#from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
#import pooler


class hr_holidays(osv.osv):
    _name = "hr.holidays"
    _description = "HR Holidays"
    _inherit = "hr.holidays"
    _columns = {
	    'serial_no': fields.char('Serial No.', size=124),
        'category': fields.many2one('hr.employee.category',"Employee Category", size=124),
		}
    
    def holidays_first_validate(self, cr, uid, ids, context=None):
        
        self.check_holidays(cr, uid, ids, context=context)
        obj_emp = self.pool.get('hr.employee')
        ids2 = obj_emp.search(cr, uid, [('user_id', '=', uid)])
        manager = ids2 and ids2[0] or False
        self.holidays_first_validate_notificate(cr, uid, ids, context=context)
        return self.write(cr, uid, ids, {'state':'validate1', 'manager_id': manager})
    
    def holidays_validate(self, cr, uid, ids, context=None):
        
        for d in self.browse(cr, uid, ids, context=None):
            employee=d.employee_id.id
            user_id=d.employee_id.user_id.id
            
            
            if user_id==uid:
                
                raise osv.except_osv(('Error!!'),('You cannot approve your own leave'))
        self.check_holidays(cr, uid, ids, context=context)
        obj_emp = self.pool.get('hr.employee')
        ids2 = obj_emp.search(cr, uid, [('user_id', '=', uid)])
        manager = ids2 and ids2[0] or False
        self.write(cr, uid, ids, {'state':'validate'})
        data_holiday = self.browse(cr, uid, ids)
        for record in data_holiday:
            if record.double_validation:
                self.write(cr, uid, [record.id], {'manager_id2': manager})
            else:
                self.write(cr, uid, [record.id], {'manager_id': manager})
            if record.holiday_type == 'employee' and record.type == 'remove':
                meeting_obj = self.pool.get('crm.meeting')
                meeting_vals = {
                    'name': record.name or _('Leave Request'),
                    'categ_ids': record.holiday_status_id.categ_id and [(6,0,[record.holiday_status_id.categ_id.id])] or [],
                    'duration': record.number_of_days_temp * 8,
                    'description': record.notes,
                    'user_id': record.user_id.id,
                    'date': record.date_from,
                    'end_date': record.date_to,
                    'date_deadline': record.date_to,
                    'state': 'open',            # to block that meeting date in the calendar
                }
                meeting_id = meeting_obj.create(cr, uid, meeting_vals)
                self._create_resource_leave(cr, uid, [record], context=context)
                self.write(cr, uid, ids, {'meeting_id': meeting_id})
            elif record.holiday_type == 'category':
                emp_ids = obj_emp.search(cr, uid, [('category_ids', 'child_of', [record.category_id.id])])
                leave_ids = []
                for emp in obj_emp.browse(cr, uid, emp_ids):
                    vals = {
                        'name': record.name,
                        'type': record.type,
                        'holiday_type': 'employee',
                        'holiday_status_id': record.holiday_status_id.id,
                        'date_from': record.date_from,
                        'date_to': record.date_to,
                        'notes': record.notes,
                        'number_of_days_temp': record.number_of_days_temp,
                        'parent_id': record.id,
                        'employee_id': emp.id
                    }
                    leave_ids.append(self.create(cr, uid, vals, context=None))
                wf_service = netsvc.LocalService("workflow")
                for leave_id in leave_ids:
                    wf_service.trg_validate(uid, 'hr.holidays', leave_id, 'confirm', cr)
                    wf_service.trg_validate(uid, 'hr.holidays', leave_id, 'validate', cr)
                    wf_service.trg_validate(uid, 'hr.holidays', leave_id, 'second_validate', cr)
        return True
    
    def holidays_confirm(self, cr, uid, ids, context=None):
        self.check_holidays(cr, uid, ids, context=context)
        for record in self.browse(cr, uid, ids, context=context):
            if record.employee_id or record.employee_id.parent_id or record.employee_id.parent_id.user_id:
                self.message_subscribe_users(cr, uid, [record.id], user_ids=[record.employee_id.user_id.id or record.employee_id.parent_id.user_id.id], context=context)
        return self.write(cr, uid, ids, {'state': 'confirm'})

    
hr_holidays()

class hr_employee(osv.osv):
    _name = "hr.employee"
    _description = "HR Employee"
    _inherit = "hr.employee"
    _columns = {
       'category': fields.many2one('hr.employee.category',"Employee Category", size=124),       
      
       'emergency_contact': fields.char('Emergency Contact No', size=124),
       'doj':fields.date('Date of Joining', size=124),
       'emoluments':fields.integer('Emoluments Rs.', size=124),
       'app_letter':fields.char('Appointment Letter No. & Date', size=124),
       'esic_no':fields.char('ESIC No.', size=124),
       'pf_no':fields.char('PF No. GOA/12411/', size=124),
       'aadhar_no':fields.char('Aadhar Card No.', size=124),
       'employment_exchange_no':fields.char('Employment Exchange No.', size=124),
       'blood_group':fields.char('Blood Group', size=124),
       'father_name':fields.char("Father's Name", size=124),
       'driving_license_no':fields.char("Driving License No", size=124),
       'nominee':fields.char("Nominee (Next of Kin)", size=124),
       'relationship':fields.many2one('relation.name',"Relationship", size=124),
       'address':fields.text("Address", size=124),
       'telephone_no':fields.char("Telephone No. (Residence)", size=124),
       'mobile_no':fields.char("Mobile No.", size=124),
       'educational_qualification_line':fields.one2many('qualification.details1','qualification_id1'," ", size=124),
       'professional_qualification_line':fields.one2many('qualification.details2','qualification_id2'," ", size=124),
       'other_qualification_line':fields.one2many('qualification.details3','qualification_id3'," ", size=124),
       'email_id':fields.char("Email ID", size=124),
       'distance':fields.char("Distance from Residence to Work Place (in Kms.)", size=124),
       'permanent_address':fields.text("Permanent Address", size=124),
       'telephone_no1':fields.char("Telephone No.", size=124),
       'mobile_no1':fields.char("Mobile No."),
       'identification_marks':fields.char("Identification Marks", size=124),
       'height':fields.integer("Height", size=124),
       'weight':fields.integer("Weight", size=124),
       'complexion':fields.char("Complexion", size=124),
       'previous_employer':fields.char("Previous Employer", size=124),
       'previous_job':fields.text("Job Description", size=124),
       'period':fields.char("Period", size=124),
       'reason_leaving':fields.text("Reason for leaving", size=124),
       'family_line':fields.one2many('family.details','family_id'," ", size=124),
       'bank_name':fields.char("Name of Bank", size=124),
       'branch_name':fields.char("Branch", size=124),
       'bank_address':fields.text("Bank Address", size=124),
       'account_number':fields.integer("A/C No.", size=124),
       'ifsc':fields.char("IFSC", size=124),
       'code':fields.char("IFSC Code", size=124),
       'language_line':fields.one2many('language.details','language_id'," ", size=124),
       'beach_line':fields.one2many('beach.lifeguard','beach_id'," ", size=124),
       'jetski_line':fields.one2many('jetski.details','jetski_id'," ", size=124),
       'annual_line':fields.one2many('annual.assessment','annual_id'," ", size=124),
       'achievement_line':fields.one2many('achievement.details','achievement_id'," ", size=124),
       'offence_line':fields.one2many('offence.details','offence_id'," ", size=124),
       'house_no':fields.char("House No./Flat No.", size=124),
       'ward':fields.char("Ward", size=124),
       'village':fields.char("Village/Town", size=124),
       'municipality':fields.char("Municipality/Gram Panchayat", size=124),
       'district':fields.selection([('a', 'North Goa'),('b','South Goa'),('c','Other')],'District'),
       'constituency':fields.char("Constituency", size=124),
       'taluka':fields.many2one('taluka.name',"Taluka", size=124),
       'state_name':fields.many2one('state.name',"State", size=124),
       'post_office':fields.char("Post Office", size=124),
       'pincode':fields.char("Pincode", size=124),
       'landmark':fields.char("Landmark", size=124),
       'other':fields.char("Other", size=124),  
       'address_home_id': fields.many2one('res.partner', 'Home Address'),
       'gender': fields.selection([('male', 'Male'),('female', 'Female')], 'Gender'),
       'bank_account_id':fields.many2one('res.partner.bank', 'Bank Account Number', help="Employee bank salary account"),
       'country_id': fields.many2one('res.country', 'Nationality'),
      
       'place_of_birth': fields.char('Place of Birth', size=32),
       'bank_bic': fields.char('Bank Identifier Code', size=32),
       'passport_id':fields.char('Passport No', size=64),
       'acc_number':fields.char('Account Number', size=64),
       'bank_account_id':fields.many2one('res.partner.bank', 'Bank Account Number', domain="[('partner_id','=',address_home_id)]", help="Employee bank salary account"),
       'otherid': fields.char('Other Id', size=64),
       'marital': fields.selection([('single', 'Single'), ('married', 'Married'), ('widower', 'Widower'), ('divorced', 'Divorced')], 'Marital Status'),
       'birthday': fields.date("Date of Birth"),
       'address_home_id': fields.many2one('res.partner', 'Home Address', invisible="True"),
       'bank_line': fields.one2many('res.partner.bank', 'bank_no', 'Bank Details'),
       'state': fields.related('bank_line', 'state', type='selection', size=240, string='Bank Account Type'),
       
       'bank_field':fields.many2one('res.bank', 'Bank'),
      
       'footer': fields.related('bank_line','footer', type="boolean", string='Display on Reports', help="Display this bank account on the footer of printed documents like invoices and sales orders."),
       'partner_id': fields.related('bank_line','partner_id',type="many2one",relation='res.partner', string='Account Owner', required=True,
            ondelete='cascade', select=True),
       'bank_account_name': fields.related('bank_line','name',type="char",string='Bank Account', size=64),
      
       'bank_name': fields.related('bank_line','bank_name',type="char",string='Bank Name', size=32),
       'owner_name': fields.related('bank_line','bank_name',type="char",string='Account Owner Name', size=128),
       'street': fields.related('bank_line','bank_name',type="char",string='Street', size=128),
       'zip': fields.related('bank_line','zip',type="char",string='Zip', change_default=True, size=24),
       'city': fields.related('bank_line','city',type="char",string='City', size=128),
       'country_id1': fields.related('bank_line','country_id',type="many2one",relation='res.country',string='Country',
            change_default=True),
       'state_id': fields.related('bank_line','state_id',type='many2one',relation='res.country.state', string='Fed. State',
            change_default=True, domain="[('country_id','=',country_id)]"),
       'sequence': fields.related('bank_line','sequence',type="integer",string='Sequence'),
       'attachment_line':fields.one2many('ir.attachment','attachment_id','Attachments', size=124),
      'attendance':fields.boolean('Attendance'),
    
         
        }
    
    def onchange_bank_id(self, cr, uid, ids, bank_id, context=None):
        result = {}
        if bank_id:
            bank = self.pool.get('res.bank').browse(cr, uid, bank_id, context=context)
            result['bank_name'] = bank.name
            result['bank_bic'] = bank.bic
        return {'value': result}

    
    def onchange_partner_id(self, cr, uid, id, partner_id, context=None):
        result = {}
        if partner_id:
            part = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            result['owner_name'] = part.name
            result['street'] = part.street or False
            result['city'] = part.city or False
            result['zip'] =  part.zip or False
            result['country_id'] =  part.country_id.id
            result['state_id'] = part.state_id.id
        return {'value': result}
    
    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        result = {}
        if company_id:
            c = self.pool.get('res.company').browse(cr, uid, company_id, context=context)
            if c.partner_id:
                r = self.onchange_partner_id(cr, uid, ids, c.partner_id.id, context=context)
                r['value']['partner_id'] = c.partner_id.id
                r['value']['footer'] = 1
                result = r
        return result


    
hr_employee()

class res_partner_bank(osv.osv):
    _name = "res.partner.bank"
    _description = "Bank Details"
    _inherit = "res.partner.bank"
    _columns = {
        'bank_no': fields.many2one('hr.employee','Bank No.', size=124),
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



class qualification_details1(osv.osv):
    _name = "qualification.details1"
    _description = "Educational Qualifications"
    _columns = {
        'qualification_id1': fields.integer('Qualification No.', size=124),
        'degree':fields.char('Degree', size=124),
        'institute':fields.char('Institute', size=124),
        'board': fields.char('University/Board', size=124),
        'marks': fields.char('% Marks', size=124),
        'year': fields.char('Year of Completion', size=124),

        }

qualification_details1()

class qualification_details2(osv.osv):
    _name = "qualification.details2"
    _description = "Professional Qualifications"
    _columns = {
        'qualification_id2': fields.integer('Qualification No.', size=124),
        'degree':fields.char('Degree', size=124),
        'institute':fields.char('Institute', size=124),
        'board': fields.char('University/Board', size=124),
        'marks': fields.char('% Marks', size=124),
        'year': fields.char('Year of Completion', size=124),

        }

qualification_details2()

class qualification_details3(osv.osv):
    _name = "qualification.details3"
    _description = "Other Qualifications"
    _columns = {
        'qualification_id3': fields.integer('Qualification No.', size=124),
        'degree':fields.char('Degree', size=124),
        'institute':fields.char('Institute', size=124),
        'board': fields.char('University/Board', size=124),
        'marks': fields.char('% Marks', size=124),
        'year': fields.char('Year of Completion', size=124),

        }

qualification_details3()

class family_details(osv.osv):
    _name = "family.details"
    _description = "Family Details"
    _columns = {
        'family_id': fields.integer('Family No.', size=124),
        'name':fields.char('Name', size=124),
        'relation':fields.many2one('relation.name','Relation', size=124),
        'date_of_birth': fields.date('Date of Birth', size=124),
        'age': fields.integer('Age', size=124),
        'occupation': fields.char('Occupation', size=124),

        }

family_details()

class language_details(osv.osv):
    _name = "language.details"
    _description = "Language Details"
    _columns = {
        'language_id': fields.integer('Language No.', size=124),
        'name':fields.many2one('language.name','Language', size=124),
        'proficiency':fields.selection([('yes', 'Yes'),('no','No')],'Proficiency'),
        'read': fields.selection([('yes', 'Yes'),('no','No')],'Read'),
        'write': fields.selection([('yes', 'Yes'),('no','No')],'Write'),
        'speak': fields.selection([('yes', 'Yes'),('no','No')],'Speak'),

        }

language_details()

class language_name(osv.osv):
    _name = "language.name"
    _description = "Language"
    _columns = {
        'name':fields.char('Language', size=124),

        }

language_name()

class taluka_name(osv.osv):
    _name = "taluka.name"
    _description = "Taluka"
    _columns = {
        'name':fields.char('Taluka', size=124),

        }

taluka_name()

class relation_name(osv.osv):
    _name = "relation.name"
    _description = "Relation"
    _columns = {
        'name':fields.char('Relation', size=124),

        }

relation_name()


class state_name(osv.osv):
    _name = "state.name"
    _description = "State"
    _columns = {
        'name':fields.char('State', size=124),

        }

state_name()



class beach_lifeguard(osv.osv):
    _name = "beach.lifeguard"
    _description = "Beach Lifeguard"
    _columns = {
        'beach_id': fields.integer('Beach No.', size=124),
        'sl_no':fields.integer('Sl No.', size=124),
        'slsg_no':fields.integer('SLSG No', size=124),
        'name': fields.char('Name', size=124),
        'swim': fields.char('400 mtr. Swim', size=124),
        'rsr': fields.char('RSR', size=124),
        'uw': fields.char('25 mtr. U/W', size=124),
        'bt':fields.char('BT', size=124),
        'jump':fields.char('5 mtr. Jump', size=124),
        'rescue_tube': fields.char('Rescue Tube', size=124),
        'rescue_board': fields.char('Rescue Board', size=124),
        'spine_board': fields.char('Spine Board', size=124),
        'cpr': fields.char('CPR', size=124),
        'fa':fields.char('FA', size=124),
        'aed':fields.char('AED', size=124),
        'o2': fields.char('O2', size=124),
        'cert_date': fields.date('Cert Date', size=124),
        'result': fields.char('Result', size=124),



        }

beach_lifeguard()

class jetski_details(osv.osv):
    _name = "jetski.details"
    _description = "Jetski (Surf Rescue) Operator"
    _columns = {
        'jetski_id': fields.integer('Jetski ID', size=124),
        'sr_no': fields.integer('Sr. No.', size=124),
        'slsg_code':fields.integer('SLSG Code', size=124),
        'name':fields.char('Name', size=124),
        'date_of_test': fields.date('Date of Test', size=124),
        'ops_checks': fields.char('Pre/post ops checks', size=124),
        'confined_space_manevur': fields.char('Confined Space Manevur', size=124),
        'cap_size_drill': fields.char('Cap size Drill', size=124),
        'engine_cut_off_drill': fields.char('Engine Cut Off Drill', size=124),
        'patient_recovery': fields.char('Patient Recovery', size=124),
        'parallel_drill': fields.char('Parallel Drill', size=124),
        'ins_outs': fields.char('Ins/Outs', size=124),
        'result': fields.char('Result', size=124),

        }

jetski_details()

class annual_assessment(osv.osv):
    _name = "annual.assessment"
    _description = "Annual Assessment"
    _columns = {
        'annual_id': fields.integer('Assessment No.', size=124),
        'efficiency':fields.text('Suggested Efficiency'),
        'date':fields.date('Date', size=124),
        'by_whom': fields.char('By whom', size=124),

        }

annual_assessment()

class achievement_details(osv.osv):
    _name = "achievement.details"
    _description = "Achievement/Certificates"
    _columns = {
        'achievement_id': fields.integer('Achievement No.', size=124),
        'date': fields.date('Date', size=124),
        'incident_reference':fields.text('Incident Reference'),
        'remarks':fields.text('Remarks'),

        }

achievement_details()

class offence_details(osv.osv):
    _name = "offence.details"
    _description = "Record of Offences"
    _columns = {
        'offence_id': fields.integer('Offence No.', size=124),
        'date': fields.date('Date', size=124),
        'offence_description':fields.text('Offence Description'),
        'punishment':fields.text('Punishment Awarded'),

        }

offence_details()






