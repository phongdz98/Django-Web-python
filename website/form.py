from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from .models import Record, Person


# Form for user
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="First Name", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'First Name'}))
    last_name = forms.CharField(label="Last Name", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Last Name'}))

    ROLE_CHOICES = (
        ('is_admin', 'Admin'),
        ('is_employee', 'Employee'),
        ('is_technician', 'Technician'),
    )
    role = forms.ChoiceField(label='Role', choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = 'User Name'
        self.fields['username'].help_text = '<span class="form-text text-muted">' \
                                            '<small>Required. 150 characters or fewer. ' \
                                            'Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = 'Passsword 1'
        self.fields['password1'].help_text = '<ul class="form-text text-muted ' \
                                             'small"><li>Your password can\'t be' \
                                             ' too similar to your other personal' \
                                             ' information.</li><li>Your password' \
                                             ' must contain at least 8 characters.' \
                                             '</li><li>Your password can\'t be' \
                                             ' a commonly used password.</li>' \
                                             '<li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = 'Password 2'
        self.fields['password2'].help_text = '<span class="form-text' \
                                             ' text-muted"><small>Enter the same password' \
                                             ' as before, for verification.</small></span>'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="First Name", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'First Name'}))
    last_name = forms.CharField(label="Last Name", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Last Name'}))

    ROLE_CHOICES = (
        ('is_admin', 'Admin'),
        ('is_employee', 'Employee'),
        ('is_technician', 'Technician'),
    )
    role = forms.ChoiceField(label='Role', choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = 'User Name'
        self.fields['username'].help_text = '<span class="form-text text-muted">' \
                                            '<small>Required. 150 characters or fewer. ' \
                                            'Letters, digits and @/./+/-/_ only.</small></span>'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username


# Form for person
class PersonForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'First Name'}), label='First Name')
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'placeholder': 'Last Name'}), label='Last Name')
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Email'}), label='Email')
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Phone'}), label='Phone')
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Adress'}), label='Adress')
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'City'}), label='City')
    state = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'State'}), label='State')
    zipcode = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Zipcode'}), label='Zipcode')
    username = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                      label='Username')
    class Meta:
        model = Person
        fields = '__all__'


class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'First Name'}), label='')
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'placeholder': 'Last Name'}), label='')
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Email'}), label='')
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Phone'}), label='')
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Adress'}), label='')
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'City'}), label='')
    state = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'State'}), label='')
    zipcode = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Zipcode'}), label='')

    class Meta:
        model = Record
        exclude = ("user",)
