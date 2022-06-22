from django import forms
from django.contrib.auth.models import User
import random
from .models import Round


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        widgets = {'email':forms.EmailInput(attrs={'required':'true'})}

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = '__all__'

    def turn(self):
        """
        Рандомизируем выпадение чисел, сохраняем ход в БД
        """
        ordinary_numbers = [self.one, self.two,
                            self.three, self.four,
                            self.five, self.six,
                            self.seven, self.eight,
                            self.nine, self.ten]
        availible_numbers = list(filter(lambda x: x is not None, ordinary_numbers))
        if len(availible_numbers) == 0:
            self.jackpot = None
            self.save()
            return 'jackpot!'
        else:
            rolled_point = random.choice(availible_numbers)
            if rolled_point == 1:
                self.one = None
            elif rolled_point == 2:
                self.two = None
            elif rolled_point == 3:
                self.three = None
            elif rolled_point == 4:
                self.four = None
            elif rolled_point == 5:
                self.five = None
            elif rolled_point == 6:
                self.six = None
            elif rolled_point == 7:
                self.seven = None
            elif rolled_point == 8:
                self.eight = None
            elif rolled_point == 9:
                self.nine = None
            elif rolled_point == 10:
                self.ten = None
            self.save()
            return rolled_point


