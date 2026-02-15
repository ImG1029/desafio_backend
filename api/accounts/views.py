from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.accounts.permissions import IsAdminUser
from api.accounts.serializers import (
    AccountReadSerializer,
    AccountRegistrationSerializer,
    AccountUpdateSerializer,
    LoginSerializer
)
from api.accounts.services import AccountService


class AccountListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    def get(self, request):
        accounts = AccountService.list_accounts()
        serializer = AccountReadSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AccountRegistrationSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        account = AccountService.create_account(
            serializer.validated_data
        )

        output = AccountReadSerializer(account)
        return Response(
            output.data,
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, account = AccountService.authenticate_user(
            serializer.validated_data['username'],
            serializer.validated_data['password']
        )

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'account': AccountReadSerializer(account).data
        })

class AccountDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        account = AccountService.retrieve_account(pk)

        serializer = AccountReadSerializer(account)
        return Response(serializer.data)

    def put(self, request, pk):
        account = AccountService.retrieve_account(pk)

        if account.user != request.user and not request.user.is_superuser:
            return Response(
                {"detail": "You can only update your own account."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = AccountUpdateSerializer(
            instance=account,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        updated_account = AccountService.update_account(
            account,
            serializer.validated_data
        )

        output = AccountReadSerializer(updated_account)

        return Response(
            output.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        account = AccountService.retrieve_account(pk)

        if account.user != request.user and not request.user.is_superuser:
            return Response(
                {"detail": "You can only update your own account."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = AccountUpdateSerializer(
            instance=account,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_account = AccountService.update_account(
            account,
            serializer.validated_data
        )

        output = AccountReadSerializer(updated_account)

        return Response(
            output.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        if not request.user.is_superuser:
            return Response(
                {"detail": "Only administrators can delete accounts."},
                status=status.HTTP_403_FORBIDDEN
            )

        account = AccountService.retrieve_account(pk)
        AccountService.delete_account(account)

        return Response(status=status.HTTP_204_NO_CONTENT)


class PromoteToVeterinarianView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, pk):
        account = AccountService.retrieve_account(pk)

        license_number = request.data.get('license_number')
        if not license_number:
            return Response(
                {"detail": "license_number is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        account.license_number = license_number
        account.save()

        return Response({
            "message": f"User {account.user.username} promoted to veterinarian",
            "account": AccountReadSerializer(account).data
        })

    def delete(self, request, pk):
        account = AccountService.retrieve_account(pk)

        account.license_number = None
        account.save()

        return Response({
            "message": f"Veterinary privileges removed from {account.user.username}",
            "account": AccountReadSerializer(account).data
        })