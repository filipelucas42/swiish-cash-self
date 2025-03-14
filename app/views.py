from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout
from app.models import User, Wallet, OTP, LoginUserID
from app import service
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import AccessMixin
from functools import wraps

def login_required_with_redirect(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('http://127.0.0.1:3000')  # Change 'home' to your desired URL name
        return view_func(request, *args, **kwargs)
    return wrapper
class LoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and has required permissions."""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('http://127.0.0.1:3000')  # Change 'home' to your desired URL name
        return super().dispatch(request, *args, **kwargs)
    
class CustomView(View, LoginRequiredMixin):
    http_method_names = ['get', 'post', 'put', 'delete', 'patch']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('__method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(CustomView, self).dispatch(*args, **kwargs)

@login_required_with_redirect
def home(request):
    if request.user.is_authenticated:
        return redirect('send')
    return render(request, 'app/home.html')

@login_required_with_redirect
def sendtest(request):
    return render(request, 'app/sendtest.html')

@login_required_with_redirect
def send_transaction(request):
    user = request.user
    value = request.POST.get('value')
    recipient = request.POST.get('recipient')

    wallet_from = Wallet.objects.get(user=user)

    if recipient.startswith("+"):
        wallet_to = Wallet.objects.get(user__handle=recipient)
        print("Wallet to: ", wallet_to.address)
        address = wallet_to.address
    else:
        address = recipient
    service.send_transaction(wallet_from.address, address, value, wallet_from.private_key)
    context = {}
    context["amount"] = value
    context["recipient"] = recipient
    return render(request, 'app/confirmTransfer.html', context)

@login_required_with_redirect
def confirm(request):
    user = request.user
    value = request.POST.get('value')
    phone_number = request.POST.get('passport_number')
    country_code = request.POST.get('country_code')
    handle = f'{country_code}{phone_number}'
    address = request.POST.get('address')
    if address == "":
        recipient = handle
        try:
            user_to_send = User.objects.get(handle=handle)
        except ObjectDoesNotExist:
            user_to_send = service.create_user(handle)

        wallet_to = Wallet.objects.get(user=user_to_send)
        address = wallet_to.address
    else:
        recipient = address
    wallet_from = Wallet.objects.get(user=user)
    gas_estimate = service.estimate_gas_for_transfer(wallet_from.address, address, value)
    context = {}
    context["value"] = value
    context["gas"] = gas_estimate["total_cost_avax"]
    context["recipient"] = recipient
    return render(request, 'app/confirm.html', context)

@login_required_with_redirect
def send(request):
    context = {}
    country_list = [
        ("+1", "US"), ("+351", "PT"), ("+44", "GB"), ("+55", "BR"),
        ("+33", "FR"), ("+49", "DE"), ("+81", "JP"), ("+91", "IN"),
        ("+61", "AU"), ("+86", "CN"), ("+34", "ES"), ("+7", "RU"),
        ("+39", "IT"), ("+82", "KR"), ("+90", "TR"), ("+964", "IQ"),
    ]
    
    context["country_list"] = country_list
        
    if request.user.is_authenticated:
        wallet = Wallet.objects.get(user=request.user)
        wallet_balance = service.get_balance(wallet.address)
        context["wallet_balance"] =  wallet_balance
    return render(request, 'app/send.html', context)

@login_required_with_redirect
def history(request):
    return render(request, 'app/history.html')

@login_required_with_redirect
def page(request):
    return render(request, "app/page1.html")

@login_required_with_redirect
def index(request):
    response = render(request, 'app/index.html')
    return response

@login_required_with_redirect
def logout_handler(request):
    logout(request)
    return redirect('home')

def self(request):
    return HttpResponse(request.body)

@login_required_with_redirect
def confirm_transfer(request):
    response = render(request, 'app/confirmTransfer.html')
    return response
@method_decorator(csrf_exempt, name='dispatch')
class Login(CustomView):
    def get(self, request):
        user_uuid = request.GET.get('user_uuid')
        login_user_id = LoginUserID.objects.filter(user_uuid=user_uuid).first()
        user = login_user_id.user
        login_user_id.delete()
        login(request, user)
        return redirect('send')
        
    def delete(self, request):
        logout(request)
        return redirect('home')

@method_decorator(csrf_exempt, name='dispatch')
class CreateLogin(CustomView):
    def post(self, request):
        country = request.POST.get('country')
        passport_number = request.POST.get('passport_number').strip("<")
        user_id = request.POST.get('user_id')
        handle = country + passport_number
        try:
            user = User.objects.get(handle=handle)
        except ObjectDoesNotExist:
            user = service.create_user(handle)
        LoginUserID.objects.create(user_uuid=user_id, user=user)
        return HttpResponse("OK")
        