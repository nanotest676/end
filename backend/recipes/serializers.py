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
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'user', 'description', 'ingredients', 'instructions', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

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
