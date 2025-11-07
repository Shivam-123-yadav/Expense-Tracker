from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from .models import Expense
from django.utils import timezone


def home(request):
    search = request.GET.get("search", "")
    filter_category = request.GET.get("category", "")

    expenses = Expense.objects.all().order_by("-created_at")

    # ✅ Search filter
    if search:
        expenses = expenses.filter(
            Q(descriptions__icontains=search) |
            Q(category__icontains=search)
        )

    # ✅ Category filter
    if filter_category:
        expenses = expenses.filter(category=filter_category)

    # ✅ Pagination
    paginator = Paginator(expenses, 5)  # 5 per page
    page_number = request.GET.get("page")
    expenses = paginator.get_page(page_number)

    # ✅ Monthly summary
    now = timezone.now()
    month_expense = Expense.objects.filter(
        created_at__year=now.year,
        created_at__month=now.month
    ).aggregate(Sum("amount"))["amount__sum"] or 0

    return render(request, "home.html", {
        "expenses": expenses,
        "total": month_expense,
        "search": search,
        "filter_category": filter_category
    })


def add_expense(request):
    if request.method == "POST":
        category = request.POST.get("category")
        amount = request.POST.get("amount")
        descriptions = request.POST.get("descriptions", "")

        Expense.objects.create(
            category=category,
            amount=amount,
            descriptions=descriptions or "",
        )
        return redirect("/")
    return redirect("/")



# ✅ Edit Expense
def edit_expense(request, id):
    exp = get_object_or_404(Expense, id=id)

    if request.method == "POST":
        exp.category = request.POST.get("category")
        exp.amount = request.POST.get("amount")
        exp.descriptions = request.POST.get("descriptions")
        exp.save()
        return redirect("/")

    return render(request, "edit.html", {"expense": exp})


# ✅ Delete Expense
def delete_expense(request, id):
    exp = get_object_or_404(Expense, id=id)
    exp.delete()
    return redirect("/")
