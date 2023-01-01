from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import Candidates, History
from app.func import *
from app.sms import sendSMS, sendMessageNow
import datetime
from background_task.models import Task
from django.core.paginator import Paginator


# Create your views here.
def makeExcuse(request):
    if request.method == 'GET':
        cand_id = request.GET['id']
        cand = Candidates.objects.filter(id=cand_id)
        cand.update(excuse=True)
        for a in cand:
            mdfD = a.mdf_date
            nextD = nextCand(mdfD)
            excuseRequest(mdfD,nextD)
            return redirect('home')

def messageNow(request):
    msg = sendMessageNow()
    return HttpResponse(msg)

def eye3StartTask(request):
    eye3 = "eye3"
    sendSMS(eye3,repeat=Task.DAILY, repeat_until=None)
    return HttpResponse("Background Sending Message Started.")

def eye3DeleteTask(request):
    Task.objects.all().delete()
    return HttpResponse("All Background Task Deleted.")


def tryit(request):
    task = Task.objects.all()
    for t in task:
        return HttpResponse(t.task_name)

def index(request):
    request.session['USERNAME'] = ''
    saveHistory(request)
    candList = Candidates.objects.filter(is_active='True')
    dutyBoy = candList.filter(mdf_date=datetime.date.today(),is_active='True')
    dutyBoy.update(excuse=False)
    history_list = History.objects.all()
    paginator = Paginator(history_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'candList':candList,'dutyBoy':dutyBoy,'page_obj':page_obj})

def auth(request):
    request.session['USERNAME'] = 'eye3'
    return redirect('home')

def logout(request):
    request.session['USERNAME'] = ''
    return redirect('index')

def home(request):
    token = request.session['USERNAME']
    if token == 'eye3':
        candList = Candidates.objects.all()
        dutyBoy = candList.filter(mdf_date=datetime.date.today(),is_active='True')
        return render(request, 'home.html',{'candList':candList,'dutyBoy':dutyBoy})
    else:
        return redirect('index')

def addCand(request):
    if request.method == 'POST':
        cand_name = request.POST['cand_name']
        cand_mobile = request.POST['cand_mobile']
        try:
            lastD = Candidates.objects.filter(is_active='True').latest('act_date')
            if lastD.act_date is not None:
                plus_oneDay = datetime.datetime.strptime(lastD.act_date, "%Y-%m-%d") + datetime.timedelta(days=1)
                setD = plus_oneDay.strftime("%Y-%m-%d")
            else:
                setD = datetime.date.today()
        except:
            setD = datetime.date.today()
        candidates = Candidates(cand_name=cand_name,cand_mobile=cand_mobile,act_date=setD,mdf_date=setD)
        candidates.save()
        return redirect('home')

def chngStatus(request):
    if request.method == 'POST':
        cand_id = request.POST['cand_id']
        cand_action = request.POST['candStatus']
        if cand_action == 'True':
            cand = Candidates.objects.filter(id=cand_id)
            setD = datetime.date.today()
            for data in cand:   
                if data.is_active == True:
                    pass
                else:
                    act_ins = Candidates.objects.filter(act_date=setD)
                    for x in act_ins:
                        actD = x.act_date
                        actActiveCand(actD)   
                    mdf_ins = Candidates.objects.filter(mdf_date=setD)
                    for x in mdf_ins:
                        mdfD = x.mdf_date
                        actModifiedCand(mdfD)
                    cand.update(mdf_date=setD,act_date=setD,is_active="True")
        elif cand_action == 'False':
            cand = Candidates.objects.filter(id=cand_id)
            for data in cand:    
                if data.is_active == False:
                    pass
                else:
                    ins = Candidates.objects.filter(id=cand_id)
                    for x in ins:
                        actD = x.act_date
                        mdfD = x.mdf_date
                        deactActiveCand(actD)
                        deactModifiedCand(mdfD)
                    Candidates.objects.filter(id=cand_id).update(is_active=cand_action,act_date='Nil',mdf_date='Nil')
        else:
            ins = Candidates.objects.filter(id=cand_id)
            for x in ins:
                actD = x.act_date
                mdfD = x.mdf_date
                deactActiveCand(actD)
                deactModifiedCand(mdfD)
            ins.delete()
        return redirect('home')