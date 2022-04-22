from django.db import models

# Create your models here.

class Participant(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(verbose_name="选手游戏ID",max_length=64)
    qq = models.CharField(verbose_name="QQ号",max_length=32)

    gender_choices = (
        (1,'男'),
        (2,'女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别',choices=gender_choices,default=1)

    type_of_team_choices = (
        (1,'队套'),
        (2,'传奇套'),
        (3,'非整套'),
    )
    type_of_team = models.SmallIntegerField(verbose_name='球队类型',choices=type_of_team_choices)

    highest_rank_choices = (
        (1,'青铜'),
        (2,'白银'),
        (3,'黄金'),
        (4,'钻石'),
        (5,'挑战者1'),
    )
    highest_rank = models.SmallIntegerField(verbose_name='单排历史最高段位',choices=highest_rank_choices,default=1)
    
    password = models.CharField(verbose_name="登录密码",max_length=64,default='111')



class Game(models.Model):
    def __str__(self):
        return self.home.name+self.away.name
    event_choices = (
        (1,"新旅程杯"),
        (2,"不存在的杯")
    )
    event = models.SmallIntegerField(verbose_name="赛事",choices=event_choices,default=1)
    game_date = models.DateField(verbose_name="比赛日期")
    home = models.ForeignKey(related_name='host',verbose_name='主队',to='Participant',to_field='id',on_delete= models.CASCADE)
    home_goal =models.SmallIntegerField(verbose_name='主队进球数')
    away = models.ForeignKey(related_name='away',verbose_name='客队',to='Participant',to_field='id',on_delete= models.CASCADE)
    away_goal =models.SmallIntegerField(verbose_name='客队进球数')

    


class Admin(models.Model):
    def  __str__(self):
        return self.username
    username = models.CharField(verbose_name='用户名',max_length=64)
    password = models.CharField(verbose_name='密码',max_length=64)


class NewJourneyCup(models.Model):
    def __str__(self):
        return ( "新旅程杯积分表"+  self.participant.name)
    participant = models.ForeignKey(verbose_name="参赛者",to='Participant',to_field='id',on_delete=models.CASCADE)
    points = models.SmallIntegerField(verbose_name="积分",default=0)
    wins = models.SmallIntegerField(verbose_name="胜场数",default=0)
    draws = models.SmallIntegerField(verbose_name="平场数",default=0)
    losts = models.SmallIntegerField(verbose_name="负场数",default=0)
    games = models.SmallIntegerField(verbose_name="比赛数",default=0)   
    goals = models.SmallIntegerField(verbose_name="进球数",default=0)
    goals_conceded = models.SmallIntegerField(verbose_name="失球数",default=0)
    current_rank = models.SmallIntegerField(verbose_name="排名",default=0)


class FakeCup(models.Model):
    def __str__(self):
        return ( "不存在的杯积分表"+  self.participant.name)
    participant = models.ForeignKey(verbose_name="参赛者",to='Participant',to_field='id',on_delete=models.CASCADE)
    points = models.SmallIntegerField(verbose_name="积分",default=0)
    wins = models.SmallIntegerField(verbose_name="胜场数",default=0)
    draws = models.SmallIntegerField(verbose_name="平场数",default=0)
    losts = models.SmallIntegerField(verbose_name="负场数",default=0)
    games = models.SmallIntegerField(verbose_name="比赛数",default=0)   
    goals = models.SmallIntegerField(verbose_name="进球数",default=0)
    goals_conceded = models.SmallIntegerField(verbose_name="失球数",default=0)
    current_rank = models.SmallIntegerField(verbose_name="排名",default=0)








#Admin.objects.create(username="gabi",password="50b0c8fea1fe9d4c5cdfdcbc8d3129e4")

'''
with open('D:\ol3杯赛\新旅程杯\计算积分榜\players.csv',encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for line in reader:
        #print(line)
        if line[1] == '队套':
            team_type = 1
        else:
            team_type = 2
        Participant.objects.create(name=line[0],type_of_team=team_type)

'''
'''
with open('D:\ol3杯赛\新旅程杯\计算积分榜\match.csv',encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for line in reader:
        #print(line)
        if line[0] == '':
            pass
        else:
            home = Participant.objects.filter(name=line[0]).first().id
            away = Participant.objects.filter(name=line[3]).first().id
            home_goal = line[1]
            away_goal = line[2]
            game_date = line[4] + '-' + line[5] + '-' +  line[6]
            Game.objects.create(game_date=game_date,host_id=home,away_id=away,home_goal=home_goal,away_goal=away_goal)
'''

