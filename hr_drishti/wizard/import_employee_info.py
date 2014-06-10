from openerp.osv import fields, osv
#from tools.translate import _
import StringIO
import cStringIO
import base64
import xlrd
import string
import calendar
from calendar import monthrange
from datetime import datetime
import datetime



class attendance_import(osv.osv_memory):
    _inherit='attendance.import'
    
    def import_employees(self,cr,uid,ids,context=None):
        
        
        print "uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu"
        cur_obj = self.browse(cr,uid,ids)[0]
        file_data=cur_obj.file
        val=base64.decodestring(file_data)
        fp = StringIO.StringIO()
        fp.write(val)     
        wb = xlrd.open_workbook(file_contents=fp.getvalue())
        sheet=wb.sheet_by_index(0)
        
        
        
        for i in range(1,sheet.nrows):
            emp_deatil={}
            emp_code =sheet.row_values(i,0,sheet.ncols)[1]
            emp_name =sheet.row_values(i,0,sheet.ncols)[2]
            #emp_site =sheet.row_values(i,0,sheet.ncols)[3]
            tag =sheet.row_values(i,0,sheet.ncols)[3]
            emp_designation =sheet.row_values(i,0,sheet.ncols)[4]
            emp_department =sheet.row_values(i,0,sheet.ncols)[5]
            emp_epf_no =sheet.row_values(i,0,sheet.ncols)[6] 
            if emp_epf_no=='NA':
                emp_epf_no=str(emp_epf_no)
            elif emp_epf_no=='':
                emp_epf_no=str(emp_epf_no)
            else:
                emp_epf_no =str(int(emp_epf_no))
  
            #reason_for_leaving =sheet.row_values(i,0,sheet.ncols)[10]
            dt_of_joining =str(sheet.row_values(i,0,sheet.ncols)[11])
            dt_of_birth =str(sheet.row_values(i,0,sheet.ncols)[12])
            father_name =sheet.row_values(i,0,sheet.ncols)[14]
            pincode =sheet.row_values(i,0,sheet.ncols)[18] and str(int(sheet.row_values(i,0,sheet.ncols)[18]))
            city =sheet.row_values(i,0,sheet.ncols)[17]
            mobile_no =sheet.row_values(i,0,sheet.ncols)[19] and str(sheet.row_values(i,0,sheet.ncols)[19])
            gender =sheet.row_values(i,0,sheet.ncols)[44]
            gender=gender.lower()
            country =sheet.row_values(i,0,sheet.ncols)[63]
            bank_name =sheet.row_values(i,0,sheet.ncols)[98]
            branch_name=sheet.row_values(i,0,sheet.ncols)[99]
            bank_code=sheet.row_values(i,0,sheet.ncols)[100]
            company_name=sheet.row_values(i,0,sheet.ncols)[101]
            address =sheet.row_values(i,0,sheet.ncols)[16]
            blood_group =sheet.row_values(i,0,sheet.ncols)[21]
            active =sheet.row_values(i,0,sheet.ncols)[37]
            emp_mail =sheet.row_values(i,0,sheet.ncols)[26]
            work_phone =sheet.row_values(i,0,sheet.ncols)[27]
            work_mobile =sheet.row_values(i,0,sheet.ncols)[28]
            office_location =sheet.row_values(i,0,sheet.ncols)[29]
            reason =sheet.row_values(i,0,sheet.ncols)[10]
            other_info =sheet.row_values(i,0,sheet.ncols)[34]
            company_vehicle =sheet.row_values(i,0,sheet.ncols)[39]
            work_distance =sheet.row_values(i,0,sheet.ncols)[40]
            
            adhar_no =sheet.row_values(i,0,sheet.ncols)[43]
            martial_status =sheet.row_values(i,0,sheet.ncols)[45]
            service_remark =sheet.row_values(i,0,sheet.ncols)[22]
            place_of_birth =sheet.row_values(i,0,sheet.ncols)[46]
            district = sheet.row_values(i,0,sheet.ncols)[56]
            post_office =sheet.row_values(i,0,sheet.ncols)[60]
            constituency =sheet.row_values(i,0,sheet.ncols)[57]
            emp_taluka =sheet.row_values(i,0,sheet.ncols)[58]
            emp_state = sheet.row_values(i,0,sheet.ncols)[59]
            nominee_name = sheet.row_values(i,0,sheet.ncols)[76]
            nominee_address =sheet.row_values(i,0,sheet.ncols)[78]
            nominee_phone =sheet.row_values(i,0,sheet.ncols)[79]
            nominee_relationship =sheet.row_values(i,0,sheet.ncols)[77]
            
            if bank_name=='HDFC Bank':
                bank_account_no =sheet.row_values(i,0,sheet.ncols)[97] and str(int(sheet.row_values(i,0,sheet.ncols)[97]))
            else:
                bank_account_no=sheet.row_values(i,0,sheet.ncols)[7] and str(int(sheet.row_values(i,0,sheet.ncols)[7]))
                
            esic_no =sheet.row_values(i,0,sheet.ncols)[8] 
            if esic_no=='NA':
                esic_no=str(esic_no)
            elif esic_no=='':
                esic_no=str(esic_no)
            elif esic_no=='YES':
                esic_no=str(esic_no)
            else:
                esic_no =str(int(esic_no))
  
            driving_licence_no = sheet.row_values(i,0,sheet.ncols)[42] and str(sheet.row_values(i,0,sheet.ncols)[42])
             
            if dt_of_joining:
                print'/////dt_of_joining==================/////',dt_of_joining
                dt_of_joining=datetime.datetime.strptime(dt_of_joining,"%m/%d/%Y").date()
                emp_deatil['doj']=dt_of_joining
                
            if dt_of_birth:
                print'===========dt_of_birth=================',dt_of_birth,
                dt_of_birth=datetime.datetime.strptime(dt_of_birth,"%d/%m/%Y").date()
                emp_deatil['birthday']=dt_of_birth
            
            employee_id = self.pool.get('hr.employee').search(cr,uid,[('identification_id1','=',emp_code)])
            print employee_id, "EMPLOYEE-ID !!!!!!!!!!!!!!!",emp_code
            print company_name, "COMPANY NAME !!!!!!!!!!"
            
            position = self.pool.get('hr.job').search(cr,uid,[('name','=',emp_designation)])
            print position, "POSITION ARRAY.............."
            for jl in self.pool.get('hr.job').browse(cr,uid,position):
                position=jl.id
                print position,"POSITION-ID..........."
            if not position:
                position= self.pool.get('hr.job').create(cr,uid,{'name': emp_designation})
                print position, "POSITION-ID..........."
                
            emp_tag = self.pool.get('hr.employee.category').search(cr,uid,[('name','=',tag)])
            print emp_tag, "TAG ARRAY.............."
            for tl in self.pool.get('hr.employee.category').browse(cr,uid,emp_tag):
                tag_id=tl.id
                print tag_id,"TAG-NAME..........."
            if not emp_tag:
                tag_id= self.pool.get('hr.employee.category').create(cr,uid,{'name': tag})
                print tag_id, "TAG-ID..........."    
                
            department = self.pool.get('hr.department').search(cr,uid,[('name','=',emp_department)])
            print department, "DEPARTMENT ARRAY.............."
            for pl in self.pool.get('hr.department').browse(cr,uid,department):
                department=pl.id
                print department,"DEPARTMENT-ID............"
            if not department:
                department= self.pool.get('hr.department').create(cr,uid,{'name': emp_department})
                print department,"DEPARTMENT-ID............"
          
            taluka_name= self.pool.get('taluka.name').search(cr,uid,[('name','=',emp_taluka)])
            print taluka_name, "TALUKA -ID.............."
            for al in self.pool.get('taluka.name').browse(cr,uid,taluka_name):
                taluka_name=al.id
                print taluka_name,"TALUKA-ID............"
            if not taluka_name:
                taluka_name= self.pool.get('taluka.name').create(cr,uid,{'name': emp_taluka})
                print taluka_name,"TALUKA-ID............"
                 
            district_name= self.pool.get('res.state.district').search(cr,uid,[('name', '=',district)])
            print district_name,"DISTRICT-ID..........................." 
            for al in self.pool.get('res.state.district').browse(cr,uid,district_name):
                district_name=al.id
                print district_name,"DISTRICT-ID............"
            if not district_name:
                district_name= self.pool.get('res.state.district').create(cr,uid,{'name': district})
                print district_name,"DISTRICT-ID............"   
             
                   
            nominee= self.pool.get('relation.name').search(cr,uid,[('name', '=',nominee_relationship)])
            print nominee,"NOMINEE-ID..........................." 
            for kl in self.pool.get('relation.name').browse(cr,uid,nominee):
                nominee=kl.id
                print nominee,"NOMINEE-ID............"
            if not nominee:
                nominee= self.pool.get('relation.name').create(cr,uid,{'name': nominee_relationship})
                print nominee,"NOMINEE-ID............"   
            
            state_name = self.pool.get('res.country.state').search(cr,uid,[('name','=',emp_state)])
            print state_name, "State Name.............."
            for cl in self.pool.get('res.country.state').browse(cr,uid,state_name):
                state_name=cl.id
                print state_name, "State Name.............."
                
                
                
            country_number = self.pool.get('res.country').search(cr,uid,[('name','=',country)])
            print country_number, "COUNTRY ARRAY.............."
            for cl in self.pool.get('res.country').browse(cr,uid,country_number):
                country_number=cl.id
                print country_number,"COUNTRY-ID..........."
                
            bank = self.pool.get('res.bank').search(cr,uid,[('name','=',bank_name)])
            print bank, "BANK ARRAY.............."
            for bl in self.pool.get('res.bank').browse(cr,uid,bank):
                bank_number=bl.id
                print bank_number,"BANK-ID............"
            if not bank:
                bank_number= self.pool.get('res.bank').create(cr,uid,{'name': bank_name})
                print bank_number,"BANK-ID............"
                
            company_number = self.pool.get('res.company').search(cr,uid,[('name','=',company_name)]) and \
                                self.pool.get('res.company').search(cr,uid,[('name','=',company_name)])[0] or False
            
            if not employee_id:
                employee_identification_proof_detail = []
                if adhar_no:
                    employee_identification_proof_detail.append((0,0,{'name':'aadhar_card','number' :adhar_no}))
                if driving_licence_no:
                    employee_identification_proof_detail.append((0,0,{'name':'driving_licence','number':driving_licence_no}))
                offence_line = []
                if service_remark:
                    offence_line.append((0,0,{'name':'punishment','punishment':service_remark}))
                    
                emp_deatil.update({'identification_id1': emp_code,
                                  'name':emp_name,
                                                                          'current_country_id':country_number,
                                                                          'relationship':nominee,
                                                                          'nominee':nominee_name,
                                                                          'address':nominee_address,
                                                                          'telephone_no':nominee_phone,
                                                                          'post_office':post_office,
                                                                          'constituency':constituency,
                                                                          'place_of_birth':place_of_birth,
                                                                          'category':tag_id,
                                                                          'vehicle':company_vehicle,
                                                                          'vehicle_distance':work_distance,
                                                                          'notes':other_info,
                                                                          'name':emp_name,
                                                                          'job_id':position, 
                                                                          'department_id':department,
                                                                          'pf_no':emp_epf_no,
                                                                          'father_name':father_name,
                                                                          'current_pincode':pincode,
                                                                          'mobile_no1':mobile_no,
                                                                          'blood_group':blood_group, 
                                                                          'active':str(active),
                                                                          'gender':str(gender),
                                                                          'bank_field':bank_number, 
                                                                                'branch_name':branch_name,
                                                                                'bank_bic':bank_code,
                                                                                 'company_id':company_number,
                                                                                 'marital':martial_status,
                                                                                 'work_email':emp_mail,
                                                                                 'work_phone':work_phone,
                                                                                 'mobile_phone':work_mobile,
                                                                                 'work_location':office_location,
                                                                                 'reason_leaving':reason,
                                                                                 'acc_number':bank_account_no,
                                                                                 'esic_no':esic_no,
                                                                                 'bank_field':bank_number,
                                                                                 'bank_bic':bank_code,
                                                                                 'employee_identification_proof_detail' : employee_identification_proof_detail,
                                                                                 'current_city':city,
                                                                                 'current_street1':address,
                                                                                 'current_district_id':district_name,
                                                                                 'taluka':taluka_name,
                                                                                 'offence_line':offence_line,
                                                                                 'current_state_id':state_name,})
              
                employee_id = self.pool.get('hr.employee').create(cr,uid,emp_deatil)
                print "employee_id==============",employee_id
                                                                                 
   
            elif employee_id:
                employee_id = self.pool.get('hr.employee').write(cr,uid,employee_id,emp_deatil)
  
            else:
                employee_id = employee_id[0]
        return True
    
    def import_payment_info(self,cr,uid,ids,context=None):

        cur_obj = self.browse(cr,uid,ids)[0]
        file_data=cur_obj.file
        val=base64.decodestring(file_data)
        fp = StringIO.StringIO()
        fp.write(val)     
        wb = xlrd.open_workbook(file_contents=fp.getvalue())
        sheet=wb.sheet_by_index(0)
        
        for i in range(1,sheet.nrows):
            emp_code =sheet.row_values(i,0,sheet.ncols)[1]
            emp_wage =sheet.row_values(i,0,sheet.ncols)[2]
            salary_structure =sheet.row_values(i,0,sheet.ncols)[3]
            nutritional_allowance =sheet.row_values(i,0,sheet.ncols)[4]
            att_inc_allowance =sheet.row_values(i,0,sheet.ncols)[6]
            holidays_calendar =sheet.row_values(i,0,sheet.ncols)[7]
            working_schedule =sheet.row_values(i,0,sheet.ncols)[8]
            contract_start_date =sheet.row_values(i,0,sheet.ncols)[9]
            da_lta_fa =sheet.row_values(i,0,sheet.ncols)[10]
            house_rent_allowance =sheet.row_values(i,0,sheet.ncols)[11]
            over_time =sheet.row_values(i,0,sheet.ncols)[5]
            
            
            date_of_joining = datetime.datetime.strptime(contract_start_date, "%d/%m/%Y")
            print date_of_joining, "CONTRACT START DATE"
            
            print emp_code,emp_wage,salary_structure,nutritional_allowance,att_inc_allowance,holidays_calendar,date_of_joining,da_lta_fa,house_rent_allowance, "ooooooooooooooooooooooooooooooooooooo"
            
        
            #emp_code = 'SLSG-' + str(emp_code)
            print emp_code, "EMPLOYEE CODE"
            
            employee_id = self.pool.get('hr.employee').search(cr,uid,[('identification_id1','=',emp_code)])
            print employee_id, "EMPLOYEE-ID ARRAY !!!!!!!!!!!!!!!"
            for el in self.pool.get('hr.employee').browse(cr,uid,employee_id):
                emp_number=el.id
                emp_name=el.name
                print emp_number,emp_name,"EMPLOYEE-ID............"
                
            structure_id = self.pool.get('hr.payroll.structure').search(cr,uid,[('name','=',salary_structure)])
            print structure_id, "SALARY STRUCTURE ARRAY !!!!!!!!!!!!!!!"
            for sl in self.pool.get('hr.payroll.structure').browse(cr,uid,structure_id):
                structure_number=sl.id
                print structure_number,"SALARY STRUCTURE-ID............"
            if not structure_id:
                structure_number=self.pool.get('hr.payroll.structure').create(cr,uid,{'name': salary_structure})
                
            calendar_id = self.pool.get('holidays.calendar').search(cr,uid,[('name','=',holidays_calendar)])
            print calendar_id, "HOLIDAYS CALENDAR ARRAY !!!!!!!!!!!!!!!"
            for tl in self.pool.get('holidays.calendar').browse(cr,uid,calendar_id):
                calendar_number=tl.id
                print calendar_number,"HOLIDAYS CALENDAR-ID............"
                
            schedule_id = self.pool.get('resource.calendar').search(cr,uid,[('name','=',working_schedule)])
            print schedule_id, "WORKING SCHEDULE ARRAY !!!!!!!!!!!!!!!"
            for wl in self.pool.get('resource.calendar').browse(cr,uid,schedule_id):
                schedule_number=wl.id
                print schedule_number,"WORKING SCHEDULE ID............"    
                
            contract_id = self.pool.get('hr.contract').search(cr,uid,[('name','=',emp_name)]) #'struct_id': structure_number, 'holidays_id': calendar_number,
            print contract_id, "CONTRACT-ID exists............."
            if not contract_id:
                print "new contract created"
                new_contract = self.pool.get('hr.contract').create(cr,uid,{'over_time_allowence':over_time,
                                                                           'struct_id': structure_number,
                                                                            'holidays_id': calendar_number,
                                                                           'struct_id': structure_number,
                                                                           'name' : emp_name,
                                                                           'employee_id' : emp_number,
                                                                           'wage': emp_wage, 
                                                                           'nutritional_allowance': nutritional_allowance,  
                                                                           'attendance_incentive': att_inc_allowance, 
                                                                           'working_hours': schedule_number, 
                                                                           'date_start': date_of_joining, 
                                                                           'da_lta_fa': da_lta_fa, 
                                                                           'hra': house_rent_allowance})
        for cl_browse in self.pool.get('hr.contract').browse(cr,uid,contract_id):
                        self.pool.get('hr.contract').write(cr,uid,cl_browse.id,{'wage': emp_wage, 
                                                                            'struct_id': structure_number, 
                                                                            'nutritional_allowance': nutritional_allowance,  
                                                                            'attendance_incentive': att_inc_allowance, 
                                                                            'holidays_id': calendar_number})
                    
                        
        return True

