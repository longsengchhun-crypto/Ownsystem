from django.test import SimpleTestCase

from .khqr import build_khqr_payload, crc16_ccitt_false, qr_data_uri


class KhqrPayloadTests(SimpleTestCase):
    def test_builds_dynamic_payload_with_valid_crc(self):
        payload = build_khqr_payload(
            bakong_account_id="merchant@aba",
            merchant_name="VANGUARD CREATIVE CO LTD",
            merchant_city="Phnom Penh",
            amount="125.50",
            bill_number="BK-12345",
        )

        self.assertIn("000201", payload)
        self.assertIn("010212", payload)
        self.assertIn("5303840", payload)
        self.assertIn("5405125.5", payload)
        self.assertIn("5802KH", payload)
        self.assertTrue(payload.endswith(crc16_ccitt_false(payload[:-4])))

    def test_qr_data_uri_returns_png_image(self):
        payload = build_khqr_payload(
            bakong_account_id="merchant@aba",
            merchant_name="VANGUARD CREATIVE CO LTD",
            merchant_city="Phnom Penh",
            amount="1.00",
            bill_number="BK-1",
        )

        self.assertTrue(qr_data_uri(payload).startswith("data:image/png;base64,"))

# Create your tests here.
