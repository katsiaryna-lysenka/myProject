from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from core.views import ChoosePeriodView

schema_view = get_schema_view(
   openapi.Info(
      title="Young Specialists API",
      default_version='v1',
      description="API documentation for Young Specialists project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@youngspecialists.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('choose-period/', ChoosePeriodView.as_view(), name='choose_period')
]

