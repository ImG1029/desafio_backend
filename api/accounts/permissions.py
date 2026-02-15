from rest_framework import permissions

from api.accounts.models import Account


class IsVeterinarian(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            account = request.user.accounts
            return account.license_number is not None
        except Account.DoesNotExist:
            return False

    message = "Only veterinarians can perform this action."

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser

    message = "Only administrators can perform this action."

class IsRecordOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.method == 'POST':
            try:
                account = request.user.accounts
                return account.license_number is not None and account.license_number != ""
            except:
                return False

        if request.method == 'GET':
            return True

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method == 'GET':
            return True

        try:
            account = request.user.accounts
            return obj.veterinarian == account
        except:
            return False

    message = "Only the veterinarian who created this record can modify it."


class ResourcePermission(permissions.BasePermission):
    REGULAR_USER_CRU_MODELS = ['Owner', 'Pet']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        is_vet = False
        try:
            account = request.user.accounts
            is_vet = account.license_number is not None and account.license_number != ""
        except:
            pass

        model_name = self._get_model_name(view)

        if is_vet:
            if request.method == 'DELETE':
                return False
            return True

        if model_name in self.REGULAR_USER_CRU_MODELS:
            return request.method in ['GET', 'POST', 'PUT', 'PATCH']

        return request.method in permissions.SAFE_METHODS

    def _get_model_name(self, view):
        if hasattr(view, 'queryset') and view.queryset is not None:
            return view.queryset.model.__name__

        view_name = view.__class__.__name__
        for model in ['Owner', 'Pet', 'Vaccine', 'VaccinationRecord', 'Account']:
            if model in view_name:
                return model

        return None

    message = "You do not have permission to perform this action."