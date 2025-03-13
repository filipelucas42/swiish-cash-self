from django import template
from app.models import Wallet
register = template.Library()

@register.simple_tag(takes_context=True)
def user_address(context):
    request = context['request']
    user = request.user
    if user.is_authenticated:
        wallet = Wallet.objects.get(user=user)
        return wallet.address