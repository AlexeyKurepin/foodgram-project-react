import django_filters

from recipes.models import Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=Tag.objects.all(),
        to_field_name="slug",)
    is_in_favorite = django_filters.NumberFilter(method='get_is_in_favorite')
    is_in_shopping_cart = django_filters.NumberFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = {'author', }

    def get_is_in_favorite(self, queryset, name, value):
        user = self.request.user
        if value == 1:
            return queryset.filter(favorite__user=user)
        return Recipe.objects.all()

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == 1:
            return queryset.filter(cart__user=user)
        return Recipe.objects.all()
