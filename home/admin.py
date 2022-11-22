from django.contrib import admin
import csv
from django.http import HttpResponse


from .models import FreshersMail

def export_to_csv(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    for obj in queryset:
        row = writer.writerow([getattr(obj, 'email')])

    return response
    
export_to_csv.short_description = 'Export to csv'

class FreshersMailAdmin(admin.ModelAdmin):
    list_display = ['email']
    actions = [export_to_csv]


admin.site.register(FreshersMail, FreshersMailAdmin)


