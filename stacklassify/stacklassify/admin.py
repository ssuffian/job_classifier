from django.contrib import admin
from .models import Job, JobClassification


class JobAdmin(admin.ModelAdmin):
    list_display = ('guid','title')
class JobClassificationAdmin(admin.ModelAdmin):
    list_display = ('person_id','job_id','classification','duration_looked_at')
admin.site.register(Job,JobAdmin)
admin.site.register(JobClassification,JobClassificationAdmin)