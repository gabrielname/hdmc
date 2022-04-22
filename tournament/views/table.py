from unittest import result
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import render
from tournament import models


def table(request):
    if request.GET.get("event") == '1':  
        players = models.NewJourneyCup.objects.all().order_by('-points')
        param_dict = {
        "players":players,
        }
        return render(request,'table.html',param_dict)
    if request.GET.get("event") == '2':  
        players = models.FakeCup.objects.all().order_by('-points')
        param_dict = {
        "players":players,
        }
        return render(request,'table.html',param_dict)
    
    
    

def participant_detail(request):

    #从URL中获取当前查看的选手的id
    pid = request.GET.get('pid')

    #根据选手id从数据库中筛选选手参加的比赛
    games = models.Game.objects.filter(Q(home_id=pid)|Q(away_id=pid))

    #主场比赛
    home_games = games.filter(home_id=pid)
   
    param_dict = {
        "games":games,
        "home_games":home_games,
    }

    return render(request,'participant_detail.html',param_dict)

def pdetail_data(request):
    pid = request.GET.get('pid')

    #根据选手id从数据库中筛选选手参加的比赛
    games = models.Game.objects.filter(Q(home_id=pid)|Q(away_id=pid))

    #比赛场数
    game_count =len(games)
    #主场场数
    home_games = games.filter(home_id=pid)
    home_game_count = len(home_games)
    #客场场数
    away_games = games.filter(away_id=pid)
    away_game_count = len(away_games)
    #主场胜、平、负
    home_wins = home_games.filter(home_goal__gt=F('away_goal'))     
    home_draws = home_games.filter(home_goal=F('away_goal'))
    home_loses = home_games.filter(home_goal__lt=F('away_goal'))
    home_win_count, home_draw_count, home_lose_count = len(home_wins),\
        len(home_draws), len(home_loses)
    home_win_rate, home_draw_rate, home_lose_rate =\
        home_win_count / home_game_count,\
        home_draw_count / home_game_count,\
        home_lose_count / home_game_count
    
    #客场胜、平、负
    away_wins = away_games.filter(away_goal__gt=F('home_goal'))
    away_draws = away_games.filter(away_goal=F('home_goal'))
    away_loses = away_games.filter(away_goal__lt=F('home_goal'))
    away_win_count, away_draw_count, away_lose_count = len(away_wins),\
        len(away_draws), len(away_loses)
    away_win_rate, away_draw_rate, away_lose_rate =\
        away_win_count / away_game_count,\
        away_draw_count / away_game_count,\
        away_lose_count / away_game_count

    db_data_list = [
        { "value": home_win_count + away_win_count, "name": '胜' },
        { "value": home_draw_count + away_draw_count, "name": '平' },
        { "value": home_lose_count + away_lose_count, "name": '负' },
    ]
    result = {
        "status":True,
        "data":db_data_list
    }
    return JsonResponse(result)



# #计算积分及得失球数据
    # players = models.Participant.objects.all()
    # for p in players:
    #     win = 0
    #     draw = 0
    #     lose = 0
    #     goal = 0
    #     goal_conceded = 0
    #     games = 0

    #     h = models.Game.objects.filter(home_id=p.id)
    #     a = models.Game.objects.filter(away_id=p.id)
    #     for game in h:
    #         games = games + 1
    #         goal = goal + game.home_goal
    #         goal_conceded = goal_conceded + game.away_goal
    #         if game.home_goal > game.away_goal:
    #             win = win + 1
    #         elif game.home_goal == game.away_goal:
    #             draw = draw + 1
    #         else:
    #             lose = lose + 1
    #     for game in a:
    #         games = games + 1
    #         goal = goal + game.away_goal
    #         goal_conceded = goal_conceded + game.home_goal
    #         if game.home_goal < game.away_goal:
    #             win = win + 1
    #         elif game.home_goal == game.away_goal:
    #             draw = draw + 1
    #         else:
    #             lose = lose + 1
    #     models.Participant.objects.filter(id=p.id).update(points=3*win+draw,games=games,wins=win,draws=draw,loses=lose,goals=goal,goals_conceded=goal_conceded)
