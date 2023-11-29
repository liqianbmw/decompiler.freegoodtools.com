from django.urls import path
from .views import LogInView
from authentication import views

app_name = 'accounts'
urlpatterns = [
    path('log-in/', LogInView.as_view(), name='log_in'),
    # path('log-out/', , name='log_out'),
    path('news-manager/',views.viewAllNews,name="news-manager"),
    path('news-detail/<str:title>',views.detailNews,name="news-detail"),
    path('news-update/',views.updateNews,name="news-update"),

]
