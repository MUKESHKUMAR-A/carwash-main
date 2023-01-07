from django.urls import path
from . import views
from django.conf.urls import handler404

# add_place -> add_service
urlpatterns = [
    path('', views.welcomePage, name='welcome'),
    path('login', views.loginUser, name='login'),
    path('register', views.register, name='register'),
    path('homepage', views.homePage, name='home'),
    path('logout', views.logoutUser, name='logout'),
    path('showservices', views.showServices, name='showServices'),
    path('bookservice/<str:pk>',views.bookService, name='bookService'),
    path('showbookings', views.showBookings, name='showBookings'),
    path('admin_add_places', views.adminAddPlaces, name='admin_add_places'),
    path('admin_show_all_bookings', views.adminShowAllBookings, name='show_all_bookings'),
    path('admin_modify_status/<str:pk>/<str:status>', views.adminModifyStatus, name='admin_modify_status'),
]
handler404 = 'app.views.error_404_view'