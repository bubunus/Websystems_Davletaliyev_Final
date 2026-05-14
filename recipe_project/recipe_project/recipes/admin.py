from django.contrib import admin
from .models import Recipe, Ingredient, Comment

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['author', 'created_at']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    inlines = [IngredientInline, CommentInline]

admin.site.register(Ingredient)
admin.site.register(Comment)
