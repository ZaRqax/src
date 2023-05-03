from django.urls import (
    include,
    path,
)


urlpatterns = [
    path('token/', include('core.api.users.urls')),
    path('types/', include('core.api.types.urls')),
    path('entities/', include('core.api.entities.urls')),
]
