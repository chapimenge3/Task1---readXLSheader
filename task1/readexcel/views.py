from django.shortcuts import render, redirect
from django.http import JsonResponse


from django.conf import settings

import os  
import requests
import openpyxl
from pathlib import Path

def process_excel(file, row_num):
    wb_obj = openpyxl.load_workbook(file)
    sheet = wb_obj.active
    r = {}
    c = 0 
    for row in sheet.iter_rows():
        # if row == row_num :
        c+=1
        if c == row_num :
            
            for cell in row:
                if cell.value:
                    r[ f'Column{cell.column_letter}' ] = cell.value
            print(r)
            return r
           
    return {}

def analays_excel(file, row_num, num_rec):
    wb_obj = openpyxl.load_workbook(file)
    sheet = wb_obj.active
    r = {}
    c = 0 
    for row in sheet.iter_rows():
        # if row == row_num :
        c+=1
        if c == row_num :
            
            for cell in row:
                if cell.value:
                    r[ f'Column{cell.column_letter}' ] = cell.value
            
            break
    c = 0 
    checked = 0
    l = [ {"string" : 0, "integer" : 0, "decimal" : 0} for i in r ]
    for row in sheet.iter_rows():
        c += 1
        
        if c <= row_num :
            continue

        if checked == num_rec:
            break
        checked += 1 
        
        rc = 0
        for cell in row:
            
            if cell.value:
                if str(cell.value).isdigit() :
                    l[rc]["integer"] += 1
                    
                elif str(cell.value).replace(',','').isdecimal() :
                    
                    l[rc]['decimal'] += 1
                
                else:
                    l[rc]["string"] += 1 
                    
                rc += 1
                
                
    types = [] 
    for i in l:
        max_ = ""
        max_n = 0
        for j in i :
            if max_n <= i[j] :
                max_ = j
                max_n = i[j]
                
        types.append(max_)
    
    return { i:j for i,j in zip(r,types) }

            
    

def download_file(url):

    # this will grab the filename from the url
    filename = url.split('/')[-1]

    print(f'Downloading {filename}')

    r = requests.get(url)
    path = os.path.join(settings.BASE_DIR, filename)
    with open(path, 'wb') as output_file:
        output_file.write(r.content)
        
    return path
    
    

def redirect_home(request):
    return redirect("readXLSheader")



def renderexcel(request):
    if request.method == "GET" :
        return render(request, "index.html")
    else:
        url = request.POST.get("link")
        row_req = 1
        
        if request.POST.get("row", None):

            row_req = int(request.POST.get("row"))
            
        file = download_file(url)
        print(file)
        col = process_excel(file, row_req)
        
        
    return JsonResponse(col)

def analysis(request):
    
    if request.method == "GET" :
        return render(request, "indext3.html")
    else:
        url = request.POST.get("link")
        row_req = 1
        
        if request.POST.get("row", None):

            row_req = int(request.POST.get("row"))
        numrec = int(request.POST.get("numrec", 0))
        
        file = download_file(url)
        
        print(file)
        
        col = process_excel(file, row_req)
        
        analysed = analays_excel(file, row_req, numrec)
        
    return JsonResponse( {  "ColumnVales" : col , "types" : analysed })


def log_to_db(data):
    pass