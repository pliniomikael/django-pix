from django.db import models
from django.dispatch import receiver

from django.urls import reverse

from django.utils.translation import gettext as _


# Create your models here.
class Pix(models.Model):
    pixkey = models.CharField(_("Chave do PIX"), max_length=255)
    description = models.CharField(_("Descrição do Pagamento PIX"), max_length=255)
    merchant_name = models.CharField(_("Nome do Titular da Conta"), max_length=255)
    merchant_city = models.CharField(_("Nome da Cidade do Titular da Conta"), max_length=255)
    txid = models.CharField(_("ID da Transação"), max_length=255)
    amount = models.CharField(_("Valor da Transação"), max_length=255)


    class Meta:
        verbose_name = _("Pix")
        verbose_name_plural = _("Pixs")

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("pix_detail", kwargs={"pk": self.pk})
