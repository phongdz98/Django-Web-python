from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .form import SignUpForm, AddRecordForm
from .models import Record


def home(request):
    if request.user.is_authenticated:
        records = Record.objects.all()
        # Check to see if logging in
        return render(request, 'home.html', {"records": records})
    else:
        messages.success(request, "You must be Logged In to View That Page!!!")
        return redirect('login')



def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_admin:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('admin')
        elif user is not None and user.is_technician:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('technician')
        elif user is not None and user.is_employee:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('employee')
        else:
            messages.success(request, "Error Logging In!")
            return redirect('login')
    return render(request, 'login.html')



def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged Out...")
    return redirect('login')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered!")
            return redirect('login')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def admin(request):
    return render(request, 'admin.html')


def technician(request):
    return render(request, 'technician.html')


def employee(request):
    return render(request, 'employee.html')


def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look Up Record
        cus_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'cus_record': cus_record})
    else:
        messages.success(request, "You must be Logged In to View That Page!!!")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_cus = Record.objects.get(id=pk)
        delete_cus.delete()
        messages.success(request, f"Record Deleted Successfully ...")
        return redirect('home')
    else:
        messages.success(request, "You must be Logged In to do that!!!")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_rec = form.save()
                messages.success(request, f"Record Added....")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, f"You must be logged in....")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,f'Record Has Been Updated!!!')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, f"You must be logged in....")
        return redirect('home')


