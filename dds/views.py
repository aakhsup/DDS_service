from django.db.models import Sum, Q
from django.shortcuts import render, redirect

from .models import Type, Category, Status, Subcategory, Transaction
from .forms import TransactionForm

def categories_list(request):
    categories = Category.objects.select_related('type')
    context = {'categories': categories}
    return render(request, 'dds/categories_list.html', context)

def transactions_list(request):
    transactions = Transaction.objects.select_related(
        'status', 'type', 'category', 'subcategory'
    ).order_by('-date')

    # --- Фильтры из GET-параметров ---
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status_id = request.GET.get('status')
    type_id = request.GET.get('type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    if status_id:
        transactions = transactions.filter(status_id=status_id)
    if type_id:
        transactions = transactions.filter(type_id=type_id)
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    if subcategory_id:
        transactions = transactions.filter(subcategory_id=subcategory_id)

    # --- Баланс по отфильтрованному набору (бонус остаётся) ---
    totals = transactions.aggregate(
        income=Sum('amount', filter=Q(type__name='Пополнение')),
        expense=Sum('amount', filter=Q(type__name='Списание')),
    )
    income = totals['income'] or 0
    expense = totals['expense'] or 0

    context = {
        'transactions': transactions,
        'income': income,
        'expense': expense,
        'balance': income - expense,
        # Справочники для выпадающих списков фильтра
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.select_related('type'),
        'subcategories': Subcategory.objects.select_related('category'),
        # Чтобы после фильтрации формы показывали выбранные значения
        'filters': {
            'date_from': date_from or '',
            'date_to': date_to or '',
            'status': status_id or '',
            'type': type_id or '',
            'category': category_id or '',
            'subcategory': subcategory_id or '',
        },
    }
    return render(request, 'dds/transactions_list.html', context)

def home(request):
    return render(request, 'dds/base.html')


def types_list(request):
    types = Type.objects.all()
    return render(request, 'dds/types_list.html', {'types': types})

def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transactions_list')
    else:
        form = TransactionForm()

    contex = {'form': form}
    return render(request, 'dds/transaction_create.html', contex)

