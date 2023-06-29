from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import register, hello, BookViewSet, PageViewSet ,get_user, get_author_books
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'pages', PageViewSet, basename='page')


urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", register),
    path("hello/", hello),
    path("getuser/" , get_user),
    path("getbooks/" , get_author_books )
    
] + router.urls
