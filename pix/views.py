from django.shortcuts import render
from pix.models import Pix
from core.settings import (
    ID_PAYLOAD_FORMAT_INDICATOR, 
    ID_MERCHANT_ACCOUNT_INFORMATION, 
    ID_MERCHANT_ACCOUNT_INFORMATION_GUI,
    ID_MERCHANT_ACCOUNT_INFORMATION_KEY,
    ID_MERCHANT_ACCOUNT_INFORMATION_DESCRIPTION,
    ID_MERCHANT_CATEGORY_CODE,
    ID_TRANSACTION_CURRENCY,
    ID_TRANSACTION_AMOUNT,
    ID_COUNTRY_CODE,
    ID_MERCHANT_NAME,
    ID_MERCHANT_CITY,
    ID_ADDITIONAL_DATA_FIELD_TEMPLATE,
    ID_ADDITIONAL_DATA_FIELD_TEMPLATE_TXID,
    ID_CRC16,
    )
# Create your views here.
def tamanhot(desc, value):
    tamanho = len(("%s") % (value))
    if tamanho < 10:
        return ("%s0%s%s") % (desc, tamanho, value)
    return ("%s%s%s") % (desc, tamanho, value)

def tamanhotot(desc, value, value2, value3):
    tamanho = len(("%s%s%s") % (value, value2, value3))
    return ("%s%s%s%s%s") % (desc, tamanho, value, value2, value3)

#errando aqui#
def tex(desc, value):
    novo = tamanhot(ID_ADDITIONAL_DATA_FIELD_TEMPLATE_TXID, value)
    return ("%s") % (tamanhot(desc, novo))

def toHex(dec: float):
    digits = "0123456789ABCDEF"
    x = dec % 16
    rest = dec // 16
    if rest == 0:
        return digits[x]
    return toHex(rest) + digits[x]
     
def crc(value):
    new = ("%s%s%s") % (value, ID_CRC16, "04")
   
    crc = 0xFFFF
    for i in range(len(new)):
        crc ^= ord(new[i]) << 8
        for j in range(8):
            if (crc & 0x8000) > 0:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return "{}{}{}".format(ID_CRC16, "04", toHex(crc & 0xFFFF).upper())



def index(request, pk):
    pix = Pix.objects.get(id=pk)
    tamanho_id_payload = tamanhot(ID_PAYLOAD_FORMAT_INDICATOR, "01")

    merchant_gui = ("%s") % (tamanhot(ID_MERCHANT_ACCOUNT_INFORMATION_GUI, "br.gov.bcb.pix"))
    merchant_key = ("%s") % (tamanhot(ID_MERCHANT_ACCOUNT_INFORMATION_KEY, pix.pixkey))
    merchant_desc = ("%s") % (tamanhot(ID_MERCHANT_ACCOUNT_INFORMATION_DESCRIPTION, pix.description))
    merchant_pix_com = ("%s") % (tamanhotot(ID_MERCHANT_ACCOUNT_INFORMATION, merchant_gui, merchant_key, merchant_desc))
    merchant_category = ("%s") % (tamanhot(ID_MERCHANT_CATEGORY_CODE, "0000"))

    payload_pix = ("%s%s%s%s%s%s%s%s%s") % (tamanhot(ID_PAYLOAD_FORMAT_INDICATOR, "01"),
    merchant_pix_com, merchant_category, 
    tamanhot(ID_TRANSACTION_CURRENCY, "986"), 
    tamanhot(ID_TRANSACTION_AMOUNT, pix.amount),
    tamanhot(ID_COUNTRY_CODE, "BR"),
    tamanhot(ID_MERCHANT_NAME, pix.merchant_name),
    tamanhot(ID_MERCHANT_CITY, pix.merchant_city),
    tex(ID_ADDITIONAL_DATA_FIELD_TEMPLATE, pix.txid),
    )

    qrcode_pix = ("%s%s") % (payload_pix, crc(payload_pix))


    context = {
        "pix": pix,
        "payload_pix": payload_pix,
        "qrcode_pix": qrcode_pix,

    }
    return render(request, "index.html", context)
