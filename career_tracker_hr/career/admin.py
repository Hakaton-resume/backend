from django.contrib import admin


from .models import (Favourite, Invitation, Resp,
                     SkillVacancy, Tag, Vacancy, TagVacancy)


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

@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    pass

@admin.register(Invitation)
class FavouriteAdmin(admin.ModelAdmin):
    pass
