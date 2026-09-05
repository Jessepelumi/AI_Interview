from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import Membership, Organisation
from payments.models import Payment
from disputes.models import Dispute

class Command(BaseCommand):
    help = "Create deterministic demonstration records"
    def handle(self, *args, **options):
        user, _ = get_user_model().objects.get_or_create(username="agent", defaults={"email": "agent@example.test"})
        org, _ = Organisation.objects.get_or_create(processor_account_id="acct_demo", defaults={"name": "Demo Bikes Ltd"})
        Membership.objects.get_or_create(user=user, organisation=org, defaults={"role": Membership.Role.MANAGER})
        payment, _ = Payment.objects.get_or_create(processor_reference="pay_demo_1001", defaults={
            "organisation": org, "amount": Decimal("129.99"), "currency": "GBP",
            "captured_at": timezone.now() - timedelta(days=10), "refundable_amount": Decimal("129.99")})
        Dispute.objects.get_or_create(payment=payment, defaults={"organisation": org, "reason": "goods_not_received",
            "amount": Decimal("129.99"), "created_by": user, "response_due_at": timezone.now() + timedelta(days=7)})
        self.stdout.write(self.style.SUCCESS("Demo records ready; user: agent"))
