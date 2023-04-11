from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .form import SignUpForm, AddRecordForm, UpdateUserForm
from .models import Record, User


def home(request):
    if request.user.is_authenticated:
        records = Record.objects.all()
        # Check to see if logging in
        return render(request, 'home.html', {"records": records})
    else:
        messages.success(request, "You must be Logged In to View That Page!!!")
        return redirect('login')


def watch_users(request):
    if request.user.is_authenticated :
        if request.user.is_admin:
            users = User.objects.all()
            # Check to see if logging in
            return render(request, 'user/user.html', {"users": users})
        else:
            messages.success(request, "You do not have permission to access this page!")
            return redirect('employee')
    else:
        messages.success(request, "You must be Logged In to View That Page!!!")
        return redirect('login')


def customer_user(request, pk):
    if request.user.is_authenticated:
        # Look Up Record
        if request.user.is_admin:
            cus_user = User.objects.get(id=pk)
            return render(request, 'user/user_info.html', {'cus_user': cus_user})
        else:
            messages.success(request, "You do not have permission to access this page!")
            return redirect('employee')
    else:
        messages.success(request, "You must be Logged In to View That Page!!!")
        return redirect('login')


def delete_user(request, pk):
    if request.user.is_authenticated:
        if request.user.is_admin:
            delete_cus_user = User.objects.get(id=pk)
            delete_cus_user.delete()
            messages.success(request, f"User Deleted Successfully ...")
            return redirect('users')
        else:
            messages.success(request, "You do not have permission to access this page!")
            return redirect('employee')
    else:
        messages.success(request, "You must be Logged In to do that!!!")
        return redirect('login')


def update_user(request, pk):
    if request.user.is_authenticated:
        if request.user.is_admin:
            current_user = User.objects.get(id=pk)
            if request.method == 'POST':
                form = UpdateUserForm(request.POST, instance=current_user)
                # Kiểm tra giá trị của username có trùng lặp hay không
                if form.is_valid() and form.clean_username():
                    role = form.cleaned_data.get('role')
                    current_user = form.save(commit=False)
                    if role == 'is_admin':
                        current_user.is_admin = True
                        current_user.is_employee = False
                        current_user.is_technician = False
                    elif role == 'is_employee':
                        current_user.is_admin = False
                        current_user.is_employee = True
                        current_user.is_technician = False
                    elif role == 'is_technician':
                        current_user.is_admin = False
                        current_user.is_employee = False
                        current_user.is_technician = True

                    current_user.save()
                    messages.success(request, f'User Has Been Updated!!!')
                    return redirect('user_info', pk=current_user.id)
            else:
                form = UpdateUserForm(instance=current_user)
            return render(request, 'user/update_user.html', {'form': form, 'user_id': current_user.id})
        else:
            messages.success(request, "You do not have permission to access this page!")
            return redirect('employee')
    else:
        messages.success(request, f"You must be logged in....")
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
            return redirect('users')
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
    if request.user.is_authenticated:
        if request.user.is_admin:
            if request.method == "POST":
                form = SignUpForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    role = form.cleaned_data.get('role')  # Lấy giá trị của trường role từ form
                    if role == 'is_admin':
                        user.is_admin = True
                    elif role == 'is_employee':
                        user.is_employee = True
                    elif role == 'is_technician':
                        user.is_technician = True
                    user.save()
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password1']
                    user = authenticate(username=username, password=password)
                    messages.success(request, "You Have Successfully Add New User!")
                    return redirect('users')
            else:
                form = SignUpForm()
                return render(request, 'user/register.html', {'form': form})
        else:
            messages.success(request, "You do not have permission to access this page!")
            return redirect('employee')
    else:
        messages.success(request, f"You must be logged in....")
        return redirect('login')


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
            messages.success(request, f'Record Has Been Updated!!!')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, f"You must be logged in....")
        return redirect('home')
