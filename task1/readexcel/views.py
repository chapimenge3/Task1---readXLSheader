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
        col = process_excel(file, row_req)
            
    return JsonResponse(col)
