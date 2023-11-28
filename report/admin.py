from django.contrib import admin
from .models import Laporan

@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):
    list_display = ['id', 'pelapor', 'terlapor', 'alasan', 'reviewed']