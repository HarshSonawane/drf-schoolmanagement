from django.contrib import admin
from .models import School, Student, Grade


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'city', 'pincode')
    list_filter = ('city', 'pincode')


    def name(self, obj):
        return obj.user.get_full_name()

    def email(self, obj):
        return obj.user.email


admin.site.register(School, SchoolAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'school', 'grade')
    list_filter = ('school', 'grade')

    def name(self, obj):
        return obj.user.get_full_name()

    def username(self, obj):
        return obj.user.username


admin.site.register(Student, StudentAdmin)


class GradeAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Grade, GradeAdmin)
