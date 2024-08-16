from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category


def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

    return token


def create_default_categories(user):
    default_categories = [
        {'name': 'Salary', 'type': Category.INCOME, 'icon': 'spend_keeper/income/salary_icon'},
        {'name': 'Gifts', 'type': Category.INCOME, 'icon': 'spend_keeper/income/gift_icon'},
        {'name': 'Other', 'type': Category.INCOME, 'icon': 'spend_keeper/income/other_icon'},

        {'name': 'Groceries', 'type': Category.EXPENSE, 'icon': 'spend_keeper/expense/groceries_icon'},
        {'name': 'House', 'type': Category.EXPENSE, 'icon': 'spend_keeper/expense/house_icon'},
        {'name': 'Restaurant', 'type': Category.EXPENSE, 'icon': 'spend_keeper/expense/restaurant_icon'},
        {'name': 'Gifts', 'type': Category.EXPENSE, 'icon': 'spend_keeper/expense/gifts_icon'},
        {'name': 'Shopping', 'type': Category.EXPENSE, 'icon': 'spend_keeper/expense/shopping_icon'},
        {'name': 'Health', 'type': Category.EXPENSE, 'icon': 'spend_keeper/expense/health_icon'},
        {'name': 'Transport', 'type': Category.EXPENSE, 'icon': 'spend_keeper/expense/transport_icon'},
        {'name': 'Leisure', 'type': Category.EXPENSE, 'icon': 'spend_keeper/expense/leisure_icon'},
        {'name': 'Family', 'type': Category.EXPENSE, 'icon': 'spend_keeper/expense/family_icon'},
    ]

    for category_data in default_categories:
        Category.objects.create(user=user, **category_data)
