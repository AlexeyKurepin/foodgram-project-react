from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (IngredientSerializer, MiniRecipeSerializer,
                             RecipeCreateSerializer, RecipeSerializer,
                             SubscriptionSerializer, TagSerializer)
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from users.models import Subscription, User


class SubscriptionsViewSet(viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer
    queryset = User.objects.all()

    @action(detail=False,
            permission_classes=[IsAuthenticated, ],
            )
    def subscriptions(self, request):
        user = self.request.user
        subscriptions = user.follower.all().values('author')
        result = User.objects.filter(id__in=subscriptions)
        page = self.paginate_queryset(result)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthorOrAdminOrReadOnly, ])
    def subscribe(self, request, pk):
        user = self.request.user
        author = get_object_or_404(User, pk=pk)
        serializer = self.get_serializer(author)

        if self.request.method == 'POST':
            subscription = Subscription(user=user, author=author)
            if user == author:
                raise serializers.ValidationError(
                    'Нельзя подписаться на самого себя!')
            if user.follower.filter(author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого пользователя!')
            subscription.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif self.request.method == 'DELETE':
            if not user.follower.filter(author=author).exists():
                raise serializers.ValidationError(
                    'Вы не подписаны на этого пользователя!')
            subscription = get_object_or_404(user.follower, author=author)
            subscription.delete()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipeCreateSerializer
        return RecipeSerializer


class FavoriteViewSet(viewsets.GenericViewSet):
    serializer_class = MiniRecipeSerializer
    queryset = Recipe.objects.all()

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthorOrAdminOrReadOnly, ])
    def favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = self.get_serializer(recipe)

        if self.request.method == 'POST':
            favorite = Favorite(user=user, recipe=recipe)
            if user.favorite.filter(recipe=recipe).exists():
                raise serializers.ValidationError(
                    'Этот рецепт уже в избранном!')
            favorite.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif self.request.method == 'DELETE':
            if not user.favorite.filter(recipe=recipe).exists():
                raise serializers.ValidationError(
                    'Этого рецепта нет в избранном!')
            favorite = get_object_or_404(user.favorite, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartViewSet(viewsets.GenericViewSet):
    serializer_class = MiniRecipeSerializer
    queryset = Recipe.objects.all()

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthorOrAdminOrReadOnly, ])
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = self.get_serializer(recipe)

        if self.request.method == 'POST':
            cart = ShoppingCart(user=user, recipe=recipe)
            if user.cart.filter(recipe=recipe).exists():
                raise serializers.ValidationError(
                    'Этот рецепт уже в корзине!')
            cart.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif self.request.method == 'DELETE':
            if not user.cart.filter(recipe=recipe).exists():
                raise serializers.ValidationError(
                    'Этого рецепта нет в корзине!')
            cart = get_object_or_404(user.cart, recipe=recipe)
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=['get', ],
            permission_classes=[IsAuthenticated, ],
            )
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipes__cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            total_amount=Sum('amount'))
        content_list = []
        for ingredient in ingredients:
            content_list.append(
                f'{ingredient["ingredient__name"]} '
                f'({ingredient["ingredient__measurement_unit"]}): '
                f'{ingredient["total_amount"]}')
        content = 'Ваш список покупок:\n\n' + '\n'.join(content_list)
        filename = 'shopping_list.txt'
        file = HttpResponse(content, content_type='text/plain')
        file['Content-Disposition'] = 'attachment; filename={0}'.format(
            filename)
        return file
