from django.urls import path

from .views import (delete, home, logout_reqest, products, search, 
                    add_customer, business_overview, by_title, latest, 
                    latest_5, login, oldest, oldest_5, register, update, view
                    )
urlpatterns = [
    path('', register, name='register' ),
    path('home/',home, name='home'),
    path('register/', register, name='register' ),
    path('login/',login, name='login'),
    path('add-customer/',add_customer, name='add_customer'),
    path('latest/',latest, name='latest'),
    path('latest/5/',latest_5, name='latest_5'),
    path('oldest/', oldest, name='oldest'),
    path('oldest/5/',oldest_5, name="oldest_5"),
    path('bytitle/',by_title, name='bytitle'),
    path('business/overview/', business_overview, name="business_overview" ),
    path('search/<int:id>/', search, name='search' ),
    path('show/', products, name='name'),
    path('view/<int:id>/', view, name='view'),
    path('update/<int:id>/', update, name='update'),
    path('delete/<int:id>', delete, name='delete'),
    path('logout/', logout_reqest, name='logout')


]
