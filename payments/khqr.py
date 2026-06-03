import base64
from decimal import Decimal, ROUND_HALF_UP
from io import BytesIO

import qrcode


def tlv(tag, value):
    value = str(value)
    return f"{tag}{len(value):02d}{value}"


def crc16_ccitt_false(payload):
    crc = 0xFFFF
    for byte in payload.encode("ascii"):
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return f"{crc:04X}"


def format_amount(amount):
    quantized = Decimal(amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{quantized:.2f}".rstrip("0").rstrip(".")


def build_khqr_payload(
    *,
    bakong_account_id,
    merchant_name,
    merchant_city,
    amount,
    bill_number,
    currency="840",
    mcc="7399",
):
    payload = "".join(
        [
            tlv("00", "01"),
            tlv("01", "12"),
            tlv("29", tlv("00", bakong_account_id)),
            tlv("52", mcc),
            tlv("53", currency),
            tlv("54", format_amount(amount)),
            tlv("58", "KH"),
            tlv("59", merchant_name[:25]),
            tlv("60", merchant_city[:15]),
            tlv("62", tlv("01", bill_number[:25])),
        ]
    )
    payload_for_crc = f"{payload}6304"
    return f"{payload_for_crc}{crc16_ccitt_false(payload_for_crc)}"


def qr_data_uri(payload):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    image = qr.make_image(fill_color="#020617", back_color="white")

    output = BytesIO()
    image.save(output, format="PNG")
    encoded = base64.b64encode(output.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"
