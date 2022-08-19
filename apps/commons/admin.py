from django.contrib import admin

from .forms import EditForm, PostForm
from .models import Post,Faq


class PostAdmin (admin.ModelAdmin):
    list_display = ["title"]
    search_fields =["title", "body"]
    add_form = PostForm
    form = EditForm

    fieldsets = (
        (None, {
            'fields': ('title','title_tag', )}),
            ('Blog Post', {
                'fields': ('body',)}),
                                    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('title', 'title_tag', 'body',),
            }),
            )
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)

admin.site.register(Faq)
