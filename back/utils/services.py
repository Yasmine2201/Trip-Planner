from budget.models import ExpenseCategory
from visits.models import Location


class CategoryService:
    """
    this service is visible only for the admin
    """

    @staticmethod
    def create_category(name: str):
        category = ExpenseCategory.objects.create(name=name)
        category.save()
        return category

    @staticmethod
    def get_category(category_id: str):
        category = ExpenseCategory.objects.get(category_id=category_id)
        return category

    @staticmethod
    def get_all_categories():
        return ExpenseCategory.objects.all()

    @staticmethod
    def update_category(category_id: str, name: str):
        category = ExpenseCategory.objects.get(category_id=category_id)
        category.name = name
        category.save()
        return category

    @staticmethod
    def delete_category(category_id: str):
        category = ExpenseCategory.objects.get(category_id=category_id)
        category.delete()
        return category


class LocationService:
    @staticmethod
    def create_location(location_data: dict):
        location = Location.objects.create(**location_data)
        location.save()
        return location

    @staticmethod
    def get_all_locations():
        return Location.objects.all()
