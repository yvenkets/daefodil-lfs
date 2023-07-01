from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    
    #signup
    path('work',views.work,name='work'),
    path('personal',views.personal,name='personal'),
    
    #terms and privacy policy
    path('terms',views.terms,name='terms'),
    path('privacypol',views.privacypol,name='privacypol'),
    
    #email-to verify
    path('email',views.email,name='email'),
    path('loader',views.loader,name='loader'),
    
    #login/logout
    path('login',views.login,name='login'),
    path('logout', views.logout, name="logout"),
    
    #forgotpassword-pages
    path('verification',views.verification,name='verification'),
    path('forgotpassword',views.forgotpassword, name='forgotpassword'),
    path('forgotpasswordtwo',views.forgotpasswordtwo, name='forgotpasswordtwo'),
    path('setnewpassword',views.setnewpassword, name='setnewpassword'),
    path('successpage',views.successpage, name='successpage'),
    
    # dashboard pages
    path('userdashboard',views.userdashboard,name='userdashboard'),
    path('userdetails',views.userdetails,name='userdetails'),
    path('newuser',views.newuser,name='newuser'),
    path('documentstable',views.documentstable,name='documentstable'),
    
    #document-mapping
    path('uploadpage',views.uploadpage,name='uploadpage'),
    path('docmapping',views.docmapping,name="docmapping"),
    path('process',views.process,name='process'),
    path('download_table/', views.download_table_view, name='download_table'),
    path('delete_data',views.delete_data,name='delete_data'),
    path('save',views.save,name='save'),
    path('preview/',views.preview,name='preview'),
    
    #subscription and pricing
    path('subscribe',views.subscribe,name='subscribe'), 
    
    #super-admin -table
    path('categorytable',views.categorytable,name='categorytable'),
    path('plantable',views.plantable,name='plantable'),
    path('pricetable',views.pricetable,name='pricetable'),
    path('featuretable',views.featuretable,name='featuretable'),
    path('tenanttable',views.tenanttable,name='tenanttable'),
    path('clientsTable',views.clientsTable,name='clientsTable'),
     
    #super-admin -add
    path('addcategory',views.addcategory,name='addcategory'),
    path('addplan',views.addplan,name='addplan'),
    path('addprice',views.addprice,name='addprice'),
    path('addfeature',views.addfeature,name='addfeature'),
    
    #super-admin -edit
    path('editcategory/<int:iddlm_doctype>',views.editcategory, name="editcategory"), 
    path('editplan/<int:iddlm_plan>', views.editplan,name="editplan"),
    path('editprice/<int:iddlm_price>', views.editprice,name="editprice"),
    path('editfeature/<int:iddlm_feature>', views.editfeature,name="editfeature"),
    
    #super-admin -activate
    path('ActiveClient/<int:iddlm_cust>', views.ActiveClient,name="ActiveClient"),
    path('Activatetenant/<int:iddlm_tenant>', views.Activatetenant,name="Activatetenant"),
    
    #super-admin -delete
    path('deletecategory/<int:iddlm_doctype>',views.deletecategory, name="deletecategory"),
    path('deleteplan/<int:iddlm_plan>', views.deleteplan,name="deleteplan"),
    path('deleteprice/<int:iddlm_price>', views.deleteprice,name="deleteprice"),
    path('deletefeature/<int:iddlm_feature>', views.deletefeature,name="deletefeature"),
    path('deleteClient/<int:iddlm_cust>', views.deleteClient,name="deleteClientt"),
    path('disabletenant/<int:iddlm_tenant>', views.disabletenant,name="disabletenant"),
    
    #app-admin work -table
    path('usertable',views.usertable,name='usertable'),
    path('clienttable',views.clienttable,name='clienttable'),
    
    #app-admin work -add
    path('adduser',views.adduser,name='adduser'),
    path('addclient',views.addclient,name='addclient'),
    
    #app-admin work -edit
    path('edituser/<int:iddlm_custuser>', views.edituser),
    path('editclient/<int:iddlm_cust>', views.editclient),
    
    #app-admin work-activate client/user
    path('activateclient/<int:iddlm_cust>', views.activateclient,name="activateclient"),
    path('activateuser/<int:iddlm_custuser>', views.activateuser,name="activateuser"),  
    
    #app-admin work -destroy
    path('disableuser/<int:iddlm_custuser>', views.disableuser,name="dibsaleuser"), 
    path('disableclient/<int:iddlm_cust>', views.disableclient,name="disableclient"),
    
    #app-admin work/personal
    path('newpassword',views.resetpassword,name='newpassword'),
    path('deleteaccount',views.deleteaccount,name="deleteaccount"),
    
    
    
]