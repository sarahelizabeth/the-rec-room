from django.contrib import admin

from .models import Post, MediaType, Genre, Comment, Report, Save

class ReportAdmin(admin.ModelAdmin):
  list_display= ('__str__', 'addressed')

admin.site.register(Post)
admin.site.register(MediaType)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Report, ReportAdmin)
admin.site.register(Save)
