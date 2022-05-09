from django.shortcuts import redirect,render
from tournament import models
from tournament.utils.md5 import md5

def tmp(request):
    return render(request,'tmp.html')
    
def doit(request):
    
    return redirect("/index")


def update_table():
    players = models.Participant.objects.all()
    for p in players:
        win = 0
        draw = 0
        lose = 0
        goal = 0
        goal_conceded = 0
        games = 0

        h = models.Game.objects.filter(home_id=p.id)
        a = models.Game.objects.filter(away_id=p.id)
        for game in h:
            games = games + 1
            goal = goal + game.home_goal
            goal_conceded = goal_conceded + game.away_goal
            if game.home_goal > game.away_goal:
                win = win + 1
            elif game.home_goal == game.away_goal:
                draw = draw + 1
            else:
                lose = lose + 1
        for game in a:
            games = games + 1
            goal = goal + game.away_goal
            goal_conceded = goal_conceded + game.home_goal
            if game.home_goal < game.away_goal:
                win = win + 1
            elif game.home_goal == game.away_goal:
                draw = draw + 1
            else:
                lose = lose + 1
        models.Participant.objects.filter(id=p.id).update(points=3*win+draw,games=games,wins=win,draws=draw,losts=lose,goals=goal,goals_conceded=goal_conceded)
    players = models.Participant.objects.all().order_by("-points")
    i = 1
    for p in players:
        models.Participant.objects.filter(id=p.id).update(current_rank=i)
        i = i + 1

def update_njcup_table():
    
    players = models.NewJourneyCup.objects.all()
    for p in players:
        win = 0
        draw = 0
        lose = 0
        goal = 0
        goal_conceded = 0
        games = 0

        h = models.Game.objects.filter(home_id=p.id,event=1)
        a = models.Game.objects.filter(away_id=p.id,event=1)
        for game in h:
            games = games + 1
            goal = goal + game.home_goal
            goal_conceded = goal_conceded + game.away_goal
            if game.home_goal > game.away_goal:
                win = win + 1
            elif game.home_goal == game.away_goal:
                draw = draw + 1
            else:
                lose = lose + 1
        for game in a:
            games = games + 1
            goal = goal + game.away_goal
            goal_conceded = goal_conceded + game.home_goal
            if game.home_goal < game.away_goal:
                win = win + 1
            elif game.home_goal == game.away_goal:
                draw = draw + 1
            else:
                lose = lose + 1
        models.NewJourneyCup.objects.filter(id=p.id).update(points=3*win+draw,games=games,wins=win,draws=draw,losts=lose,goals=goal,goals_conceded=goal_conceded)
    players = models.NewJourneyCup.objects.all().order_by("-points")
    i = 1
    for p in players:
        models.NewJourneyCup.objects.filter(id=p.id).update(current_rank=i)
        i = i + 1

def update_fakecup_table():
    players = models.FakeCup.objects.all()
    for p in players:
        win = 0
        draw = 0
        lose = 0
        goal = 0
        goal_conceded = 0
        games = 0

        h = models.Game.objects.filter(home_id=p.participant_id,event=2)
        a = models.Game.objects.filter(away_id=p.participant_id,event=2)
        for game in h:
            #print(game)
            games = games + 1
            goal = goal + game.home_goal
            goal_conceded = goal_conceded + game.away_goal
            if game.home_goal > game.away_goal:
                win = win + 1
            elif game.home_goal == game.away_goal:
                draw = draw + 1
            else:
                lose = lose + 1
        for game in a:
            #print(game)
            games = games + 1
            goal = goal + game.away_goal
            goal_conceded = goal_conceded + game.home_goal
            if game.home_goal < game.away_goal:
                win = win + 1
            elif game.home_goal == game.away_goal:
                draw = draw + 1
            else:
                lose = lose + 1
        models.FakeCup.objects.filter(participant_id=p.participant_id).update(points=3*win+draw,games=games,wins=win,draws=draw,losts=lose,goals=goal,goals_conceded=goal_conceded)
    players = models.FakeCup.objects.all().order_by("-points")
    i = 1
    for p in players:
        models.FakeCup.objects.filter(id=p.id).update(current_rank=i)
        i = i + 1

def update_pwd():
    players = models.Participant.objects.all()
    for p in players:
        old = p.password
        new = md5(old)
        models.Participant.objects.filter(id=p.id).update(password=new)