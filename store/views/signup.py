from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View


class Signup (View):
    def get(self, request):
        return render (request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer (first_name=first_name,
                             last_name=last_name,
                             phone=phone,
                             email=email,
                             password=password)
        error_message = self.validateCustomer (customer)

        if not error_message:
            print (first_name, last_name, phone, email, password)
            customer.password = make_password (customer.password)
            customer.register ()
            return redirect ('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Пожалуйста введите имя"
        elif len (customer.first_name) < 3:
            error_message = 'Имя должно состоять не менее, чем из 3 символов'
        elif not customer.last_name:
            error_message = 'Пожалуйста введите фамилию'
        elif len (customer.last_name) < 3:
            error_message = 'Фамилия должно состоять не менее, чем из 3 символов'
        elif not customer.phone:
            error_message = 'Введите номер телефона'
        elif len (customer.phone) < 11:
            error_message = 'Номер телефона должен состоять из 11'
        elif len (customer.password) < 5:
            error_message = 'Пароль должен состоять не менее, чем из 3 символов'
        elif len (customer.email) < 5:
            error_message = 'Электронная почта должна состоять не менее, чем из 5 символов'
        elif customer.isExists ():
            error_message = 'Аккаунт с этой электронной почтой уже существует'

        return error_message
