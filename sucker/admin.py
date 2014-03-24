from django.contrib import admin

from .models import Citation, Person, Patent, Claim


admin.site.register(Citation)
admin.site.register(Patent)
admin.site.register(Person)
admin.site.register(Claim)
