"""nitishopshpk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from nitishop.views import index, show_data, expense_page, total_page, add_data, statistics_page, settings_page, deletedata, suppliers, del_supplier, edit_supplier, storage, del_storage, edit_storage, reset_total


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('show_data/<int:year>/<int:month>', show_data, name='show_data'),
    path('expense/', expense_page, name='expense'),
    path('budget/', total_page, name='total'),
    path('add_data/', add_data, name='add_data'),
    path('statistics/', statistics_page, name='statistics_page'),
    path('settings/', settings_page, name='settings_page'),
    path('delete/<int:o_id>/', deletedata, name='delete'),
    path('suppliers/', suppliers, name='suppliers'),
    path('del_supplier/<int:o_id>/', del_supplier, name='del_supplier'),
    path('edit_supplier/<int:supp_id>/', edit_supplier, name='edit_supplier'),
    path('storage/', storage, name='storage'),
    path('del_storage/<int:p_id>/', del_storage, name='del_storage'),
    path('edit_storage/<int:s_id>', edit_storage, name='edit_storage'),
    path('reset/', reset_total, name='reset_total'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
