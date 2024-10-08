from django.contrib import admin
from .models import Department, Class, Unit, Exam, Question, StudentPortfolio

admin.site.register(Department)
admin.site.register(Class)
admin.site.register(Unit)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(StudentPortfolio)