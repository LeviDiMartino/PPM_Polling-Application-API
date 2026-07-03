from django.contrib import admin
from .models import Poll, Choice, Vote

# Definiamo come mostrare le Scelte "dentro" la pagina del Sondaggio
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # Mostra 3 spazi vuoti pronti per essere compilati

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['question', 'created_by', 'created_at']
    # Agganciamo le scelte direttamente qui!
    inlines = [ChoiceInline]

# Registriamo gli altri modelli normalmente
admin.site.register(Choice)
admin.site.register(Vote)