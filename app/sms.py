import requests
import datetime
from app.models import Candidates
from background_task import background

@background(schedule=1)
def sendSMS(eye3):
    try:
        dutyBoy = Candidates.objects.filter(mdf_date=datetime.date.today(),is_active=True)
        for value in dutyBoy:
            cand_name = value.cand_name
            cand_mobile = value.cand_mobile
            send(cand_name,cand_mobile)
    except:
        pass

def send(cand_name,cand_mobile):
    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=IMPSMS&language=english&route=qt&numbers=" + str(cand_mobile) + "&message=33886&variables={#EE#}&variables_values=" + str(cand_name)
    headers = {
        'authorization': "Z3zNAjh8xvaYqsPuyQLFnRKCrVWo470BX2p1cgOw6UbtJSGdIirFz6y4VOkLnYHva1pe9PSlmhfT02XG",
        'cache-control': "no-cache",
        'content-type': "application/x-www-form-urlencoded"
        }
    requests.request("POST", url, data=payload, headers=headers)

def sendMessageNow():
    try:
        dutyBoy = Candidates.objects.filter(mdf_date=datetime.date.today(),is_active=True)
        for value in dutyBoy:
            cand_name = value.cand_name
            cand_mobile = value.cand_mobile
            url = "https://www.fast2sms.com/dev/bulk"
            payload = "sender_id=IMPSMS&language=english&route=qt&numbers=" + str(cand_mobile) + "&message=33886&variables={#EE#}&variables_values=" + str(cand_name)
            headers = {
                'authorization': "Z3zNAjh8xvaYqsPuyQLFnRKCrVWo470BX2p1cgOw6UbtJSGdIirFz6y4VOkLnYHva1pe9PSlmhfT02XG",
                'cache-control': "no-cache",
                'content-type': "application/x-www-form-urlencoded"
                }
            requests.request("POST", url, data=payload, headers=headers)
    except:
        pass
    return "<center><h1 style='margin-top:100px; color: green;'>Message sent Successfully.</h1></center>"