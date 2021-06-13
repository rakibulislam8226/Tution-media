from django.contrib import admin
from django.db import models
from . models import Feedback, Contact, Post, Class_in, Comment, District


#custom Admin site start #
admin.site.site_header = 'Blog Admin Panel'
admin.site.site_title='Blog Admin Panel'
admin.site.index_title=''

class CommentInline(admin.TabularInline):
  model=Comment

class PostAdmin(admin.ModelAdmin):
  # fields = ('user', 'email')
  # exclude = ('user', 'email')
  readonly_fields = ('user',)
  list_display = ('user','title', 'email', 'date_time')
  list_filter = ('user', 'date_time','salary', 'avaliable', 'category')
  search_fields = ('user__username', 'date_time', 'salary',
                   'avaliable', 'category', 'email', 'class_in__name')
  # list_editable = ('date_time',)
  list_display_links = ('title',)
  inlines=[
      CommentInline,
  ]

#custom Admin site end #



# Register your models here.
admin.site.register(Feedback)
admin.site.register(Contact)
admin.site.register(Post, PostAdmin)
admin.site.register(Class_in)
admin.site.register(Comment)
admin.site.register(District)

