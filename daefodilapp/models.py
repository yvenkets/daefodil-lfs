from django.db import models

# Create your models here.
#from django.db import models

class DlmTenant(models.Model):
    iddlm_tenant = models.AutoField(db_column='idDLM_TENANT', primary_key=True)  # Field name made lowercase.
    dlm_tenant_nam = models.CharField(db_column='DLM_TENANT_NAM', max_length=50)  # Field name made lowercase.
    dlm_tenant_secky = models.CharField(db_column='DLM_TENANT_SECKY', max_length=5)  # Field name made lowercase.
    dlm_tenant_sts = models.CharField(db_column='DLM_TENANT_STS', max_length=250)  # Field name made lowercase.
    dlm_tenant_cdate = models.DateTimeField(db_column='DLM_TENANT_CDATE', blank=True, null=True)  # Field name made lowercase.
    dlm_tenant_cat = models.CharField(db_column='DLM_TENANT_CAT', max_length=45)  # Field name made lowercase.

    def __str__(self):
        return self.iddlm_tenant

    class Meta:
        managed = False
        db_table = 'dlm_tenant'

class DlmCust(models.Model):
    STATUS_CHOICES = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )
    iddlm_cust = models.AutoField(db_column='idDLM_CUST', primary_key=True)  # Field name made lowercase.
    dlm_cust_tntid = models.CharField( db_column='DLM_CUST_TNTID',max_length=50)  # Field name made lowercase.
    dlm_cust_nam = models.CharField(db_column='DLM_CUST_NAM', max_length=50)  # Field name made lowercase.
    dlm_cust_mobnum = models.IntegerField(db_column='DLM_CUST_MOBNUM', unique=True)  # Field name made lowercase.
    dlm_cust_email = models.EmailField(db_column='DLM_CUST_EMAIL', unique=True, max_length=50)  # Field name made lowercase.
    dlm_cust_diml = models.CharField(db_column='DLM_CUST_DIML', max_length=50)  # Field name made lowercase.
    dlm_cust_cdate = models.DateTimeField(db_column='DLM_CUST_CDATE', blank=True, null=True)  # Field name made lowercase.
    dlm_cust_status = models.CharField(max_length=8, choices= STATUS_CHOICES, default='active',db_column='DLM_CUST_STATUS')

    def __str__(self):
        return self.iddlm_cust

    class Meta:
        managed = False
        db_table = 'dlm_cust'
        
class DlmCustuser(models.Model):
    STATUS_CHOICES = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )
    iddlm_custuser = models.AutoField(db_column='idDLM_CUSTUSER', primary_key=True)  # Field name made lowercase.
    dlm_custuser_grpid = models.CharField(db_column='DLM_CUSTUSER_GRPID',max_length=250)  # Field name made lowercase.
    dlm_custuser_custid = models.CharField( db_column='DLM_CUSTUSER_CUSTID',max_length=250)  # Field name made lowercase.
    dlm_custuser_code = models.CharField(db_column='DLM_CUSTUSER_CODE', max_length=250)  # Field name made lowercase.
    dlm_custuser_pwd = models.CharField(db_column='DLM_CUSTUSER_PWD', max_length=50)  # Field name made lowercase.
    dlm_custuser_type = models.CharField(db_column='DLM_CUSTUSER_TYPE', max_length=45)  # Field name made lowercase.
    dlm_custuser_date = models.DateTimeField(db_column='DLM_CUSTUSER_DATE', blank=True, null=True)  # Field name made lowercase.
    dlm_custuser_status = models.CharField(max_length=8, choices= STATUS_CHOICES, default='active',db_column='DLM_CUSTUSER_STATUS')
    dlm_custuser_verify=models.IntegerField(db_column='DLM_CUSTUSER_VERIFY')
    def __str__(self):
        return self.iddlm_custuser 

    class Meta:
        managed = False
        db_table = 'dlm_custuser'
        
class DlmGroup(models.Model):
    iddlm_group = models.AutoField(db_column='idDLM_GROUP', primary_key=True)  # Field name made lowercase.
    dlm_group_custid = models.CharField(db_column='DLM_GROUP_CUSTID',max_length=250)  # Field name made lowercase.
    dlm_group_code = models.CharField(db_column='DLM_GROUP_CODE', max_length=250)  # Field name made lowercase.
    dlm_group_des = models.CharField(db_column='DLM_GROUP_DES', max_length=100)  # Field name made lowercase.
    dlm_group_activity = models.TextField(db_column='DLM_GROUP_ACTIVITY', blank=True, null=True)  # Field name made lowercase.
    dlm_group_cdate = models.DateTimeField(db_column='DLM_GROUP_CDATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dlm_group'

class dlt_passreset(models.Model):
    iddlt_passreset=models.AutoField(db_column='idDLT_PASSRESET',primary_key=True)
    dlt_passreset_usrid=models.IntegerField(db_column='DLT_PASSRESET_USRID',default='')
    dlt_passreset_otpcode=models.CharField(db_column='DLT_PASSRESET_OTPCODE',max_length=45)
    dlt_passreset_expdate=models.DateTimeField()
    dlt_passreset_cdate=models.DateTimeField()
    
    class Meta:
        managed=False
        db_table="dlt_passreset"
        
class dlm_plan(models.Model):
    iddlm_plan = models.AutoField(db_column='idDLM_PLAN', primary_key=True)  # Field name made lowercase.
    dlm_plan_catgrp = models.CharField( db_column='DLM_PLAN_CATGRP',max_length=50)  # Field name made lowercase.
    dlm_plan_nam = models.CharField(db_column='DLM_PLAN_NAM', max_length=50)  # Field name made lowercase.
    dlm_plan_trncnt = models.CharField(db_column='DLM_PLAN_TRNCNT',max_length=50)  # Field name made lowercase.
    dlm_plan_usrcnt = models.IntegerField(db_column='DLM_PLAN_USRCNT')  # Field name made lowercase.
    dlm_plan_filesize = models.CharField(db_column='DLM_PLAN_FILESIZE', max_length=50)  # Field name made lowercase.
    dlm_plan_catsize = models.CharField(db_column='DLM_PLAN_CATSIZE',max_length=50)  # Field name made lowercase.
    dlm_plan_cdate=models.DateTimeField(db_column='DLM_PLAN_CDATE')
    dlm_plan_cby=models.CharField(db_column='DLM_PLAN_CBY' ,default='superadmin',max_length=50)
    dlm_plan_status=models.CharField(db_column='DLM_PLAN_STATUS',default='active',max_length=50)
    dlm_plan_usrtype=models.CharField(db_column='DLM_PLAN_USRTYPE', max_length=45, blank=True, null=True)
    dlm_plan_featureid = models.CharField(db_column='DLM_PLAN_FEATURE', max_length=50) 
    
    class Meta:
        managed = False
        db_table = 'dlm_plan'

class dlm_price(models.Model):
    iddlm_price=models.AutoField(db_column='idDLM_PRICE',primary_key=True)
    dlm_price_planid=models.IntegerField(db_column='DLM_PRICE_PLANID')
    dlm_price_valtype=models.CharField(db_column='DLM_PRICE_VALTYPE',max_length=50)
    dlm_price_amt=models.IntegerField(db_column='DLM_PRICE_AMT')
    dlm_price_cdate=models.DateTimeField(db_column='DLM_PRICE_CDATE')
    dlm_price_cby=models.CharField(db_column='DLM_PRICE_CBY' ,default='superadmin',max_length=50)
    
    class Meta:
        managed = False
        db_table = 'dlm_price'


class dlm_doctype(models.Model):
    iddlm_doctype = models.AutoField(db_column='idDLM_DOCTYPE', primary_key=True)  # Field name made lowercase.
    dlm_doctype_nam = models.CharField(db_column='DLM_DOCTYPE_NAM', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dlm_doctype_catgrp = models.CharField(db_column='DLM_DOCTYPE_CATGRP', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dlm_doctype_cdate = models.DateTimeField(db_column='DLM_DOCTYPE_CDATE', blank=True, null=True)  # Field name made lowercase.
    dlm_doctype_cby = models.CharField(db_column='DLM_DOCTYPE_CBY', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dlm_doctype'
        
class View2(models.Model):
    dlm_pricingpage_id =models.AutoField(db_column='idDLM_PRICE', primary_key=True)
    iddlm_plan = models.IntegerField(db_column='idDLM_PLAN')
    dlm_plan_nam = models.CharField(db_column='DLM_PLAN_NAM', max_length=45, blank=True, null=True)
    dlm_price_amt = models.CharField(db_column='DLM_PRICE_AMT', max_length=45)
    dlm_price_valtype = models.CharField(db_column='DLM_PRICE_VALTYPE', max_length=5)
    dlm_plan_usrtype = models.CharField(db_column='DLM_PLAN_USRTYPE', max_length=5)
    dlm_plan_feature = models.CharField(db_column='DLM_PLAN_FEATURE', max_length=5)
    
    class Meta:
        managed = False
        db_table = 'view2'

class DlmFeature(models.Model):
    iddlm_feature =models.AutoField(db_column='idDLM_FEATURE', primary_key=True)
    dlm_feature_name = models.CharField(db_column='DLM_FEATURE_NAME', max_length=45, blank=True, null=True)
    dlm_feature_desc = models.CharField(db_column='DLM_FEATURE_DESC', max_length=45)
    dlm_feature_cdate = models.DateTimeField(db_column='DLM_FEATURE_CDATE',blank=True, null=True )
    dlm_feature_cby = models.CharField(db_column='DLM_FEATURE_CBY', max_length=45)
    class Meta:
        managed = False
        db_table = 'dlm_feature'

class dlt_melements(models.Model):
    iddlt_melements =models.AutoField(db_column='idDLT_MELEMENTS', primary_key=True)
    dlt_melements_tid=models.IntegerField(db_column='DLT_MELEMENTS_TID')
    dlt_melements_cid=models.IntegerField(db_column='DLT_MELEMENTS_CID')
    dlt_melements_dtype=models.CharField(db_column='DLT_MELEMENTS_DTYPE',max_length=100)
    dlt_melements_1=models.CharField(db_column='DLT_MELEMENTS_1',max_length=200)
    dlt_melements_2=models.CharField(db_column='DLT_MELEMENTS_2',max_length=200)
    dlt_melements_3=models.CharField(db_column='DLT_MELEMENTS_3',max_length=200)
    dlt_melements_4=models.CharField(db_column='DLT_MELEMENTS_4',max_length=200)
    dlt_melements_5=models.CharField(db_column='DLT_MELEMENTS_5',max_length=200)
    dlt_melements_6=models.CharField(db_column='DLT_MELEMENTS_6',max_length=200)
    dlt_melements_7=models.CharField(db_column='DLT_MELEMENTS_7',max_length=200)
    dlt_melements_8=models.CharField(db_column='DLT_MELEMENTS_8',max_length=200)
    dlt_melements_9=models.CharField(db_column='DLT_MELEMENTS_9',max_length=200)
    dlt_melements_10=models.CharField(db_column='DLT_MELEMENTS_10',max_length=200)
    dlt_melements_11=models.CharField(db_column='DLT_MELEMENTS_11',max_length=200)
    dlt_melements_12=models.CharField(db_column='DLT_MELEMENTS_12',max_length=200)
    dlt_melements_13=models.CharField(db_column='DLT_MELEMENTS_13',max_length=200)
    dlt_melements_14=models.CharField(db_column='DLT_MELEMENTS_14',max_length=200)
    dlt_melements_15=models.CharField(db_column='DLT_MELEMENTS_15',max_length=200)
    dlt_melements_uid=models.CharField(db_column='DLT_MELEMENTS_UID',max_length=200)
    dlt_melements_cdate=models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'dlt_melements'

class DltDocproc(models.Model):
    iddlt_docproc = models.AutoField(db_column='idDLT_DOCPROC', primary_key=True)  # Field name made lowercase.
    dlt_docproc_userid = models.IntegerField(db_column='DLT_DOCPROC_USERID')  # Field name made lowercase.
    dlt_docproc_filesize = models.CharField(db_column='DLT_DOCPROC_FILESIZE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    dlt_docproc_filetype = models.CharField(db_column='DLT_DOCPROC_FILETYPE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    dlt_docproc_filename = models.CharField(db_column='DLT_DOCPROC_FILENAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dlt_docproc_cdate = models.DateTimeField(db_column='DLT_DOCPROC_CDATE', blank=True, null=True)  # Field name made lowercase.
    dlt_docproc_sts = models.CharField(db_column='DLT_DOCPROC_STS', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dlt_docproc_accrcy = models.CharField(db_column='DLT_DOCPROC_ACCRCY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dlt_docproc_dataid = models.IntegerField(db_column='DLT_DOCPROC_DATAID', blank=True, null=True)  # Field name made lowercase.
    dlt_docproc_dwldsts=models.CharField(db_column='DLT_DOCPROC_DWLDSTS',blank=True,null=True,max_length=45)
    dlt_docproc_elemid = models.IntegerField(db_column='DLT_DOCPROC_ELEMID', blank=True, null=True)  # Field name made lowercase.
    dlt_docproc_pagcount = models.IntegerField(db_column='DLT_DOCPROC_PAGCOUNT', blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'dlt_docproc'

class dlm_docmap(models.Model):
    iddlm_docmap=models.AutoField(db_column='idDLM_DOCMAP', primary_key=True)
    dlm_docmap_clientid=models.IntegerField(db_column='DLM_DOCMAP_CLIENTID')
    dlm_docmap_dtype=models.CharField(db_column='DLM_DOCMAP_DTYPE',max_length=100)
    dlm_docmap_element=models.CharField(db_column='DLM_DOCMAP_ELEMENT',max_length=600)
    dlm_docmap_cname=models.CharField(db_column='DLM_DOCMAP_CNAME',max_length=100)
    dlm_docmap_uid=models.IntegerField(db_column='DLM_DOCMAP_UID')
   # dlm_docmap_cdate=models.DateTimeField(db_column='DLM_DOCMAP_CDATE')
    
    class Meta:
        managed = False
        db_table = 'dlm_docmap'
