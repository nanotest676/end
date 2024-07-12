from django.contrib import admin
from .models import Tag, Ingredient, Recipe, RecipeIngredient


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Класс TagAdmin отвечает за отображение и управление моделью Tag в админке.
    Он отображает поля 'id', 'name' и 'slug' в списке,
    позволяет искать по полю 'name' и автоматически заполняет поле 'slug' на основе 'name'.
    """
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Класс IngredientAdmin отвечает за отображение и управление моделью Ingredient в админке.
    Он отображает поля 'id', 'name' и 'measurement_unit' в списке,
    и позволяет искать по полю 'name'.
    """
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    """
    Класс RecipeIngredientInline используется для отображения и управления
    моделью RecipeIngredient в составе модели Recipe в виде вложенной формы.
    Он позволяет добавлять и редактировать ингредиенты, связанные с конкретным рецептом.
    """
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Класс RecipeAdmin отвечает за отображение и управление моделью Recipe в админке.
    Он отображает поля 'id', 'name', 'author', 'cooking_time', 'is_favorited' и 'is_in_shopping_cart' в списке,
    позволяет искать по полям 'name', 'author__username' и 'tags__name',
    а также фильтровать по полям 'tags' и 'author'.
    Вложенные модели RecipeIngredientInline позволяют управлять ингредиентами рецепта.
    """
    list_display = (
        'id', 'name', 'author', 'cooking_time', 'is_favorited', 'is_in_shopping_cart'
    )
    search_fields = ('name', 'author__username', 'tags__name')
    list_filter = ('tags', 'author')
    inlines = [RecipeIngredientInline]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """
    Класс RecipeIngredientAdmin отвечает за отображение и управление моделью RecipeIngredient в админке.
    Он отображает поля 'id', 'recipe', 'ingredient' и 'amount' в списке,
    и позволяет искать по полям 'recipe__name' и 'ingredient__name'.
    """
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name', 'ingredient__name')
