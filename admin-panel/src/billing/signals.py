import stripe
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.conf import settings

from billing.models import Subscription

stripe.api_key = settings.STRIPE_API_KEY


@receiver(post_save, sender=Subscription)
def create_product_price_stripe(sender, instance, **kwargs):
    subscription = stripe.Product.create(
        name=instance.name,
        description=instance.description,
        default_price_data={
            "currency": "USD",
            "unit_amount": instance.cost * 100,
        },

    )
    post_save.disconnect(create_product_price_stripe, sender=sender)
    instance.payment_gw_product_id = subscription.id
    instance.payment_gw_price_id = subscription.default_price
    instance.save()
    post_save.connect(create_product_price_stripe, sender=sender)
