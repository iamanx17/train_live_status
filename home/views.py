from django.shortcuts import render
from django.contrib import messages
import requests, json
# Create your views here.

def home(request):
    if request.method=='POST':
        train_number=request.POST['train_number']
        date=request.POST['date']
        y=date[:4]
        m=date[5:7]
        d=date[8:]
        current_date=str(y)+str(m)+str(d)

        api_key='421fe95cb0455d813dd14d176502894c'
        base_url='http://indianrailapi.com/api/v2/livetrainstatus/apikey/'
        complete_url = base_url+api_key+ "/trainnumber/" + train_number + "/date/" + current_date
        response_obj=requests.get(complete_url)
        result=response_obj.json()
        note=False
        code=int(result['ResponseCode'])
        
        if code==200:
            if result['CurrentStation']!=None:
                train_status=result['CurrentStation']['StationName']
                note=True
                return render(request,'result.html',{'train_status':train_status,'note':note})     
            else:
                messages.info(request,'Data Not Found, Possible reasons: Train has not yet started or it has reached the destination')
                return render(request,'result.html')
        else:
            messages.info(request,'An Internal Error Occurred!!')
            return render(request,'result.html')
        
    return render(request,'home.html')