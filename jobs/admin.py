from django.contrib import admin
from jobs.models import JobsSource, Jobs
# Register your models here.


class JobsSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_active')
    list_editable = ('url', 'is_active' )


class JobsAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'job_id', 'name', 'salary_from', 'salary_to', 'employer_name', 'published_at', 'new')
    list_display_links = ('name', 'employer_name')
    list_editable = ('new',)
    # list_editable = ('name', 'url')
    pass


admin.site.register(JobsSource, JobsSourceAdmin)
admin.site.register(Jobs, JobsAdmin)
