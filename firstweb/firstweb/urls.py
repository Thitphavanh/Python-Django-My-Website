"""firstweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views


# include ແມ່ນ ການລິ້ງຄ໌ໂປຣເຄກັບແອພເຂົ້າກັນ
# path ແມ່ນ ການເຮັດໃຫ້ເວ໊ບໄຊຕ໌ເຮົາມີ url ຍ່ອຍ

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('myapp.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='myapp/logout.html'),name='logout'),
    # ແຖວເທິງນີ້ເປັນການເຮັດໃຫ້ໂປຣເຈຄລິ້ງຄ໌ກັບ urls ຂອງແອພ
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
