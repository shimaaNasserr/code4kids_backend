from django.contrib import admin
from accounts.models import User, KidParentRelation

# Register your models here.
admin.site.site_header = "Code4Kids Admin"
admin.site.register(User)
admin.site.register(KidParentRelation)