from django.contrib import admin
from users.models import User
from users.models import User, VerificationToken

admin.site.register(User)

admin.site.register(VerificationToken)



