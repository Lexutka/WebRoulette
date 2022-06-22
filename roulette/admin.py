from django.contrib import admin
from .models import Round, RollLog, ActivityLog, RoundLog
# Register your models here.

admin.site.register(Round)
admin.site.register(RollLog)
admin.site.register(ActivityLog)
admin.site.register(RoundLog)
