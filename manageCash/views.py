from django.shortcuts import render,redirect,get_object_or_404
from manageCash.forms import *
from manageCash.models import *
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def register_view(req):
    form_data = RegistrationForm()
    if req.method == "POST":
        form_data = RegistrationForm(req.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('login_view')

    context = {
            'form_data':form_data,
            'form_title':'Registration Form',
            'form_btn':'Register',
            'extra_link':'login_view',
            'extra_text':'Already have an account!',
            } 
    
    return render(req, 'master/baseform.html',context)

def login_view(req):
    form_data = AuthenticationForm()
    if req.method == 'POST':
        form_data = AuthenticationForm(req, data = req.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            if user:
                login(req,user)
                return redirect('dashboard_view')

    context = {'form_data':form_data,
               'form_title':'Please complete LOGIN with valid credentials',
                'form_btn':'Login',
                'extra_link':'register_view',
                'extra_text':'Dont have an account yet!',
                }

    return render(req, 'master/baseform.html',context)

@login_required
def expense_view(req):
    form_data = ExpenseForm()
    if req.method == "POST":
        form_data = ExpenseForm(req.POST)
        if form_data.is_valid():
            form_data.instance.user = req.user
            form_data.save()
            return redirect('dashboard_view')

    context = {
            'form_data':form_data,
            'form_title':'Add Expenses',
            'form_btn':'ADD'
            } 

    return render(req,'master/baseform.html',context)

@login_required
def addCash_view(req):
    form_data = AddCashForm()
    if req.method == "POST":
        form_data = AddCashForm(req.POST)
        if form_data.is_valid():
            form_data.instance.user = req.user
            form_data.save()
            return redirect('dashboard_view')

    context = {
            'form_data':form_data,
            'form_title':'Add Cash',
            'form_btn':'ADD'
            }

    return render(req,'master/baseform.html',context)

@login_required
def dashboard_view(req):

    cash_list = AddCashModel.objects.filter(user=req.user)
    expense_list = ExpenseModel.objects.filter(user=req.user)

    total_cash = 0
    for cash in cash_list:
        total_cash += cash.amount or 0

    total_expense = 0
    for expense in expense_list:
        total_expense += expense.amount or 0

    context={
        'total_cash': total_cash,
        'total_expense': total_expense,
        'balance':total_cash-total_expense,
        'cash_list':cash_list,
        'expense_list':expense_list,
    }
    return render(req,'dashboard.html',context)

def logout_view(req):
    logout(req)
    return redirect('login_view')


@login_required
def delete_view(req,id,model_input):
    model_type = {
        'cash' : AddCashModel,
        'expense' : ExpenseModel,
    }
    model = model_type.get(model_input)

    get_object_or_404(model,id=id,user=req.user).delete()
    return redirect('dashboard_view')

@login_required
def edit_view(req,id,model_input):
    model_type = {
        'cash' : AddCashModel,
        'expense' : ExpenseModel,
    }

    model= model_type.get(model_input)
    data = get_object_or_404(model,id=id,user=req.user)
    if model_input == 'cash':
        form_data = AddCashForm(instance=data)
        if req.method == "POST":
            form_data = AddCashForm(req.POST, instance=data)
            if form_data.is_valid():
                form_data.instance.user = req.user
                form_data.save()
                return redirect('dashboard_view')

        context = {
            'form_data': form_data,
            'form_title': 'Edit Cash',
            'form_btn': 'Update',
        }
    
    elif model_input == 'expense':
            form_data = ExpenseForm(instance=data)
            if req.method == "POST":
                form_data = ExpenseForm(req.POST, instance=data)
                if form_data.is_valid():
                    form_data.instance.user = req.user
                    form_data.save()
                    return redirect('dashboard_view')

            context = {
            'form_data': form_data,
            'form_title': 'Edit Expense',
            'form_btn': 'Edit',
        }



    return render(req,'master/baseform.html',context)