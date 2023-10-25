from django.contrib import admin

from .models import Company, HRUser,  StudentUser, User


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


@admin.register(HRUser)
class HRUserAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentUser)
class StudentUserAdmin(admin.ModelAdmin):
    pass
