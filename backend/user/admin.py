from django.contrib import admin
from user import models

admin.site.register(models.User)
admin.site.register(models.Session)
admin.site.register(models.Account)
admin.site.register(models.VerificationToken)
