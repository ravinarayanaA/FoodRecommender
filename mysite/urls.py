from django.conf.urls import url


urlpatterns = [
	url(r"^(.*)home$", "mysite.views.get_name"),
	url(r"^(.*)about$", "mysite.views.about_view"),
     url(r"^(.*)$", "mysite.views.get_name"),
     url(r"^(.*)$", "mysite.views.static_view"),
    
   
]
