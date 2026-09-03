from billing.models import Subscription
from plans.models import PlanFeature


def has_feature_access(customer, feature_code, as_of):
    try:
        subscription = customer.subscription
    except Subscription.DoesNotExist:
        return False
    if subscription.status != Subscription.Status.ACTIVE:
        return False
    if subscription.ends_on and as_of.date() > subscription.ends_on:
        return False
    return PlanFeature.objects.filter(
        plan=subscription.plan,
        feature__code=feature_code,
        enabled=True,
    ).exists()


def feature_limit(customer, feature_code):
    rule = PlanFeature.objects.get(
        plan=customer.subscription.plan, feature__code=feature_code, enabled=True
    )
    return rule.limit
