from rest_framework import permissions


class DoCollectMetaPermission(permissions.BasePermission):
    """
        Global permission which checks if you can create ShortURL
        depending on did you collect metadata or not
        Only for POST and GET requests.
    """

    message = 'Only authorised users can create URLs which are collecting metadata.'

    def has_permission(self, request, view):
        if request.method == 'POST':
            do_collect_meta = request.POST.get('do_collect_meta')
        else:
            do_collect_meta = request.GET.get('do_collect_meta')

        if do_collect_meta == 'false':
            do_collect_meta = False
        try:
            if int(do_collect_meta) <= 0:
                do_collect_meta = False
        except ValueError:
            pass
        except TypeError:
            pass

        if not bool(do_collect_meta) or request.user.is_authenticated:
            return True
        return False


class IsVisitOwner(permissions.BasePermission):
    """
        Permission for Visit model, which tells if
        you are it's owner or not.
    """

    message = 'Only owners of this shorturl can see it\'s visits.'

    def has_object_permission(self, request, view, obj):
        if obj.shorturl.author == request.user:
            return True
        else:
            try:
                if obj.shorturl.key == request.auth.key:
                    return True
            except AttributeError:
                pass
        return False


class IsShorturlOwner(permissions.BasePermission):
    """
        Permission for ShortUrl model, which tells if
        you are it's owner or not.
    """

    message = 'Only owners of this shorturl can access it.'

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        else:
            try:
                if obj.key == request.auth.key:
                    return True
            except AttributeError:
                pass
        return False
