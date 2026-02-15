from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.accounts.serializers import AccountReadSerializer, AccountRegistrationSerializer, AccountUpdateSerializer
from api.accounts.services import AccountService


class AccountListCreateView(APIView):
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

class AccountDetailView(APIView):
    def get(self, request, pk):
        account = AccountService.retrieve_account(pk)

        serializer = AccountReadSerializer(account)
        return Response(serializer.data)

    def put(self, request, pk):
        account = AccountService.retrieve_account(pk)

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
        account = AccountService.retrieve_account(pk)
        AccountService.delete_account(account)

        return Response(status=status.HTTP_204_NO_CONTENT)