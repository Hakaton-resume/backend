from django.contrib import admin

from .models import (Activity, Company, HRUser, StudentsActivities,
                     StudentUser, User, Skill, SkillStudent)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =(
        'id',
        # 'username',
        'first_name',
        'last_name',
        'email',
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # list_display =(
    #     'id',
    #     'username',
    #     'first_name',
    #     'last_name',
    #     'email',
    # )
    pass


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(HRUser)
class HRUserAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentUser)
class StudentUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass


@admin.register(SkillStudent)
class SkillStudentAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentsActivities)
class SkillStudentAdmin(admin.ModelAdmin):
    pass
