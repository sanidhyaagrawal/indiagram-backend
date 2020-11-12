from django.contrib import admin
from . import models
# Register your models here.

# Register your models here.
admin.site.register(models.user_details)
admin.site.register(models.otps)
admin.site.register(models.tokenised_contact_info)

admin.site.register(models.sessionToken)
