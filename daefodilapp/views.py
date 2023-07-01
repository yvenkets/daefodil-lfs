from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from .forms import SignIn
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from .models import dlt_passreset
from django.conf import Settings, settings
from django.core.mail import EmailMessage, send_mail 
from django.core import mail
import random
import datetime
import string
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json
import requests
import csv
import pandas as pd
import io
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
from django.utils import timezone
from django.forms.models import model_to_dict
import openpyxl
from django.core import serializers
from PIL import Image, ImageOps, ImageEnhance, ImageFilter,  ImageDraw, ImageFont
import re
from django.db.models import Max
from django.db import transaction
import base64
from io import BytesIO

import inspect
# Create your views here.
def home(request):
    #if  request.method=="POST":
        #if ''
    if 'username' in request.session:
        return redirect('/userdashboard')
    return render(request,'MainPage.html')

#sign-up pages

def work(request):
    if request.method == 'POST':
        print('in')
        typeval ='Work'
        tname = request.POST["tname"]
        
        
        uname = request.POST["uname"]
        password = request.POST["password"]
        grpcode='CAdmin' 
        grpactivity= 'All'
        grpdes = 'Admin'
        usertype ='App Admin-Work'
        dlm_cust_email= uname 
        
        global val                  
        def val():
            return uname
   
        encryptedpassword=make_password(password)
        
        if DlmCust.objects.filter(dlm_cust_email = dlm_cust_email).exists():  
            messages.info(request, 'user name is already taken')
          
        else:
            print('in')
            ten = DlmTenant.objects.create(dlm_tenant_nam=tname,dlm_tenant_cat =typeval,dlm_tenant_sts = 'Active')
        
            cus = DlmCust.objects.create(dlm_cust_tntid =ten.iddlm_tenant,dlm_cust_nam =tname,dlm_cust_email=uname)
            
            
            grp = DlmGroup.objects.create(dlm_group_custid= cus.iddlm_cust, dlm_group_code=grpcode, dlm_group_activity=grpactivity,dlm_group_des=grpdes)
        
            user = DlmCustuser.objects.create(dlm_custuser_grpid=grp.iddlm_group ,dlm_custuser_custid=cus.iddlm_cust, dlm_custuser_code=uname, dlm_custuser_pwd=encryptedpassword ,dlm_custuser_type = usertype)

            return redirect("/email")


    return render(request,'WorkSignUp.html')

def personal(request):
    if request.method == 'POST':
        print('in')
        typeval ='Personal'
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        tname = fname+' '+lname
        
        uname = request.POST["uname"]
        password = request.POST["password"]
        grpcode='CAdmin' 
        grpactivity= 'All'
        grpdes = 'Admin'
        dlm_cust_email= uname 
        usertype ='App Admin-Personal'
        global val                  
        def val():
            return uname
   
        encryptedpassword=make_password(password)
        
        if DlmCust.objects.filter(dlm_cust_email = dlm_cust_email).exists():  
            messages.info(request, 'user name is already taken')
          
        else:
            print('in')
            ten = DlmTenant.objects.create(dlm_tenant_nam=tname,dlm_tenant_cat =typeval,dlm_tenant_sts = 'Active')
        
            cus = DlmCust.objects.create(dlm_cust_tntid =ten.iddlm_tenant,dlm_cust_nam =tname,dlm_cust_email=uname)
            
            
            grp = DlmGroup.objects.create(dlm_group_custid= cus.iddlm_cust, dlm_group_code=grpcode, dlm_group_activity=grpactivity,dlm_group_des=grpdes)
        
            user = DlmCustuser.objects.create(dlm_custuser_grpid=grp.iddlm_group ,dlm_custuser_custid=cus.iddlm_cust, dlm_custuser_code=uname, dlm_custuser_pwd=encryptedpassword ,dlm_custuser_type = usertype)

            return redirect("/email")



    return render(request,'PersonalSignUp.html')

# terms and privacy policy
def terms(request):
    return render(request,'terms_and_condition.html')

def privacypol(request):
    return render(request,'privacy_policy.html')
#email-verification###

def email(request):
    value=0   
    global valuesend
    def valuesend():
        return value  

    sendotp() #calling the function

    uname=val()

    idusr=idusn()   
    
   
    if request.method=="POST":
        print("inside if")
        print(request.POST)
        if 'verify' in request.POST:
            print("inside verify")
            d1=request.POST["digit-1"]
            d2=request.POST["digit-2"]
            d3=request.POST["digit-3"]
            d4=request.POST["digit-4"]
            d5=request.POST["digit-5"]
            d6=request.POST["digit-6"]
            otp_code="".join([d1,d2,d3,d4,d5,d6])
            try:
                cdate=dlt_passreset.objects.filter(dlt_passreset_usrid=idusr,dlt_passreset_otpcode=otp_code).values('dlt_passreset_cdate')[0]['dlt_passreset_cdate']
                exdate=dlt_passreset.objects.filter(dlt_passreset_usrid=idusr,dlt_passreset_otpcode=otp_code).values('dlt_passreset_expdate')[0]['dlt_passreset_expdate']
                cdate= cdate.strftime("%Y-%m-%d %H:%M")
                exdate= exdate.strftime("%Y-%m-%d %H:%M")
                print(cdate)
                print(exdate)
   
                now=datetime.datetime.now()
                now=now.strftime("%Y-%m-%d %H:%M")
                print(now)
    
                checkdate=cdate<=now<=exdate
                print(checkdate)

            except:
                messages.info(request,'')
           
    
               
            try:
               if dlt_passreset.objects.filter(dlt_passreset_otpcode=otp_code,dlt_passreset_usrid=idusr).exists() and checkdate==True :
                    custcode=DlmCustuser.objects.get(dlm_custuser_code=uname)
                    custcode.dlm_custuser_verify=1
                    custcode.save()
        
                    
                    return redirect("/loader")
                   
               else:
                    
                   

                    
        
                    cus = DlmCust.objects.get(dlm_cust_email=uname)
        
              
        
                    user = DlmCustuser.objects.get( dlm_custuser_code=uname)

                    idcust= DlmCust.objects.filter(dlm_cust_email=uname).values('iddlm_cust')[0]['iddlm_cust']
                    
                    grp = DlmGroup.objects.get(dlm_group_custid=idcust)

                    user1= DlmCust.objects.filter(dlm_cust_email=uname).values('dlm_cust_nam')[0]['dlm_cust_nam']
                    print(user1)
                    
                    ten = DlmTenant.objects.get(dlm_tenant_nam=user1)

                    pas=dlt_passreset.objects.get(dlt_passreset_usrid=idusr)
                    
                   
                    
                    #execute=True
                    messages.info(request,'invalid credentials')
            except:
                    execute=True
                    messages.info(request,'invalid credentials')
        if 'resend' in request.POST:
            value=1
            sendotp()
            
    
    return render(request,'Confirm_email.html')

def loader(request):
    return render(request,'Loader.html')

#login/logout####

def login(request):
    if request.method=="POST":
        username=request.POST["username"]
        print('insideif')
        print(username)
        password=request.POST["password"]

        
       
        
        global val    #declaring username as global variable using "val" variable
        def val():
            return username

        
        if 'login' in request.POST:
            try:
                encryptedpassword=DlmCustuser.objects.filter(dlm_custuser_code = username).values('dlm_custuser_pwd')[0]['dlm_custuser_pwd']
                #print(encryptedpassword)
                checkpassword=check_password(password,encryptedpassword)
                userstatus= DlmCustuser.objects.filter(dlm_custuser_code = username).values('dlm_custuser_status')[0]['dlm_custuser_status'] 
                print(userstatus)
                #print(checkpassword)
            except:
                messages.info(request,'')
            #clientstatus= DlmCust.objects.filter(dlm_cust_email = username).values('dlm_cust_status')[0]['dlm_cust_status']
              
            if DlmCustuser.objects.filter(dlm_custuser_code= username,dlm_custuser_verify=1).exists() and checkpassword == True:
                #request.session['username']=username 
                print("account")
                if  userstatus == 'active':
                    print("active")
                    request.session['username'] = username
                    return redirect('userdashboard')
                else:
                    messages.error(request,'Your account is disabled')

                return redirect('/userdashboard')
            elif DlmCustuser.objects.filter(dlm_custuser_code= username).exists() and checkpassword == True:
                return redirect("/email")

            else:
                messages.info(request,'invalid username or password')
                
        if 'forgotpassword' in request.POST: 
            if DlmCustuser.objects.filter(dlm_custuser_code=username).exists():
                print("valid")
                return redirect("/forgotpassword")
            else:
                print("not valid")
                messages.info(request,'invalid username')


  
  

    return render(request,'Login.html')

def logout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect('home')

#forgot password logic pages######

def forgotpassword(request):
    
    
    if request.method=="POST":
        username=request.POST["username"]
        global usnam   #declaring username as global variable using "usnam" variable
        def usnam():
            return username
            
           
        
        id= DlmCustuser.objects.filter(dlm_custuser_code=username).values('iddlm_custuser')[0]['iddlm_custuser']
        
        global idun # declaring  idun function as a global function
        def idun():
            return id
        
         #calling the resend function
        return redirect("/forgotpasswordtwo")

    usen=val() # calling username
    return render(request,"ForgotPasswordOne.html",{'usen':usen})     
    
def forgotpasswordtwo(request):
    id=idun()
    
    resend() 
    print("hello")
    if 'resend' in request.POST:
            print("inside resend")
            resend()   # calling the resend function
            return redirect("/verification")

    
    return render(request,"ForgotPasswordTwo.html")     

def verification(request):
    id=idun()  #calling the id of username
    #id1=str(id1)
    #c=len(id1)
    #d=[]
    #for i in range(c):
    #    if id1[i].isnumeric():
     #       d.append(id1[i])
   # c=[str(i) for i in d]
    #e=''.join(c)
    now=datetime.datetime.now()
    now=now.strftime("%T-%m-%d %H:%M")
    cdate=cdt()
    exdate=exdt()

    if request.method=="POST":
        print("inside if")
        print(request.POST)
        if 'verify' in request.POST:
            print("inside verify")
            print(cdate)
            print(exdate)
            print(now)
            
            d1=request.POST["digit-1"]
            d2=request.POST["digit-2"]
            d3=request.POST["digit-3"]
            d4=request.POST["digit-4"]
            d5=request.POST["digit-5"]
            d6=request.POST["digit-6"]
            otp_code="".join([d1,d2,d3,d4,d5,d6])

               
            if dlt_passreset.objects.filter(dlt_passreset_otpcode=otp_code,dlt_passreset_usrid=id,dlt_passreset_cdate=cdate).exists() :
                    return redirect("/setnewpassword")
                   
            else:
                    messages.info(request,'invalid credentials')
        if 'resend' in request.POST:
            print("inside resend")
            resend()   # calling the resend function
        
            
    
    return render(request,"Verification.html")


def setnewpassword(request):
    username=val()   #calling the username
    if request.method=="POST":
        
       
       
       
        password1=make_password(request.POST['password1'])
        newp=DlmCustuser.objects.get(dlm_custuser_code=username)
        newp.dlm_custuser_pwd=password1
        newp.save()
        return redirect("/successpage")   
       
    
    return render(request,"SetNewPassword.html")   

def successpage(request):
    
    return render(request,"SuccessPage.html")     

#userdashboard ######  
def userdashboard(request):
    if 'username' in request.session:
        name=request.session['username']
        uid=DlmCustuser.objects.filter(dlm_custuser_code=name).values('iddlm_custuser')[0]['iddlm_custuser']
        usertype=DlmCustuser.objects.filter(dlm_custuser_code=name).values('dlm_custuser_type')[0]['dlm_custuser_type']
        request.session['usertype']=usertype
        print(usertype)
        
        context={'usertype':usertype}
        try:
            user_id=dlm_docmap.objects.get(dlm_docmap_uid=uid)
            user_mapped="existing-user"
            request.session['usermapped']=user_mapped
        except:
            user_mapped="new-user"
            request.session['usermapped']=user_mapped
            
        if user_mapped=="existing-user":
            
            return redirect('/userdetails')
        elif user_mapped=="new-user":
            return redirect('/newuser')
    
        return render(request,'userdashboard.html',context)
    else:
        
       return redirect("/login") 

#related to userdashboard#######
def userdetails(request):
    if 'username' in request.session:
        user_mapped="existing-user"
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        return render(request,'userdetails.html',{'username':username,'usertype':usertype,'user_mapped':user_mapped})
    else:
        
       return redirect("/login") 
    

def newuser(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        return render(request,'newuser.html',{'username':username,'usertype':usertype,'user_mapped':user_mapped})
    else:
        
       return redirect("/login") 

#document-mapping pages#####

def uploadpage(request):
    if 'username' in request.session:
        print('inside uploadpage')
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        execute="False"
        extract=''
        data=''
        
        C_id=DlmCust.objects.filter(dlm_cust_email = username).values('iddlm_cust')[0]['iddlm_cust']
        T_id=DlmCust.objects.filter(dlm_cust_email = username).values('dlm_cust_tntid')[0]['dlm_cust_tntid']
        U_id=DlmCustuser.objects.filter(dlm_custuser_code = username).values('iddlm_custuser')[0]['iddlm_custuser']
        if request.method == 'POST':
            
            uploaded_file = request.FILES['file']
            # handle the uploaded file here
            print(uploaded_file.name)
            execute=uploaded_file.name
            request.session['execute']=execute
            file = {'image': uploaded_file}
            if 'file' in request.POST:
                api_url = 'http://localhost:8023/submitform/'
                response = requests.post(api_url, json=data,params={'C_id': C_id,'T_id':T_id,'U_id':U_id},files=file)
                
                if response.status_code == 200:
                    # Do something with the response data
                    data = response.json()
                    #data = json.loads(response.text)
                    print('dataresponse')
                    print(data)
                    value = data["T_id"]
                    value1=data["C_id"]
                    value2=data["id"]
                    value3=data["U_id"]
                    value4=data["dtype"]
                    filepath=data["filepath"]
                    print("filepath")
                    print(filepath)
                    try:
                        value5=data["Final_text"]
                        #print(value5)
                    except:
                        print('none')
                    #if dlm_docmap.objects.filter(dlm_docmap_dtype=).exists() 
                    value6=data['docproc_id']
                    value7=data['colvalues']
                    value8=data['column_headers']
                    value9=data['datapp']
                    value10=data['index_values']
                    print(value)
                    print(value1)
                    print(value2)
                    print(value3)
                    print(value4)
                    print(value6)
                    request.session['t_id']= value
                    request.session['c_id'] =value1
                    request.session['id']= value2
                    request.session['u_id']= value3
                    request.session['dtype']=value4
                    request.session['rawval']=value5
                    request.session['docproc_id']=value6
                    request.session['fp']=filepath
                    request.session['colvalues']=value7
                    request.session['column_headers']=value8
                    request.session['data_list']=value9
                    request.session['index_values']=value10
                    if dlm_docmap.objects.filter(dlm_docmap_dtype=value4).exists():
                        print("mapping")
                    execute=True
                        # if 'ok' in request.POST:
                        #     print('data1')
                        
                        #     print('data2')
                        #     data = response.json()
                    return redirect("/docmapping")

                        #print(response_data)
                else:
                    return HttpResponse('Error')
                    
        return render(request,'uploadpage.html',{'username':username,'usertype':usertype,'user_mapped':user_mapped,'execute':execute})
    else:
       return redirect("/login")
   
def process(request):
    return render(request,'process.html')

def save(request):
    #docmapping(request,'test')
    print("inside save")
    return redirect("/docmapping")

def docmapping(request):   
    print("docmap")
    if 'form_submitted' in request.session:
        print(request.session['form_submitted'])
    ten_id=request.session['t_id']
    #print(ten_id)
    client_id=request.session['c_id']
    #print(client_id)
    id_element=request.session['id']
    #print(id_element)
    u_id=request.session['u_id']
    #print(u_id)
    docproc_id=request.session.get('docproc_id')
    d_type=request.session['dtype']
    docmap=dlm_docmap.objects.all()
    maped= dlm_docmap.objects.filter(dlm_docmap_clientid=client_id ).values_list('dlm_docmap_dtype')
    maped_list = [str(t[0]) for t in maped]
    #print(maped_list)
    elem=dlt_melements.objects.filter(dlt_melements_cid=client_id ).values_list('dlt_melements_dtype')
    elem_list= [str(t[0]) for t in elem]
    #print(elem_list)
    value2=request.session['id']
    latest_record1 =  dlt_melements.objects.get(iddlt_melements=value2)
    doctype=latest_record1.dlt_melements_dtype
    found = False
    
    #download = False
    
   
    #for element in maped_list:
    if doctype in maped_list:
        #print("found")
        found = True
        
    
    if 'username' in request.session:
            username=request.session['username']   #calling username
            usertype=request.session['usertype']
            user_mapped=request.session['usermapped']
            #query_result = dlt_melements.objects.filter(iddlt_melements=25)
            #element = dlt_melements.objects.get(iddlt_melements=25)
            #context = {'element': element}
            columns = [field.name for field in dlt_melements._meta.get_fields()]
            
            # print(columns)
            data_dict = {'dlt_melements_1': columns[4], 'dlt_melements_2': columns[5], 'dlt_melements_3': columns[6], 'dlt_melements_4': columns[7], 'dlt_melements_5': columns[8], 'dlt_melements_6': columns[9], 'dlt_melements_7':columns[10], 'dlt_melements_8':columns[11], 'dlt_melements_9':columns[12], 'dlt_melements_10':columns[13], 'dlt_melements_11':columns[14], 'dlt_melements_12':columns[15], 'dlt_melements_13':columns[16], 'dlt_melements_14':columns[17], 'dlt_melements_15':columns[18]}
            # print(data_dict)
            #today = datetime.now().strftime("%Y-%m-%d  %H:%M:00")
            now=datetime.datetime.now()
            now=now.strftime("%T-%m-%d %H:%M")
            #print(now)
            #print(today)
            #print(id_element)
            try:
                elements = dlt_melements.objects.get(dlt_melements_tid=ten_id,dlt_melements_cid=client_id,iddlt_melements=id_element)
                #print(elements)
            except:
                elements="YOUR RECORDS NOT MATCH"
                #print(elements)
            is_active = True
            
            print("hiiii")
            print(value2)
            #latest_record1 = dlt_melements.objects.filter(dlt_melements_cid=client_id).order_by('-dlt_melements_cdate').first()
            latest_record1 =  dlt_melements.objects.get(iddlt_melements=value2)
            print(latest_record1)
            original_value1 = latest_record1.dlt_melements_1
            original_value2 = latest_record1.dlt_melements_2
            original_value3 = latest_record1.dlt_melements_3
            original_value4 = latest_record1.dlt_melements_4
            original_value5 = latest_record1.dlt_melements_5
            original_value6 = latest_record1.dlt_melements_6
            original_value7 = latest_record1.dlt_melements_7
            original_value8 = latest_record1.dlt_melements_8
            original_value9 = latest_record1.dlt_melements_9
            original_value10 = latest_record1.dlt_melements_10
            original_value11 = latest_record1.dlt_melements_11
            original_value12 = latest_record1.dlt_melements_12
            original_value13 = latest_record1.dlt_melements_13
            original_value14 = latest_record1.dlt_melements_14
            original_value15 = latest_record1.dlt_melements_15
            
            #if 'buttonval' not in request.session:
            #    request.session['buttonval'] = 'test'
       
            
  
            if request.method=="POST":
                #downloads = True
                print('inside post')
                
                buttonval = request.POST["selected_butotn"]
                request.session['form_submitted'] = buttonval

                print(buttonval)
                print("here")
                is_active= True
                #print('in')
                var1=[]
                var2=[]
                for i in range(1,16):
                    #print('in1')
                    # checkbox_value = locals().get('checkbox_' + str(i))
                    # print(checkbox_value)
                    # checkbox_value = 'checkbox_'+ str(i)
                    # print(checkbox_value)
                    try:
                        checkbox=request.POST['checkbox_'+ str(i)]
                        #print(checkbox)
                        if checkbox == 'SELECTED':
                                 #print('in2')
                                 my_variable1 =request.POST['input_' + str(i)]
                                 my_variable2 =request.POST['input' + str(i)]
                        #         my_var1=request.POST.get(my_variable1)
                        #         my_var2=request.POST.get(my_variable2)
                                 #print(my_variable1,my_variable2)
                                 var1.append(my_variable1)
                                 var2.append(my_variable2)
                                 
                    
                    except:
                        pass
                result1 = ', '.join(var1)
                result2 = ', '.join(var2)
                #print(result1,result2) 
                if found:
                    print("yeah")
                    # Replace existing data
                    existing_data = dlm_docmap.objects.get(dlm_docmap_clientid=client_id, dlm_docmap_dtype=d_type)
                    #existing_data = dlm_docmap.objects.filter(dlm_docmap_clientid=client_id, dlm_docmap_dtype=d_type)

                    existing_data.dlm_docmap_element = result2
                    existing_data.dlm_docmap_cname = result1
                    existing_data.dlm_docmap_uid = u_id
                    existing_data.save()
                    docmap_id = dlm_docmap.objects.order_by('-iddlm_docmap').first()
                    docmap_id=docmap_id.iddlm_docmap
                    DltDocproc.objects.filter(iddlt_docproc=docproc_id).update(dlt_docproc_dataid=docmap_id)
                    
                   
                    prompt_value = request.POST.get('prompt')
                    print(prompt_value)
                    if prompt_value == 'Yes':
                        print("No")
                        new_key1 = request.POST.get('input_1')
                        if new_key1 :
                            print("python")
                            key_value_parts1=[]
                            if original_value1 is not None:
                                key_value_parts1 = original_value1.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts1) > 1:
                                updated_value1 = new_key1 + ':' + key_value_parts1[1]
                            else:
                                updated_value1 = new_key1
                            if original_value1.startswith("td!"):
                                updated_value1 = "td!"+updated_value1
                            else:
                                updated_value1 =   updated_value1 
                            latest_record1.dlt_melements_1 = updated_value1
                            latest_record1.save()
                        
                        new_key2 = request.POST.get('input_2')
                        if new_key2 :
                            key_value_parts2=[]
                            if original_value2 is not None:
                                key_value_parts2 = original_value2.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts2) > 1:
                                updated_value2 = new_key2 + ':' + key_value_parts2[1]
                            else:
                                updated_value2 = new_key2
                            if original_value2.startswith("td!"):
                                updated_value2 = "td!"+updated_value2
                            else:
                                updated_value2 =   updated_value2 
                            latest_record1.dlt_melements_2 = updated_value2
                            latest_record1.save()
                            
                        new_key3 = request.POST.get('input_3')
                        if new_key3 :
                            key_value_parts3=[]
                            if original_value3 is not None:
                                key_value_parts3 = original_value3.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts3) > 1:
                                updated_value3 = new_key3 + ':' + key_value_parts3[1]
                            else:
                                updated_value3 = new_key3
                            if original_value3.startswith("td!"):
                                updated_value3 = "td!"+updated_value3
                            else:
                                updated_value3 =   updated_value3 
                            latest_record1.dlt_melements_3 = updated_value3
                            latest_record1.save()
                        
                        new_key4 = request.POST.get('input_4')
                        if new_key4 :
                            key_value_parts4=[]
                            if original_value4 is not None:
                                key_value_parts4 = original_value4.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts4) > 1:
                                updated_value4 = new_key4 + ':' + key_value_parts4[1]
                            else:
                                updated_value4 = new_key4
                            if original_value4.startswith("td!"):
                                updated_value4 = "td!"+updated_value4
                            else:
                                updated_value4 =   updated_value4 
                            latest_record1.dlt_melements_4 = updated_value4
                            latest_record1.save()
                        
                        new_key5 = request.POST.get('input_5')
                        if new_key5 :
                            key_value_parts5=[]
                            if original_value5 is not None:
                                key_value_parts5 = original_value5.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts5) > 1:
                                updated_value5 = new_key5 + ':' + key_value_parts5[1]
                            else:
                                updated_value5 = new_key5
                            if original_value5.startswith("td!"):
                                updated_value5 = "td!"+updated_value5
                            else:
                                updated_value5 =   updated_value5 
                            latest_record1.dlt_melements_5 = updated_value5
                            latest_record1.save()
                    
                        new_key6 = request.POST.get('input_6')
                        if new_key6 :
                            key_value_parts6=[]
                            if original_value6 is not None:
                                key_value_parts6 = original_value6.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts6) > 1:
                                updated_value6 = new_key6 + ':' + key_value_parts6[1]
                            else:
                                updated_value6 = new_key6
                            if original_value6.startswith("td!"):
                                updated_value6 = "td!"+updated_value6
                            else:
                                updated_value6 =   updated_value6 
                            latest_record1.dlt_melements_6 = updated_value6
                            latest_record1.save()
                        
                        new_key7 = request.POST.get('input_7')
                        if new_key7 :
                            key_value_parts7=[]
                            if original_value7 is not None:
                                key_value_parts7 = original_value7.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts7) > 1:
                                updated_value7 = new_key7 + ':' + key_value_parts7[1]
                            else:
                                updated_value7 = new_key7 
                            if original_value7.startswith("td!"):
                                updated_value7 = "td!"+updated_value7
                            else:
                                updated_value7 =   updated_value7 
                            latest_record1.dlt_melements_7 = updated_value7
                            latest_record1.save()
                        
                        new_key8 = request.POST.get('input_8')
                        if new_key8 :
                            key_value_parts8=[]
                            if original_value8 is not None:
                                key_value_parts8 = original_value8.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts8) > 1:
                                updated_value8 = new_key8 + ':' + key_value_parts8[1]
                            else:
                                updated_value8 = new_key8
                            if original_value8.startswith("td!"):
                                updated_value8 = "td!"+updated_value8
                            else:
                                updated_value8 =   updated_value8 
                            latest_record1.dlt_melements_8 = updated_value8
                            latest_record1.save()
                        
                        new_key9 = request.POST.get('input_9')
                        if new_key9 :
                            key_value_parts9=[]
                            if original_value9 is not None:
                                key_value_parts9 = original_value9.split(':', 1)  # Split the original value into key and value
                                print(key_value_parts9)
                            if len(key_value_parts9) > 1:
                                updated_value9 = new_key9 + ':' + key_value_parts9[1]
                            else:
                                updated_value9 = new_key9
                            if original_value9.startswith("td!"):
                                updated_value9 = "td!"+updated_value9
                            else:
                                updated_value9 =   updated_value9 
                            latest_record1.dlt_melements_9 = updated_value9
                            latest_record1.save()
                        
                        new_key10 = request.POST.get('input_10')
                        if new_key10 :
                            key_value_parts10=[]
                            if original_value10 is not None:
                                key_value_parts10 = original_value10.split(':', 1)  # Split the original value into key and value
                            
                            if len(key_value_parts10) > 1:
                                updated_value10 = new_key10 + ':' + key_value_parts10[1]
                            else:
                                updated_value10 = new_key10
                            if original_value10.startswith("td!"):
                                updated_value10 = "td!"+updated_value10
                            else:
                                updated_value10 =   updated_value10 
                            latest_record1.dlt_melements_10 = updated_value10
                            latest_record1.save()
                            
                        new_key11 = request.POST.get('input_11')
                        if new_key11 :
                            key_value_parts11=[]
                            if original_value11 is not None:
                                key_value_parts11 = original_value11.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts11) > 1:
                                updated_value11 = new_key11 + ':' + key_value_parts11[1]
                            else:
                                updated_value11 = new_key11 
                            if original_value11.startswith("td!"):
                                updated_value11 = "td!"+updated_value11
                            else:
                                updated_value11 =   updated_value11 
                            latest_record1.dlt_melements_11 = updated_value11
                            latest_record1.save()
                        
                        new_key12 = request.POST.get('input_12')
                        if new_key12 :
                            key_value_parts12=[]
                            if original_value12 is not None:
                                key_value_parts12 = original_value12.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts12) > 1:
                                updated_value12 = new_key12 + ':' + key_value_parts12[1]
                            else:
                                updated_value12 = new_key12
                            if original_value12.startswith("td!"):
                                updated_value12 = "td!"+updated_value12
                            else:
                                updated_value12 =   updated_value12 
                            latest_record1.dlt_melements_12 = updated_value12
                            latest_record1.save()
                        
                        new_key13 = request.POST.get('input_13')
                        if new_key13 :
                            key_value_parts13=[]
                            if original_value13 is not None:
                                key_value_parts13 = original_value13.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts13) > 1:
                                updated_value13 = new_key13 + ':' + key_value_parts13[1]
                            else:
                                updated_value13 = new_key13 
                            if original_value13.startswith("td!"):
                                updated_value13 = "td!"+updated_value13
                            else:
                                updated_value13 =   updated_value13 
                            latest_record1.dlt_melements_13 = updated_value13
                            latest_record1.save()
                        
                        new_key14 = request.POST.get('input_14')
                        if new_key14 :
                            key_value_parts14=[]
                            if original_value14 is not None:
                                key_value_parts14 = original_value14.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts14) > 1:
                                updated_value14 = new_key14 + ':' + key_value_parts14[1]
                            else:
                                updated_value14 = new_key14
                            if original_value14.startswith("td!"):
                                updated_value14 = "td!"+updated_value14
                            else:
                                updated_value14 =   updated_value14 
                            latest_record1.dlt_melements_14 = updated_value14
                            latest_record1.save()
                        
                        new_key15 = request.POST.get('input_15')
                        if new_key15 :
                            key_value_parts15=[]
                            if original_value15 is not None:
                                key_value_parts15 = original_value15.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts15) > 1:
                                updated_value15 = new_key15 + ':' + key_value_parts15[1]
                            else:
                                updated_value15 = new_key15
                            if original_value15.startswith("td!"):
                                updated_value15 = "td!"+updated_value15
                            else:
                                updated_value15 =   updated_value15 
                            latest_record1.dlt_melements_15 = updated_value15
                            latest_record1.save()
                            
                        return redirect("/save")
                        
                    else:
                        print("NOpe")
                        new_key1 = request.POST.get('input_1')
                        if new_key1 :
                            print("python")
                            key_value_parts1=[]
                            if original_value1 is not None:
                                key_value_parts1 = original_value1.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts1) > 1:
                                updated_value1 = new_key1 + ':' + key_value_parts1[1]
                            else:
                                updated_value1 = new_key1
                            if original_value1.startswith("td!"):
                                updated_value1 = "td!"+updated_value1
                            else:
                                updated_value1 =   updated_value1 
                            latest_record1.dlt_melements_1 = updated_value1
                            latest_record1.save()
                        
                        new_key2 = request.POST.get('input_2')
                        if new_key2 :
                            key_value_parts2=[]
                            if original_value2 is not None:
                                key_value_parts2 = original_value2.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts2) > 1:
                                updated_value2 = new_key2 + ':' + key_value_parts2[1]
                            else:
                                updated_value2 = new_key2
                            if original_value2.startswith("td!"):
                                updated_value2 = "td!"+updated_value2
                            else:
                                updated_value2 =   updated_value2 
                            latest_record1.dlt_melements_2 = updated_value2
                            latest_record1.save()
                            
                        new_key3 = request.POST.get('input_3')
                        if new_key3 :
                            key_value_parts3=[]
                            if original_value3 is not None:
                                key_value_parts3 = original_value3.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts3) > 1:
                                updated_value3 = new_key3 + ':' + key_value_parts3[1]
                            else:
                                updated_value3 = new_key3
                            if original_value3.startswith("td!"):
                                updated_value3 = "td!"+updated_value3
                            else:
                                updated_value3 =   updated_value3 
                            latest_record1.dlt_melements_3 = updated_value3
                            latest_record1.save()
                        
                        new_key4 = request.POST.get('input_4')
                        if new_key4 :
                            key_value_parts4=[]
                            if original_value4 is not None:
                                key_value_parts4 = original_value4.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts4) > 1:
                                updated_value4 = new_key4 + ':' + key_value_parts4[1]
                            else:
                                updated_value4 = new_key4
                            if original_value4.startswith("td!"):
                                updated_value4 = "td!"+updated_value4
                            else:
                                updated_value4 =   updated_value4 
                            latest_record1.dlt_melements_4 = updated_value4
                            latest_record1.save()
                        
                        new_key5 = request.POST.get('input_5')
                        if new_key5 :
                            key_value_parts5=[]
                            if original_value5 is not None:
                                key_value_parts5 = original_value5.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts5) > 1:
                                updated_value5 = new_key5 + ':' + key_value_parts5[1]
                            else:
                                updated_value5 = new_key5
                            if original_value5.startswith("td!"):
                                updated_value5 = "td!"+updated_value5
                            else:
                                updated_value5 =   updated_value5 
                            latest_record1.dlt_melements_5 = updated_value5
                            latest_record1.save()
                    
                        new_key6 = request.POST.get('input_6')
                        if new_key6 :
                            key_value_parts6=[]
                            if original_value6 is not None:
                                key_value_parts6 = original_value6.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts6) > 1:
                                updated_value6 = new_key6 + ':' + key_value_parts6[1]
                            else:
                                updated_value6 = new_key6
                            if original_value6.startswith("td!"):
                                updated_value6 = "td!"+updated_value6
                            else:
                                updated_value6 =   updated_value6 
                            latest_record1.dlt_melements_6 = updated_value6
                            latest_record1.save()
                        
                        new_key7 = request.POST.get('input_7')
                        if new_key7 :
                            key_value_parts7=[]
                            if original_value7 is not None:
                                key_value_parts7 = original_value7.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts7) > 1:
                                updated_value7 = new_key7 + ':' + key_value_parts7[1]
                            else:
                                updated_value7 = new_key7 
                            if original_value7.startswith("td!"):
                                updated_value7 = "td!"+updated_value7
                            else:
                                updated_value7 =   updated_value7 
                            latest_record1.dlt_melements_7 = updated_value7
                            latest_record1.save()
                        
                        new_key8 = request.POST.get('input_8')
                        if new_key8 :
                            key_value_parts8=[]
                            if original_value8 is not None:
                                key_value_parts8 = original_value8.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts8) > 1:
                                updated_value8 = new_key8 + ':' + key_value_parts8[1]
                            else:
                                updated_value8 = new_key8
                            if original_value8.startswith("td!"):
                                updated_value8 = "td!"+updated_value8
                            else:
                                updated_value8 =   updated_value8 
                            latest_record1.dlt_melements_8 = updated_value8
                            latest_record1.save()
                        
                        new_key9 = request.POST.get('input_9')
                        if new_key9 :
                            key_value_parts9=[]
                            if original_value9 is not None:
                                key_value_parts9 = original_value9.split(':', 1)  # Split the original value into key and value
                                print("key")
                                print(key_value_parts9)
                            if len(key_value_parts9) > 1:
                                updated_value9 = new_key9 + ':' + key_value_parts9[1]
                            else:
                                updated_value9 = new_key9
                            if original_value9.startswith("td!"):
                                updated_value9 = "td!"+updated_value9
                            else:
                                updated_value9 =   updated_value9 
                            latest_record1.dlt_melements_9 = updated_value9
                            latest_record1.save()
                        
                        new_key10 = request.POST.get('input_10')
                        if new_key10 :
                            key_value_parts10=[]
                            if original_value10 is not None:
                                key_value_parts10 = original_value10.split(':', 1)  # Split the original value into key and value
                            
                            if len(key_value_parts10) > 1:
                                updated_value10 = new_key10 + ':' + key_value_parts10[1]
                            else:
                                updated_value10 = new_key10
                            if original_value10.startswith("td!"):
                                updated_value10 = "td!"+updated_value10
                            else:
                                updated_value10 =   updated_value10 
                            latest_record1.dlt_melements_10 = updated_value10
                            latest_record1.save()
                            
                        new_key11 = request.POST.get('input_11')
                        if new_key11 :
                            key_value_parts11=[]
                            if original_value11 is not None:
                                key_value_parts11 = original_value11.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts11) > 1:
                                updated_value11 = new_key11 + ':' + key_value_parts11[1]
                            else:
                                updated_value11 = new_key11 
                            if original_value11.startswith("td!"):
                                updated_value11 = "td!"+updated_value11
                            else:
                                updated_value11 =   updated_value11 
                            latest_record1.dlt_melements_11 = updated_value11
                            latest_record1.save()
                        
                        new_key12 = request.POST.get('input_12')
                        if new_key12 :
                            key_value_parts12=[]
                            if original_value12 is not None:
                                key_value_parts12 = original_value12.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts12) > 1:
                                updated_value12 = new_key12 + ':' + key_value_parts12[1]
                            else:
                                updated_value12 = new_key12
                            if original_value12.startswith("td!"):
                                updated_value12 = "td!"+updated_value12
                            else:
                                updated_value12 =   updated_value12 
                            latest_record1.dlt_melements_12 = updated_value12
                            latest_record1.save()
                        
                        new_key13 = request.POST.get('input_13')
                        if new_key13 :
                            key_value_parts13=[]
                            if original_value13 is not None:
                                key_value_parts13 = original_value13.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts13) > 1:
                                updated_value13 = new_key13 + ':' + key_value_parts13[1]
                            else:
                                updated_value13 = new_key13 
                            if original_value13.startswith("td!"):
                                updated_value13 = "td!"+updated_value13
                            else:
                                updated_value13 =   updated_value13 
                            latest_record1.dlt_melements_13 = updated_value13
                            latest_record1.save()
                        
                        new_key14 = request.POST.get('input_14')
                        if new_key14 :
                            key_value_parts14=[]
                            if original_value14 is not None:
                                key_value_parts14 = original_value14.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts14) > 1:
                                updated_value14 = new_key14 + ':' + key_value_parts14[1]
                            else:
                                updated_value14 = new_key14
                            if original_value14.startswith("td!"):
                                updated_value14 = "td!"+updated_value14
                            else:
                                updated_value14 =   updated_value14 
                            latest_record1.dlt_melements_14 = updated_value14
                            latest_record1.save()
                        
                        new_key15 = request.POST.get('input_15')
                        if new_key15 :
                            key_value_parts15=[]
                            if original_value15 is not None:
                                key_value_parts15 = original_value15.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts15) > 1:
                                updated_value15 = new_key15 + ':' + key_value_parts15[1]
                            else:
                                updated_value15 = new_key15
                            if original_value15.startswith("td!"):
                                updated_value15 = "td!"+updated_value15
                            else:
                                updated_value15 =   updated_value15 
                            latest_record1.dlt_melements_15 = updated_value15
                            latest_record1.save()
                        return redirect("/save")
                
                    
                else:  
                    mapping=dlm_docmap.objects.create(dlm_docmap_clientid=client_id,dlm_docmap_dtype=d_type,dlm_docmap_element=result2,dlm_docmap_cname=result1,dlm_docmap_uid=u_id)
                    print('success')
                    docmap_id = dlm_docmap.objects.order_by('-iddlm_docmap').first()
                    docmap_id=docmap_id.iddlm_docmap
                    DltDocproc.objects.filter(iddlt_docproc=docproc_id).update(dlt_docproc_dataid=docmap_id)
                    prompt_value = request.POST.get('prompt', '')
                    if prompt_value == 'Yes':
                        print("inside if")
                        new_key1 = request.POST.get('input_1')
                        if new_key1 :
                            print("python")
                            key_value_parts1=[]
                            if original_value1 is not None:
                                key_value_parts1 = original_value1.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts1) > 1:
                                updated_value1 = new_key1 + ':' + key_value_parts1[1]
                            else:
                                updated_value1 = new_key1
                            if original_value1.startswith("td!"):
                                updated_value1 = "td!"+updated_value1
                            else:
                                updated_value1 =   updated_value1 
                            latest_record1.dlt_melements_1 = updated_value1
                            latest_record1.save()
                        
                        new_key2 = request.POST.get('input_2')
                        if new_key2 :
                            key_value_parts2=[]
                            if original_value2 is not None:
                                key_value_parts2 = original_value2.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts2) > 1:
                                updated_value2 = new_key2 + ':' + key_value_parts2[1]
                            else:
                                updated_value2 = new_key2
                            if original_value2.startswith("td!"):
                                updated_value2 = "td!"+updated_value2
                            else:
                                updated_value2 =   updated_value2 
                            latest_record1.dlt_melements_2 = updated_value2
                            latest_record1.save()
                            
                        new_key3 = request.POST.get('input_3')
                        if new_key3 :
                            key_value_parts3=[]
                            if original_value3 is not None:
                                key_value_parts3 = original_value3.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts3) > 1:
                                updated_value3 = new_key3 + ':' + key_value_parts3[1]
                            else:
                                updated_value3 = new_key3
                            if original_value3.startswith("td!"):
                                updated_value3 = "td!"+updated_value3
                            else:
                                updated_value3 =   updated_value3 
                            latest_record1.dlt_melements_3 = updated_value3
                            latest_record1.save()
                        
                        new_key4 = request.POST.get('input_4')
                        if new_key4 :
                            key_value_parts4=[]
                            if original_value4 is not None:
                                key_value_parts4 = original_value4.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts4) > 1:
                                updated_value4 = new_key4 + ':' + key_value_parts4[1]
                            else:
                                updated_value4 = new_key4
                            if original_value4.startswith("td!"):
                                updated_value4 = "td!"+updated_value4
                            else:
                                updated_value4 =   updated_value4 
                            latest_record1.dlt_melements_4 = updated_value4
                            latest_record1.save()
                        
                        new_key5 = request.POST.get('input_5')
                        if new_key5 :
                            key_value_parts5=[]
                            if original_value5 is not None:
                                key_value_parts5 = original_value5.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts5) > 1:
                                updated_value5 = new_key5 + ':' + key_value_parts5[1]
                            else:
                                updated_value5 = new_key5
                            if original_value5.startswith("td!"):
                                updated_value5 = "td!"+updated_value5
                            else:
                                updated_value5 =   updated_value5 
                            latest_record1.dlt_melements_5 = updated_value5
                            latest_record1.save()
                    
                        new_key6 = request.POST.get('input_6')
                        if new_key6 :
                            key_value_parts6=[]
                            if original_value6 is not None:
                                key_value_parts6 = original_value6.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts6) > 1:
                                updated_value6 = new_key6 + ':' + key_value_parts6[1]
                            else:
                                updated_value6 = new_key6
                            if original_value6.startswith("td!"):
                                updated_value6 = "td!"+updated_value6
                            else:
                                updated_value6 =   updated_value6 
                            latest_record1.dlt_melements_6 = updated_value6
                            latest_record1.save()
                        
                        new_key7 = request.POST.get('input_7')
                        if new_key7 :
                            key_value_parts7=[]
                            if original_value7 is not None:
                                key_value_parts7 = original_value7.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts7) > 1:
                                updated_value7 = new_key7 + ':' + key_value_parts7[1]
                            else:
                                updated_value7 = new_key7 
                            if original_value7.startswith("td!"):
                                updated_value7 = "td!"+updated_value7
                            else:
                                updated_value7 =   updated_value7 
                            latest_record1.dlt_melements_7 = updated_value7
                            latest_record1.save()
                        
                        new_key8 = request.POST.get('input_8')
                        if new_key8 :
                            key_value_parts8=[]
                            if original_value8 is not None:
                                key_value_parts8 = original_value8.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts8) > 1:
                                updated_value8 = new_key8 + ':' + key_value_parts8[1]
                            else:
                                updated_value8 = new_key8
                            if original_value8.startswith("td!"):
                                updated_value8 = "td!"+updated_value8
                            else:
                                updated_value8 =   updated_value8 
                            latest_record1.dlt_melements_8 = updated_value8
                            latest_record1.save()
                        
                        new_key9 = request.POST.get('input_9')
                        if new_key9 :
                            key_value_parts9=[]
                            if original_value9 is not None:
                                key_value_parts9 = original_value9.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts9) > 1:
                                updated_value9 = new_key9 + ':' + key_value_parts9[1]
                            else:
                                updated_value9 = new_key9
                            if original_value9.startswith("td!"):
                                updated_value9 = "td!"+updated_value9
                            else:
                                updated_value9 =   updated_value9 
                            latest_record1.dlt_melements_9 = updated_value9
                            latest_record1.save()
                        
                        new_key10 = request.POST.get('input_10')
                        if new_key10 :
                            key_value_parts10=[]
                            if original_value10 is not None:
                                key_value_parts10 = original_value10.split(':', 1)  # Split the original value into key and value
                            
                            if len(key_value_parts10) > 1:
                                updated_value10 = new_key10 + ':' + key_value_parts10[1]
                            else:
                                updated_value10 = new_key10
                            if original_value10.startswith("td!"):
                                updated_value10 = "td!"+updated_value10
                            else:
                                updated_value10 =   updated_value10 
                            latest_record1.dlt_melements_10 = updated_value10
                            latest_record1.save()
                            
                        new_key11 = request.POST.get('input_11')
                        if new_key11 :
                            key_value_parts11=[]
                            if original_value11 is not None:
                                key_value_parts11 = original_value11.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts11) > 1:
                                updated_value11 = new_key11 + ':' + key_value_parts11[1]
                            else:
                                updated_value11 = new_key11 
                            if original_value11.startswith("td!"):
                                updated_value11 = "td!"+updated_value11
                            else:
                                updated_value11 =   updated_value11 
                            latest_record1.dlt_melements_11 = updated_value11
                            latest_record1.save()
                        
                        new_key12 = request.POST.get('input_12')
                        if new_key12 :
                            key_value_parts12=[]
                            if original_value12 is not None:
                                key_value_parts12 = original_value12.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts12) > 1:
                                updated_value12 = new_key12 + ':' + key_value_parts12[1]
                            else:
                                updated_value12 = new_key12
                            if original_value12.startswith("td!"):
                                updated_value12 = "td!"+updated_value12
                            else:
                                updated_value12 =   updated_value12 
                            latest_record1.dlt_melements_12 = updated_value12
                            latest_record1.save()
                        
                        new_key13 = request.POST.get('input_13')
                        if new_key13 :
                            key_value_parts13=[]
                            if original_value13 is not None:
                                key_value_parts13 = original_value13.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts13) > 1:
                                updated_value13 = new_key13 + ':' + key_value_parts13[1]
                            else:
                                updated_value13 = new_key13 
                            if original_value13.startswith("td!"):
                                updated_value13 = "td!"+updated_value13
                            else:
                                updated_value13 =   updated_value13 
                            latest_record1.dlt_melements_13 = updated_value13
                            latest_record1.save()
                        
                        new_key14 = request.POST.get('input_14')
                        if new_key14 :
                            key_value_parts14=[]
                            if original_value14 is not None:
                                key_value_parts14 = original_value14.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts14) > 1:
                                updated_value14 = new_key14 + ':' + key_value_parts14[1]
                            else:
                                updated_value14 = new_key14
                            if original_value14.startswith("td!"):
                                updated_value14 = "td!"+updated_value14
                            else:
                                updated_value14 =   updated_value14 
                            latest_record1.dlt_melements_14 = updated_value14
                            latest_record1.save()
                        
                        new_key15 = request.POST.get('input_15')
                        if new_key15 :
                            key_value_parts15=[]
                            if original_value15 is not None:
                                key_value_parts15 = original_value15.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts15) > 1:
                                updated_value15 = new_key15 + ':' + key_value_parts15[1]
                            else:
                                updated_value15 = new_key15
                            if original_value15.startswith("td!"):
                                updated_value15 = "td!"+updated_value15
                            else:
                                updated_value15 =   updated_value15 
                            latest_record1.dlt_melements_15 = updated_value15
                            latest_record1.save()
                        return redirect("/save")
                    else:
                        print('inside else')
                        new_key1 = request.POST.get('input_1')
                        if new_key1 :
                            print("python")
                            key_value_parts1=[]
                            if original_value1 is not None:
                                key_value_parts1 = original_value1.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts1) > 1:
                                updated_value1 = new_key1 + ':' + key_value_parts1[1]
                            else:
                                updated_value1 = new_key1
                            if original_value1.startswith("td!"):
                                updated_value1 = "td!"+updated_value1
                            else:
                                updated_value1 =   updated_value1 
                            latest_record1.dlt_melements_1 = updated_value1
                            latest_record1.save()
                        
                        new_key2 = request.POST.get('input_2')
                        if new_key2 :
                            key_value_parts2=[]
                            if original_value2 is not None:
                                key_value_parts2 = original_value2.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts2) > 1:
                                updated_value2 = new_key2 + ':' + key_value_parts2[1]
                            else:
                                updated_value2 = new_key2
                            if original_value2.startswith("td!"):
                                updated_value2 = "td!"+updated_value2
                            else:
                                updated_value2 =   updated_value2 
                            latest_record1.dlt_melements_2 = updated_value2
                            latest_record1.save()
                            
                        new_key3 = request.POST.get('input_3')
                        if new_key3 :
                            key_value_parts3=[]
                            if original_value3 is not None:
                                key_value_parts3 = original_value3.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts3) > 1:
                                updated_value3 = new_key3 + ':' + key_value_parts3[1]
                            else:
                                updated_value3 = new_key3
                            if original_value3.startswith("td!"):
                                updated_value3 = "td!"+updated_value3
                            else:
                                updated_value3 =   updated_value3 
                            latest_record1.dlt_melements_3 = updated_value3
                            latest_record1.save()
                        
                        new_key4 = request.POST.get('input_4')
                        if new_key4 :
                            key_value_parts4=[]
                            if original_value4 is not None:
                                key_value_parts4 = original_value4.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts4) > 1:
                                updated_value4 = new_key4 + ':' + key_value_parts4[1]
                            else:
                                updated_value4 = new_key4
                            if original_value4.startswith("td!"):
                                updated_value4 = "td!"+updated_value4
                            else:
                                updated_value4 =   updated_value4 
                            latest_record1.dlt_melements_4 = updated_value4
                            latest_record1.save()
                        
                        new_key5 = request.POST.get('input_5')
                        if new_key5 :
                            key_value_parts5=[]
                            if original_value5 is not None:
                                key_value_parts5 = original_value5.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts5) > 1:
                                updated_value5 = new_key5 + ':' + key_value_parts5[1]
                            else:
                                updated_value5 = new_key5
                            if original_value5.startswith("td!"):
                                updated_value5 = "td!"+updated_value5
                            else:
                                updated_value5 =   updated_value5 
                            latest_record1.dlt_melements_5 = updated_value5
                            latest_record1.save()
                    
                        new_key6 = request.POST.get('input_6')
                        if new_key6 :
                            key_value_parts6=[]
                            if original_value6 is not None:
                                key_value_parts6 = original_value6.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts6) > 1:
                                updated_value6 = new_key6 + ':' + key_value_parts6[1]
                            else:
                                updated_value6 = new_key6
                            if original_value6.startswith("td!"):
                                updated_value6 = "td!"+updated_value6
                            else:
                                updated_value6 =   updated_value6 
                            latest_record1.dlt_melements_6 = updated_value6
                            latest_record1.save()
                        
                        new_key7 = request.POST.get('input_7')
                        if new_key7 :
                            key_value_parts7=[]
                            if original_value7 is not None:
                                key_value_parts7 = original_value7.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts7) > 1:
                                updated_value7 = new_key7 + ':' + key_value_parts7[1]
                            else:
                                updated_value7 = new_key7 
                            if original_value7.startswith("td!"):
                                updated_value7 = "td!"+updated_value7
                            else:
                                updated_value7 =   updated_value7 
                            latest_record1.dlt_melements_7 = updated_value7
                            latest_record1.save()
                        
                        new_key8 = request.POST.get('input_8')
                        if new_key8 :
                            key_value_parts8=[]
                            if original_value8 is not None:
                                key_value_parts8 = original_value8.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts8) > 1:
                                updated_value8 = new_key8 + ':' + key_value_parts8[1]
                            else:
                                updated_value8 = new_key8
                            if original_value8.startswith("td!"):
                                updated_value8 = "td!"+updated_value8
                            else:
                                updated_value8 =   updated_value8 
                            latest_record1.dlt_melements_8 = updated_value8
                            latest_record1.save()
                        
                        new_key9 = request.POST.get('input_9')
                        if new_key9 :
                            key_value_parts9=[]
                            if original_value9 is not None:
                                key_value_parts9 = original_value9.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts9) > 1:
                                updated_value9 = new_key9 + ':' + key_value_parts9[1]
                            else:
                                updated_value9 = new_key9
                            if original_value9.startswith("td!"):
                                updated_value9 = "td!"+updated_value9
                            else:
                                updated_value9 =   updated_value9 
                            latest_record1.dlt_melements_9 = updated_value9
                            latest_record1.save()
                        
                        new_key10 = request.POST.get('input_10')
                        if new_key10 :
                            key_value_parts10=[]
                            if original_value10 is not None:
                                key_value_parts10 = original_value10.split(':', 1)  # Split the original value into key and value
                            
                            if len(key_value_parts10) > 1:
                                updated_value10 = new_key10 + ':' + key_value_parts10[1]
                            else:
                                updated_value10 = new_key10
                            if original_value10.startswith("td!"):
                                updated_value10 = "td!"+updated_value10
                            else:
                                updated_value10 =   updated_value10 
                            latest_record1.dlt_melements_10 = updated_value10
                            latest_record1.save()
                            
                        new_key11 = request.POST.get('input_11')
                        if new_key11 :
                            key_value_parts11=[]
                            if original_value11 is not None:
                                key_value_parts11 = original_value11.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts11) > 1:
                                updated_value11 = new_key11 + ':' + key_value_parts11[1]
                            else:
                                updated_value11 = new_key11 
                            if original_value11.startswith("td!"):
                                updated_value11 = "td!"+updated_value11
                            else:
                                updated_value11 =   updated_value11 
                            latest_record1.dlt_melements_11 = updated_value11
                            latest_record1.save()
                        
                        new_key12 = request.POST.get('input_12')
                        if new_key12 :
                            key_value_parts12=[]
                            if original_value12 is not None:
                                key_value_parts12 = original_value12.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts12) > 1:
                                updated_value12 = new_key12 + ':' + key_value_parts12[1]
                            else:
                                updated_value12 = new_key12
                            if original_value12.startswith("td!"):
                                updated_value12 = "td!"+updated_value12
                            else:
                                updated_value12 =   updated_value12 
                            latest_record1.dlt_melements_12 = updated_value12
                            latest_record1.save()
                        
                        new_key13 = request.POST.get('input_13')
                        if new_key13 :
                            key_value_parts13=[]
                            if original_value13 is not None:
                                key_value_parts13 = original_value13.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts13) > 1:
                                updated_value13 = new_key13 + ':' + key_value_parts13[1]
                            else:
                                updated_value13 = new_key13 
                            if original_value13.startswith("td!"):
                                updated_value13 = "td!"+updated_value13
                            else:
                                updated_value13 =   updated_value13 
                            latest_record1.dlt_melements_13 = updated_value13
                            latest_record1.save()
                        
                        new_key14 = request.POST.get('input_14')
                        if new_key14 :
                            key_value_parts14=[]
                            if original_value14 is not None:
                                key_value_parts14 = original_value14.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts14) > 1:
                                updated_value14 = new_key14 + ':' + key_value_parts14[1]
                            else:
                                updated_value14 = new_key14
                            if original_value14.startswith("td!"):
                                updated_value14 = "td!"+updated_value14
                            else:
                                updated_value14 =   updated_value14 
                            latest_record1.dlt_melements_14 = updated_value14
                            latest_record1.save()
                        
                        new_key15 = request.POST.get('input_15')
                        if new_key15 :
                            key_value_parts15=[]
                            if original_value15 is not None:
                                key_value_parts15 = original_value15.split(':', 1)  # Split the original value into key and value
                            if len(key_value_parts15) > 1:
                                updated_value15 = new_key15 + ':' + key_value_parts15[1]
                            else:
                                updated_value15 = new_key15
                            if original_value15.startswith("td!"):
                                updated_value15 = "td!"+updated_value15
                            else:
                                updated_value15 =   updated_value15 
                            latest_record1.dlt_melements_15 = updated_value15
                            latest_record1.save()
                        return redirect("/save")
                     # Retrieve the latest dlt_melements_1 for the given client ID based on creation date
                    

            elif 'form_submitted' in request.session:
                # delete the session value when the page is reloaded
                request.session.pop('form_submitted', None)       
            
            return render(request,'uploadpage.html',{'found':found,'elem_list':elem_list,'maped_list':maped_list,'maped':maped,'client_id':client_id,'docmap':docmap,'is_active':is_active,'username':username,'elements':elements,'data_dict':data_dict,'usertype':usertype,'user_mapped':user_mapped})

    else:

       return redirect("/login")

def extract_field_name_and_value(field_value):
    field_parts = str(field_value).split(":")
    if len(field_parts) >= 2:
        field_name = field_parts[0].strip()
        value = ":".join(field_parts[1:]).strip()
        return field_name, value
    else:
        return None, None
    
    

   
   

def download_table_view(request):
    print("download")
    client_id = request.session.get('c_id')
    value2=request.session['id']
    latest_record =  dlt_melements.objects.get(iddlt_melements=value2)
    dwld_sts=''
    updated_list=''
    #latest_record = dlt_melements.objects.filter(dlt_melements_cid=client_id).order_by('-dlt_melements_cdate').first()

    # Check if the latest_record exists
    if latest_record:
        # Create a dictionary dynamically using field values with modified field names
        record_dict = {}

        # Iterate over the fields and get their values
        for field in latest_record._meta.fields:
            print(field)
            if field.name != 'dlt_melements_cdate':  # Exclude the specific column name
                field_value = getattr(latest_record, field.name)
                #print("value")
                print(field_value)
                if type(field_value) == str:
                    if field_value.startswith("td!"):
                        field_value=field_value[3:]
                    else:
                        field_value=field_value
                field_name, value = extract_field_name_and_value(field_value)
                print("name")
                print(field_name)
                print(value)
                if value:
                    for i in value:
                        if i in '[':
                            value = value.strip('][').split(', ')
                            print(type(value))
                            value = [element.strip().strip("'") for element in value]
                
                if field_name and value:
                    record_dict[field_name] = value

        # Determine the desired format based on the request
        format = request.GET.get('format', 'csv').lower()

        if format == 'csv':
            print("csv")
            # Create a response object with the appropriate content type
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="latest_record.csv"'

            # Create a CSV writer and write the record dictionary values
            writer = csv.writer(response)
            writer.writerow(record_dict.keys())
            writer.writerow(record_dict.values())

            val=1
            dwld_sts+=str(val)
            print(dwld_sts)
            obj = DltDocproc.objects.get(dlt_docproc_elemid=value2)
            print(obj)
            
            existing_list = obj.dlt_docproc_dwldsts
            print(existing_list)
            if (existing_list):
                updated_list = (existing_list) +','+ (dwld_sts)
            else:
                updated_list +=  dwld_sts
            DltDocproc.objects.filter(dlt_docproc_elemid=value2).update(dlt_docproc_dwldsts=updated_list)
            
            return response

        elif format == 'xlsx':
            # Create a DataFrame from record_dict
            #df = pd.DataFrame([record_dict], columns=record_dict.keys())
            # Create an empty DataFrame
            df = pd.DataFrame(columns=record_dict.keys())

            # Iterate over the record_dict and add rows to the DataFrame
            for key, value in record_dict.items():
                if isinstance(value, list):
                    # If the value is a list, add each non-empty element (with quotes removed) to a separate row in the corresponding column
                    for i, val in enumerate(value):
                        if val != '':
                            val = val.strip("'")  # Remove surrounding quotes from the value
                            if i >= len(df):
                                df.loc[i] = [None] * len(df.columns)  # Add an empty row
                            df.loc[i, key] = val  # Add the non-empty list value to the corresponding column
                else:
                    # If the value is not a list and not an empty string, add it to the first row in the corresponding column (with quotes removed)
                    if value != '':
                        value = value.strip("'")  # Remove surrounding quotes from the value
                        df.loc[0, key] = value

            # Create a BytesIO buffer to save the Excel file
            excel_buffer = io.BytesIO()

            # Create an Excel writer using pandas and write the DataFrame to it
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')

            # Set the buffer's file position to the start
            excel_buffer.seek(0)

            # Create a response object with the Excel file content
            response = HttpResponse(excel_buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="latest_record.xlsx"'
            
            val=2
            dwld_sts+=str(val)
            print(dwld_sts)
            obj = DltDocproc.objects.get(dlt_docproc_elemid=value2)
            print(obj)
            existing_list = obj.dlt_docproc_dwldsts
            print(existing_list)
            if (existing_list):
                updated_list = (existing_list) +','+ (dwld_sts)
            else:
                updated_list +=  dwld_sts
            DltDocproc.objects.filter(dlt_docproc_elemid=value2).update(dlt_docproc_dwldsts=updated_list)

            return response
                    
           
           

        elif format == 'json':
            # Create a response object with the appropriate content type
            response = HttpResponse(content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="latest_record.json"'

            # Convert the record dictionary to JSON and write it to the response
            json.dump(record_dict, response)
            
            val=3
            dwld_sts+=str(val)
            print(dwld_sts)
            obj = DltDocproc.objects.get(dlt_docproc_elemid=value2)
            print(obj)
            existing_list = obj.dlt_docproc_dwldsts
            print(existing_list)
            if (existing_list):
                updated_list = (existing_list) +','+ (dwld_sts)
            else:
                updated_list +=  dwld_sts
            DltDocproc.objects.filter(dlt_docproc_elemid=value2).update(dlt_docproc_dwldsts=updated_list)
            
            return response

    # If the latest_record doesn't exist, return an error message or handle it accordingly
    else:
        return HttpResponse('No latest record found.')
    # If the latest_record doesn't exist, return an error message or handle it accordingly
    #else:
        #return HttpResponse('No latest record found.')


def delete_data(request):
    client_id = request.session.get('c_id')
    value2=request.session['id']
    latest_record =  dlt_melements.objects.get(iddlt_melements=value2)
    #latest_record = dlt_melements.objects.filter(dlt_melements_cid=client_id).latest('iddlt_melements')
    #latest_record = dlt_melements.objects.latest('iddlt_melements')
    latest_record.delete()
    return HttpResponse('Record deleted successfully')

def preview(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        fp=request.session['fp']
        filename=request.session['execute']
        columns=request.session['colvalues']
        column_names=request.session['column_headers']
        data_list=request.session['data_list']
        TableDetails=request.session['index_values']
        print(TableDetails)
        image = Image.open(fp)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        #img_str='hello'
        CompanyDetails = {}
        InvoiceDetails = {}
        CustomerDetails = {}
        ShiptoAddress = {}
        
        for item in data_list:
            if item.startswith('Company'):
                key, value = item.split(':')
                CompanyDetails[key.strip()] = value.strip()
            elif item.startswith('invoice') or 'invoice' in item.lower():
                key_value = item.split(':', 1)  # Split at the first occurrence of ':'
                key = key_value[0].strip()
                value = key_value[1].strip() if len(key_value) > 1 else ''
                InvoiceDetails[key] = value
            elif item.startswith('To Customer') or item.startswith('Sold') or item.startswith('Customer') or item.endswith('Customer') or item.endswith('customer'):
                key_value = item.split(':', 1)  # Split at the first occurrence of ':'
                key = key_value[0].strip()
                value = key_value[1].strip() if len(key_value) > 1 else ''
                CustomerDetails[key] = value
            elif item.startswith('Ship'):
                key, value = item.split(':')
                ShiptoAddress[key.strip()] = value.strip()
        print(CompanyDetails)
        print(InvoiceDetails)
        print(CustomerDetails)
        print(ShiptoAddress)
        my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
        data = {
"xmin":[], "ymin":[], "xmax":[], "ymax":[], 
"confidence":[], "class":[], "name":[]
}
        if request.method=='POST':
                selected_values = request.POST.getlist('SELECTED')
                print(selected_values)
                if selected_values==['']:
                    print('else')
                    image = Image.open(fp)
                    # image.show()
                    buffer = BytesIO()
                    image.save(buffer, format="PNG")
                    img_str = base64.b64encode(buffer.getvalue()).decode()
                    response = {'img_str': img_str}
                
                    return JsonResponse(response)
            # Generate new image based on selected values
                
                else:
                    # Use default image if no values are selected
                    # image = Image.open('C:\\Users\\dev6\\Pictures\\B13.jpg')
                    # buffer = BytesIO()
                    # image.save(buffer, format="PNG")
                    # img_str = base64.b64encode(buffer.getvalue()).decode()
                    # response = {'img_str': img_str}
                
                    # return JsonResponse(response)
                    
                    # value=dict(value)
                    # data['xmin']=value['xmin']
                    # print(value['xmin'])
                    
                    if selected_values[0].startswith('invoice'):
                        name = 'InvoiceDetails'
                    elif selected_values[0] == 'Company name' or selected_values[0] == 'Company Name':
                        name='CompanyName'
                    elif selected_values[0].startswith('Company'):
                        name='CompanyDetails'
                    elif selected_values[0].startswith('Ship') or selected_values[0].startswith('Shipped') :
                        name='ShiptoAddress'
                    elif selected_values[0].startswith('To Customer') or selected_values[0].startswith('Sold') or selected_values[0].startswith('Customer') or selected_values[0].endswith('Customer') or selected_values[0].endswith('customer'):
                        name='CustomerDetails'
                    elif selected_values[0] in TableDetails:
                        name='TableDetails'
                    position = columns[-1].index(name)
                    print(position)
                    a=position
                    first_values = [column[a] for column in columns]
                    print(first_values)
                    
                    data['xmin']=first_values[0]
                    data['ymin']=first_values[1]
                    data['xmax']=first_values[2]
                    data['ymax']=first_values[3]
                    data['confidence']=first_values[4]
                    data['class']=first_values[5]
                    data['name']=first_values[6]
                    print(data)
                    df = pd.DataFrame(data, index=[0])
                    print(df)

                    
                    image = Image.open(fp)
                    buffer = BytesIO()
                    image.save(buffer, format="PNG")
                    i_str = base64.b64encode(buffer.getvalue()).decode()
                    
                    draw = ImageDraw.Draw(image)
                    font = ImageFont.load_default()


                    color = "#4892EA"
                    draw.rectangle([
                        int(float(df['xmin'])), int(float(df['ymin'])), int(float(df['xmax'])), int(float(df['ymax']))
                    ], outline=color, width=5)

                    text = df['name'][0]

                    text_size = font.getsize(text)

                    # # set button size + 10px margins
                    button_size = (text_size[0]+20, text_size[1]+20)
                    button_img = Image.new('RGBA', button_size, color)
                    # # put text on button with 10px margins
                    button_draw = ImageDraw.Draw(button_img)
                    button_draw.text((10, 10), text, font=font, fill=(255,255,255,255))

                    # # put button on source image in position (0, 0)
                    image.paste(button_img, (int(float(df['xmin'])), int(float(df['ymin']))))
                    # image.show()
                    buffer = BytesIO()
                    image.save(buffer, format="PNG")
                    img_str = base64.b64encode(buffer.getvalue()).decode()
                    # with open(image, 'rb') as f:
                    #     img_data = base64.b64encode(f.read()).decode('utf-8')
                    
                    response = {
                    'img_str': img_str,'i_str':i_str
                }
                    return JsonResponse(response)
            # Generate new image based on selected values
                
                
                    # Use default image if no values are selected
                    # image = Image.open('C:\\Users\\dev6\\Pictures\\B13.jpg')
                    # buffer = BytesIO()
                    # image.save(buffer, format="PNG")
                    # img_str = base64.b64encode(buffer.getvalue()).decode()
                    # response = {'img_str': img_str}
                
                    # return JsonResponse(response)
                
                # value=dict(value)
                # data['xmin']=value['xmin']
                # print(value['xmin'])
                
        return render(request,'index.html',{'username':username,'usertype':usertype,'user_mapped':user_mapped,'img_str':img_str,'ShiptoAddress': ShiptoAddress,'CustomerDetails':CustomerDetails,'CompanyDetails':CompanyDetails,'InvoiceDetails':InvoiceDetails,'filename':filename,'TableDetails':TableDetails})
    else:
        return redirect("/login") 
    
#subscription
def subscribe(request):
    username= request.session['username']
    usertype=request.session['usertype']
    user_mapped=request.session['usermapped']
    return render(request,'subscription.html',{'username':username,'usertype':usertype,'user_mapped':user_mapped})

#super admin table#####

def categorytable(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        cat = dlm_doctype.objects.all()
        return render(request,'categorytable.html',{'username':username,'usertype':usertype,'cat':cat,'user_mapped':user_mapped})
    else:
        return redirect("/login") 

def plantable(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        plans=dlm_plan.objects.all()
        return render(request,'plantable.html',{'username':username,'usertype':usertype,'plans':plans,'user_mapped':user_mapped})
    else:
        return redirect("/login")

def pricetable(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        prices=dlm_price.objects.all()
        return render(request,'pricetable.html',{'username':username,'usertype':usertype,'prices':prices,'user_mapped':user_mapped})
    else:
        return redirect("/login")

def featuretable(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        feature=DlmFeature.objects.all()
        return render(request,'featuretable.html',{'username':username,'usertype':usertype,'feature':feature,'user_mapped':user_mapped})
    else:
        return redirect("/login")
    
def tenanttable(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        client=DlmCust.objects.all()
        tenant=DlmTenant.objects.all()
        
        return render(request,'tenantTable.html',{'tenant':tenant,'username':username,'usertype':usertype,'client':client ,'user_mapped':user_mapped })
    else:
        return redirect("/login")
    
    
def clientsTable(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        client=DlmCust.objects.all()
        tenant=DlmTenant.objects.all()
        distinct_tntid_list = DlmTenant.objects.values_list('iddlm_tenant', flat=True).distinct()
        
        
        return render(request,'clientstable.html',{'distinct_tntid_list':distinct_tntid_list,'tenant':tenant,'username':username,'usertype':usertype,'client':client ,'user_mapped':user_mapped })
    else:
        return redirect("/login")

#super admin details adding#####

def addcategory(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        if request.method == 'POST':
            catname = request.POST.get('catname')
            catgrp = request.POST.get('catgrp')

            cat = dlm_doctype.objects.create(dlm_doctype_nam = catname , dlm_doctype_catgrp = catgrp , dlm_doctype_cby = 'SuperAdmin')
            cat.save()
            return redirect('/categorytable')
        return render(request,'addcategory.html',{'username':username,'usertype':usertype,'user_mapped':user_mapped})
    else:
        return redirect("/login")

def addplan(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        execute=True
        grpcode='superadmin'
        feature=DlmFeature.objects.all()
        if grpcode=='superadmin':
            if request.method=='POST':
                pname=request.POST['pname']
                trn_count=request.POST['trn_count']
                user_count=request.POST['user_count']
                file_size=request.POST['file_size']
                category_size=request.POST['category_size']
                plcatgrp=request.POST.get('plcatgroup','')
                plusrtype=request.POST.get('plusrtype')
                feature= request.POST.getlist('feature')
                if plusrtype=='Personal':
                    plusrtype=0
                else:
                    plusrtype=1
                print(plusrtype)
                
                print(feature)
                ids=DlmFeature.objects.filter(dlm_feature_name__in=feature).values_list('iddlm_feature')
                print(ids)
                featid=list(ids)
                print(featid)
                feat=','.join(map(str,featid))
                print(feat)
                
                a=str(feat)
                b=""
                c=len(a)
                for i in range(c):
                    if a[i].isdigit():
                        b+=a[i]
                print(b)

                d=','.join(b)
                print(d)
                print(type(d))
                
                
                plan=dlm_plan(dlm_plan_catgrp=plcatgrp, dlm_plan_nam=pname,dlm_plan_trncnt=trn_count,dlm_plan_usrcnt=user_count,dlm_plan_filesize=file_size,
                                                dlm_plan_catsize=category_size, dlm_plan_cby = 'Super Admin',dlm_plan_status='active',dlm_plan_usrtype= plusrtype, dlm_plan_featureid = d)
                plan.save()
                
                ids=dlm_plan.objects.filter(dlm_plan_nam=pname).values('iddlm_plan')[0]['iddlm_plan']

                global id
                def id():
                    return ids
                return redirect("/plantable")
        return render(request,'addplan.html',{'username':username,'usertype':usertype,'execute':execute,'feature':feature,'user_mapped':user_mapped})
    else:
        return redirect("/login")

def addprice(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        catgroup=dlm_plan.objects.all()
        if request.method=='POST':
            plcatgroup=request.POST['plcatgroup']
            valtype=request.POST['valtype']
            amt=request.POST['amt']

            ids=dlm_plan.objects.filter(dlm_plan_nam=plcatgroup).values('iddlm_plan')[0]['iddlm_plan']

            

            price=dlm_price.objects.create(dlm_price_planid=ids,dlm_price_valtype=valtype,dlm_price_amt=amt)
            return redirect("/pricetable")
        return render(request,'addprice.html',{'username':username,'usertype':usertype,'catgroup':catgroup,'user_mapped':user_mapped})
    else:
        return redirect("/login")
    

def addfeature(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        plan=dlm_plan.objects.all()
        
        if request.method=='POST':
            fname=request.POST['Fname']
            desc=request.POST['desc']
            
            

            feature = DlmFeature.objects.create( dlm_feature_name= fname, dlm_feature_desc= desc, dlm_feature_cby='Super Admin')
            feature.save()
            return redirect("featuretable")
        return render(request,'addfeature.html',{'username':username,'usertype':usertype,'plan':plan,'user_mapped':user_mapped})
    else:
        return redirect("/login")

#super admin details editing########

def editcategory(request,iddlm_doctype):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        cat = dlm_doctype.objects.get(iddlm_doctype =iddlm_doctype ) 
        if request.method == 'POST':
            #pname=request.POST['pname']
            #pname=request.POST['pname']
            catname = request.POST.get('catname')
            catgrp = request.POST.get('catgrp')
        
            cat.dlm_doctype_nam = catname
            cat.dlm_doctype_catgrp = catgrp
            cat.save()
            return redirect('/categorytable')
        return render(request,'editcategory.html', {'username':username,'usertype':usertype,'cat':cat,'user_mapped':user_mapped}) 
    else:
        return redirect("/login")

def editplan(request,iddlm_plan):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        plans = dlm_plan.objects.get(iddlm_plan=iddlm_plan)
        plan=dlm_plan.objects.all()
        feature=DlmFeature.objects.all()  
        print(plans)
        if request.method=='POST':
            pname=request.POST['pname']
            trn_count=request.POST['trn_count']
            user_count=request.POST['user_count']
            file_size=request.POST['file_size']
            category_size=request.POST['category_size']
            plcatgrp=request.POST.get('plcatgroup','')
            plusrtype= request.POST.get('plusrtype','')
            feature= request.POST.getlist('feature')
            if plusrtype=='Personal':
                plusrtype=0
            else:
                plusrtype=1
            print(plusrtype)
            print(feature)
            ids=DlmFeature.objects.filter(dlm_feature_name__in=feature).values_list('iddlm_feature')
            print(ids)
            featid=list(ids)
            print(featid)
            feat=','.join(map(str,featid))
            print(feat)
            a=str(feat)
            b=""
            c=len(a)
            for i in range(c):
                if a[i].isdigit():
                    b+=a[i]
            print(b)

            d=','.join(b)
            print(d)
            print(type(d))
            print(pname)
            print(plans)
        
            
            plans.dlm_plan_nam=pname
            plans.dlm_plan_trncnt=trn_count
            plans.dlm_plan_usrcnt=user_count
            plans.dlm_plan_filesize=file_size
            plans.dlm_plan_catsize=category_size
            plans.dlm_plan_catgrp=plcatgrp
            plans.dlm_plan_usrtype=plusrtype
            plans.dlm_plan_featureid=d
            plans.save()
            return redirect("/plantable")
        return render(request,'editplan.html', {'username':username,'usertype':usertype,'plans':plans,'plan':plan,'feature':feature,'user_mapped':user_mapped})  
    else:
        return redirect("/login")
    
def editprice(request,iddlm_price):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        prices = dlm_price.objects.get(iddlm_price=iddlm_price)  
        plan=dlm_plan.objects.all()
        print(prices)

        ids=dlm_price.objects.filter(iddlm_price=iddlm_price).values('dlm_price_planid')[0]['dlm_price_planid']
        plnam=dlm_plan.objects.filter(iddlm_plan=ids).values('dlm_plan_nam')[0]['dlm_plan_nam']

        if request.method=='POST':
            plcatgroup=request.POST['plcatgroup']
            valtype=request.POST['valtype']
            amt=request.POST['amt']

            idplan=dlm_plan.objects.filter(dlm_plan_nam=plcatgroup).values('iddlm_plan')[0]['iddlm_plan']

            prices.dlm_price_planid=idplan
            prices.dlm_price_valtype=valtype
            prices.dlm_price_amt=amt
            prices.save()
            return redirect('/pricetable')
        return render(request,'editprice.html', {'username':username,'usertype':usertype,'prices':prices,'plan':plan,'plnam':plnam,'user_mapped':user_mapped}) 
    else:
        return redirect("/login") 

def editfeature(request,iddlm_feature):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        cat = DlmFeature.objects.get(iddlm_feature=iddlm_feature ) 
        if request.method == 'POST':
            fname=request.POST['Fname']
            desc=request.POST['desc']
            plname=request.POST.get('plnam')
        
            cat.dlm_feature_name = fname
            cat.dlm_feature_desc= desc
            cat.save()
            return redirect('featuretable')
        return render(request,'editfeature.html', {'username':username,'usertype':usertype,'cat':cat,'user_mapped':user_mapped}) 
    else:
        return redirect("/login") 

#super-admin tenant/client activate
    
def ActiveClient(request,iddlm_cust ): 
    if 'username' in request.session: 
        client = DlmCust.objects.get(iddlm_cust =iddlm_cust )
        client.dlm_cust_status = 'active'
        client.save()
        usrid=DlmCustuser.objects.filter(dlm_custuser_custid=iddlm_cust).values_list('iddlm_custuser')
        usrid_list=[int(t[0]) for t in usrid]
        print(usrid_list)
        for uid in usrid_list:
            user=DlmCustuser.objects.get(iddlm_custuser=uid)
            user.dlm_custuser_status=client.dlm_cust_status
            user.save()
         
        return redirect("clientsTable") 
    else:
        return redirect("/login")
    
    
def Activatetenant(request,iddlm_tenant): 
    if 'username' in request.session: 
        tenant = DlmTenant.objects.get(iddlm_tenant = iddlm_tenant)
        #client=DlmCust.objects.get(iddlm_tenant = iddlm_cust)
        
        tenant.dlm_tenant_sts = 'Active'
        tenant.save()
        custid=DlmCust.objects.filter(dlm_cust_tntid=iddlm_tenant).values_list('iddlm_cust')
        print(custid)
        custid_list = [int(t[0]) for t in custid]
        print(custid_list)
        for obj in custid_list:
            cust = DlmCust.objects.get(iddlm_cust=obj)
            cust.dlm_cust_status = tenant.dlm_tenant_sts
            print(cust.dlm_cust_status)
            cust.save()
            usrid=DlmCustuser.objects.filter(dlm_custuser_custid=obj).values_list('iddlm_custuser')
            usrid_list=[int(t[0]) for t in usrid]
            print(usrid_list)
            for uid in usrid_list:
                user=DlmCustuser.objects.get(iddlm_custuser=uid)
                user.dlm_custuser_status=tenant.dlm_tenant_sts
                user.save()
        #client.dlm_cust_status = 'Active'
        #client.save()
        return redirect("tenanttable") 
    else:
        return redirect("/login")

#super admin details destroy/deleting#########

def deletecategory(request,iddlm_doctype ):
    if 'username' in request.session: 
        Doctype = dlm_doctype.objects.get(iddlm_doctype =iddlm_doctype )  
        Doctype.delete()  
        return redirect('/categorytable')
    else:
        return redirect("/login") 

def deleteplan(request,iddlm_plan): 
    if 'username' in request.session:  
        try:
            plans = dlm_plan.objects.get(iddlm_plan=iddlm_plan)  
            prices=dlm_price.objects.get(dlm_price_planid=iddlm_plan)
            prices.delete()
            plans.delete()  
            #messages.info(request,'Your records in price table also deleted')
            return redirect("/plantable")
        except:
            plans = dlm_plan.objects.get(iddlm_plan=iddlm_plan)  
            
            plans.delete()  
            return redirect("/plantable")
        # messages.info(request,"Refresh the page ,Delete your registered plan in Plan page ")
    else:
        return redirect("/login") 
    
def deleteprice(request,iddlm_price): 
    if 'username' in request.session: 
        try:
            price = dlm_price.objects.get(iddlm_price=iddlm_price)  
            price.delete()  
            return redirect("/pricetable")
        except:
            messages.info(request,"") 
    else:
        return redirect("/login")   

def deletefeature(request,iddlm_feature ): 
    if 'username' in request.session:  
        Doctype = DlmFeature.objects.get(iddlm_feature =iddlm_feature )  
        Doctype.delete()  
        return redirect('/featuretable')
    else:
        return redirect("/login") 

def disabletenant(request,iddlm_tenant ): 
    if 'username' in request.session: 
        tenant = DlmTenant.objects.get(iddlm_tenant = iddlm_tenant )
        #print(tenant)
        #client=DlmCust.objects.get(iddlm_tenant = iddlm_cust)
        tenant.dlm_tenant_sts = 'inactive'
        tenant.save()
        custid=DlmCust.objects.filter(dlm_cust_tntid=iddlm_tenant).values_list('iddlm_cust')
        print(custid)
        custid_list = [int(t[0]) for t in custid]
        print(custid_list)
        for obj in custid_list:
            cust = DlmCust.objects.get(iddlm_cust=obj)
            cust.dlm_cust_status = tenant.dlm_tenant_sts
            print(cust.dlm_cust_status)
            cust.save()
            usrid=DlmCustuser.objects.filter(dlm_custuser_custid=obj).values_list('iddlm_custuser')
            usrid_list=[int(t[0]) for t in usrid]
            print(usrid_list)
            for uid in usrid_list:
                user=DlmCustuser.objects.get(iddlm_custuser=uid)
                user.dlm_custuser_status=tenant.dlm_tenant_sts
                user.save()
        #client=DlmCust.objects.create(dlm_cust_status='inactive')
        #client.save()
        # client.dlm_cust_status = 'inactive'
        # client.save()
        return redirect("tenanttable") 
    else:
        return redirect("/login")

def deleteClient(request,iddlm_cust ): 
    if 'username' in request.session: 
        client = DlmCust.objects.get(iddlm_cust =iddlm_cust )
        client.dlm_cust_status = 'inactive'
        client.save()
        usrid=DlmCustuser.objects.filter(dlm_custuser_custid=iddlm_cust).values_list('iddlm_custuser')
        usrid_list=[int(t[0]) for t in usrid]
        print(usrid_list)
        for uid in usrid_list:
            user=DlmCustuser.objects.get(iddlm_custuser=uid)
            user.dlm_custuser_status=client.dlm_cust_status
            user.save()  
        return redirect("clientsTable") 
    else:
        return redirect("/login")

#app-admin work table#####

def usertable(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        user=DlmCustuser.objects.all()
        client=DlmCust.objects.all()
        custid = DlmCust.objects.filter(dlm_cust_email=username).values('iddlm_cust')[0]['iddlm_cust']
        print(custid)
        userclientid = DlmCustuser.objects.filter(dlm_custuser_custid = custid).values('dlm_custuser_custid')[0]['dlm_custuser_custid']
        print(userclientid)
        return render(request,'usertable.html',{'client':client,'username':username,'usertype':usertype,'user':user,'userclientid':userclientid,'user_mapped':user_mapped})
    else:
        return redirect("/login")

def clienttable(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        client=DlmCust.objects.all()
        tntid = DlmCust.objects.filter(dlm_cust_email=username).values('dlm_cust_tntid')[0]['dlm_cust_tntid']
        return render(request,'clienttable.html',{'username':username,'usertype':usertype,'client':client ,'tntid':tntid,'user_mapped':user_mapped })
    else:
        return redirect("/login")

#app-admin work details adding####

def adduser(request):
    if 'username' in request.session:
        client= DlmCust.objects.all()
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        tntid = DlmCust.objects.filter(dlm_cust_email=username).values('dlm_cust_tntid')[0]['dlm_cust_tntid']
        if request.method=='POST':
            cname = request.POST.get("cname")
            uname = request.POST.get("uname")

            cid = DlmCust.objects.filter(dlm_cust_nam = cname).values('iddlm_cust')[0]['iddlm_cust']
            print(cid)
            
            grpid = DlmGroup.objects.filter(dlm_group_custid = cid).values('iddlm_group')[0]['iddlm_group']
            print(grpid)
            
            length = int(request.GET.get('length', 8))
            chars = string.ascii_letters + string.digits
            password = ''.join(random.choices(chars, k=length))
            print(password)
            
            if DlmCustuser.objects.filter(dlm_custuser_code=uname).exists():
                messages.error(request, 'Username is already taken')
            else:
                cus = DlmCustuser.objects.create(dlm_custuser_code=uname, dlm_custuser_custid = cid , dlm_custuser_grpid = grpid , dlm_custuser_type= 'Standard User' , dlm_custuser_pwd = make_password(password))
            
            
                subject = 'Password Creation'
                message = f"Dear {uname},\n\nYour account has been created with the following credentials:\n\nUsername: {uname}\nPassword: {password}\n\nPlease use the following link to log in to your account:\n\nhttp://23.22.186.68:8021/login/\n\nBest regards,\nYour Website Team"
                from_email = 'support@daefodil.com'
                recipient_list = [uname]
                send_mail(subject, message,from_email, recipient_list)

                
                
                return redirect('usertable')
        return render(request, 'adduser.html',{'username':username,'usertype':usertype,'client':client,'tntid':tntid,'user_mapped':user_mapped})
    else:
        return redirect("/login")
    

def addclient(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        client= DlmCust.objects.all()
        if request.method=='POST':
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            uname = request.POST.get("uname")
            
            username= request.session['username']
            tntid = DlmCust.objects.filter(dlm_cust_email=username).values('dlm_cust_tntid')[0]['dlm_cust_tntid']
            print(tntid)

            if DlmCust.objects.filter(dlm_cust_email=uname).exists():
                messages.error(request, 'Username is already taken')
            else:
                cus = DlmCust.objects.create( dlm_cust_tntid = tntid ,dlm_cust_nam =name,dlm_cust_email=uname,dlm_cust_mobnum=phone)
                return redirect('clienttable')
        
    
        return render(request,'addclient.html',{'username':username,'usertype':usertype,'user_mapped':user_mapped})
    else:
        return redirect("/login")

#app-admin work details editing######

def edituser(request,iddlm_custuser):
    if 'username' in request.session:
        username=request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        user = DlmCustuser.objects.get(iddlm_custuser=iddlm_custuser )
        client= DlmCust.objects.all() 
        tntid = DlmCust.objects.filter(dlm_cust_email=username).values('dlm_cust_tntid')[0]['dlm_cust_tntid']
        if request.method == 'POST':
            cname = request.POST["cname"]
            uname = request.POST["uname"]

            print(cname)
            cid = DlmCust.objects.filter(dlm_cust_nam = cname).values('iddlm_cust')[0]['iddlm_cust']
            print(cid)
            # clienid = DlmCustuser.objects.filter(dlm_cust_nam = cname).values('iddlm_cust')[0]['iddlm_cust']
            grpid = DlmGroup.objects.filter(dlm_group_custid = cid).values('iddlm_group')[0]['iddlm_group']
            print(grpid)

            # if DlmCustuser.objects.filter(dlm_custuser_code=uname).exists():
            #     messages.error(request, 'Username is already taken')
            # else:
            user.dlm_custuser_custid= cid
            user.dlm_custuser_grpid= grpid
            user.dlm_custuser_code=uname
            user.save()
            return redirect('usertable')
        return render(request,'edituser.html', {'username':username,'usertype':usertype,'user':user,'client':client ,'tntid':tntid,'user_mapped':user_mapped})
    else:
        return redirect("/login")

def editclient(request,iddlm_cust):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        client = DlmCust.objects.get(iddlm_cust=iddlm_cust ) 
        
        if request.method == 'POST':
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            uname = request.POST.get("uname")
            
            

            
            tntid = DlmCust.objects.filter(dlm_cust_email=username).values('dlm_cust_tntid')[0]['dlm_cust_tntid']
            print(tntid)

            if DlmCust.objects.filter(dlm_cust_email=uname).exists():
                messages.error(request, 'Username is already taken')
            else:
                client.dlm_cust_tntid = tntid
                client.dlm_cust_nam = name
                client.dlm_cust_mobnum= phone
                client.dlm_cust_email=uname
                client.save()
                return redirect('clienttable')
        return render(request,'editclient.html', {'username':username,'usertype':usertype,'client':client,'user_mapped':user_mapped})
    else:
        return redirect("/login")

#app-admin client/user activate
def activateclient(request,iddlm_cust ): 
    if 'username' in request.session: 
        client = DlmCust.objects.get(iddlm_cust =iddlm_cust )
        client.dlm_cust_status = 'active'
        client.save()  
        return redirect("clienttable") 
    else:
        return redirect("/login")
    
def activateuser(request,iddlm_custuser ):  
    if 'username' in request.session:
        user = DlmCustuser.objects.get(iddlm_custuser =iddlm_custuser ) 
        user.dlm_custuser_status = 'active' 
        user.save()
        print('success')
        return redirect("usertable") 
    else:
        return redirect("/login") 
    
# app-admin work details delete/destroy#####

def disableuser(request,iddlm_custuser ):  
    if 'username' in request.session:
        user = DlmCustuser.objects.get(iddlm_custuser =iddlm_custuser ) 
        user.dlm_custuser_status = 'inactive' 
        user.save()
        print('success')
        return redirect("usertable") 
    else:
        return redirect("/login")
    


    
def disableclient(request,iddlm_cust ): 
    if 'username' in request.session: 
        client = DlmCust.objects.get(iddlm_cust =iddlm_cust )
        client.dlm_cust_status = 'inactive'
        client.save()  
        return redirect("clienttable") 
    else:
        return redirect("/login")
#app-admin work/personal common things######

def resetpassword(request):
    if 'username' in request.session: 
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        if request.method == 'POST':
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
        
            username = request.session['username']
            print(username)
            encryptedpassword = DlmCustuser.objects.filter(dlm_custuser_code=username).values('dlm_custuser_pwd')[0]['dlm_custuser_pwd']
            
            if check_password(old_password, encryptedpassword):
                if new_password == confirm_password:
                    user = DlmCustuser.objects.get(dlm_custuser_code=username)
                    user.dlm_custuser_pwd = make_password(new_password)
                    user.save()
                    messages.success(request, 'Your password was successfully updated!')
                    
                else:
                    messages.error(request, 'New password and confirm password  not matching.')
            else:
                messages.error(request, 'Old password is incorrect.')
        return render(request,'Newpassword.html',{'username':username,'usertype':usertype,'user_mapped':user_mapped})
    else:
        return redirect("/login")

def deleteaccount(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        return render(request,'deleteaccount.html',{'username':username,'usertype':usertype,'user_mapped':user_mapped})
    else:
        return redirect("/login")








#OTP CALLING FUNCTIONS#########

global resend # declaring the resend as a global function
def resend():#creating resend function
    mail=usnam()
    idn=idun()
    if DlmCust.objects.filter(dlm_cust_email = mail ).exists():
            a=random.randint(1,9)
            b=random.randint(1,9)
            c=random.randint(1,9)
            d=random.randint(1,9)
            g=random.randint(1,9)
            h=random.randint(1,9)
            e=random.randint(10,99)
            f=random.randint(10,99)
            a=str(a)
            b=str(b)
            c=str(c)
            d=str(d)
            g=str(g)
            h=str(h)
            e=str(e)
            f=str(f)
            
            otp_code="".join([a,b,c,d,g,h])
            
            

            create_date=datetime.datetime.now()
            create_date=create_date.strftime("%Y-%m-%d %H:%M")
            global cdt
            def cdt():
                return create_date
            print("inside resend")
           
            expiry_date=datetime.datetime.now()+datetime.timedelta(minutes=1)
            expiry_date=expiry_date.strftime("%Y-%m-%d %H:%M")
            global exdt
            def exdt():
                return expiry_date
            


           
           
            
            subject='OTP OF THE DAEFODIL-APP'
            message=" ".join([a,b,c,d,g,h])
            email_from=settings.EMAIL_HOST_USER
            print(email_from)
            recipient_list=[mail]
            print(recipient_list)
           
            send_mail( subject, message, email_from, recipient_list )



            e=dlt_passreset.objects.create(dlt_passreset_usrid=idn, dlt_passreset_otpcode=otp_code, dlt_passreset_expdate=expiry_date, dlt_passreset_cdate=create_date)
            e.save()





global sendotp
def sendotp():
            mail=val()
            idus=DlmCustuser.objects.filter(dlm_custuser_code=mail).values('iddlm_custuser')[0]['iddlm_custuser']
          
            #id1=str(idn)
            #c=len(id1)
            #d=[]
            #for i in range(c):
             #   if id1[i].isnumeric():
                    # d.append(id1[i])
            #c=[str(i) for i in d]
            #idus=''.join(c)


            global idusn
            def idusn():
                return idus
            value=valuesend()
   
            a=random.randint(1,9)
            b=random.randint(1,9)
            c=random.randint(1,9)
            d=random.randint(1,9)
            g=random.randint(1,9)
            h=random.randint(1,9)
            e=random.randint(10,99)
            f=random.randint(10,99)
            a=str(a)
            b=str(b)
            c=str(c)
            d=str(d)
            g=str(g)
            h=str(h)
            e=str(e)
            f=str(f)
            
            otp_code="".join([a,b,c,d,g,h])
           
            

            create_date=datetime.datetime.now()
            create_date=create_date.strftime("%Y-%m-%d %H:%M")
            global cdat
            def cdat():
                return create_date
           
            expiry_date=datetime.datetime.now()+datetime.timedelta(hours=24)
            expiry_date=expiry_date.strftime("%Y-%m-%d %H:%M")
            global exdat
            def exdat():
                return expiry_date
            


          
           
           
            
            subject='OTP OF THE DAEFODIL-APP'
            message="".join([a,b,c,d,g,h])
            global retmessage
            def retmessage():
                return message
            email_from=settings.EMAIL_HOST_USER
            print(email_from)
            recipient_list=[mail]
            print(recipient_list)
            
            if dlt_passreset.objects.filter(dlt_passreset_usrid=idus).exists():
                if value==1:
                    send_mail(subject,message,email_from,recipient_list)



                    e=dlt_passreset.objects.create(dlt_passreset_usrid=idus, dlt_passreset_otpcode=otp_code, dlt_passreset_expdate=expiry_date, dlt_passreset_cdate=create_date)
                    e.save()
                else:
                    print(idus)
                
            else:

                send_mail(subject,message,email_from,recipient_list)



                save=dlt_passreset.objects.create(dlt_passreset_usrid=idus, dlt_passreset_otpcode=otp_code, dlt_passreset_expdate=expiry_date, dlt_passreset_cdate=create_date)
                save.save()
                

    
def documentstable(request):
    if 'username' in request.session:
        username= request.session['username']
        usertype=request.session['usertype']
        user_mapped=request.session['usermapped']
        documents=DltDocproc.objects.all()
        custuser=DlmCustuser.objects.all()
        
        return render(request,'documents.html',{'custuser':custuser,'documents':documents,'username':username,'usertype':usertype,'user_mapped':user_mapped })
    else:
        return redirect("/login")
                



