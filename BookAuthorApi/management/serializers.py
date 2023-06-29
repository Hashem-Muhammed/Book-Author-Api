from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Page, Book
from rest_framework.exceptions import PermissionDenied


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    def get_user_type(self, obj):
        return "reader"
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email' ,'user_type', 'username', 'password']
        extra_kwargs = {"password": {"write_only": True},
                        "username": {"write_only": True}}

    def create(self, validation_data):
        password = validation_data.pop("password", None)
        instance = self.Meta.model(**validation_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()

        return instance


class AuthorSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    def get_user_type(self, obj):
        return "author"
    user = UserSerializer()

    class Meta:
        model = Author
        fields = ["id", "bio", "user" , "user_type"]


class PageSerializer(serializers.ModelSerializer):
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Page
        fields = ["id", "title", "content", "book_id"]

    def create(self, validated_data):
        user = self.context["request"].user
        author = getattr(user, "author", None)
        if author is None:
            raise PermissionDenied("You are not authorized to create a book.")
        book = validated_data.pop("book_id")
        page = Page(book=book, **validated_data)
        page.save()
        return page


class BookSerializer(serializers.ModelSerializer):
 
    author = AuthorSerializer(read_only=True)
    pages = PageSerializer(source="page_set", many=True, read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "pages" , "author"]

    def create(self, validated_data):
        user = self.context["request"].user
        print(user)
        author = getattr(user, "author", None)
        if author is None:
            raise PermissionDenied("You are not authorized to create a book.")
        book = Book(author=author, **validated_data)
        book.save()
        return book
