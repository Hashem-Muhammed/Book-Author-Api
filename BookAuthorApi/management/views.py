from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from .models import Book , Page
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Author
from .serializers import UserSerializer, AuthorSerializer, BookSerializer, PageSerializer
from .permissions import IsAuthorOrReadOnly, IsBookOwnerOrReadOnly, IsAuthor

@api_view(["POST"])
def register(request):
    if request.method == "POST":
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            is_author = request.data.get("is_author", False)
            if is_author:
                bio = request.data.get("bio")
                author = Author(user=user, bio=bio)
                author.save()
                author_serializer = AuthorSerializer(author)
                return Response(author_serializer.data, status=status.HTTP_201_CREATED)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hello(request):
    st = f"hello , {request.user.first_name}"
    return Response(st)


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = BookSerializer
    queryset = Book.objects.all()

class PageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsBookOwnerOrReadOnly]
    serializer_class = PageSerializer
    queryset = Page.objects.all() 

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
    author = Author.objects.filter(user=request.user).first()
    if author:
        serializer = AuthorSerializer(author)
    else:
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated , IsAuthor])
def get_author_books(request):
    author = Author.objects.get(user = request.user)
    books = author.books.all()
    print(books)
    serializer = BookSerializer(books , many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)
