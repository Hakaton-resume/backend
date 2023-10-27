from django.contrib import admin

from .models import Activity, Skill

# Register your models here.
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass
