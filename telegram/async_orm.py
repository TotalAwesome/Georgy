from asgiref.sync import sync_to_async
from jobs.models import Jobs
from techworks.models import TechWork

@sync_to_async
def get_new_jobs_queryset():
    new_jobs = Jobs.objects.filter(new=True)
    return new_jobs

@sync_to_async
def get_new_techworks_queryset():
    new_techworks = TechWork.objects.filter(new=True)
    return new_techworks

@sync_to_async
def uncheck_new(queryset):
    for i in queryset:
        i.new = False
        i.save()    