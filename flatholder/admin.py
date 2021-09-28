from django.contrib import admin
from flatholder.models import Userf
from .models import *

# Register your models here.
admin.site.register(Userf)
admin.site.register(Complain)
admin.site.register(RentBuyHouse)
admin.site.register(Transaction)

