from django.urls import path
from .views import *

urlpatterns = [  #Aquí van los endpoints 
    path('groups/', GroupView.as_view(), name="grupos"),
    path('players/login', PlayerView.as_view(), name="login_player"),
    path('players_list/', PlayerListView.as_view(), name="players"),
    path('player/data/<int:pk>', PlayerDetailView.as_view(), name="player_data"),
    path('player/add', PlayerCreateView.as_view(), name="add_player"),
    path('player/update/<int:pk>', PlayerUpdateView.as_view(), name="edit_player"),
    path('player/delete/<int:pk>', PlayerDeleteView.as_view(), name="delete_player"),
    path('groups_list/', GrupoListView.as_view(), name="groups"),
    path('group/data/<int:pk>', GrupoDetailView.as_view(), name="group_data"),
    path('group/add', GrupoCreateView.as_view(), name="add_group"),
    path('group/update/<int:pk>', GrupoUpdateView.as_view(), name="edit_group"),
    path('group/delete/<int:pk>', GrupoDeleteView.as_view(), name="delete_group"),
    path('teachers/', TeacherView.as_view(), name="teachers"),
    path('teachers_list/', TeacherListView.as_view(), name="teachers"),
    path('teacher/data/<int:pk>', TeacherDetailView.as_view(), name="teacher_data"),
    path('teacher/add', TeacherCreateView.as_view(), name="add_teacher"),
    path('teacher/update/<int:pk>', TeacherUpdateView.as_view(), name="edit_teacher"),
    path('teacher/delete/<int:pk>', TeacherDeleteView.as_view(), name="delete_teacher"),
    path('sessions/', SessionView.as_view(), name="sessions"),
    path('', home, name="home"),
    path('index/', index, name="index"),
    path('global/chart/<int:pk>', chart, name="chart"),
    path('player/chart/<int:pk>', player_chart, name="player_chart"),
    path('player/scores/', ScoreView.as_view(), name="player_score"),
    path('gallery', Gallery, name="gallery"),
    path('administration/', adminHome, name="admin-home"),
    path('administration/register/', register_user, name="admin-register"),
    path('administration/logged_in/', adminAfterLogin, name="admin-a_login"),
    path('administration/logout/', logout_user, name="admin-logout"),
    path('teacher/home', teacherHome, name="teacher-home"),
    path('teacher/players', playersTView, name="players-T_view"),
    path('teacher/logged_in/', teacherAfterLogin, name="teacher-a_login"),
    path('teacher/logout/', logout_teacher, name="teacher-logout"),
    path('authT', authT, name= 'authenticationT' ),
    path('log/<int:pk>', log, name= 'log' ),
    path('player_a/<int:pk>', scoresp, name= 'player_a' ),
    path('auth', auth, name= 'authentication' )
]
