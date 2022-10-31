from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Paper)
admin.site.register(Section)
admin.site.register(MCQ)
admin.site.register(MCQOption)
admin.site.register(CRO)
admin.site.register(ERQ)