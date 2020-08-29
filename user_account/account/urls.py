from django.conf.urls import url
from account import views
# SET THE NAMESPACE!
app_name = 'account'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^signup/$',views.register,name='signup'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^user_login/delete_user',views.delete_user,name='delete_user'),
]