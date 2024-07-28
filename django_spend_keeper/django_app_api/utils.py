from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category, User


def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

    return token


def create_default_categories(user):
    default_categories = [
        {'name': 'Salary', 'type': Category.INCOME, 'description':
            'Income from salary.', 'icon': 'salary_icon.png'},
        {'name': 'Gifts', 'type': Category.INCOME, 'description':
            'Income from gifts.', 'icon': 'gift_icon.png'},
        {'name': 'Other', 'type': Category.INCOME, 'description':
            'Income from other.', 'icon': 'other_icon.png'},

        {'name': 'Groceries', 'type': Category.EXPENSE, 'description':
            'Expenses on groceries.', 'icon': 'groceries_icon.png'},
        {'name': 'Haus', 'type': Category.EXPENSE, 'description':
            'Expenses on haus.', 'icon': 'house_icon.png'},
        {'name': 'Restaurant', 'type': Category.EXPENSE, 'description':
            'Expenses on restaurant.', 'icon': 'restaurant_icon.png'},
        {'name': 'Gifts', 'type': Category.EXPENSE, 'description':
            'Expenses on gifts.', 'icon': 'gifts_icon.png'},
        {'name': 'Shopping', 'type': Category.EXPENSE, 'description':
            'Expenses on shopping.', 'icon': 'shopping_icon.png'},
        {'name': 'Health', 'type': Category.EXPENSE, 'description':
            'Expenses on health.', 'icon': 'health_icon.png'},
        {'name': 'Transport', 'type': Category.EXPENSE, 'description':
            'Expenses on transport.', 'icon': 'transport_icon.png'},
        {'name': 'Leisure', 'type': Category.EXPENSE, 'description':
            'Expenses on leisure.', 'icon': 'leisure_icon.png'},
        {'name': 'Family', 'type': Category.EXPENSE, 'description':
            'Expenses on family.', 'icon': 'family_icon.png'},
    ]

    for category_data in default_categories:
        Category.objects.create(user=user, **category_data)
