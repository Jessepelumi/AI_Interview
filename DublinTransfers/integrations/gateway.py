class ClearingGateway:
    """Pure request builder used by the asynchronous clearing worker."""

    @staticmethod
    def build_payload(transfer):
        return {
            "reference": transfer.client_reference,
            "debtor_account": str(transfer.account_id),
            "creditor_iban": transfer.beneficiary.iban.replace(" ", "").upper(),
            "amount": f"{transfer.amount:.2f}",
            "currency": transfer.account.currency,
            "requested_execution_date": transfer.settlement_date.isoformat(),
        }
