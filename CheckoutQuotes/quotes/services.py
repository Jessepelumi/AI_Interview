from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from .models import Coupon, Product

PENNY = Decimal("0.01")


@dataclass(frozen=True)
class Quote:
    subtotal: Decimal
    discount: Decimal
    total: Decimal


def build_quote(items, coupon_code=None):
    """Return a monetary quote for validated item dictionaries."""
    products = Product.objects.in_bulk(
        [item["sku"] for item in items], field_name="sku"
    )

    subtotal = sum(
        (products[item["sku"]].unit_price * item["quantity"] for item in items),
        start=Decimal("0.00"),
    )

    discount = Decimal("0.00")
    if coupon_code:
        coupon = Coupon.objects.filter(code=coupon_code, active=True).first()
        if coupon:
            discount = (
                subtotal * Decimal(coupon.percent_discount) / Decimal("100")
            ).quantize(PENNY, rounding=ROUND_HALF_UP)

    total = subtotal - discount
    return Quote(
        subtotal=subtotal.quantize(PENNY, rounding=ROUND_HALF_UP),
        discount=discount,
        total=total.quantize(PENNY, rounding=ROUND_HALF_UP),
    )

