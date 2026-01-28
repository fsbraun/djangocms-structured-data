from django.contrib import admin

from .models import TestModel


@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title",)
