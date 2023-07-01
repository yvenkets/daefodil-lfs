from django.shortcuts import render
from pathlib import Path
# Create your views here.
from rest_framework.views import APIView
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import decorators
from rest_framework.decorators import  api_view
# import local data
from .serializers import dlmcust
from daefodilapp.models import *
# from pdf_extractor.extractor import extractCompanyDet
# import pytesseract
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter,  ImageDraw, ImageFont
# import pytesseract
import re
import json
import torch
from pathlib import Path
import os
from datetime import datetime
from rest_framework import status
#import extractor
from pytesseract import pytesseract
import filetype
from typing import List
import aiofiles, shutil
from pdf2image import convert_from_path
import numpy as np
from dateutil import parser

import PyPDF2
import camelot

from img2table.document import PDF
from img2table.ocr import TesseractOCR
from paddleocr import PaddleOCR, draw_ocr
import tensorflow as tf
import pandas as pd

import nltk
#from pdfminer.high_level import extract_text
nltk.download('averaged_perceptron_tagger')
import datefinder
from collections import defaultdict, Counter
# # create a viewset
# class GeeksViewSet(viewsets.ModelViewSet):
#     # define queryset
#     queryset = DlmCust.objects.all()
     
#     # specify serializer to be used
#     serializer_class = dlmcust

def get_full_name(lst):
            for idx in lst:
                full_name = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", idx)
                if full_name is not None:
                    return idx
def get_email(lst):
            for idx in lst:
                mail = re.search(r'[\w\.-]+@[\w\.-]+', idx)
                if mail is not None:
                    return idx
def get_phone_number(lst):
            separator = ', '
            my_string = separator.join(lst)
            my_string=str(my_string)
                       
                        
            st=re.search(r'\d{3}-\d{4} \d{4}', my_string).group()
            return st
def get_company_name(lst):
            separator = ', '
            my_string = separator.join(lst)
            ls=str(my_string)
                        
                        #pattern = r"(\w+)\s+company"

            match = re.search(r"(\w+)\s+Company",ls)
                        #print(match)
            if match:
                word_before_company = match.group(1)+' '+'Company'

            return word_before_company
def fax_number(lst):
            separator = ', '
            my_string = separator.join(lst)
            ls=str(my_string)
            st=re.search(r'\(\d{3}\) \d{4} \d{4}', my_string).group()
            return st
def job(lst):
            separator = ', '
            my_string = separator.join(lst)
            ls=str(my_string)
                        
            pattern = r"[A-Za-z]+\s+developer"

            match = re.search(pattern,ls, re.IGNORECASE)
            
            if match:
                profession = match.group()

            
            return profession
                       
            
def address(lst):
            separator = ', '
            my_string = separator.join(lst)
            ls=str(my_string)
            st=re.search(r'\d{3}-\d{4} \d{4}', my_string).group()
            if st in ls:
                ls = ls.replace(st, "")
                
                ls=ls.replace(', ,',',')
                
                pattern = r"\d+[A-Za-z\s,.-]+\d+"

                match = re.search(pattern,ls)
                            #if match:
                address = match.group()

               
                return address
            else:
                print(ls)
     
def fileroot(c):
        c=str(c)
        file_root, file_ext = os.path.splitext(c)
        file_name = os.path.basename(file_root)
        print(file_name)
        return file_name
    
def fileext(c):
        c=str(c)
        file_root, file_ext = os.path.splitext(c)
    
        print(file_root,file_ext)
        return file_ext
  
def filesize(c):
    file_size = os.path.getsize(c)
    if file_size >= 1024 * 1024:
        size_mb = file_size / (1024 * 1024)
        return  f"{size_mb:.2f} MB"
    else:
        size_kb = file_size / 1024
        return f"{size_kb:.2f} KB"

def cdate():
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return today

#######  manju's code  ########

model = torch.hub.load('yolov7', 'custom', 'model_v7/best.pt', source='local',force_reload=True)
Bankmodel = torch.hub.load('yolov7', 'custom', 'bank_model/best-bank-v2.pt', source='local',force_reload=True)

CHUNK_SIZE = 1024
uri = ''
"------------------Extract Document Data -------------------------"
class DataExtractor():
    
    def convert_pdf(self, pdf_path, save_dir):
        #print('here4')
       
        #pages = convert_from_path(pdf_path, res, poppler_path=r'C:\Program Files\poppler-22.01.0\Library\bin')
        pages = convert_from_path(pdf_path, poppler_path=r'C:\Program Files\poppler-22.01.0\Library\bin')
        #print('here5')
        name_with_ext = pdf_path.rsplit('/')[-1]
        name = name_with_ext.rsplit('.')[0]
        
        totpage = 0
        fp_list = list()
        for idx, page in enumerate(pages):
            page.save(f'{save_dir}/{name}_{idx}.png', 'PNG')
            totpage = totpage + 1
            fp_list.append(f'{save_dir}/{name}_{idx}.png')
        return fp_list
    
    def invertImage(self,imgpath):
        
        img = cv2.imread(imgpath,0)
        #img.shape
        #thresholding the image to a binary image
        thresh,img_bin = cv2.threshold(img,128,255,cv2.THRESH_BINARY |cv2.THRESH_OTSU)
        #inverting the image - do it only if the background is completely black
        img_bin = 255-img_bin
        cv2.imwrite('data/input/tabledetails_2.jpg',img_bin)
        #Plotting the image to see the output
        #plotting = plt.imshow(img_bin,cmap='gray')
        #plt.show()
        
        image2 = Image.open('data/input/tabledetails_2.jpg')
        pdf = image2.convert('RGB')
        pdf.save('data/input/tabledetails_2.pdf')
    
    """def convertImgtoPdf(self,imgpath):
        image2 = Image.open(imgpath)
        pdf = image2.convert('RGB')
        pdf.save('data/input/converted.pdf')"""
    
    def imagePreprocessing(self,imgpath):
        print(imgpath)
        """im = cv2.imread(imgpath)
      
        im = cv2.resize(im,(640,640))
       
        gray_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('data/input/processed.png',gray_image)
        
        image2 = Image.open('data/input/processed.png')"""
        image2 = Image.open(imgpath)
        pdf = image2.convert('RGB')
        pdf.save('data/input/converted.pdf')
    
    def invertImage(self, imgpath):
        img = cv2.imread(imgpath,0)
        thresh,img_bin = cv2.threshold(img,128,255,cv2.THRESH_BINARY |cv2.THRESH_OTSU)
        img_bin = 255-img_bin
        cv2.imwrite('data/input/inverted.png',img_bin)
        
    
    def extractTableDetails(self,filepath):
        print(filepath)
        self.invertImage(filepath)
        
        ocr = PaddleOCR(lang='en')
        img_path = "data/input/inverted.png"
        image_cv = cv2.imread(img_path)
        imge_height = image_cv.shape[0]
        imge_weight = image_cv.shape[1]
        output = ocr.ocr(img_path)
        
        boxes = [line[0] for line in output[0]]
        texts = [line[1][0] for line in output[0]]
        prob = [line[1][1] for line in output[0]]
        
        image_boxes = image_cv.copy()
        
        for box,text in zip(boxes,texts):
            cv2.rectangle(image_boxes,(int(box[0][0]),int(box[0][1])),(int(box[2][0]),int(box[2][1])),(0,0,255),1)
            cv2.putText(image_boxes, text, (int(box[0][0]),int(box[0][1])), cv2.FONT_HERSHEY_SIMPLEX,1,(222,0,0),1)
        
        cv2.imwrite('data/input/detections.jpg',image_boxes)
        
        im = image_cv.copy()
        
        horiz_boxes=[]
        vert_boxes=[]
        for box in boxes:
          x_h, x_v = 0, int(box[0][0])
          y_h, y_v = int(box[0][1]), 0

          width_h, width_v = imge_weight, int(box[2][0]-box[0][0])
          height_h, height_v = int(box[2][1]-box[0][1]),imge_height

          horiz_boxes.append([x_h,y_h,x_h+width_h,y_h+height_h])
          vert_boxes.append([x_v,y_v,x_v+width_v,y_v+height_v])

          cv2.rectangle(im,(x_h,y_h),(x_h+width_h,y_h+height_h),(255,0,0),1)
          cv2.rectangle(im,(x_v,y_v),(x_v+width_v,y_v+height_v),(0,255,0),1)

        cv2.imwrite('data/input/horiz_verts.jpg',im)
        
        
        horiz_out=tf.image.non_max_suppression(
            horiz_boxes,
            prob,
            max_output_size=1000,
            iou_threshold=0.1,
            score_threshold=float('-inf'),
            name=None
        )
        
        horiz_lines = np.sort(np.array(horiz_out))
        
        im_mns = image_cv.copy()
        
        for val in horiz_lines:
            cv2.rectangle(im_mns,(int(horiz_boxes[val][0]),int(horiz_boxes[val][1])),(int(horiz_boxes[val][2]),int(horiz_boxes[val][3])),(0,0,255),1)

        cv2.imwrite('data/input/im_mns.jpg',im_mns)
        
        vert_out=tf.image.non_max_suppression(
            vert_boxes,
            prob,
            max_output_size=1000,
            iou_threshold=0.1,
            score_threshold=float('-inf'),
            name=None
        )
        
        vert_lines = np.sort(np.array(vert_out))
        
        for val in vert_lines:
            cv2.rectangle(im_mns,(int(vert_boxes[val][0]),int(vert_boxes[val][1])),(int(vert_boxes[val][2]),int(vert_boxes[val][3])),(222,0,0),1)

        cv2.imwrite('data/input/im_mns.jpg',im_mns)
        
        out_array = [["" for i in range(len(vert_lines))] for j in range(len(horiz_lines))]
        
        unordered_boxes = []
        for i in vert_lines:
            #print(vert_boxes[i])
            unordered_boxes.append(vert_boxes[i][0])
            
        ordered_boxes = np.argsort(unordered_boxes)
        
        for i in range(len(horiz_lines)):
            for j in range(len(vert_lines)):
                resultant = self.intersection(horiz_boxes[horiz_lines[i]], vert_boxes[vert_lines[ordered_boxes[j]]])
                #print(resultant)

                for b in range(len(boxes)):
                  the_box = [boxes[b][0][0],boxes[b][0][1],boxes[b][2][0],boxes[b][2][1]]
                  if(self.iou(resultant,the_box)>0.1):
                    out_array[i][j] = texts[b]

        
        #for out in out_array:
            #print(out)
            
        print(pd.DataFrame(out_array))
        return pd.DataFrame(out_array)
    
    
    def intersection(self,box_1,box_2):
        return [box_2[0], box_1[1], box_2[2], box_1[3]]
    
    def iou(self,box_1,box_2):
        x_1 = max(box_1[0],box_2[0])
        y_1 = max(box_1[1],box_2[1])
        x_2 = min(box_1[2],box_2[2])
        y_2 = min(box_1[3],box_2[3])

        inter = abs(max((x_2 - x_1), 0)*max((y_2 - y_1),0))
        if inter == 0:
            return 0

        box_1_area = abs((box_1[2] - box_1[0]) * (box_1[3] - box_1[1]))
        box_2_area = abs((box_2[2] - box_2[0]) * (box_2[3] - box_2[1]))

        return inter / float(box_1_area + box_2_area - inter)
        
    def getFileFormat(self,filepath):
        ocr = PaddleOCR(lang='en')
        output = ocr.ocr(str(filepath))
        text = [line[1][0].lower() for line in output[0]]
        texts = ' '.join(text)
        #print(texts)
        words = ['account statement','account summary']
        for word in words:
            if word in texts:
                ft = 'bank'
                break
            else:
                ft = 'invoice'
        """for sentence in texts:
            if any(word in sentence.split() for word in words):
                ft = 'bank'
                break
            else:
                ft = 'invoice'"""
        
        return ft
    
    def extractCompanyDet(self,result):
        parsed_vals={}
        #match = re.search(r'([a-z &]+)\n', result,re.IGNORECASE).split().strip()
        #match = re.search(r'([A-Z|a-z &]+)(\n\n|/|)(.+)\n\n', result, re.DOTALL)
        match = re.search(r'([A-Z &.]+)[\n|] ?(.+?)(?:\n\n|$)', result, re.DOTALL)

        if match:
            company_name = match.group(1)
            address = match.group(2).replace('\n', ', ')          
            parsed_vals["Company name"] =company_name
            parsed_vals["Company Address"] =address
            #print(f'Company: {company_name}\nAddress: {address}')
        return parsed_vals            
        
    def extractAddress(self,result):
        result = result.replace('\n',' ')
        parsed_vals={}
        match = re.search(r'(?P<key>Bill To|ship to|to|sold to)(:|-|\s)(?P<value>.*)', result, re.IGNORECASE)
        #print(match)
        if match:
            key = match.group('key')
            value = match.group('value').strip()
            parsed_vals[key] = value
            #print(f"{key}: {value}")
        else:
            match = re.search(r'(?P<key>Bill From|From)(:|-|\s)(?P<value>.*)', result, re.IGNORECASE)
            print(match)
            if match:
                key = match.group('key')
                value = match.group('value').strip()
                parsed_vals[key] = value
                #print(f"{key}: {value}")                 
            else:
                result = result.replace('\n\n',' ').replace('\n','')                  
                parsed_vals["ship to"] =str(result)
        return parsed_vals
    
    def extractinvoicebasic(self,result):
        vals=[]
               
        result = result.replace('\n\n','\n')
        j = result.split('\n')
        vals.append(j)
        parsed_vals={}
        for i in range(len(vals)):
            for k in range(len(vals[i])):
                j = vals[i][k]
                if j!='':
                    invoiceno_val_check = re.match('^(?=.*\d)[0-9A-Za-z]+$',j.split(':')[-1].split('.')[-1].split('#')[-1].strip())
                    invoiceno_key_check = re.match('(^IN)|.voice.',j)
                    try:
                        #print(j)
                        invoicedate_val_check = parser.parse(j.split(':')[-1].split('.')[-1].strip(),fuzzy=True)
                        invoicedate_key_check = re.match('(^date)|(^invoice.*date)',j,re.IGNORECASE)
                    except:
                        invoicedate_val_check = False
                        pass
                    try:
                        duedate_val_check = parser.parse(j.split(':')[-1].split('.')[-1].strip(),fuzzy=True)
                        duedate_key_check = re.match('^due.*date',j,re.IGNORECASE)
                    except:
                        duedate_val_check = False
                        pass  

                    if invoiceno_val_check:
                        #parsed_vals.append('invoice no: '+str(invoiceno_val_check.group()))
                        parsed_vals['invoice no']=str(invoiceno_val_check.group())                       

                    if invoicedate_val_check and not duedate_key_check:
                        if invoicedate_key_check:
                            #parsed_vals.append('invoice date: '+str(invoicedate_val_check))
                            parsed_vals['invoice date']=str(invoicedate_val_check) 
                        else:
                            invoicedate_key_check = re.match('(^date)|(^invoice.*date)',vals[i][k-1],re.IGNORECASE)
                            if invoicedate_key_check:
                                #print(j)
                                #print(vals[i][k-1])
                                #parsed_vals.append('invoice date: '+str(invoicedate_val_check))
                                parsed_vals['invoice date']=str(invoicedate_val_check) 

                    if duedate_val_check:
                        if duedate_key_check:
                            #parsed_vals.append('due date: '+str(duedate_val_check))
                            parsed_vals['due date']=str(duedate_val_check)
                        else:
                            duedate_key_check = re.match('^due.*date',vals[i][k-1],re.IGNORECASE)
                            if duedate_key_check:
                                #parsed_vals.append('due date: '+str(duedate_val_check))
                                parsed_vals['due date']=str(duedate_val_check)
        if len(parsed_vals)==0:
            #print(vals)
            try:              
                parsed_vals['invoice no'] = vals[0][1].split()[0]
                parsed_vals['invoice date'] = ' '.join(vals[0][1].split()[1:4])
                parsed_vals['due date'] = ' '.join(vals[0][1].split()[4:])
            except:
                pass
        return parsed_vals
        
    def extractMetaDetails(self,filepath):
        #print(type(filepath))
        ocr = PaddleOCR(lang='en')
        output = ocr.ocr(str(filepath))
        
        texts = [line[1][0] for line in output[0]]
        print(texts)
        delimiter = ' \n'
        pdfString = delimiter.join(texts)
        #print(pdfString)       
        
        "Extract Bank Name"
        bankdet = {}
        bank_name_raw_match = re.search(".*((acc)|(bank\s)).*((statement\s)|(summary))",pdfString,flags=re.IGNORECASE)
        if bank_name_raw_match:
            bank_name_raw = re.split('account',bank_name_raw_match.group(0),flags=re.IGNORECASE)[0]
        else:
            bank_name_raw =''
        print('line 427')    
        print(bank_name_raw)
        print('line 429')
        if bank_name_raw=='':
            #text = extract_text(filepath)
            text_all = pdfString.replace('\t','    ').split('\n')
            for txt in text_all:
                print(txt)
                bank_name_raw_match = re.search(".*((acc)|(bank\s)).*((statement\s)|(summary))",txt,flags=re.IGNORECASE)
                if bank_name_raw_match:
                    bank_name_raw = re.split('account',bank_name_raw_match.group(0),flags=re.IGNORECASE)[0]
                    break
                else:
                    bank_name_raw =''
                    
                        
        "Cleanse bank name from punctuations"
        if bank_name_raw!='':
            punctList = "\\","/",".","-","_","(",")",",",";",":","www","com"
            bank_name_raw_cleansed=re.sub('|'.join(map(re.escape,punctList))," ",bank_name_raw)
            bank_name_raw_cleansed=re.sub("\s{2,}"," ",bank_name_raw_cleansed)
            bank_name_split = re.split('bank',bank_name_raw_cleansed,re.IGNORECASE)[0]
            bank_name_statement = ' '.join([r[0] for r in nltk.pos_tag(bank_name_split.lstrip(' ').rstrip(' ').split(' ')) if ((r[1] in ['NN','NNP','JJ'])and(len(r[0])>1) and (r[0].isalpha()))])
            if len(bank_name_statement.split(' '))>1:
                bank_name = ' '.join([r[0] for r in nltk.pos_tag((bank_name_statement.split(' ')[0].title()+' '+' '.join(bank_name_statement.split(' ')[1:]).lower().rstrip(' ').lstrip(' ')).split(' ')) if r[1] in ['NNP']])
            else:
                bank_name = bank_name_statement
        else:
            bank_name=''
            
        if bank_name=="":
           bank_name_match = re.search('(www.*com)',pdfString)
           if bank_name_match:
               bank_name=bank_name_match.group(0).split('.com')[0].split('www.')[-1]
           else:
               bank_name=''
           if bank_name=="":
               bankName='Not found'
        "Extract Period of the Bank Statement"
        #date_transact = re.search(".from.*to.*20([0-2]{1})([0-9]{1})",pdfString,re.IGNORECASE).group(0)
        #return {'bankName':bank_name,'period':date_transact.replace('\t',' ')}
        #text = extract_text(filepath)
        text_all = pdfString.replace('\t','    ').split('\n')
        for tx in text_all:
            matches = datefinder.find_dates(tx)
            cnt=0
            if matches:
                try:
                    for match in matches:
                        print(match)
                        cnt+=1
                    if cnt==2:
                        date_transact=tx
                        break
                    else:
                        date_transact=''
                except:
                    date_transact=''

        if date_transact=='':
            #pdfReader = PyPDF2.PdfFileReader(pdfPath)
            #pageObj = pdfReader.getPage(0)
            #pdfString = pageObj.extractText()
            text_all = pdfString.replace('\t','    ').split('\n')
            for tx in text_all:
                matches = datefinder.find_dates(tx)
                if matches:
                    cnt=0
                    #print(tx)
                    try:
                        for match in matches:
                            print(match)
                            cnt+=1
                        if cnt==2:
                            date_transact=tx
                            break
                        else:
                            date_transact='Not Found'
                    except:
                        date_transact='Not Found'
        bankdet['bankName'] = str(bank_name)
        bankdet['transactionPeriod'] = str(date_transact)
        return bankdet
#file: bytes = File(...)
    

#file: bytes = File(...)
class SubmitFormView(APIView):
    def post(self, request, *args, **kwargs):
        extractor=DataExtractor()
        C_id = request.query_params.get('C_id')
        T_id = request.query_params.get('T_id')
        U_id = request.query_params.get('U_id')
        print(C_id, T_id, U_id)
        file = request.FILES.get('image')
        print(file)
        # extension = os.path.splitext(file.filename)[1][1:]  #[file.filename for file in files]
        extension = os.path.splitext(file.name)[1][1:]  #[file.filename for file in files]
  
        ext = 'data/input/image.'+extension
        fp = Path((r'{}'+ext).format(uri))
        print(fp)
        
        with open(fp, 'wb') as fh:
            for chunk in file.chunks():
                fh.write(chunk)

        pdf_path = fp
        print(pdf_path)
        file_size = os.path.getsize(pdf_path)
        file_size_mb = file_size / (1024 * 1024)
        formatted_file_size = f"{file_size_mb:.2f} MB"
        print(str(formatted_file_size))
        if filetype.is_image(pdf_path):
            fp_lists = []
            fp_lists.append(pdf_path)
            
            conpdf = r'data/input/image.png'
            #from PIL import Image
            image2 = Image.open(pdf_path)
            imgtopdf = image2.convert('RGB')
            
            imgtopdf.save('data/input/converted.pdf')
        elif extension=='pdf':
            
            fp_lists = extractor.convert_pdf('C:/Users/dev6/project-daefodil/daefodil/data/input/image.pdf', 'C:/Users/dev6/project-daefodil/daefodil/data/input')
        
        else:
            print('File type is not valid!!')
            return
    
        print(fp_lists)
        # ####
        print(uri,'present')
        # path_to_tesseract = ("C:/Users/dev6project-daefodil\daefodil\ocr_model\Tesseract-OCR/tesseract.exe").format(uri)
        path_to_tesseract = (r"{}ocr_model/Tesseract-OCR/tesseract.exe").format(uri)
        pytesseract.tesseract_cmd = path_to_tesseract
        
        dicts = {}
        values=[]
        keyslist=[]
        actualvalues=[]
        metaDetails=''    
        for iteration,img_path in enumerate(fp_lists):
            # print(img_path)
            #img_path.replace('\\','/')
            

            """path = str(img_path)
            newPath = path.replace(os.sep, '/')
            print(newPath)
            
            im = cv2.imread(newPath)
            gray_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            im = cv2.resize(gray_image,(640,640))
        

            cv2.imwrite('data/input/processed.png',im)
            
            input_image = Image.open('data/input/processed.png')"""
        
            fileformat = extractor.getFileFormat(img_path)
            print(fileformat)
            
            input_image =Image.open(img_path).convert("RGB")
            if fileformat=='invoice':           
                results = model(input_image) 
            else:
                results = Bankmodel(input_image) 
            
            data = results.pandas().xyxy[0]
            #print(data)
            
            results_json =   json.loads(results.pandas().xyxy[0].to_json(orient="records"))
  
            fp = Path((r'{}data/input/image.jpeg').format(uri))
            print(fp)
            f = img_path
            image = Image.open(f)
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()
        
            
            
            #get the rows unique class name based on their confidence level.
            idx = data.groupby('class')['confidence'].idxmax()  
            df = data.loc[idx]
            print('result1')
            print(df)
            column_headers = df.columns.tolist()

            print(column_headers)
            col = df.columns
  
# Printing Number of columns
            colvalues= []
            for i in range(len(col)):
                colvalues.append(df.iloc[:, i].tolist())
            #print(collength)
            print(colvalues)
            for i in range(len(colvalues)):
                for j in range(len(colvalues[i])):
                    if isinstance(colvalues[i][j], float) and colvalues[i][j] == 0.0:
                        colvalues[i][j] = '0.000000'
                    elif isinstance(colvalues[i][j], float):
                        colvalues[i][j] = '{:.6f}'.format(colvalues[i][j])
            print(colvalues)
            for ind in df.index:
                #print(df['name'][ind], df['class'][ind])
                unqkey = df['name'][ind]+''+str(iteration)
                keyslist.append(unqkey)
                #im1 = im.crop((left, top, right, bottom))

                color = "#4892EA"
                draw.rectangle([
                    df['xmin'][ind], df['ymin'][ind], df['xmax'][ind], df['ymax'][ind]
                ], outline=color, width=5)
                
                text = df['name'][ind]
                
                text_size = font.getsize(text)
                fp = r'data/input/'+text+'.png'
                print(fp)
                fpdf = r'data/input/'+text+'.pdf'
                # set button size + 10px margins
                button_size = (text_size[0]+20, text_size[1]+20)
                button_img = Image.new('RGBA', button_size, color)
                # put text on button with 10px margins
                button_draw = ImageDraw.Draw(button_img)
                button_draw.text((10, 10), text, font=font, fill=(255,255,255,255))

                # put button on source image in position (0, 0)
                image.paste(button_img, (int(df['xmin'][ind]), int(df['ymin'][ind])))
                
                crop_rectangle = (df['xmin'][ind], df['ymin'][ind], df['xmax'][ind], df['ymax'][ind])
                #print(crop_rectangle)
                image1 = input_image.crop(crop_rectangle)
                image1 = ImageOps.invert(image1)
                # image1.show()
                image1.save(fp)
            
                #result = pytesseract.image_to_string(image1) config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'
                result = pytesseract.image_to_string(image1)
                
                print(result)
                table_vals=''
                if fileformat=='bank':
                    metaDetails = extractor.extractMetaDetails(img_path)
                    print(metaDetails)
                if text=='InvoiceDetails':
                    actualval = result
                    parsed_vals = extractor.extractinvoicebasic(result)
                    #print(vals)
                    #print(parsed_vals)
                    #values.append(parsed_vals)
                elif text=='TableDetails':
                    actualval = result
                    #image2 = Image.open(img_path)
                    #Save cropped image as pdf
                    """image2 = Image.open(fp)
                    pdf = image2.convert('RGB')
                    pdf.save(fpdf)"""
                    # table_vals = extractor.extractTableDetails(fpdf,extension)
                    table_vals = extractor.extractTableDetails(fp)
                    # table_vals = 'hi'
                    parsed_vals = table_vals
                    #print(table_vals)                     
                elif text=='ShiptoAddress':
                    actualval = result
                    #print(result)
                    parsed_vals = extractor.extractAddress(result)
                elif text=='CustomerDetails':
                    actualval = result
                    #print(result)
                    parsed_vals = extractor.extractAddress(result)
                elif text=='CompanyName':
                    actualval = result
                    parsed_vals = extractor.extractCompanyDet(result)
                elif text=='CompanyDetails':
                    actualval = result
                    parsed_vals = extractor.extractCompanyDet(result)
                else:
                    actualval = result
                    parsed_vals = result
                    
                actualvalues.append(actualval)        
                values.append(parsed_vals) 
            print('hi')
            print(values)
            dicts = dict(zip(keyslist, values))
            adicts = dict(zip(keyslist, actualvalues))
            print('dicts')
            print(dicts)
            print(adicts)
            # values = dicts.values()

            
            
            #image.show()
        # print(dicts['CompanyName0'])
        # print(next(iter(dicts['CompanyName0'])))
        # elements = dlt_melements.objects.create(dlt_melements_tid=T_id,dlt_melements_cid=C_id,dlt_melements_dtype=fileformat,dlt_melements_1=dicts['CompanyDetails0'],dlt_melements_2=dicts['CompanyName0'],dlt_melements_3=dicts['CustomerDetails0'],dlt_melements_4=dicts['InvoiceDetails0'],dlt_melements_5=dicts['ShiptoAddress0'],dlt_melements_6=dicts['TableDetails0'],dlt_melements_uid=U_id)
        #a=dicts[''] 
        datas=dicts['TableDetails0']  
        dicts.pop('TableDetails0', None)

        print(dicts)
        value_list = dicts
        datapp = []
# Iterate over the dictionaries and extract the key-value pairs
        for key, subdict in value_list.items():
            if isinstance(subdict, dict):
            
                for key, value in subdict.items():
                

                    datapp.append(f"{key}: {value}")
        #datapp = [f"{key}: {value}" for subdict in [values['CompanyName0'], values['CustomerDetails0'], values['InvoiceDetails0'], values['ShiptoAddress0']] for key, value in subdict.items()]

        
        #datapp=app[:6]
        print(datapp)
        print('tabledetails')
        
        col = datas.columns
  
# Printing Number of columns
        collength= []
        for i in range(len(col)):
            collength.append(datas.iloc[:, i].tolist())
        #print(collength)
        print(collength)
        index_values = []

        for sublist in collength:
            if sublist[0] != '':
                index_values.append(sublist[0])

        print(index_values)
        target_list = collength[0]
#print(target_list)
        target_sublist = next((sublist for sublist in collength if sublist[0].startswith('DESCRIPTION') or any('DESCRIPTION' in item for item in sublist) or any('Description' in item for item in sublist) or any('description' in item for item in sublist) ), None)
        a=target_list[1:]
#print(a)
        b=target_sublist[1:]
        print(b)
        result = []

        for item in collength:
            key = item[0].replace('#', '#')
            if key != '':
                key = 'td!' + key
                values = [value.strip() for value in item[1:] if value != '']
                result.append({key: values})
        new_list=''
        if a[0] != '' and b[0] != '':
            new_list+=b[0]
        else:
            a.pop(0)
            b.pop(0)
            print('none')
        for i in range(len(b)):
            
                if a[i] != '' and b[i] != '':
                    new_list += ","+ b[i]
                elif a[i] == '' and b[i] != '':
                    if new_list is None:
                        pass
                    else:
                        new_list += ' '+ b[i]
                
        # Condition 2
        #for i in range(len(a)):
        #    if a[i] != '':
        #print(new_list)
        new=[new_list]
        print(new)
        desired_list = [item.strip() for item in new[0].split(',') if item.strip() != '']
        print(desired_list)
        result[2]['td!DESCRIPTION']=desired_list
        print(result) 
        datadict=datapp+result
        datacol = []
        for item in datadict:
            if isinstance(item, dict):
                for key, value in item.items():
                    datacol.append(f"{key}: {value}")
            else:
                datacol.append(item)
        
        if len(datacol) < 15:
            # Append empty spaces to make it a 15-element list
            datacol += [''] * (15 - len(datacol))
        
        print('datacol')
        print(datacol)  
        print(len(datacol))
        formatted_file_size=str(formatted_file_size)
        #print(datacol[12])
        datasave=dlt_melements.objects.create(dlt_melements_tid=T_id,dlt_melements_cid=C_id,dlt_melements_dtype=fileformat,dlt_melements_1=datacol[0],dlt_melements_2=datacol[1],dlt_melements_3=datacol[2],dlt_melements_4=datacol[3],dlt_melements_5=datacol[4],dlt_melements_6=datacol[5],dlt_melements_7=datacol[6],dlt_melements_8=datacol[7],dlt_melements_9=datacol[8],dlt_melements_10=datacol[9],dlt_melements_11=datacol[10],dlt_melements_12=datacol[11],dlt_melements_13=datacol[12],dlt_melements_14=datacol[13],dlt_melements_15=datacol[14],dlt_melements_uid=U_id)
        latest_data = dlt_melements.objects.order_by('-iddlt_melements').first()
        id = latest_data.iddlt_melements
        print(id)
        docproc_save=DltDocproc.objects.create(dlt_docproc_userid=U_id,dlt_docproc_filesize=formatted_file_size,dlt_docproc_filetype=fileformat,dlt_docproc_filename=file,dlt_docproc_sts="PROCESSED",dlt_docproc_accrcy="80%",dlt_docproc_elemid=id)
        latest_docproc_data = DltDocproc.objects.order_by('-iddlt_docproc').first()
        docproc_id=latest_docproc_data.iddlt_docproc
        print(docproc_id)
        response_data = {'message': 'Data received and processed successfully'}
        print(str(pdf_path))
        path = Path(pdf_path)
        fp = str(path)
        print(fp)
        datas= {"T_id":T_id,"C_id":C_id,"id":id,"U_id":U_id,"dtype":fileformat,"Final_text": datacol,"docproc_id":docproc_id,"filepath":fp,'column_headers':column_headers,'colvalues':colvalues,'datapp':datapp,'index_values':index_values}
        print(datas)
  #return {"result": results_json}
        return Response(datas)
