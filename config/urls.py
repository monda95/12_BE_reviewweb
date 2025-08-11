#config / urls.py

from django.contrib import admin
from django.urls import path, include
from config.schema import schema_view
from restaurants.urls import router as restaurants_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include(restaurants_router.urls)),
    path('', include('reviews.urls')),

    # swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]