from app.models import Candidates, History
import datetime
from django.http import HttpResponse

def saveHistory(request):
    D = datetime.date.today()
    minus_oneDay = datetime.datetime.strptime(str(D), "%Y-%m-%d") - datetime.timedelta(days=1)
    filterD = minus_oneDay.strftime("%Y-%m-%d")
    Cand = Candidates.objects.filter(mdf_date=filterD)
    for y in Cand:
        cand_name = y.cand_name
        mdf_date = y.mdf_date
        act_date = y.act_date
        lastD = Candidates.objects.filter(is_active='True').latest('act_date')
        plus_oneDay = datetime.datetime.strptime(lastD.act_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        setD = plus_oneDay.strftime("%Y-%m-%d")
        Candidates.objects.filter(mdf_date=mdf_date).update(act_date=setD,mdf_date=setD)
        ins = History(cand_name=cand_name,mdf_date=mdf_date,act_date=act_date)
        ins.save()

def nextCand(mdfD):
    Cand = Candidates.objects.filter(excuse=False,mdf_date__gte=mdfD).order_by('mdf_date')
    for y in Cand:
        return y.mdf_date

def excuseRequest(mdfD,nextD):
    Cand = Candidates.objects.filter(mdf_date=nextD)
    for y in Cand:
        nCand_id = y.id
    Cand = Candidates.objects.filter(mdf_date=mdfD)
    for y in Cand:
        cCand_id = y.id
    Candidates.objects.filter(id=cCand_id).update(mdf_date=nextD)
    Candidates.objects.filter(id=nCand_id).update(mdf_date=mdfD)
    
def  deactActiveCand(actD):
    Cand = Candidates.objects.filter(is_active=True,act_date__gte=actD).order_by('act_date')
    for y in Cand:
        plus_oneDay = datetime.datetime.strptime(y.act_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        filterD = plus_oneDay.strftime("%Y-%m-%d")
        setD = y.act_date
        Candidates.objects.filter(act_date=filterD,is_active="True").update(act_date=setD)

def deactModifiedCand(mdfD):
    Cand = Candidates.objects.filter(is_active=True,mdf_date__gte=mdfD).order_by('mdf_date')
    for y in Cand:
        plus_oneDay = datetime.datetime.strptime(y.mdf_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        filterD = plus_oneDay.strftime("%Y-%m-%d")
        setD = y.mdf_date
        Candidates.objects.filter(mdf_date=filterD,is_active="True").update(mdf_date=setD)

def actActiveCand(actD):
    Cand = Candidates.objects.filter(is_active=True,act_date__gte=actD).order_by('-act_date')
    for y in Cand:
        plus_oneDay = datetime.datetime.strptime(y.act_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        setD = plus_oneDay.strftime("%Y-%m-%d")
        filterD = y.act_date
        Candidates.objects.filter(act_date=filterD,is_active="True").update(act_date=setD)

def actModifiedCand(mdfD):
    Cand = Candidates.objects.filter(is_active=True,mdf_date__gte=mdfD).order_by('-mdf_date')
    for y in Cand:
        plus_oneDay = datetime.datetime.strptime(y.mdf_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        setD = plus_oneDay.strftime("%Y-%m-%d")
        filterD = y.mdf_date
        Candidates.objects.filter(mdf_date=filterD,is_active="True").update(mdf_date=setD)
