from django.contrib import admin
from .models import Law , LegalCase , Quiz , Profile# Register your models here.
admin.site.register(Law)
admin.site.register(LegalCase)
admin.site.register(Quiz)
admin.site.register(Profile)