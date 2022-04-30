from django.db import models

TYPE_CHOICES = (
    ("kitchen", "kitchen"),
    ("client", "client"),
)


class Printer(models.Model):

    name = models.CharField(max_length=250, verbose_name="Название принтера")
    api_key = models.CharField(
        max_length=250, verbose_name="Ключ доступа к API", unique=True
    )
    check_type = models.CharField(
        max_length=250,
        verbose_name="Тип чека которые печатает принтер",
        choices=TYPE_CHOICES,
    )
    point_id = models.CharField(
        max_length=250, verbose_name="Точка к которой привязан принтер"
    )

    class Meta:
        verbose_name = "Принтер"
        verbose_name_plural = "Принтеры"

    def __str__(self):
        return f"{self.name} / {self.point_id}"


class Check(models.Model):
    STATUS_CHOICES = (
        ("new", "new"),
        ("rendered", "rendered"),
        ("printed", "printed"),
    )
    printer_id = models.ForeignKey(
        Printer, verbose_name="Принтер", on_delete=models.CASCADE, related_name="checks"
    )
    type = models.CharField(
        max_length=250, verbose_name="Тип чека", choices=TYPE_CHOICES
    )
    order = models.JSONField(verbose_name="Информация о заказе")
    status = models.CharField(
        max_length=250,
        verbose_name="Статус чека",
        choices=STATUS_CHOICES,
        default="new",
    )
    pdf_file = models.FileField(
        verbose_name="Ссылка на созданный PDF-файл", upload_to="pdf/"
    )

    class Meta:
        verbose_name = "Чек"
        verbose_name_plural = "Чеки"

    def __str__(self):
        return f"{self.type} / {self.status} - {self.printer_id}"
