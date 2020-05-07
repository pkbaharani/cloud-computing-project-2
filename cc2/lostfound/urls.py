from django.urls import path

from . import views

urlpatterns=[path('',views.home,name='Lost-Found-Home'),
             path('login/',views.login,name='Lost-Found-Login'),
             path('found/',views.found,name='Report any found item '),
             path('search/',views.search,name='Search general stuff'),
             path('sensitivesearch/',views.sensitive_search,name='Enter details to search for sensitve item'),
             path('validatecred/',views.validatecred,name='Search general stuff'),
             path('postgeneralitem/',views.post_general_item,name='new post item'),
             path('register/',views.register,name='new post item'),
             path('postsensitiveitem/',views.post_sensitive_item,name='new post item'),
             path('display_general_items/',views.display_general_items,name='new post item'),
             ]