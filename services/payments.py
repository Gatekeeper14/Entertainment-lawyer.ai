import stripe, os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

PRICE_MAP = {
    "basic": "price_basic",
    "pro": "price_pro",
    "elite": "price_elite"
}

def create_checkout(user_id, tier):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": PRICE_MAP[tier],
            "quantity": 1,
        }],
        mode="payment",
        success_url="https://t.me/Entertainment_Lawyer_bot",
        cancel_url="https://t.me/Entertainment_Lawyer_bot",
        metadata={"user_id": user_id}
    )
    return session.url
