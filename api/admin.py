from django.contrib import admin

from .models import Check, Printer


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "check_type",
        "point_id",
    )
    search_fields = (
        "name",
        "check_type",
        "point_id",
    )
    list_filter = (
        "name",
        "check_type",
        "point_id",
    )


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "printer_id",
        "type",
        "status",
    )
    search_fields = (
        "printer_id",
        "type",
        "status",
    )
    list_filter = (
        "printer_id",
        "type",
        "status",
    )
