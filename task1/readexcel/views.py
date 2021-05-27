from django.shortcuts import render, redirect
from django.http import JsonResponse


from django.conf import settings

import os  
import requests
import openpyxl
from pathlib import Path

def process_excel(file):
    wb_obj = openpyxl.load_workbook(file)
    sheet = wb_obj.active
    rows = [] 
    cols = []
    count = 0 
    for row in sheet.iter_rows(max_row=6):
        a = []
        count += 1
        for cell in row:
            if cell.value:
                a.append(cell.value)
        if len(a) > 1 :
            cols = a 
            break
    print("Columns ----- " , cols, )
    
    for row in sheet.iter_rows():
        if count != 0 :
            count -= 1
            continue
        r = [] 
        for cell in row:
            if cell.value:
                r.append(cell.value) 
                
        # if len(r) == len(cols):
        
        rows.append(r)
    
    print(rows)
    return cols, rows

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
    print(settings.BASE_DIR)
    if request.method == "GET" :
        return render(request, "index.html")
    else:
        url = request.POST.get("link")
        row_req = 1
        
        if request.POST.get("row", None):

            row_req = int(request.POST.get("row"))
            
        file = download_file(url)
        print(file)
        col, row = process_excel(file)
        data = []
        for i in col:
            print(i, end=" ")
        print()
        
        data = [] 
        for i in row:
            d = {}
            if len(i) < len(col):
                for j in range(len(col)-len(i)):
                    i.append(None)
            for i,j in zip(col, i):
                d[i] = j
            data.append(d)
            
    return JsonResponse({"columns" : data[:row_req] })
