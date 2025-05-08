from django.urls import path
from myapp import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index),
    path('login', views.userLogin),
    path('register',views.register),
    path('details/<petid>', views.getPetById),
    path('logout',views.userlogout),
    path('filter-by-cat/<catName>',views.filterByCategory),
    path('sort-by-price/<direction>', views.sortByPrice),
    path('filter-by-range',views.filterByrange),
    path('addtocart/<petid>',views.addTocart),
    path('showmycart',views.showMycart),
    path('removecart/<cartid>',views.removeCart),
    path('updatequantity/<cartid>/<operation>', views.updateQuantity),
    path('confirmorder',views.confirmOrder),
    path('makepayment',views.makepayment),
    path('contact',views.contact),
    path('placeorder',views.placeOrder)

]


urlpatterns += static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)