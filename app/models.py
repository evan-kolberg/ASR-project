from django.db import models


class applicant(models.Model):
    jobid = models.TextField()
    applicantid = models.TextField()
    salary = models.TextField()
    
class employer(models.Model):
    jobid = models.TextField()
    employerid = models.TextField()
    salary = models.TextField()

class responses(models.Model):
    jobid = models.TextField()
    employerid = models.TextField()
    applicantid = models.TextField()
    boolean = models.BooleanField()
    datetime = models.DateTimeField(auto_now_add=True)



