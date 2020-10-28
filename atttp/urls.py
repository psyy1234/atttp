from django.urls import path
from atttp import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

'''
home_list_view = views.HomeStatisticsView.as_view(
    queryset=GameDetail.objects.order_by("niz").order_by("igra_id")[:7],
    context_object_name="gamedet_list",
    template_name="atttp/home.html"
)
'''
'''
    path("", home, name="home"),
    path("challenge/", challenge, name='create_chall'),
    path('game/<int:pk>', views )
    path('game/create/', views.GameHeadCreate.as_view(), name = 'gamehead_create'),
    path("challenges/<str:head_id>/", manage_gamedetail, name='challenges'),
'''


app_name = 'atttp'

urlpatterns = [
    path('', login_required(views.StandingsTableView.as_view()), name='game_stats'),
	#path('game2/<int:pk>/', login_required(views.GameUpdateView.as_view()), name='game_detail2'),
    path('game/<int:pk>/', views.game_update, name='game_detail'),
    path('game/create/', login_required(views.GameCreate.as_view()), name='game_create'),
    #path('game/delete/<int:pk>/', login_required(views.GameDelete.as_view()), name='game_delete'),
    path('courts/', login_required(views.IgrisceDetail.as_view()), name='court_detail'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='atttp/login.html'), name='login'),
    path('game/create/ajax/get_users/', views.get_users_by_group, name='get_users_by_group'),
]