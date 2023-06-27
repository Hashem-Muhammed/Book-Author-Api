from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author.user == request.user 
        

class IsBookOwnerOrReadOnly(permissions.BasePermission):    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.book.author.user == request.user 
    
class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        author = getattr(user, "author", None)
        if author is None:
            return False
        return True    