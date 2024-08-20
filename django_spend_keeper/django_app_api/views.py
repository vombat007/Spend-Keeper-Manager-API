from django.db.models import Sum
from django.utils import timezone
from .utils import generate_jwt_token
from datetime import timedelta, datetime
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Account, Category, Transaction
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, AccountSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import TransactionSerializer, CategorySerializer, SavingSerializer
import cloudinary.api
import cloudinary.uploader


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_jwt_token(user)
            return Response(token)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountsListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = AccountSerializer

    def get_queryset(self):
        # Retrieve all Account instances associated with the authenticated user
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associate the authenticated user with the newly created Account instance
        serializer.save(user=self.request.user)


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        # Filter accounts based on the authenticated user and account ID
        return self.queryset.filter(user=self.request.user, id=self.kwargs['pk'])


class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        if not Account.objects.filter(user=user).exists():
            raise ValidationError("User must have at least one account to create a transaction.")

        # Check if datetime is provided; if not, use the current datetime
        datetime_value = serializer.validated_data.get('datetime', datetime.now())
        serializer.save(user=user, datetime=datetime_value)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_update(self, serializer):
        old_instance = self.get_object()
        old_amount = old_instance.amount

        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError({"detail": str(e)})

        new_instance = serializer.instance
        if old_instance.amount != new_instance.amount:
            new_instance.account.total_balance -= old_amount
            new_instance.account.save()

    def perform_destroy(self, instance):
        instance.delete()
        return Response({"detail": "Transaction deleted"}, status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class SavingCreateView(generics.CreateAPIView):
    serializer_class = SavingSerializer
    permission_classes = [IsAuthenticated]


class CloudinaryResourceList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Fetch resources recursively, including subfolders
            resources = []
            next_cursor = None
            while True:
                result = cloudinary.api.resources(
                    type='upload',
                    prefix='spend_keeper/all_category_icon/',
                    max_results=500,
                    next_cursor=next_cursor
                )
                resources.extend(result.get('resources', []))
                next_cursor = result.get('next_cursor')
                if not next_cursor:
                    break

            return Response({"resources": resources})
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class UploadIconView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=400)

        try:
            upload_result = cloudinary.uploader.upload(file, folder='spend_keeper/custom_category_icons/')
            return Response({"secure_url": upload_result.get("secure_url")}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class AccountSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, account_id):
        period = request.query_params.get('period')
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if not period and not start_date_str and not end_date_str:
            return Response({"error": "Please provide either period or start_date and end_date parameters."},
                            status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()

        if period:
            if period == 'day':
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = now
            elif period == 'week':
                start_date = now - timedelta(days=now.weekday())
                start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59)
            elif period == 'month':
                start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(seconds=1)
            elif period == 'year':
                start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                end_date = now
            else:
                return Response({"error": "Invalid period specified. Please use day, week, month, or year."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                start_date = (datetime.strptime(start_date_str, '%Y-%m-%d').replace
                              (hour=0, minute=0, second=0, microsecond=0))
                end_date = (datetime.strptime(end_date_str, '%Y-%m-%d').replace
                            (hour=23, minute=59, second=59, microsecond=999999))
                start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
                end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

            except ValueError:
                return Response({"error": "Invalid date format. Please use YYYY-MM-DD format."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Ensure the account belongs to the authenticated user
        account = Account.objects.filter(id=account_id, user=request.user).first()
        if not account:
            return Response({"error": "Account not found or does not belong to the user."},
                            status=status.HTTP_404_NOT_FOUND)

        transactions = Transaction.objects.filter(account=account, datetime__range=[start_date, end_date])

        income = transactions.filter(category__type='Income').aggregate(
            total_income=Sum('amount'))['total_income'] or 0
        expense = transactions.filter(category__type='Expense').aggregate(
            total_expense=Sum('amount'))['total_expense'] or 0

        if income != 0:
            percent_spent = (abs(expense) / income) * 100
        else:
            percent_spent = 0

        data = {
            'account_name': account.name,
            'total_balance': account.total_balance,
            'income': income,
            'expense': abs(expense),  # Ensure expense is positive for the response
            'percent_spent': round(percent_spent)
        }

        return Response(data)
