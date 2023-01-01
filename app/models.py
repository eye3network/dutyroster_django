from django.db import models

# Create your models here.
class Candidates(models.Model):
    cand_name = models.CharField(max_length=50)
    cand_mobile = models.CharField(max_length=10)
    cand_email = models.EmailField()
    mdf_date = models.CharField(max_length=30)
    act_date = models.CharField(max_length=30)
    excuse = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return("Saved Successfully.")

class History(models.Model):
    cand_name = models.CharField(max_length=50)
    mdf_date = models.CharField(max_length=30)
    act_date = models.CharField(max_length=30)

class SMSHistory(models.Model):
    cand_mobile = models.CharField(max_length=10)
    send_date = models.CharField(max_length=30)
    send_time = models.CharField(max_length=2)