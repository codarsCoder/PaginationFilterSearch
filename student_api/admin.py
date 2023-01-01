from django.contrib import admin
from .models import Student, Path
from import_export import resources
from .models import Student

class StudentResource(resources.ModelResource):

    class Meta:
        model = Student


from import_export.admin import ImportExportModelAdmin

class StudentAdmin(ImportExportModelAdmin):
    resource_classes = [StudentResource]

# Register your models here.
admin.site.register(Student,StudentAdmin)
admin.site.register(Path)