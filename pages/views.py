from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Expense
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Expense, Budget
from django.db.models import Sum

def login_signup(request):
    return render(request, 'login_signup.html')

def handle_login(request):
    if request.method == 'POST':
        username = request.POST['login_username']
        password = request.POST['login_password']
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('dashboard')
    return redirect('login_signup')

def handle_signup(request):
    if request.method == 'POST':
        username = request.POST['signup_username']
        email = request.POST['signup_email']
        password1 = request.POST['signup_password1']
        password2 = request.POST['signup_password2']
        if password1 == password2:
            User.objects.create_user(username=username, email=email, password=password1)
            return redirect('login_signup')
    return redirect('login_signup')

@login_required
def dashboard(request):
    # Get the current budget (income)
    try:
        budget = Budget.objects.get(id=1)
        income = budget.amount
    except Budget.DoesNotExist:
        income = 0
    
    # Get the total spent amount
    spent = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get the remaining balance
    remaining = income - spent

    # Fetch all expenses
    expenses = Expense.objects.all()

    # Pass the data to the template
    return render(request, 'dashboard.html', {
        'income': income,
        'spent': spent,
        'remaining': remaining,
        'expenses': expenses,
    })



@csrf_exempt
@login_required

def log_expense(request):
    if request.method == 'POST':
        # Get the updated budget if provided
        new_budget = request.POST.get('monthly_income')
        
        if new_budget:
            # Update the monthly income budget
            Budget.objects.update_or_create(id=1, defaults={'amount': new_budget})
        
        # Log expense if data is provided
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        date = request.POST.get('date', timezone.now().date())
        
        if amount and category:
            Expense.objects.create(amount=amount, category=category, date=date)
        
        return redirect('dashboard')  # Redirect to the dashboard or where you want

    # Get the current budget value (or default to 0 if not set)
    try:
        budget = Budget.objects.get(id=1)
        monthly_income = budget.amount
    except Budget.DoesNotExist:
        monthly_income = 0

    categories = ['Food', 'Transport', 'Entertainment', 'Bills']  # Example categories
    return render(request, 'log_expense.html', {'monthly_income': monthly_income, 'categories': categories})
