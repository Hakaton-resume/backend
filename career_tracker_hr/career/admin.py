from django.contrib import admin

from .models import (Activity, Resp, Tag,
                     Vacancy, SkillVacancy, TagVacancy)

# Register your models here.
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    pass

@admin.register(Resp)
class RespAdmin(admin.ModelAdmin):
    pass

@admin.register(TagVacancy)
class TagVacancyAdmin(admin.ModelAdmin):
    pass

@admin.register(SkillVacancy)
class SkillVacancyAdmin(admin.ModelAdmin):
    pass