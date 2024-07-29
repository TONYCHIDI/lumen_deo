from django.contrib import admin

from .models import CompanyBank, Houses, NewUser, Project, Prototype, Subscription, User, UserCategory

# Register your models here.
admin.site.register(CompanyBank)
admin.site.register(Houses)
admin.site.register(NewUser)
admin.site.register(Project)
admin.site.register(Prototype)
admin.site.register(Subscription)
admin.site.register(User)
admin.site.register(UserCategory)