from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView # For Swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')), # Include your app's URLs

    # Swagger Documentation URLs [cite: 27, 28]
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), # Available at /swagger/
]