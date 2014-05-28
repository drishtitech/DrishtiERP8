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



class hr_holidays(osv.osv):
    _name = "hr.holidays"
    _description = "HR Holidays"
    _inherit = "hr.holidays"
    _columns = {
	    'serial_no': fields.char('Serial No.', size=124),
        'leave_allocation_date':fields.date('Leave Allocation date',required=True),
		}
    
hr_holidays()

class hr_employee(osv.osv):
    _name = "hr.employee"
    _description = "HR Employee"
    _inherit = "hr.employee"
    _columns = {
       'category': fields.many2one('hr.employee.category',"Employee Category", size=124),       
      # 'identification_id': fields.integer('Identification No', size=124),
       'emergency_contact': fields.char('Emergency Contact No', size=124),
       'doj':fields.date('Date of Joining', size=124),
       'emoluments':fields.integer('Emoluments Rs.', size=124),
       'app_letter':fields.char('Appointment Letter No. & Date', size=124),
       'esic_no':fields.char('ESIC No.', size=124),
       'pf_no':fields.char('PF No. GOA/12411/', size=124),
       'aadhar_no':fields.char('Aadhar Card No.', size=124),
       'employment_exchange_no':fields.char('Employment Exchange No.', size=124),
       'blood_group':fields.selection([('A-ve','A-ve'),('B-ve','B-ve'),('AB-ve','AB-ve'),('O-ve','O-ve'),('A+ve','A+ve'),('B+ve','B+ve'),('AB+ve','AB+ve'),('O+ve','O+ve')],'Blood Group'),
       'father_name':fields.char("Father's Name", size=124),
       'employee_identification_proof_detail':fields.one2many("hr.employee.identification.detail",'employee_id',"Identification Proof Detail", size=124),
       'nominee':fields.char("Nominee (Next of Kin)", size=124),
       'relationship':fields.many2one('relation.name',"Relationship", size=124),
       'address':fields.text("Address", size=124),
       'telephone_no':fields.char("Telephone No. (Residence)", size=124),
       'mobile_no':fields.char("Mobile No.", size=124),
       
       'educational_qualification_line':fields.one2many('hr.employee.qualification','employee_id1',"Educational Qualification ", size=124),
       'professional_qualification_line':fields.one2many('hr.employee.qualification','employee_id2',"Professional Qualification ", size=124),
       'other_qualification_line':fields.one2many('hr.employee.qualification','employee_id3'," Other Qualification", size=124),
       'email_id':fields.char("Email ID", size=124),
       'distance':fields.integer("Distance from Residence to Work Place (in Kms.)", size=124),
       'permanent_address':fields.text("Permanent Address", size=124),
       'telephone_no1':fields.char("Telephone No.", size=124),
       'mobile_no1':fields.char("Mobile No.",size=124),
       'identification_marks':fields.char("Identification Marks", size=124),
       'height':fields.integer("Height", size=124),
       'weight':fields.integer("Weight", size=124),
       'complexion':fields.char("Complexion", size=124),
       'previous_job_history':fields.one2many("hr.employee.job.history",'employee_id','Previous Job History',size=124),
       'previous_job':fields.text("Job Description", size=124),
       'period':fields.char("Period", size=124),
       'reason_leaving':fields.text("Reason for leaving", size=124),
       'family_line':fields.one2many('family.details','family_id'," Family Particulars", size=124),
       'bank_name':fields.char("Name of Bank", size=124),
       'branch_name':fields.char("Branch", size=124),
       'bank_address':fields.text("Bank Address", size=124),
       'account_number':fields.integer("A/C No.", size=124),
       'ifsc':fields.char("IFSC", size=124),
       'code':fields.char("IFSC Code", size=124),
       'language_line':fields.one2many('language.details','language_id'," Language Proficiency ", size=124),
       'beach_line':fields.one2many('beach.lifeguard','beach_id'," Beach Lifeguard Details ", size=124),
       'jetski_line':fields.one2many('jetski.details','jetski_id'," Jetski (Surf Rescue) Operator ", size=124),
       'annual_line':fields.one2many('annual.assessment','annual_id'," Annual Assessment ", size=124),
       'achievement_line':fields.one2many('achievement.details','achievement_id'," Achievements/Certificates ", size=124),
       'offence_line':fields.one2many('offence.details','offence_id'," Offence Details ", size=124),
       'house_no':fields.char("House No./Flat No.", size=124),
       'ward':fields.char("Ward", size=124),
       'home_village':fields.char("Village/Town/City", size=124),
       'municipality':fields.char("Municipality/Gram Panchayat", size=124),
       'district':fields.selection([('North Goa', 'North Goa'),('South Goa','South Goa'),('Other','Other')],'District'),
       'constituency':fields.char("Constituency", size=124),
       'taluka':fields.many2one('taluka.name',"Taluka", size=124),
       'home_state_id':fields.many2one('res.country.state',"State", size=124),
       'post_office':fields.char("Post Office", size=124),
       'current_pincode':fields.char("Pincode", size=124),
       'landmark':fields.char("Landmark", size=124),
       'other':fields.char("Other", size=124),  
       'address_home_id': fields.many2one('res.partner', 'Home Address'),
       'gender': fields.selection([('male', 'male'),('female', 'female')], 'Gender'),
       'bank_account_id':fields.many2one('res.partner.bank', 'Bank Account Number', help="Employee bank salary account"),
       'current_country_id': fields.many2one('res.country', 'Nationality'),
       'identification_id1': fields.char('Employee Id No.', size=32),
#        'birth_state':fields.many2one('res.country.state','State',size=124),
#        'birth_city':fields.many2one('res.city','City',size=124,select=True,domain="[('state','=',birth_state)]"),
       'bank_bic': fields.char('Bank Identifier Code', size=32),
       'passport_id':fields.char('Passport No', size=64),
       'acc_number':fields.char('Account Number', size=124),
       'bank_account_id':fields.many2one('res.partner.bank', 'Bank Account Number', domain="[('partner_id','=',address_home_id)]", help="Employee bank salary account"),
       'otherid': fields.char('Other Id', size=64),
       'marital': fields.selection([('Unmarried', 'Unmarried'), ('Married', 'Married'), ('Widower', 'Widower'), ('Divorced', 'Divorced')], 'Marital Status'),
       'birthday': fields.date("Date of Birth"),
       'address_home_id': fields.many2one('res.partner', 'Home Address', invisible="True"),
       'bank_line': fields.one2many('res.partner.bank', 'bank_no', 'Bank Details'),
       'state': fields.related('bank_line', 'state', type='selection', size=240, string='Bank Account Type'),
       #'acc_number': fields.related('bank_line', 'acc_number', type='char', size=240, string='Account Number'),
       'bank_field':fields.many2one('res.bank', 'Bank'),
      # 'bank': fields.related('bank_line', 'bank', type='many2one', relation='res.bank', size=240, string='Bank '),
#        'company_id': fields.related('bank_line','company_id', relation='res.company', string='Company',
#             ondelete='cascade', help="Only if this bank account belong to your company"),
       'footer': fields.related('bank_line','footer', type="boolean", string='Display on Reports', help="Display this bank account on the footer of printed documents like invoices and sales orders."),
       'partner_id': fields.related('bank_line','partner_id',type="many2one",relation='res.partner', string='Account Owner', required=True,
            ondelete='cascade', select=True),
       'bank_account_name': fields.related('bank_line','name',type="char",string='Bank Account', size=64),
       #'bank_bic': fields.related('bank_line','bank_bic',type="char",string='Bank Identifier Code', size=16),
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
      'creation_date':fields.date("Date",required=True),
      'birthday':fields.date('Birth Date'),
      'place_of_birth':fields.char('Birth Place',size=124),
      'lifeguard':fields.boolean('Life Guard'),
      'current_street1':fields.char("Street1"),
      'current_street2':fields.char("Street2"),
      'home_landmark':fields.char("Landmark"),
      'current_landmark':fields.char("Landmark"),
      'current_city':fields.char("City"),
      'current_state_id':fields.many2one("res.country.state",'State'),
      'country_id':fields.many2one("res.country",'Country'),
      #'current_pincode':fields.char("Zip"),
      'emp_first_name':fields.char("First Name"),
      'emp_middle_name':fields.char("Middle Name"),
      'emp_last_name':fields.char("Last Name"),
      'marrage_date':fields.date("Marriage date"),
      'no_of_children':fields.integer("Number of children"),
      'goa_employee':fields.boolean("Goa Employee"),
      'same_current_address':fields.boolean("Same as above address"),
      'home_street1':fields.char("Street1"),
      'home_street2':fields.char("Street2"),
      'home_pin_code':fields.char("Zip"),
      'home_country_id': fields.many2one('res.country', 'Nationality'),

      

        }
    
    
    _defaults={
               
               
               'creation_date': time.strftime('%Y-%m-%d'),
               'lifeguard':True
               
               }
           
    def _check_birth_date(self, cr, uid, ids, context=None):
        for date in self.read(cr,uid,ids,['birthday','creation_date'],context=None):
                #bday = datetime.strptime(date['birthday'],'%Y-%m-%d')
            if date['birthday']:
                dob=date['birthday']
                dob_year = int(dob[:4])
                print ">>>>>>>>>>>>>>>>>dob year>>>>>>>>>>>>>>>>",dob_year
                
                current_date=date['creation_date']
                current_year= int(current_date[:4])
                print ">>>>>>>>>>>>>>>>>>current year>>>>>>>>>>>>>>>>",current_year
                
                age=current_year-dob_year
                print "age>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",age
                print type(date['birthday'])
                
                if date['birthday'] and date['creation_date'] and date['creation_date']<=date['birthday']:
                        
                        return False
                    
                if age<18:
                        return False
            else:
                pass
        return True
    
    _constraints=[(_check_birth_date,'Error!birth date must be 18 years and lesser than current date.',['birthday','creation_date'])] 
    
    
    def onchange_same_current_address(self, cr, uid,ids,same_current_address,street1,street2,current_city,Current_state_id,pincode,landmark):
         
        return {'value':{'same_current_address':same_current_address,'street':street1,'landmark1':landmark,'street3':street2,'village':current_city,'state_name':Current_state_id,'zip_code':pincode}}
 
    def onchange_name(self, cr, uid,ids,emp_first_name,emp_middle_name,emp_last_name):
        name = ''
        if emp_first_name:
            name += emp_first_name
        if emp_middle_name:
            name += ' ' +emp_middle_name
        if emp_last_name:
            name += ' ' +emp_last_name    
        
        return {'value':{'name':name}}
    

    
   
    def onchange_bank_id(self, cr, uid, ids, bank_id, context=None):
        result = {}
        if bank_id:
            bank = self.pool.get('res.bank').browse(cr, uid, bank_id, context=context)
            result['bank_name'] = bank.name
            result['bank_bic'] = bank.bic
            
        return {'value': result}

    
    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        result = {}
        if partner_id:
            part = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            result['owner_name'] = part.name
            result['street'] = part.street or False
            result['street1'] = part.city or False
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
    _name = "hr.employee.qualification"
    _description = "Educational Qualifications"
    _columns = {
        'employee_id1': fields.many2one("hr.employee",'Employee Name(Educational)'),
        'employee_id2': fields.many2one("hr.employee",'Employee Name(Professional)'),
        'employee_id3': fields.many2one("hr.employee",'Employee Name(Other)'),
        'degree':fields.many2one('hr.employee.academic.degree','Degree'),
        'specialization':fields.many2one('hr.employee.academic.degree.division','specialization'),
        'institute':fields.char('Institute', size=124),
        'board': fields.char('University/Board', size=124),
        'marks': fields.char('% Marks', size=124),
        'year': fields.char('Year of Completion', size=124),

        }

qualification_details1()


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

class beach_lifeguard(osv.osv):
    _name = "beach.lifeguard"
    _description = "Beach Lifeguard"
    _columns = {
        'beach_id': fields.integer('Beach No.', size=124),
        'sl_no':fields.integer('Sl No.', size=124),
        'slsg_no':fields.integer('SLSG No', size=124),
        'name': fields.char('Name', size=124),
        'swim': fields.char('40 mtr. Swim', size=124),
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

class hr_employee_job_history(osv.osv):
    
    _name = "hr.employee.job.history"
    
    _columns = {
                
                'employee_id':fields.many2one('hr.employee','Previous job History',required=True),
                'name':fields.char("Previouse Employee Name",required=True),
                'designation':fields.char("Designation",required=True),
                'joining_date':fields.date("Date of Joining",required=True),
                'total_exp':fields.integer("Total Experience(In Months)",required=True),
                'change_reason':fields.char("Reason For change",required=True)
                
                }

class hr_employee_identification_detail(osv.osv):
    
    _name = "hr.employee.identification.detail"
    
    _columns = {
                
               'employee_id':fields.many2one("hr.employee",'Employee'),
               'name':fields.selection([('driving_licence','Driving License'),('aadhar_card','Aadhar Card'),('pan_card','Pan Card'),('voter_id_card','Voter Id Card'),('other','Other')],'Identification Name'),
               'number':fields.char("Identification Number"), 
               'document_no':fields.integer("Document No"),
               'attachment':fields.many2one('ir.attachment',"Attachment"),
               'document_purpose':fields.char("Document Purpose")
               
                
                }
    
class hr_employee_academic_degree(osv.osv):
    
    _name= "hr.employee.academic.degree" 
    _columns = {
                'name':fields.char("Name",required =  True),
                'code':fields.char("Code",required= True)
                
                }
class hr_employee_academic_degree_division(osv.osv):
    
    _name= "hr.employee.academic.degree.division" 
    _columns = {
                'name':fields.char("Name",required =  True),
                'code':fields.char("Code",required= True)
                
                }
