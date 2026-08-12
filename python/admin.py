from django.contrib import admin
from .models import Chapters, Topics, Interview, CodingQuestion

# Register your models here.
admin.site.register(Chapters)
admin.site.register(Topics)
admin.site.register(Interview)
admin.site.register(CodingQuestion)
