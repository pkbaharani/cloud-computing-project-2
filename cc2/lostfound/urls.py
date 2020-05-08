from django.urls import path

from . import views

urlpatterns=[path('',views.home,name='Lost-Found-Home'),
             path('login/',views.login_user,name='Lost-Found-Login'),
             path('logout/',views.logout_user,name='Lost-Found-Logout'),
             path('found/',views.found,name='Report any found item '),
             path('search/',views.search,name='Search general stuff'),
             path('sensitivesearch/',views.sensitive_search,name='Enter details to search for sensitve item'),
             path('validatecred/',views.validatecred,name='Search general stuff'),
             path('postgeneralitem/',views.post_general_item,name='new post item'),
             path('register/',views.register,name='new post item'),
             path('postsensitiveitem/',views.post_sensitive_item,name='new post item'),
             path('postlostsensitiveitem/',views.post_lost_sensitive_item,name='new post item'),
             path('display_general_items/',views.display_general_items,name='new post item'),
             path('display_general_lost_items/',views.display_general_lost_items,name='new post lost item'),
             path('resolve/',views.resolvePost,name='resolve post'),
             path('display_found_items/',views.display_general_items,name='new post item'),
             path('homepage/',views.homepage,name='Homepage of user'),
             path('postfounditem/', views.post_found_item, name=" Post generic or sensitive found document"),
             path('postlostitem/', views.post_lost_item, name=" Post generic or sensitive  lost document"),
             ]
