from rest_framework import permissions

class IsCustomerUser(permissions.BasePermission):
    """
    Allows access only to authenticated users who are explicitly marked as customers.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'is_customer', False)
        )

class IsSupportAgentUser(permissions.BasePermission):
    """
    Allows access only to support staff members handling chats or inventory adjustments.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (getattr(request.user, 'is_support_agent', False) or request.user.is_staff)
        )

class IsOwnerOrStaff(permissions.BasePermission):
    """
    Object-level permission to ensure users can only read/edit their own data 
    (like profiles, carts, or orders), while allowing support staff access.
    """
    def has_object_permission(self, request, view, obj):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False

        # Allow administrators or support staff full visibility
        if getattr(user, 'is_staff', False) or getattr(user, 'is_support_agent', False):
            return True

        # Common ownership patterns across models
        # 1) Direct `user` FK on the object
        if hasattr(obj, 'user'):
            return obj.user == user

        # 2) Numeric user id field
        if hasattr(obj, 'user_id'):
            return obj.user_id == getattr(user, 'id', None)

        # 3) Cart-related objects (CartItem -> cart -> user)
        if hasattr(obj, 'cart'):
            cart = getattr(obj, 'cart')
            if hasattr(cart, 'user'):
                return cart.user == user
            if hasattr(cart, 'user_id'):
                return cart.user_id == getattr(user, 'id', None)

        # 4) Session-related objects (e.g., chat session -> user)
        if hasattr(obj, 'session') and hasattr(obj.session, 'user'):
            return obj.session.user == user

        return False