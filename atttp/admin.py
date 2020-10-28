from django.contrib import admin

# Register your models here.
from atttp.models import Igrisce, GameHead, GameDetail

admin.site.register(Igrisce)
admin.site.register(GameHead)
admin.site.register(GameDetail)