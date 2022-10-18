from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (FavoriteViewSet, IngredientsViewSet, RecipesViewSet,
                       ShoppingCartViewSet, SubscriptionsViewSet, TagsViewSet)

router = DefaultRouter()
router.register('users', SubscriptionsViewSet, basename='subscription')
router.register('recipes', ShoppingCartViewSet, basename='shopping_cart')
router.register('recipes', FavoriteViewSet, basename='favorite')
router.register('recipes', RecipesViewSet)
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
