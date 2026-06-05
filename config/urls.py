from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('hotel/', include('apps.hotel.urls')),
    path('reservations/', include('apps.reservations.urls')),
    path('restaurant/', include('apps.restaurant.urls')),
    path('kitchen/', include('apps.kitchen_display.urls')),
    path('billing/', include('apps.billing.urls')),
    path('accounting/', include('apps.accounting.urls')),
    path('crm/', include('apps.crm.urls')),
    path('housekeeping/', include('apps.housekeeping.urls')),
    path('hr/', include('apps.hr.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('ai/', include('apps.ai_services.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('branches/', include('apps.branches.urls')),
    path('inventory/', include('apps.inventory.urls')),        # ← added this line
    path('realtime/', include('apps.realtime.urls')),
    path('offline/', include('apps.offline.urls')),
    path('advanced/', include('apps.advanced_features.urls')),
    path('operations/', include('apps.operations.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)