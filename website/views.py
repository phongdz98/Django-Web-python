from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .form import SignUpForm, AddRecordForm, UpdateUserForm, PersonForm
from .models import Record, User, Person, Frame, Slot, SlotValue, Example


def home(request):
    if request.user.is_authenticated:
        records = Record.objects.all()
        # Check to see if logging in
        return render(request, 'home.html', {"records": records})
    else:
        messages.success(request, "You must be Logged In to View That Page!!!")
        return redirect('login')


# views for user
def watch_users(request):
    if request.user.is_authenticated:
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
    return render(request, 'user/login.html')


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


# views for person

def person_read(request):
    if request.user.is_authenticated:
        persons = Person.objects.all()
        # Check to see if logging in
        return render(request, 'person/persons.html', {"persons": persons})
    else:
        messages.success(request, "You must be Logged In to View That Page!!!")
        return redirect('login')


def add_person(request):
    form = PersonForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_per = form.save()
                messages.success(request, f"Person Added....")
                return redirect('person')
        return render(request, 'person/add_person.html', {'form': form})
    else:
        messages.success(request, f"You must be logged in....")
        return redirect('login')


# Dialog System

def frame_read(request):
    if request.user.is_authenticated:
        frames = Frame.objects.all()
        if request.method == 'POST':
            frame_name = request.POST.get('frame-name')
            if Frame.objects.filter(frame_name=frame_name).exists():
                messages.error(request, f"The frame '{frame_name}' already exists!")
            else:
                frame = Frame(frame_name=frame_name)
                frame.save()
                messages.success(request, f"Frame '{frame_name}' added successfully!")
            return redirect('frame')
        return render(request, 'dialog/frames.html', {"frames": frames})
    else:
        messages.success(request, "You must be Logged In to View That Page!!!")
        return redirect('login')


def frame_info(request, pk):
    if request.user.is_authenticated:
        current_frame = Frame.objects.get(id=pk)
        slots = Slot.objects.filter(frames=current_frame)
        examples = Example.objects.filter(frame=current_frame)
        return render(request, 'dialog/frame_info.html',
                      {'current_frame': current_frame, 'current_slots': slots, 'examples': examples})
    else:
        messages.success(request, "You must be Logged In to View That Page!!!")
        return redirect('home')


def delete_frame(request, pk):
    if request.user.is_authenticated:
        delete_fr = Frame.objects.get(id=pk)
        delete_fr.delete()
        messages.success(request, f"Frame Deleted Successfully ...")
        return redirect('frame')
    else:
        messages.success(request, "You must be Logged In to do that!!!")
        return redirect('login')


def slot_read(request):
    if request.user.is_authenticated:
        slots = Slot.objects.all()
        if request.method == 'POST':
            slot_name = request.POST.get('slot-name')
            slot = Slot(slot_name=slot_name)
            slot.save()
            messages.success(request, f"Slot Added....")
            return redirect('slot')
        return render(request, 'dialog/slots.html', {"slots": slots})
    else:
        messages.success(request, "You must be Logged In to View That Page!!!")
        return redirect('login')


def delete_slot(request, pk):
    if request.user.is_authenticated:
        delete_sl = Slot.objects.get(id=pk)
        delete_sl.delete()
        messages.success(request, f"Slot Deleted Successfully ...")
        return redirect('slot')
    else:
        messages.success(request, "You must be Logged In to do that!!!")
        return redirect('login')


def add_slots_to_frame(request, frame_id):
    frame = Frame.objects.get(id=frame_id)
    slots = Slot.objects.all()
    if request.method == 'POST':
        if 'add' in request.POST:
            # Lấy danh sách các slot được chọn từ form
            selected_slots = request.POST.getlist('selected_slots')
            # Thêm các slot được chọn vào frame
            for slot_id in selected_slots:
                slot = Slot.objects.get(id=slot_id)
                slot.frames.add(frame)
            return redirect('add_slots_to_frame', frame_id=frame_id)
        elif 'delete' in request.POST:
            # Lấy danh sách các slot được chọn từ form
            selected_slots = request.POST.getlist('selected_slots')
            # Xoa các slot được chọn neu co trong frame
            for slot_id in selected_slots:
                slot = Slot.objects.get(id=slot_id)
                slot.frames.remove(frame)
            return redirect('add_slots_to_frame',frame_id=frame_id)
    return render(request, 'dialog/add_slots_to_frame.html', {'frame': frame, 'slots': slots})


def add_slot_values(request, frame_id):
    frame = Frame.objects.get(id=frame_id)
    slots = Slot.objects.filter(frames=frame)
    examples = Example.objects.filter(frame=frame)

    if request.method == 'POST':
        for slot in slots:
            slot_value_name = request.POST.get('slot_value_{}'.format(slot.id))
            example = Example.objects.get(frame=frame, slot=slot)
            if slot_value_name:
                # Kiểm tra nếu example.slot_value không có giá trị, thì thêm mới SlotValue vào bảng SlotValue
                if not example.slot_value:
                    slot_value = SlotValue(value_name=slot_value_name, frame=frame, slot=slot)
                    slot_value.save()
                    example.slot_value = slot_value
                else:
                    # Nếu example.slot_value đã có giá trị, thì cập nhật lại giá trị mới
                    example.slot_value.value_name = slot_value_name
                    example.slot_value.save()
                example.save()
        return redirect('frame_info', pk=frame_id)
    return render(request, 'dialog/add_slot_values.html', {'frame': frame, 'slots': slots, 'examples': examples})


# Dialog for expert system

def start_dialog(request):
    # Đặt lại giá trị cho session  về 0
    request.session.update({
        'current_slot_index': 0,
        'current_slot_value_index': 0,
        'result': 0,
        'frame_answer': [],
        'dialogs': [],
        'view_question': 1
    })


# Lọc các giá trị của slot_value dựa trên frame_answer
def get_slot_values(slot, frame_answer):
    queryset = SlotValue.objects.filter(slot=slot)
    if frame_answer:
        queryset = queryset.filter(frame__frame_name__in=frame_answer)
    return queryset


def get_current_value_name(slot, frame_answer, current_slot_value_index):
    slot_values = get_slot_values(slot, frame_answer).order_by('value_name')
    value_names = slot_values.values_list('value_name', flat=True).distinct()
    value_name = value_names[current_slot_value_index]
    return value_names, value_name


def dialog_view(request):
    # Lấy giá trị của session
    current_slot_index = request.session.get('current_slot_index', 0)
    current_slot_value_index = request.session.get('current_slot_value_index', 0)
    result = request.session.get('result', 0)
    frame_answer = request.session.get('frame_answer', [])
    dialogs = request.session.get('dialogs', [])
    view_question = request.session.get('view_question', 0)

    # Lấy danh sách slots và slot hiện tại
    slots = Slot.objects.all()
    slot = slots[current_slot_index]

    # Lọc các giá trị của slot_value dựa trên frame_answer
    value_names, value_name = get_current_value_name(slot, frame_answer, current_slot_value_index)

    # Xử lý khi form được submit
    if request.method == 'POST':
        if 'start' in request.POST:
            # Nếu nhấn vào nút "Start", đặt lại giá trị cho session  về 0
            start_dialog(request)
            return redirect('dialog')
        if 'reset' in request.POST:
            request.session['view_question'] = 0
            return redirect('dialog')

        answer = request.POST['answer']
        # Lưu lại câu hỏi và câu trả lời nếu như chưa tìm ra được result
        if not result:
            dialog = {'slot_name': slot.slot_name, 'slot_value': value_name, 'answer': answer}
            dialogs.append(dialog)
        # Xử lí khi câu trả lời là Yes
        if answer == 'Yes':
            frame_answer = None
            # Khảo sát dialog để tìm frame phù hợp với dialog
            for dialog in dialogs:
                if dialog['answer'] == 'Yes':
                    examples = Example.objects.filter(Q(slot__slot_name=dialog['slot_name'])
                                                      & Q(slot_value__value_name=dialog['slot_value']))
                    # Nếu không tìm thấy examples phù hợp với dialog thì trả về không tìm thấy kết quả và thoát
                    # vòng lặp
                    if not examples:
                        result = 'Cant find data'
                        break
                    # Tìm thấy thì lưu vào biến frame_answer . Dùng intersection để  tìm giao 2 tập hợp
                    frames = set(examples.values_list('frame__frame_name', flat=True))
                    frame_answer = frames if frame_answer is None else frame_answer.intersection(frames)
            if not result:
                # Nếu chưa xét hết slot thì chuyển sang  slot tiếp theo
                if current_slot_index < len(slots) - 1:
                    current_slot_index += 1
                    slot = slots[current_slot_index]
                    current_slot_value_index = 0
                    frame_answer = list(frame_answer)
                    value_names, value_name = get_current_value_name(slot, frame_answer, current_slot_value_index)
                # Nếu đã xét hết slot thì đưa ra kết quả cuối cùng
                else:
                    result = ', '.join(list(frame_answer))

        # Xử lí khi câu trả lời là No
        elif answer == 'No' and not result:
            # Nếu chưa xét hết slot value thì chuyển sang  slot value tiếp theo
            if current_slot_value_index < len(value_names) - 1:
                current_slot_value_index += 1
                value_name = value_names[current_slot_value_index]
            # Nếu đã xét hết thì mà trả về không tìm thấy kết quả
            else:
                result = 'Cant find data'
    # Hiển thị kết quả
    question = f"{slot.slot_name} {value_name}"
    request.session.update({
        'current_slot_index': current_slot_index,
        'current_slot_value_index': current_slot_value_index,
        'result': result,
        'dialogs': dialogs,
        'frame_answer': list(frame_answer) if frame_answer is not None else []
    })
    predicted_results = ' or '.join(list(frame_answer))
    context = {
        'predicted_results': predicted_results,
        'dialogs': dialogs,
        'result': result,
        'question': question,
        'view_question':view_question
    }
    return render(request, 'dialog/dialog.html', context)
