from django.contrib import admin
from tournament.models import Participant,Game,NewJourneyCup,FakeCup
# Register your models here.
admin.site.register(Participant)
admin.site.register(Game)
admin.site.register(NewJourneyCup)
admin.site.register(FakeCup)