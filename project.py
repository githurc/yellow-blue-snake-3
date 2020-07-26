#!/usr/bin/env python
# coding: utf-8

# ##  1. Import packages and define basics for data:#

# In[2]:


import zipfile
from zipfile import ZipFile
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

# declare dictionaries to provide structures for data storage and searching
page_img_dic = {} # relate page file name and the scanned image of the page
page_text_dic = {} # relate page file name and text of the page
page_faces_dic = {} # relate page file name and images of faces of the page

# set up Image font type
font = ImageFont.truetype(r'readonly/fanwood-webfont.ttf', 24) 


# ## 2. Open zip file and assign relevant data to dictionaries:

# In[ ]:


with ZipFile('readonly/images.zip', 'r') as img_source:
    p_lst = img_source.infolist()    
    for i in p_lst:
        f = i.filename
        p = img_source.open(i)
        page = Image.open(p).convert('RGB')
        page_img_dic[f] = page
        page_text_dic[f] = ""
        page_faces_dic[f] = "" 
        

# to test file data retrieval:
# print (p_lst[0])
# test_img = page_img_dic.get('a-0.png')
# display (test_img)
# print(page_img_dic)


# ## 3. Proceed with "page to text" handling and save as strings in page_text_dic:

# In[ ]:


for k, v in page_img_dic.items():
    text = pytesseract.image_to_string(v)
    page_text_dic[k] = text

# to test if data was saved in page_text_dic:
# t = page_text_dic.get('a-0.png')
# print (t)


# ## 4. Proceed with "page to face" handling and save lists of face images in page_img_dic:

# In[ ]:


for k, v in page_img_dic.items():
    face_lst = []
    cv_img = np.array(v)
    cv_img_gray = cv.cvtColor(cv_img, cv.COLOR_BGR2GRAY)
    face_frames = face_cascade.detectMultiScale(cv_img_gray, 1.3, 5)
    
    for x, y, w, h in face_frames:
        face = v.crop((x,y,x+w,y+h))
        face.thumbnail((100, 100) )
        face_lst.append(face)
    
    page_faces_dic[k] = face_lst
    
# to test if data was saved in page_faces_dic:
# print (page_faces_dic.get('a-1.png'))


# ## 5. Define a function that generates different images for pages with/ without faces:

# In[ ]:


def face_results(filename):
    x=0
    y=0
    f_img_lst = page_faces_dic.get(filename)
    if not f_img_lst:
        # "results found in file but there were no faces in that file!"
        face_no_res_label =Image.new("RGB", (500,80), (255, 255, 255))
        no_res = "Results found in {}\n\nBut there were no faces found in that file!".format(filename)
        f_d = ImageDraw.Draw(face_no_res_label)
        f_d.text((0, 10),no_res,(0,0,0), font = font)
        return face_no_res_label
        display(face_no_res_label)
    else:
        face_res_label =Image.new("RGB", (500,40), (255, 255, 255))
        res = "Results found in {}".format(filename)
        f_d = ImageDraw.Draw(face_res_label)
        f_d.text((0, 10),res,(0,0,0), font = font)
        if len(f_img_lst) % 5 < 1:
            h = 100 * (len(f_img_lst) // 5)
        else:
            h = 100 * (len(f_img_lst) // 5 + 1)
        face_res =Image.new("RGB", (500,h))
        f_1 = f_img_lst[0]
        for i in f_img_lst:    
            face_res.paste(i, (x, y))
            if x+f_1.width == face_res.width:
                x=0
                y=y + f_1.height
            else:
                x=x + f_1.width
        face_result =Image.new("RGB", (500,face_res.height + face_res_label.height))
        face_result.paste(face_res_label, (0, 0))
        face_result.paste(face_res, (0, face_res_label.height))
        return (face_result)
    

# to test if different images can be generated for different pages
# a = 'a-0.png'    
# face_results(a)
# b = 'a-8.png'    
# face_results(b)


# ## 6. Define a function that searches user queries and combine all results into one image:

# In[35]:


def search():
    print("Search for images: ")
    query = input () 
    f_lst = []
    for k, v in page_text_dic.items():
        if query in v:
            f_lst.append(k)
    if len(f_lst) == 0:
        print ("no result in newspaper files")
        return
    else:
        result_img_lst = []
        for i in f_lst:
            r = face_results(i)
            result_img_lst.append(r)
        combined_h = 0
        x = 0
        y = 0
        r_1 = result_img_lst[0]
        for i in result_img_lst:
            combined_h += i.height
        results_img = Image.new("RGB", (500,combined_h))
        for i in result_img_lst:    
            results_img.paste(i, (x, y))
            y += i.height
        return results_img
        


# ## Test 1: Try searching with the word "Mark":

# In[36]:


search()


# ## Test 2: Try searching with the word "Christopher":

# In[37]:


search()


# ## Test 3: Try searching with the word "hard":

# In[38]:


search()

