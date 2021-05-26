import pytest

from duffel_api.api import PaymentClient

from .fixtures import fixture


def test_create_payment(requests_mock):
    with fixture("create-payment", "/payments", requests_mock.post) as client:
        payment_details = {
            "type": "balance",
            "currency": "GBP",
            "amount": "30.20",
        }
        payment = (
            client.payments.create()
            .order_id("order-id")
            .payment(payment_details)
            .execute()
        )
        assert payment.id == "pay_00009hthhsUZ8W4LxQgkjo"
        assert payment.type == "balance"
        assert payment.amount == "30.20"
        assert payment.currency == "GBP"


def test_create_payment_with_invalid_payment_details(requests_mock):
    with fixture("create-payment", "/payments", requests_mock.post) as client:
        payment_details = {
            "currency": "GBP",
            "amount": "30.20",
        }
        payments_create_client = client.payments.create().order_id("order-id")
        with pytest.raises(
            PaymentClient.InvalidPayment,
            match="{'currency': 'GBP', 'amount': '30.20'}",
        ):
            payments_create_client.payment(payment_details).execute()
        payment_details["type"] = "credit"
        with pytest.raises(PaymentClient.InvalidPaymentType, match="credit"):
            payments_create_client.payment(payment_details).execute()
