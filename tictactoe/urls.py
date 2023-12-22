from django.urls import path
from .views import JoinGame, SetGameInactive, StartGame, SetGameInactive, MakeMove, CurrentGame

urlpatterns = [
    path('start-game/', StartGame.as_view(), name='StartGame'),
    path('join-game/', JoinGame.as_view(), name='joinGame'),
    path('end-game/', SetGameInactive.as_view(), name='deleteGame'),
    path('make-move/', MakeMove.as_view(), name='makeMove'),
    path('current-game/', CurrentGame.as_view(), name='currentGame')
]