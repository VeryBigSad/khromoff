from rest_framework import permissions


class IsShortURLOwner(permissions.BasePermission):
    """
        Object-level permission to only allow owners of an object to view or edit it.
        Only for ShortURL objects.
    """

    def has_object_permission(self, request, view, obj):
        # if user has created object, allow.

        # thinks that
        try:
            return obj.author == request.user
            # auth on site
        except KeyError:
            try:
                return obj.key == request.POST['key']
                # it was api-generated
            except KeyError:
                # link was generated anonymously, no owner
                return False


class IsVisitOwner(permissions.BasePermission):
    """
        Object-level permission to only allow owners of an object to view or edit it.
        Only for Visit objects.
    """

    def has_object_permission(self, request, view, obj):
        # if user has created object, allow.

        # thinks that
        try:
            return obj.shorturl.author == request.user
            # auth on site
        except KeyError:
            try:
                return obj.shorturl.key == request.POST['key']
                # it was api-generated
            except KeyError:
                # link was generated anonymously, no owner
                return False
