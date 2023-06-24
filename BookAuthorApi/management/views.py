from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Author
from .serializers import UserSerializer, AuthorSerializer


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
