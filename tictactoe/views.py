from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import CustomUser
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Game
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import random
from account.serializers import UserSerializer
from .serializers import GameSerializer
from pusher import Pusher

pusher = Pusher(
    app_id=settings.PUSHER['APP_ID'],
    key=settings.PUSHER['KEY'],
    secret=settings.PUSHER['SECRET'],
    cluster=settings.PUSHER['CLUSTER'],
    ssl=settings.PUSHER['USE_SSL'],
)

# This generates a unique 5 digit gamecode when the user "create game" on the frontend
class StartGame(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        code = random.randint(10000, 99999)
        game = Game.objects.create(player_1_id=user_id, code=code)

        game_serializer = GameSerializer(game)
        return Response({'game': game_serializer.data})

# This is called when a user joins a game on the frontend by entering a game code
class JoinGame(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        code = request.data.get('code')

        game = get_object_or_404(Game, code=code)

        if game.player_2_id is not None:
            return Response({'message': 'Game is already full'}, status=400)

        game.player_2_id = user_id
        game.save()

        pusher.trigger(f'game_{game.id}', 'player.joined', {'message': 'Player Joined'})

        return Response({'message': 'Joined Successfully'})
    
# This is called when a player leaves a game or cancels a game on the frontend it sets the game inactive in the database
class SetGameInactive(APIView):
    def post(self, request, *args, **kwargs):
        game_id = request.data.get('id')

        try:
            game = Game.objects.get(id=game_id)
        except game.DoesNotExist: 
            return Response({'message': 'Game does not exist.'})
        
        game.active = False
        game.save()
        return Response({'message': 'Game Aborted.'})

    
# This is called every time a user makes a move on the tic tac toe board
class MakeMove(APIView): 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        game_id = request.data.get('id')
        index = request.data.get('index')

        game = get_object_or_404(Game, id=game_id)

        user1 = CustomUser.objects.get(id = game.player_1_id)
        user2 = CustomUser.objects.get(id = game.player_2_id)

        if game.winner_id:
            return

        if game.player_1_id == user_id:
            player_moves = game.player_1_moves.split(',')
            player_moves.append(str(index))
            game.player_1_moves = ','.join(player_moves)
            game.turn = 2
        else:
            player_moves = game.player_2_moves.split(',')
            player_moves.append(str(index))
            game.player_2_moves = ','.join(player_moves)
            game.turn = 1

        game.save()
        game_serializer = GameSerializer(game)
        
        pusher.trigger(f'game_{game.id}', 'player.moved', {'game': game_serializer.data})

        if winOrLose(game):
            game.winner_id = user_id
            game.save()
            if game.winner_id == user1.id:
                user1.wins +=1
                user2.losses += 1
            else:
                user2.wins += 1
                user1.losses += 1
            user1.save()
            user2.save()

            finalResults = {
                'winner': UserSerializer(CustomUser.objects.get(id=user_id)).data,
                'gameData': game_serializer.data
            }

            pusher.trigger(f'game_{game.id}', 'game.over', {'finalResults': finalResults})

            return Response({'message': 'Game Over'})

        if tie(game):
            user1.ties += 1 
            user2.ties += 1
            user1.save()
            user2.save()

            finalResults = {
                'tie': True,
                'gameData': game_serializer.data
            }
            pusher.trigger(f'game_{game.id}', 'game.over', {'finalResults': finalResults})

            return Response({'message': 'Game Over'})

        return Response({'message': 'Player Moved'})
    
# This is called for accessing information on the current game between two users
class CurrentGame(APIView):
    def get(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('id')

        try:
            game = Game.objects.get(Q(player_1_id=user_id) | Q(player_2_id=user_id), Q(active=True))
            game_serializer = GameSerializer(game)
            player1 = CustomUser.objects.get(id=game.player_1_id)
            player1_serializer = UserSerializer(player1).data
            player2 = CustomUser.objects.get(id=game.player_2_id)
            player2_serializer = UserSerializer(player2).data

            game_data = {
                'player1': player1_serializer,
                'player2': player2_serializer,
                'game': game_serializer.data
            }

            if game.winner_id:
                game_data['winner'] = UserSerializer(CustomUser.objects.get(id=game.winner_id)).data

            return Response({'gameData': game_data})
        except Game.DoesNotExist:
            return Response({'message': 'No Active Games'})

# This is a helper function for the "MakeMove" function it is used for determining when the game has resulted in a win or loss
def winOrLose(game):
    player_moves = (
        game.player_1_moves.split(',') if game.turn == 2
        else game.player_2_moves.split(',')
    )
    win_arrays = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6],
    ]

    for win_array in win_arrays:
        if all(str(element) in player_moves for element in win_array):
            return True
    return False

# This is a helper function for the "MakeMove" function it is used for determining when the game has resulted in a tie
def tie(game):
    player_moves = (
        game.player_1_moves.split(',')
    )
    if len(player_moves) == 6:
        return True



