from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def fill_extra_fields(request, user, **kwargs):
    """
    ده بيتنادى أوتوماتيك أول ما اليوزر يتسجل بجوجل أو أي social account.
    """
    # لو role فاضي → نحط default
    if not user.role:
        user.role = "kid"  # ممكن تخليها parent لو عايزة
        user.save()