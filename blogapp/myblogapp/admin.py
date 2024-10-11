from django.contrib import admin
from .models import Post, Likes, Comments, CustomUser

# Register your models here



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('text_content', 'created_at', 'created_by')
    search_fields = ('text_content',)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user','comment')
    search_fields = ('comment',)



@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')
    fields = ('user',)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display =('username', 'email', 'first_name', 'last_name')
    fields = ('email', 'username', 'first_name', 'last_name')
    search_fields = ('email',)

    
# search fields should be a tuple and one itm in a tuple must have a comma,


