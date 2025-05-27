from django.contrib import admin
from .models import add_team,incident_report, incident_history
# Register your models here.
admin.site.register(add_team)
admin.site.register(incident_report)
admin.site.register(incident_history)