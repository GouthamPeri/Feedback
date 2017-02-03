from __future__ import unicode_literals

from django.db import models

# Create your models here.
class AcademicYear(models.Model):
    academic_year_code=models.IntegerField(primary_key=True)
    academic_year=models.CharField(max_length=10)
    def __str__(self):
        return str(self.academic_year_code)
    
class Department(models.Model):
    department_code=models.CharField(primary_key=True,max_length=10)
    depratment_name=models.CharField(max_length=30)
    inception_year=models.ForeignKey(AcademicYear)
    def __str__(self):
        return self.department_code