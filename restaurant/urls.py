from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),
    path('bookings', views.bookings, name='bookings'),
    path('', views.index, name='index'),

    path('api/menu/', views.MenuItemsView.as_view()),
    path('api/menu/<int:pk>', views.SingleMenuItemView.as_view()),

    path('api/book/', views.BookingView.as_view()),
    path('api/book/<int:pk>', views.SingleBookingView.as_view()),


    path('api-token-auth/', obtain_auth_token),
]
