from django.urls import path
from .import views

#app_name='project1'

urlpatterns = [

    
    #path('', views.HomeView.as_view(), name="HomeView"),
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('product_list/', views.product_list, name="product_list"),
    
    path('<slug:category_slug>/', views.product_list, name="product_by_category"),
    # path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('add_to_cart/<int:id>/<slug>/', views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:id>/<slug>/', views.remove_from_cart, name="remove_from_cart"),
    path('remove_single_from_cart/<int:id>/<slug>/', views.remove_single_from_cart, name="remove_single_from_cart"),
    path('order_summary', views.OrderSummaryView.as_view(), name="order_summary"),
    path('<int:id>/<slug:slug>/', views.product_detail, name="product_detail"),
   # path('product_detail/<slug>/', views.product_detail.as_view(), name="product_detail"),
    path('base/', views.base, name="base"),
    
    
  
 
]

