from pyexpat import model
from unittest import result
from django.db.models import F, Q,Avg,Max,Sum
from django.http import JsonResponse
from django.shortcuts import render
from tournament import models


def table(request):
    if request.GET.get("event") == '1':  
        players = models.NewJourneyCup.objects.all().order_by('-points')

        club_players = models.NewJourneyCup.objects.all().filter(participant__type_of_team=1).order_by('-points')
        i = 1
        club_rank = []
        for p in club_players:
            club_rank.append([i,p])
            i = i + 1
        
        legend_players = models.NewJourneyCup.objects.all().filter(participant__type_of_team=2).order_by('-points')
        legend_rank = []
        i = 1
        for p in legend_players:
            legend_rank.append([i,p])
            i = i + 1
        
        param_dict = {
        "players":players,
        'club_players':club_rank,
        'legend_players':legend_rank
        }
        return render(request,'table.html',param_dict)
    if request.GET.get("event") == '2':  
        players = models.FakeCup.objects.all().order_by('-points')
        param_dict = {
        "players":players,
        }
        return render(request,'table.html',param_dict)
    
def get_participant_stat():

    #计算所有选手的平均进失球数，aggregate(Avg()) 返回字典类型 {'goals__avg': 30.3158}
    avg_goal = models.NewJourneyCup.objects.aggregate(Avg('goals'))
    avg_goal_conceded = models.NewJourneyCup.objects.aggregate(Avg('goals_conceded'))
    max_game_count = models.NewJourneyCup.objects.aggregate(Max('games'))
    result = {
        'avg_goal':avg_goal['goals__avg'],
        'avg_goal_conceded':avg_goal_conceded['goals_conceded__avg'],
        'max_game_count':max_game_count['games__max']
        }

    return result
    

def participant_detail(request):

    #从URL中获取当前查看的选手的id
    pid = request.GET.get('pid')
    #根据选手id从数据库中筛选选手参加的比赛
    games = models.Game.objects.filter(Q(home_id=pid)|Q(away_id=pid))

    #主场场数
    home_games = games.filter(home_id=pid)
    home_game_count = len(home_games)

    #客场场数
    away_games = games.filter(away_id=pid)
    away_game_count = len(away_games)

    #主场
    home_wins = home_games.filter(home_goal__gt=F('away_goal'))     
    home_win_count = len(home_wins)
    home_win_rate = '{:.0%}'.format(home_win_count / home_game_count)
    home_goal_count = home_games.aggregate(Sum('home_goal'))['home_goal__sum']
    home_goal_conceded_count = home_games.aggregate(Sum('away_goal'))['away_goal__sum']
    home_clean_sheet_count = len(home_games.filter(away_goal=0))
    home_big_win_count = len(home_games.filter(home_goal__gte=F('away_goal')+3))
    home_slaughter_count = len(home_games.filter(home_goal__gte=F('away_goal')+5))
    
    #客场
    away_wins = away_games.filter(away_goal__gt=F('home_goal'))
    away_win_count = len(away_wins)
    away_win_rate = '{:.0%}'.format(away_win_count / away_game_count)
    away_goal_count = away_games.aggregate(Sum('away_goal'))['away_goal__sum']
    away_goal_conceded = away_games.aggregate(Sum('home_goal'))['home_goal__sum']
    away_clean_sheet_count = len(away_games.filter(home_goal=0))
    away_big_win_count = len(away_games.filter(away_goal__gte=F('home_goal')+3))
    away_slaughter_count = len(away_games.filter(away_goal__gte=F('home_goal')+5))


    details = [
        ['胜率',home_win_rate,away_win_rate],
        ['进球数',home_goal_count,away_goal_count],
        ['失球数',home_goal_conceded_count,away_goal_conceded],
        ['零封场数',home_clean_sheet_count,away_clean_sheet_count],
        ['净胜3+球场数',home_big_win_count,away_big_win_count],
        ['净胜5+球场数',home_slaughter_count,away_slaughter_count]
    ]
   
    param_dict = {
        "games":games,
        "home_games":home_games,
        'details':details,
    }

    return render(request,'participant_detail.html',param_dict)

def pdetail_bar_data(request):
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
    {
      'name': '胜',
      'type': 'bar',
      'stack': 'total',
      'label': {
        'show': 'true'
      },
      'emphasis': {
        'focus': 'series'
      },
      'data': [home_win_count+away_win_count,]
    },
    {
      'name': '平',
      'type': 'bar',
      'stack': 'total',
      'label': {
        'show':'true'
      },
      'emphasis': {
        'focus': 'series'
      },
      'data': [home_draw_count+away_draw_count,]
    },
    {
      'name': '负',
      'type': 'bar',
      'stack': 'total',
      'label': {
        'show':'true'
      },
      'emphasis': {
        'focus': 'series'
      },
      'data': [home_lose_count+away_lose_count,]
    },
    

  ]
    result = {
        "status":True,
        "data":db_data_list
    }
    return JsonResponse(result)


def pdetail_pie_data(request):
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

def pdetail_radar_data(request):
    pid = request.GET.get('pid')
    p = models.NewJourneyCup.objects.filter(participant=pid).first()
    name = models.Participant.objects.filter(id=pid).first().name
    #根据选手id从数据库中筛选选手参加的比赛
    games = models.Game.objects.filter(Q(home_id=pid)|Q(away_id=pid))
    begin_date = games.order_by('game_date').first().game_date
    finish_date = games.order_by('-game_date').first().game_date

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
    
    data_list = [{
        'name': 'hahahahha',
                'type': 'radar',
                'data': [
                    {
                    'value': [
                            (home_win_count + away_win_count) / game_count * 100,
                            p.goals / p.games * 30,
                            100 - p.goals_conceded / p.games * 10,
                            100 - abs((home_win_count/home_game_count-away_win_count/away_game_count)) * 100,
                            100-pow((finish_date-begin_date).days,1.1), 
                            p.games / get_participant_stat().get('max_game_count') * 100, 
                            ],
                    'name': '选手'
                    },  
                ]
    }]
    result = {  
                'status':True,
                'data':data_list
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
