from locale import currency
from django.db import models

class JobsSource(models.Model):
    name = models.CharField(max_length=100, null=False)
    url = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

class Jobs(models.Model):
    source = models.ForeignKey(JobsSource, on_delete=models.CASCADE)
    job_id = models.PositiveIntegerField()
    name = models.CharField(max_length=150)
    salary_from = models.PositiveIntegerField(null=True)
    salary_to = models.PositiveIntegerField(null=True)
    schedule = models.CharField(max_length=50)
    employer_name = models.CharField(max_length=150)
    published_at = models.DateTimeField()
    url = models.CharField(default='', max_length=500)
    new = models.BooleanField(default=True)
    currency = models.CharField(default='RUR', max_length=100)

    class Meta:
        verbose_name_plural = 'Jobs'
    
    def __str__(self):
        return f'{self.job_id}: {self.name}'