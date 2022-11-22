from django.contrib import admin
from .models import Opportunity, Question, Answer, Material, Proposal, Application, Post
from accounts.models import CustomUser
from django.http import HttpResponse
from io import BytesIO


from reportlab.pdfgen import canvas


def export_to_csv(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    for obj in queryset:
        row = writer.writerow([getattr(obj, 'char_field_1')])

    return response
    
export_to_csv.short_description = 'Export to csv'


def export_to_pdf(self, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Start writing the PDF here
    p.drawString(300, 300, 'Hello world.')
    # End writing

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


export_to_pdf.short_description = 'Export to pdf'

class ApplicationAdmin(admin.ModelAdmin):
    search_fields = (
    'user__email',
    'opportunity__title'
    )
    list_display = ['user','opportunity', 'successful']
    actions = [export_to_pdf, export_to_csv] 

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'visible')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    
def make_published(modeladmin, request, queryset):
    queryset.update(status='p')

def open_to_all_users(self, request, queryset):
    for opportunity in queryset:
        opportunity.visible_to.set(CustomUser.objects.all())

def close_to_all_users(self, request, queryset):
    for opportunity in queryset:
        opportunity.visible_to.set(CustomUser.objects.none())

class OpportunityAdmin(admin.ModelAdmin):
    actions = [open_to_all_users, close_to_all_users]

admin.site.register(Opportunity, OpportunityAdmin)
admin.site.register(Question)
admin.site.register(Post, PostAdmin)
admin.site.register(Answer)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Proposal)
admin.site.register(Application, ApplicationAdmin)