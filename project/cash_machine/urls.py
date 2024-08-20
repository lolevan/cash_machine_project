from django.urls import path
from .views import CashMachineView


urlpatterns = [
    path('', CashMachineView.as_view(), name='cash_machine'),
]
