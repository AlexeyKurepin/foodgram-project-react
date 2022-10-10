from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'author',
                    'quantity_in_favorites',
                    )
    list_editable = ('name', 'author')
    search_fields = ('name', 'author', 'author__first_name', 'author__email')
    list_filter = ('tags',)
    empty_value_display = '-пусто-'

    def quantity_in_favorites(self, obj):
        return obj.favorite.count()

    quantity_in_favorites.short_description = 'Количество в избранном'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'slug',
                    )
    list_editable = ('name', 'slug',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'measurement_unit',
                    )
    list_editable = ('name', 'measurement_unit',)
    search_fields = ('name',)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'ingredient',
                    'amount',
                    'measurement_unit',
                    )
    list_editable = ('ingredient', 'amount')
    search_fields = ('ingredient',)

    @staticmethod
    def measurement_unit(obj):
        return obj.ingredient.measurement_unit


class FavoriteAndCartAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'user',
                    'recipe',
                    )
    list_editable = ('user', 'recipe',)
    list_filter = ('user', 'recipe')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAndCartAdmin)
admin.site.register(ShoppingCart, FavoriteAndCartAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
