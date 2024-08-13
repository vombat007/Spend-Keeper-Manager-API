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
        {'name': 'Salary', 'type': Category.INCOME, 'icon': 'salary_icon.png'},
        {'name': 'Gifts', 'type': Category.INCOME, 'icon': 'gift_icon.png'},
        {'name': 'Other', 'type': Category.INCOME, 'icon': 'other_icon.png'},


        {'name': 'Groceries', 'type': Category.EXPENSE, 'icon': 'groceries_icon.png'},
        {'name': 'Haus', 'type': Category.EXPENSE, 'icon': 'house_icon.png'},
        {'name': 'Restaurant', 'type': Category.EXPENSE, 'icon': 'restaurant_icon.png'},
        {'name': 'Gifts', 'type': Category.EXPENSE, 'icon': 'gifts_icon.png'},
        {'name': 'Shopping', 'type': Category.EXPENSE, 'icon': 'shopping_icon.png'},
        {'name': 'Health', 'type': Category.EXPENSE, 'icon': 'health_icon.png'},
        {'name': 'Transport', 'type': Category.EXPENSE, 'icon': 'transport_icon.png'},
        {'name': 'Leisure', 'type': Category.EXPENSE, 'icon': 'leisure_icon.png'},
        {'name': 'Family', 'type': Category.EXPENSE, 'icon': 'family_icon.png'},
    ]

    for category_data in default_categories:
        Category.objects.create(user=user, **category_data)
