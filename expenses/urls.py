from django.urls import path
from .views import home, add_expense, edit_expense, delete_expense

urlpatterns = [
    path("", home),
    path("add/", add_expense),
    path("edit/<int:id>", edit_expense),
    path("delete/<int:id>", delete_expense),
]
