from rest_framework import serializers
from .models import Tag, Ingredient, Recipe, RecipeIngredient

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'color']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'amount']

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'author', 'name', 'text', 'cooking_time', 'ingredients', 'tags']

    def create(self, validated_data):
        # Удаляем автора из validated_data, если он там есть
        validated_data.pop('author', None)
        # Получаем автора из аргументов
        author = self.context['request'].user
        # Создаем объект рецепта
        recipe = Recipe.objects.create(author=author, **validated_data)
        
        # Добавляем связанные данные для ингредиентов и тегов
        ingredients_data = self.initial_data.get('ingredients')
        for ingredient_data in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(**ingredient_data)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient)

        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.tags.set(validated_data.get('tags', instance.tags))
        instance.save()

        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.create(**ingredient_data['ingredient'])
            RecipeIngredient.objects.update_or_create(recipe=instance, ingredient=ingredient, defaults={'amount': ingredient_data['amount']})
        return instance
