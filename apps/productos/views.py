from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.utils import timezone

class ViandaAutocomplete(AutocompleteJsonView):
    def get_queryset(self):        
        qs = super().get_queryset()        
        today = timezone.now().date()
        return qs.filter(agenda__fechas__fecha=today)