from django.urls import path

from .views import (
    unit_detail,
    unit_list,
)


urlpatterns = [
    path('<int:pk>', unit_detail.UnitDetailApi.as_view(), name='units-detail'),
    path('', unit_list.UnitListView.as_view(), name='units-list'),
]
