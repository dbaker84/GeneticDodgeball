__author__ = 'Daniel Baker'

# TODO:
#
# Nicknames
# New targeting algorithm
# Add speed/turn order
# Add team creation
# Add time/calender system


from tkinter import *
import random
import statistics
import operator
import math
import csv
from tkinter import font


root = Tk()
root.geometry("1600x900")
root.wm_title("Genetic Dodgeball")
root.resizable(width=FALSE, height=FALSE)


freeagents = []
freedoctors = []
freetrainers = []
freescouts = []
teams = []
cities = []
usednames = []
curnum = 1

calendars = []



# GAME BEHAVIOR CONSTANTS
#     Use these to modify game behavior
#     Default values commented below

# global variables for decoding genomes
posfactor = 4
divfactor = 4.5
negfactor = 20
salaryfactor = 4

# staff constants
staffsalary = 1000
doctorfactor = 5.0
trainerfactor = 3.0
scoutfactor = 3.0

# END BEHAVIOR CONSTANTS


# randomize what genes control which attributes
skills = ["dodge", "catch", "tpower", "taccuracy", "stamina", "tricky", "awareness", "tactics", "pconsist", "mconsist",
          "leadership", "flair", "speed", "clutch", "deflection", "ego", "confidence", "nerves", "workethic",
          "charisma", "unused", "patience", "ethics", "winner"]

stats = []

stronggenes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z']
weakgenes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z']
contragenes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z']

for skill in skills:
    genes = [random.randrange(0, len(stronggenes)), random.randrange(0, len(weakgenes)), random.randrange(0, len(contragenes))]
    stats.append([skill, stronggenes.pop(genes[0]), weakgenes.pop(genes[1]), contragenes.pop(genes[2])])



geneseq = "ABCDEFGHJKLMNOPQRSTUWXYZ"

# stats to track
season_stat_list = [
        "season_throws",
        "season_dodge_fail",
        "season_catch_fail",
        "season_deflect_fail",
        "season_dodge_succ",
        "season_catch_succ",
        "season_deflect_succ",
        "season_hits",
        "season_misses",
        "season_wasdodged",
        "season_wascaught",
        "season_blindsided",
        "season_assassinations",
        "season_wins",
        "season_losses"]


def all_the_players():
    for team in teams:
        for player in team.roster:
            yield player


def best_player(stat_name):
    return max(all_the_players(), key=operator.attrgetter(stat_name))


sclamp = lambda n: round(max(min(100, n), 1))

class Date:
    def __init__(self, day=1, week=1, year=None):
        self.day = day
        self.week = week
        self.year = year

    def inc(self, num=1):
        self.day += num
        if self.day > 7:
            self.week += 1
            self.day %= 7

        date_box.config(text="Week %s    Day %s    Year %s" % (global_date.week, global_date.day, global_date.year))
global_date = Date(1, 1, 2000 + int(random.uniform(100, 20)))

class Matchup:
    def __init__(self, home, away, date, winner=None):
        self.home = home
        self.away = away
        self.date = date
        self.winner = winner


class Calendar:
    def __init__(self, year):
        self.year = year
        self.matches = []


class Team:
    def __init__(self, city, name, roster):
        self.name = name
        self.city = city
        self.roster = roster
        self.fullname = city.name + " " + name
        self.id = hash(self.fullname) % 100000000
        
        # Staff Positions
        self.doctor = freedoctors.pop(random.randint(0, len(freedoctors)-1))
        self.trainer = freetrainers.pop(random.randint(0, len(freetrainers)-1))
        self.scout = freescouts.pop(random.randint(0, len(freescouts)-1))

        self.alltime_wins = 0
        self.alltime_losses = 0
        self.alltime_winpercentage = 0.000

        self.wins = 0
        self.losses = 0
        self.winpercentage = 0.000

        self.active = True

    def salary(self):
        salary = 0
        for player in self.roster:
            salary += player.salary
        return salary

    def operating_costs(self):
        return None

    def offrating(self):
        troster = []
        for x in self.roster:
            troster.append(x.offense)
        return round(statistics.mean(troster))

    # dynamic ratings calculations

    def defrating(self):
        troster = []
        for x in self.roster:
            troster.append(x.defense)
        return round(statistics.mean(troster))

    def playersleft(self):
        ticker = 0
        for x in self.roster:
            if x.ingame:
                ticker += 1
        return ticker

    def winpercent(self):
        if self.losses == 0:
            x = 1.000
        else:
            x = round(self.wins/(self.wins + self.losses), 3)
        self.winpercentage = x

    def alltime_winpercent(self):
        if self.alltime_losses == 0:
            x = 1.000
        else:
            x = round(self.alltime_wins/(self.alltime_wins + self.alltime_losses), 3)
        self.alltime_winpercentage = x
        
    def win(self):
        self.wins += 1
        self.alltime_wins += 1

    def loss(self):
        self.losses += 1
        self.alltime_losses += 1


class Stadium:
    def __init__(self, name, seats, ticket_price, box_price):
        self.name = name
        self.seats = seats
        self.ticket_price = ticket_price
        self.box_price = box_price


class City:
    def __init__(self, name, country, unique_factor, fans, rabidity, loyalty, avg_income):
        self.name = name
        self.country = country
        self.unique_factor = unique_factor
        self.fans = fans
        self.rabidity = rabidity
        self.loyalty = loyalty
        self.avg_income = avg_income

        self.stadium = None

        self.appeal = int(self.unique_factor * self.fans * self.rabidity * self.loyalty * self.avg_income)

    def recalc_city(self):
        self.appeal = int(self.rabidity * self.population * self.avg_income)


class Player:
    def __init__(self, name, number, genome):
        holder = name.split()
        self.formalname = name
        self.firstname = holder[0]
        self.lastname = holder[1]
        self.fullname = name
        self.number = number
        self.nickname = None

        for stat in stats:
            setattr(self, stat[0], sclamp(((((getattr(genome, stat[1]).value + random.uniform(-(math.sqrt(getattr(genome, stat[1]).error)), (math.sqrt(getattr(genome, stat[1]).error)))) *
                        posfactor) + (getattr(genome, stat[2]).value + random.uniform(-(math.sqrt(getattr(genome, stat[2]).error)),
                        (math.sqrt(getattr(genome, stat[2]).error))))) / divfactor) - ((getattr(genome, stat[3]).value +
                        random.uniform(-(math.sqrt(getattr(genome, stat[3]).error)), (math.sqrt(getattr(genome, stat[3]).error)))) / negfactor)))

        # all players start alive
        self.alive = True
        self.ingame = True
        self.team = False
        self.starter = True

        self.ticker = 0

        self.offhate = random.randrange(1, 100)
        self.defhate = random.randrange(1, 100)
        self.inthate = random.randrange(1, 100)
        self.pershate = random.randrange(1, 100)

        self.defense = self.awareness + self.dodge + self.catch + self.deflection + self.nerves
        self.offense = self.tpower + self.taccuracy + self.tactics + self.tricky + self.speed
        self.intangibles = self.leadership + self.clutch + self.winner + self.patience + self.workethic
        self.personality = self.flair + self.charisma + self.ego + self.ethics + self.confidence
        self.rating = self.defense + self.offense + self.intangibles + self.personality

        # calc initial salary
        self.salary = round(self.rating * salaryfactor * (1 + (self.ego / 400)), 2)

        # print("the rating for ", self.name, " is ", str(self.rating))

        self.career_throws = 0
        self.career_dodge_fail = 0
        self.career_catch_fail = 0
        self.career_deflect_fail = 0
        self.career_dodge_succ = 0
        self.career_catch_succ = 0
        self.career_deflect_succ = 0
        self.career_hits = 0
        self.career_misses = 0
        self.career_wasdodged = 0
        self.career_wascaught = 0
        self.career_blindsided = 0
        self.career_assassinations = 0
        self.career_wins = 0
        self.career_losses = 0

    def turn_reset(self):
        self.ticker = 110 - self.speed

    def turn_dec(self, dec):
        self.ticker -= dec

    def targetvalue(self, thrower):
        x = ((self.offense * thrower.offhate) + (self.defense * thrower.defhate) +
             (self.intangibles * thrower.inthate) + (self.personality * thrower.pershate)) * varyby(thrower.tactics)

        return x


class Staff:
    def __init__(self, name, job, ability, reliability, loyalty, self_worth):
        holder = name.split()
        self.formalname = name
        self.firstname = holder[0]
        self.lastname = holder[1]
        self.fullname = name

        self.job = job
        self.ability = ability
        self.reliability = reliability
        self.loyalty = loyalty
        self.self_worth = self_worth

        if self.job == "Doctor":
            factor = doctorfactor
        if self.job == "Trainer":
            factor = trainerfactor
        if self.job == "Scout":
            factor = scoutfactor

        self.salary = round(self.self_worth * (.5 + (self.ability / 100)) * staffsalary * factor, 2)



class Gene:
    def __init__(self):
        self.value = random.randrange(1, 100)
        self.dominance = random.randrange(1, 100)
        self.error = random.randrange(1, 100)


class Genome:
    def __init__(self):
        for x in geneseq:
            setattr(self, x, Gene())

class Owner:
    def __init__(self, team):
        self.team = team

global theowner
theowner = Owner(False)


def creategenome():
    mygenome = Genome()
    # for x in "ABCDEFGHJKLMNOPQRSTUWXYZ":
    #    print(getattr(mygenome, x).value, getattr(mygenome, x).dominance, getattr(mygenome, x).error)
    return mygenome


def createcities():
    with open('Cities.csv') as f:
        cr = csv.reader(f)
        # skip=next(cr)  #skip the first row of keys "a,b,c,d"
        citylist = [l for l in cr]
    for city in citylist:
        fans = math.sqrt(int(city[2])) * random.uniform(.1, 1.0)
        rabidity = int(random.gauss(50, 15))
        loyalty = int(random.gauss(50, 15))
        avg_income = int(random.gauss(10000, 2000))
        cities.append(City(city[0], city[1], int(city[2]), fans, rabidity, loyalty, avg_income))

    # for city in cities:
    #     print("%s %s %s %s %s" % (city.name, city.country, city.population, city.rabidity, city.loyalty))

createcities()

# debug feature - sorts cities by appeal and lists them in console
def city_list():
    cities.sort(key=lambda x: x.appeal, reverse=True)
    for city in cities:
        print(city.name, city.appeal)

def createplayer():
    filename = open("GermanFirst.txt")
    germanfirstnames = [i.strip() for i in filename.readlines()]
    filename.close()

    filename = open("GermanLast.txt")
    germanlastnames = [i.strip() for i in filename.readlines()]
    filename.close()

    filename = open("JapaneseFirst.txt")
    japanesefirstnames = [i.strip() for i in filename.readlines()]
    filename.close()

    filename = open("JapaneseLast.txt")
    japaneselastnames = [i.strip() for i in filename.readlines()]
    filename.close()

    global curnum

    needname = True

    if random.randrange(0, 100) > 40:
        nationality = "German"
    else:
        nationality = "Japanese"

    while needname:
        if nationality == "German":
            tempname = germanfirstnames[random.randint(0, len(germanfirstnames)-1)].strip() + " " + germanlastnames[random.randint(0, len(germanlastnames)-1)].strip()
        else:
            tempname = japanesefirstnames[random.randint(0, len(japanesefirstnames)-1)] + " " + japaneselastnames[random.randint(0, len(japaneselastnames)-1)]
        if tempname in usednames:
            pass
        else:
            usednames.append(tempname)
            needname = False

    # Generate Genome

    newplayer = Player(tempname, curnum, Genome())
    newplayer.nationality = nationality

    # for item in newPlayer:
    #     print(item, " ", newPlayer[item])
    curnum += 1

    return newplayer

def createstaff(job):
    filename = open("GermanFirst.txt")
    germanfirstnames = [i.strip() for i in filename.readlines()]
    filename.close()

    filename = open("GermanLast.txt")
    germanlastnames = [i.strip() for i in filename.readlines()]
    filename.close()

    filename = open("JapaneseFirst.txt")
    japanesefirstnames = [i.strip() for i in filename.readlines()]
    filename.close()

    filename = open("JapaneseLast.txt")
    japaneselastnames = [i.strip() for i in filename.readlines()]
    filename.close()

    needname = True

    if random.randrange(0, 100) > 40:
        nationality = "German"
    else:
        nationality = "Japanese"

    while needname:
        if nationality == "German":
            tempname = germanfirstnames[random.randint(0, len(germanfirstnames)-1)].strip() + " " + germanlastnames[random.randint(0, len(germanlastnames)-1)].strip()
        else:
            tempname = japanesefirstnames[random.randint(0, len(japanesefirstnames)-1)] + " " + japaneselastnames[random.randint(0, len(japaneselastnames)-1)]
        if tempname in usednames:
            pass
        else:
            usednames.append(tempname)
            needname = False

    # Generate Genome

    job = job
    ability = random.randrange(1, 100)
    reliability = random.randrange(1, 100)
    loyalty = random.randrange(1, 100)
    self_worth = random.uniform(.6, 1.4)

    newstaff = Staff(tempname, job, ability, reliability, loyalty, self_worth)
    newstaff.nationality = nationality

    # for item in newPlayer:
    #     print(item, " ", newPlayer[item])

    return newstaff

def newplayers(x):
    freeagents.clear()
    for i in range(1, x):
        freeagents.append(createplayer())

    offs = []
    for player in freeagents:
        offs.append(player.offense)

    defs = []
    for player in freeagents:
        defs.append(player.defense)

def gen_newstaff(x):
    # create doctor pool
    for i in range(1, x):
        freedoctors.append(createstaff("Doctor"))

    for i in range(1, x):
        freetrainers.append(createstaff("Trainer"))
        
    for i in range(1, x):
        freescouts.append(createstaff("Scout"))


def newteams(x):
    teams.clear()
    filename = open("AnimalNames.txt")
    namelist = [i.strip() for i in filename.readlines()]
    filename.close()

    # filename = open("Cities.txt")
    # citylist = [i.strip() for i in filename.readlines()]
    # filename.close()

    # make x number of teams
    for i in range(0, x):
        teams.append(Team(cities.pop(random.randint(0, len(cities)-1)), namelist.pop(random.randint(0, len(namelist)-1)), []))

    for team in teams:
        for i in range(0, 9):
            pick_player = random.randint(0, len(freeagents)-1)
            addplayer(freeagents[pick_player], team)

def remplayer(player):
    freeagents.append(player.team.roster.pop(player.team.roster.index(player)))
    player.team = False


def manage_drop_player(player):
    remplayer(player)
    manage_owner_team_roster(theowner.team)


def manage_add_player(player):
    addplayer(player, theowner.team)
    manage_free_agents()


def addplayer(player, team):
    player.team = team
    team.roster.append(freeagents.pop(freeagents.index(player)))

def manage_bench_player(player):
    player.starter = False
    manage_owner_team_roster(theowner.team)

def manage_start_player(player):
    player.starter = True
    manage_owner_team_roster(theowner.team)

def newleaguebutton():
    for child in mainbox.winfo_children():
        child.destroy()

    # for child in controlbar.winfo_children():
    #     child.destroy()

    newplayers(500)
    gen_newstaff(50)
    newteams(12)
    pickyourteam()


def playseason():
    for team in teams:
        team.wins = 0
        team.losses = 0

    for i in range(0, len(teams)):
        for j in range(0, len(teams)):
            if i != j:
                play_game(teams[i], teams[j])

    leaguestandings()


def next_day():
    pass

def build_season_calendar(year=global_date.year):
    # week schedule
    new_season = Calendar(year)
    for week in range(1, 11):
        teams_avail = list(teams)
        random.shuffle(teams_avail)
        while teams_avail:
            home = teams_avail.pop()
            away = teams_avail.pop()
            new_season.matches.append(Matchup(home, away, Date(6, week, year)))

    calendars.append(new_season)

    for calendar in calendars:
        if calendar.year == global_date.year:
            print("Found the correct year")
            for match in calendar.matches:
                print("Week %s  Home %s   Away %s" % (match.date.week, match.home.fullname, match.away.fullname))


def leaguestandings():
    for child in mainbox.winfo_children():
        child.destroy()

    tempframe = Frame(mainbox, width=1900)
    tempframe.pack()

    for i in teams:
        words = "%s  %s - %s (%s) [%s]" % (i.fullname, str(i.wins), str(i.losses), ('%.3f' % i.winpercentage), str(i.offrating() +i.defrating()))
        Label(tempframe, text=words).pack()


def calc_team_mgmt_eff(teams):
    effs = []
    for team in teams:
        effs.append((team.offrating() + team.defrating()) / team.salary())

    return statistics.mean(effs)

def calc_team_win_eff(teams):
    effs = []
    for team in teams:
        effs.append(team.alltime_winpercentage / team.salary())

    if statistics.mean(effs) == 0:
        return 0.000000000000001
    else:
        return statistics.mean(effs)
        
        
def league_team_data():
    for child in mainbox.winfo_children():
        child.destroy()

    tempframe = Frame(mainbox)

    row_iter = 0

    Label(tempframe, text="League-Wide Data").grid(row=row_iter, columnspan=8)
    row_iter += 1

    Label(tempframe, text="Name").grid(row=row_iter, column=0)
    Label(tempframe, text="All-Time Wins").grid(row=row_iter, column=1)
    Label(tempframe, text="All-Time Losses").grid(row=row_iter, column=2)
    Label(tempframe, text="Rating").grid(row=row_iter, column=3)
    Label(tempframe, text="Salary").grid(row=row_iter, column=4)
    Label(tempframe, text="All-time Win %").grid(row=row_iter, column=5)
    Label(tempframe, text="Salary Efficiency").grid(row=row_iter, column=6)
    Label(tempframe, text="Win Efficiency").grid(row=row_iter, column=7)
    row_iter += 1

    league_mgmt_eff = calc_team_mgmt_eff(teams)
    league_win_eff = calc_team_win_eff(teams)

    for team in teams:
        Label(tempframe, text=team.fullname).grid(row=row_iter, column=0)
        Label(tempframe, text=team.alltime_wins).grid(row=row_iter, column=1)
        Label(tempframe, text=team.alltime_losses).grid(row=row_iter, column=2)
        Label(tempframe, text=str(team.offrating() + team.defrating())).grid(row=row_iter, column=3)
        Label(tempframe, text="$%.2f" % team.salary()).grid(row=row_iter, column=4)
        Label(tempframe, text='%.3f' % team.alltime_winpercentage).grid(row=row_iter, column=5)

        eff = round(((team.offrating() + team.defrating()) / team.salary()) / league_mgmt_eff, 3)
        Label(tempframe, text=eff).grid(row=row_iter, column=6)

        eff = round((team.alltime_winpercentage / team.salary()) / league_win_eff, 3)
        Label(tempframe, text=eff).grid(row=row_iter, column=7)

        row_iter += 1

    tempframe.pack()


def playerstats():
    for child in mainbox.winfo_children():
        child.destroy()

    player_with_most_hits = best_player('career_hits')
    words = "League leader in hits - %s of the %s (%s)" % (player_with_most_hits.fullname, player_with_most_hits.team.fullname, player_with_most_hits.career_hits)
    Label(mainbox, text=words).pack()

    player_with_most_catches = best_player('career_catch_succ')
    words = "League leader in catches - %s of the %s (%s)" % (player_with_most_catches.fullname, player_with_most_catches.team.fullname, player_with_most_catches.career_catch_succ)
    Label(mainbox, text=words).pack()

    player_with_most_dodges = best_player('career_dodge_succ')
    words = "League leader in dodges - %s of the %s (%s)" % (player_with_most_dodges.fullname, player_with_most_dodges.team.fullname, player_with_most_dodges.career_dodge_succ)
    Label(mainbox, text=words).pack()

    total_hits = 0
    total_misses = 0
    total_dodge = 0
    total_catch = 0
    total_throws = 0
    for x in teams:
        for y in x.roster:
            total_hits += y.career_hits
            total_misses += y.career_misses
            total_dodge += y.career_dodge_succ
            total_catch += y.career_catch_succ
            total_throws += y.career_throws

    Label(mainbox, text="\nLeague Totals\n").pack()
    words = "%s hits   %s dodges   %s catches" % (total_hits, total_dodge, total_catch)
    Label(mainbox, text=words).pack()

    words = "%s total throws" % total_throws
    Label(mainbox, text=words).pack()

    # words = "%s average throw accuracy" % str(round(statistics.median(accuracies), 1))
    # Label(mainbox, text=words).pack()


def play_random_game():

    for child in mainbox.winfo_children():
        child.destroy()

    starters = 0
    for player in theowner.team.roster:
        if player.starter:
            starters += 1

    if starters == 9:
        new_play_game(theowner.team, random.choice(teams))
    else:
        Label(mainbox, text="Need 9 starters to play a game").pack()

    global_date.inc()


def show_owner_team_roster(team):
    for child in mainbox.winfo_children():
        child.destroy()

    tempframe = Frame(mainbox)

    row_iter = 0

    Label(tempframe, text="%s Roster" % theowner.team.fullname).grid(row=row_iter, columnspan=6)
    row_iter += 1

    Label(tempframe, text="Weekly Salary Cost: $%.2f" % theowner.team.salary()).grid(row=row_iter, columnspan=6)
    row_iter += 1

    Label(tempframe, text="Name").grid(row=row_iter, column=0)
    Label(tempframe, text="Offense").grid(row=row_iter, column=1)
    Label(tempframe, text="Defense").grid(row=row_iter, column=2)
    Label(tempframe, text="Intangibles").grid(row=row_iter, column=3)
    Label(tempframe, text="Personality").grid(row=row_iter, column=4)
    Label(tempframe, text="TOTAL").grid(row=row_iter, column=5)
    row_iter += 1

    for player in team.roster:
        Label(tempframe, text=player.fullname).grid(row=row_iter, column=0)
        Label(tempframe, text=player.offense).grid(row=row_iter, column=1)
        Label(tempframe, text=player.defense).grid(row=row_iter, column=2)
        Label(tempframe, text=player.intangibles).grid(row=row_iter, column=3)
        Label(tempframe, text=player.personality).grid(row=row_iter, column=4)
        Label(tempframe, text=player.rating).grid(row=row_iter, column=5)
        row_iter += 1

    tempframe.pack()


def manage_owner_team_roster(team):
    for child in mainbox.winfo_children():
        child.destroy()

    tempframe = Frame(mainbox)

    Label(tempframe, text="STARTERS").grid(row=0, columnspan=3)

    Label(tempframe, text="Name").grid(row=1, column=0)
    Label(tempframe, text="Rating").grid(row=1, column=1)
    Label(tempframe, text="Salary").grid(row=1, column=2)

    row_iter = 2
    for player in team.roster:
        if player.starter:
            Label(tempframe, text=player.fullname).grid(row=row_iter, column=0)
            Label(tempframe, text=player.rating).grid(row=row_iter, column=1)
            Label(tempframe, text="$%.2f" % player.salary).grid(row=row_iter, column=2)
            Button(tempframe, text="Start", width=10, command=lambda x=player: manage_start_player(x)).grid(row=row_iter, column=3)
            Button(tempframe, text="Bench", width=10, command=lambda x=player: manage_bench_player(x)).grid(row=row_iter, column=4)
            Button(tempframe, text="Drop", width=10, command=lambda x=player: manage_drop_player(x)).grid(row=row_iter, column=5)
            row_iter += 1

    Label(tempframe, text="BENCH").grid(row=row_iter, columnspan=3)
    row_iter += 1

    Label(tempframe, text="Name").grid(row=row_iter, column=0)
    Label(tempframe, text="Rating").grid(row=row_iter, column=1)
    Label(tempframe, text="Salary").grid(row=row_iter, column=2)
    row_iter += 1

    for player in team.roster:
        if not player.starter:
            Label(tempframe, text=player.fullname).grid(row=row_iter, column=0)
            Label(tempframe, text=player.rating).grid(row=row_iter, column=1)
            Label(tempframe, text="$%.2f" % player.salary).grid(row=row_iter, column=2)
            Button(tempframe, text="Start", width=10, command=lambda x=player: manage_start_player(x)).grid(row=row_iter, column=3)
            Button(tempframe, text="Bench", width=10, command=lambda x=player: manage_bench_player(x)).grid(row=row_iter, column=4)
            Button(tempframe, text="Drop", width=10, command=lambda x=player: manage_drop_player(x)).grid(row=row_iter, column=5)
            row_iter += 1

    tempframe.pack(side=LEFT)



def manage_owner_team_staff(team):
    for child in mainbox.winfo_children():
        child.destroy()

    tempframe = Frame(mainbox)

    Label(tempframe, text="Name").grid(row=0, column=0)
    Label(tempframe, text="Position").grid(row=0, column=1)
    Label(tempframe, text="Ability").grid(row=0, column=2)
    Label(tempframe, text="Salary").grid(row=0, column=3)

    # positions = ["Doctor", "Trainer", "Scout"]
    row_iter = 1

    Label(tempframe, text=team.doctor.fullname).grid(row=row_iter, column=0)
    Label(tempframe, text=team.doctor.job).grid(row=row_iter, column=1)
    Label(tempframe, text=team.doctor.ability).grid(row=row_iter, column=2)
    Label(tempframe, text="$%.2f" % team.doctor.salary).grid(row=row_iter, column=3)
    row_iter += 1

    Label(tempframe, text=team.trainer.fullname).grid(row=row_iter, column=0)
    Label(tempframe, text=team.trainer.job).grid(row=row_iter, column=1)
    Label(tempframe, text=team.trainer.ability).grid(row=row_iter, column=2)
    Label(tempframe, text="$%.2f" % team.trainer.salary).grid(row=row_iter, column=3)
    row_iter += 1
    
    Label(tempframe, text=team.scout.fullname).grid(row=row_iter, column=0)
    Label(tempframe, text=team.scout.job).grid(row=row_iter, column=1)
    Label(tempframe, text=team.scout.ability).grid(row=row_iter, column=2)
    Label(tempframe, text="$%.2f" % team.scout.salary).grid(row=row_iter, column=3)
    row_iter += 1
    
    tempframe.pack(side=LEFT)




def manage_free_agents():
    for child in mainbox.winfo_children():
        child.destroy()

    # Main window
    # Grid sizing behavior in window
    mainbox.grid_rowconfigure(0, weight=1)
    mainbox.grid_columnconfigure(0, weight=1)

    # Canvas
    cnv = Canvas(mainbox, height=900, width=1500)
    cnv.grid(row=0, column=0, sticky='nswe')

    ## Scrollbars for canvas
    vScroll = Scrollbar(mainbox, orient=VERTICAL, command=cnv.yview)
    vScroll.grid(row=0, column=1, sticky='ns')
    cnv.configure(yscrollcommand=vScroll.set)

    ## Frame in canvas
    frm = Frame(cnv, height=900, width=1500)

    ## This puts the frame in the canvas's scrollable zone
    cnv.create_window(0, 0, window=frm, anchor='nw')

    ## Frame contents
    Label(frm, font=headerfont, text="Player Name").grid(row=0, column=0)
    Label(frm, font=headerfont, text="Overall Rating").grid(row=0, column=1)
    row_iter = 1
    for player in freeagents:
        Label(frm, text=player.fullname).grid(row=row_iter, column=0)
        Label(frm, text=player.rating).grid(row=row_iter, column=1)
        Button(frm, text="Add %s" % player.fullname, width=25, command=lambda x=player: manage_add_player(x)).grid(row=row_iter, column=2)
        row_iter += 1

    ## Update display to get correct dimensions
    frm.update_idletasks()

    ## Configure size of canvas's scrollable zone
    cnv.configure(scrollregion=(0, 0, frm.winfo_width(), frm.winfo_height()))





    # for player in freeagents:
    #     # Label(newframe, text=player.fullname).pack()
    #     # Label(mainbox, text=player.rating).grid(row=row_iter, column=1)
    #     # Button(mainbox, text="Add %s" % player.fullname, width=25, command=lambda x=player: manage_add_player(x)).grid(row=row_iter, column=2)
    #     row_iter += 1



def pickteams(x):
    i = 0
    while i < x:
        home = random.choice(teams)
        visitor = home
        while home == visitor:
            visitor = random.choice(teams)
        play_game(home, visitor)
        i += 1


def pickyourteam():
    for child in mainbox.winfo_children():
        child.destroy()

    filename = open("Industries.txt")
    industries = [i.strip() for i in filename.readlines()]
    filename.close()
    industry = random.choice(industries)

    Label(mainbox, text="Your dear father, who made his fortune in the %s industry, recently passed away." % industry).grid(row=0, column=0)
    Label(mainbox, text="In his will, you are listed as the beneficiary of his prized dodgeball team.").grid(row=1, column=0)
    Label(mainbox, text="").grid(row=2, column=0)
    Label(mainbox, text="Wait... what was the name of the team?").grid(row=3, column=0)
    Label(mainbox, text="").grid(row=4, column=0)
    row_iter = 5
    for team in teams:
        Button(mainbox, text=team.fullname, width=20, command=lambda x=team: begingame(x)).grid(row=row_iter, columnspan=2)
        row_iter += 1


def begingame(team):
    for child in mainbox.winfo_children():
        child.destroy()

    drawmenubar()
    # name = get_player_name.get()
    theowner.team = team
    Label(mainbox, text="You are now the owner of the %s" % theowner.team.fullname).grid(row=0, column=0)


def drawmenubar():

    # ROW 1 BUTTONS

    Button(controlbar, text="New League", command=newleaguebutton).grid(row=0, column=0, padx=3)

    Button(controlbar, text="Play Full Season", command=playseason).grid(row=0, column=1, padx=3)

    Button(controlbar, text="League Standings", command=leaguestandings).grid(row=0, column=2, padx=3)

    Button(controlbar, text="Player Stats", command=playerstats).grid(row=0, column=3, padx=3)

    Button(controlbar, text="Play Random Game", command=play_random_game).grid(row=0, column=4, padx=2, pady=2)

    Button(controlbar, text="TEST BUTTON", command=build_season_calendar).grid(row=0, column=5, padx=2, pady=2)

    # ROW 2 BUTTONS

    Button(controlbar, text="View Roster", command=lambda: show_owner_team_roster(theowner.team)).grid(row=1, column=0, padx=2, pady=2)

    Button(controlbar, text="Manage Roster", command=lambda: manage_owner_team_roster(theowner.team)).grid(row=1, column=1, padx=2, pady=2)

    Button(controlbar, text="Manage Staff", command=lambda: manage_owner_team_staff(theowner.team)).grid(row=1, column=2, padx=2, pady=2)

    Button(controlbar, text="Free Agents", command=lambda: manage_free_agents()).grid(row=1, column=3, padx=2, pady=2)

    Button(controlbar, text="League Team Data", command=lambda: league_team_data()).grid(row=1, column=4, padx=2, pady=2)



### DRAW THE INTERFACE FRAMES ###

### GAME TITLE

titlefont = font.Font(family='Century Gothic', size=24, weight='bold')
headerfont = font.Font(family='Century Gothic', size=14, weight='bold')

Label(root, text="GENETIC DODGEBALL", font=titlefont, width=60).pack(side=TOP)

statusbar = Frame(root, width=1900, background="green", height=20)
date_box = Label(statusbar, text="Week %s    Day %s    Year %s" % (global_date.week, global_date.day, global_date.year))

date_box.pack()
statusbar.pack(side=TOP)

controlbar = Frame(root, width=1900, background="navy", height=20)
controlbar.pack(side=TOP)


### spacer frame ###
Frame(root, height=20).pack(side=TOP)

mainbox = Frame(root, width=1900, height=800)
mainbox.pack(side=TOP)


newleaguebutton()



def updatestats(team):
    team.winpercent()
    team.alltime_winpercent()

    # teams.sort(key=lambda x: x.winpercentage, reverse=True)
    # teams.sort(winpercentage, reverse=True)


def sort_by_winpercentage():
    for team in teams:
        team.winpercent()
        team.alltime_winpercent()

    teams.sort(key=lambda x: x.winpercentage, reverse=True)
    # teams.sort(winpercentage, reverse=True)





def play_game(team1, team2):
    for child in mainbox.winfo_children():
        child.destroy()

    # tempframe = Frame(mainbox)
    # tempframe.pack()

    # text2 = Text(mainbox, height=40, width=60)
    # scroll = Scrollbar(mainbox, command=text2.yview)
    # text2.configure(yscrollcommand=scroll.set)
    # text2.pack(side=LEFT)
    # scroll.pack(side=RIGHT, fill=Y)

    text2 = Text(mainbox)
    scroll = Scrollbar(mainbox, command=text2.yview)
    text2.configure(yscrollcommand=scroll.set)
    text2.pack(side=LEFT)
    scroll.pack(side=RIGHT, fill=Y)

    home = team1
    visitor = team2

    teams_in_match = [team1, team2]

    text2.insert(END, "%s [%soff %sdef] vs. %s [%soff %sdef]\n" % (home.fullname, home.offrating(), home.defrating(),
                                                                   visitor.fullname, visitor.offrating(), visitor.defrating()))
    text2.insert(END, "- Home -\n")
    for y in home.roster:
        text2.insert(END, y.fullname + "\n")
    text2.insert(END, "- Visitors -\n")
    for y in visitor.roster:
        text2.insert(END, y.fullname + "\n")

    text2.insert(END, "Start Game!\n")

    # check to make sure no team is depleted to 0 available players
    while home.playersleft() > 0 and visitor.playersleft() > 0:
        for x in home.roster:
            if x.ingame:
                target = selecttarget(x, visitor)
                if not target:
                    break
                result = throw(x, target)
                x.career_throws += 1
                if result == "unawarehit":
                    text2.insert(END, "%s sees that %s unaware and hits him!\n" % (x.fullname, target.fullname))
                    target.career_blindsided += 1
                    x.career_hits += 1
                    target.ingame = False
                if result == "catchfail":
                    text2.insert(END, "%s tries to catch a throw by %s but can't hold on!\n" % (target.fullname, x.fullname))
                    target.career_catch_fail += 1
                    x.career_hits += 1
                    target.ingame = False
                if result == "dodgefail":
                    text2.insert(END, "%s fails to dodge a throw by %s!\n" % (target.fullname, x.fullname))
                    target.career_dodge_fail += 1
                    x.career_hits += 1
                    target.ingame = False
                if result == "catch":
                    text2.insert(END, "%s's throw is caught by %s!\n" % (x.fullname, target.fullname))
                    target.career_catch_succ += 1
                    x.career_wascaught += 1
                    x.ingame = False
                if result == "dodge":
                    text2.insert(END, "%s dodges a throw by %s!\n" % (target.fullname, x.fullname))
                    target.career_dodge_succ += 1
                    x.career_wasdodged += 1
        text2.insert(END, "-- Switch Sides --\n")
        for x in visitor.roster:
            if x.ingame:
                target = selecttarget(x, home)
                if not target:
                    break
                result = throw(x, target)
                x.career_throws += 1
                if result == "unawarehit":
                    text2.insert(END, "%s sees that %s unaware and hits him!\n" % (x.fullname, target.fullname))
                    target.career_blindsided += 1
                    x.career_hits += 1
                    target.ingame = False
                if result == "catchfail":
                    text2.insert(END, "%s tries to catch a throw by %s but can't hold on!\n" % (target.fullname, x.fullname))
                    target.career_catch_fail += 1
                    x.career_hits += 1
                    target.ingame = False
                if result == "dodgefail":
                    text2.insert(END, "%s fails to dodge a throw by %s!\n" % (target.fullname, x.fullname))
                    target.career_dodge_fail += 1
                    x.career_hits += 1
                    target.ingame = False
                if result == "catch":
                    text2.insert(END, "%s's throw is caught by %s!\n" % (x.fullname, target.fullname))
                    target.career_catch_succ += 1
                    x.career_wascaught += 1
                    x.ingame = False
                if result == "dodge":
                    text2.insert(END, "%s dodges a throw by %s!\n" % (target.fullname, x.fullname))
                    target.career_dodge_succ += 1
                    x.career_wasdodged += 1
        text2.insert(END, "-- End of Round --\n")

    if home.playersleft() == 0:
        text2.insert(END, "-- Visitors Win --\n")
        visitor.win()
        home.loss()
    else:
        text2.insert(END, "-- Home Wins --\n")
        home.win()
        visitor.loss()

    updatestats(home)
    updatestats(visitor)

    text2.insert(END, "-- Remaining Players --\n")

    text2.insert(END, "- Home -\n")
    for y in home.roster:
        if y.ingame:
            text2.insert(END, y.fullname + "\n")
        else:
            y.ingame = True

    text2.insert(END, "- Visitors -\n")
    for y in visitor.roster:
        if y.ingame:
            text2.insert(END, y.fullname + "\n")
        else:
            y.ingame = True

def new_play_game(team1, team2):
    for child in mainbox.winfo_children():
        child.destroy()

    # tempframe = Frame(mainbox)
    # tempframe.pack()

    # text2 = Text(mainbox, height=40, width=60)
    # scroll = Scrollbar(mainbox, command=text2.yview)
    # text2.configure(yscrollcommand=scroll.set)
    # text2.pack(side=LEFT)
    # scroll.pack(side=RIGHT, fill=Y)

    text2 = Text(mainbox)
    scroll = Scrollbar(mainbox, command=text2.yview)
    text2.configure(yscrollcommand=scroll.set)
    text2.pack(side=LEFT)
    scroll.pack(side=RIGHT, fill=Y)

    home = team1
    visitor = team2

    # teams_in_match = [team1, team2]

    text2.insert(END, "%s [%soff %sdef] vs. %s [%soff %sdef]\n" % (home.fullname, home.offrating(), home.defrating(),
                                                                   visitor.fullname, visitor.offrating(), visitor.defrating()))
    text2.insert(END, "- Home -\n")
    for y in home.roster:
        text2.insert(END, y.fullname + "\n")
    text2.insert(END, "- Visitors -\n")
    for y in visitor.roster:
        text2.insert(END, y.fullname + "\n")

    text2.insert(END, "Start Game!\n")

    matchplayers = home.roster + visitor.roster

    for player in matchplayers:
        player.turn_reset()
        print(player.ticker)

    matchplayers.sort(key=lambda x: x.ticker)

    first_turn = True

    # check to make sure no team is depleted to 0 available players
    while matchplayers:
        # start new turn
        # sort available players by ticker

        # reset player that went ticker
        if not first_turn:
            matchplayers[0].turn_reset()

        matchplayers.sort(key=lambda x: x.ticker)

        # reduce all tickers by amount of the fastest player's ticker
        amt = matchplayers[0].ticker
        for player in matchplayers:
            player.turn_dec(amt)

        # let fastest player take turn
        print()
        text2.insert(END, "[%s (%s) of the %s]\n" % (matchplayers[0].fullname, matchplayers[0].speed, matchplayers[0].team.name))

        # select target

        if matchplayers[0].team == home:
            target = selecttarget(matchplayers[0], visitor)
        if matchplayers[0].team == visitor:
            target = selecttarget(matchplayers[0], home)
        if not target:
            break
        result = throw(matchplayers[0], target)
        matchplayers[0].career_throws += 1
        if result == "unawarehit":
            text2.insert(END, "%s sees that %s unaware and hits him!\n" % (matchplayers[0].fullname, target.fullname))
            target.career_blindsided += 1
            matchplayers[0].career_hits += 1
            target.ingame = False
        if result == "catchfail":
            text2.insert(END, "%s tries to catch a throw by %s but can't hold on!\n" % (target.fullname, matchplayers[0].fullname))
            target.career_catch_fail += 1
            matchplayers[0].career_hits += 1
            target.ingame = False
        if result == "dodgefail":
            text2.insert(END, "%s fails to dodge a throw by %s!\n" % (target.fullname, matchplayers[0].fullname))
            target.career_dodge_fail += 1
            matchplayers[0].career_hits += 1
            target.ingame = False
        if result == "catch":
            text2.insert(END, "%s's throw is caught by %s!\n" % (matchplayers[0].fullname, target.fullname))
            target.career_catch_succ += 1
            matchplayers[0].career_wascaught += 1
            matchplayers[0].ingame = False
        if result == "dodge":
            text2.insert(END, "%s dodges a throw by %s!\n" % (target.fullname, matchplayers[0].fullname))
            target.career_dodge_succ += 1
            matchplayers[0].career_wasdodged += 1

        # cleanup out players
        for player in matchplayers:
            if not player.ingame:
                matchplayers.remove(player)

        first_turn = False
                
    if home.playersleft() == 0:
        text2.insert(END, "-- Visitors Win --\n")
        visitor.win()
        home.loss()
    else:
        text2.insert(END, "-- Home Wins --\n")
        home.win()
        visitor.loss()

    updatestats(home)
    updatestats(visitor)

    text2.insert(END, "-- Remaining Players --\n")

    text2.insert(END, "- Home -\n")
    for y in home.roster:
        if y.ingame:
            text2.insert(END, y.fullname + "\n")
        else:
            y.ingame = True

    text2.insert(END, "- Visitors -\n")
    for y in visitor.roster:
        if y.ingame:
            text2.insert(END, y.fullname + "\n")
        else:
            y.ingame = True


def selecttarget(thrower, opponents):
    if opponents.playersleft() > 0:
        target = next((x for x in opponents.roster if x.ingame), None)
        # check for panic throw
        if getgauss(50, 25) < getgauss(thrower.nerves, thrower.pconsist):
            for x in opponents.roster:
                if x.ingame:
                    if target.targetvalue(thrower) < x.targetvalue(thrower):
                        target = x
                        val = x.targetvalue
        # print(str(thrower.name) + " throws at " + str(target.name))
        return target
    else:
        return False


def throw(thrower, defender):
    accuracies = []
    incomingpower = getgauss(thrower.tpower, thrower.pconsist)
    incomingaccuracy = getgauss(thrower.taccuracy, thrower.pconsist)
    accuracies.append(incomingaccuracy)
    # check to see if defender notices
    if getgauss(45, 25) < defender.awareness:
        # pick best defense
        if getgauss(incomingpower, defender.tactics) > getgauss(incomingaccuracy, defender.tactics):
            defense = "dodge"
            dval = getgauss(defender.dodge, defender.pconsist)
            oval = incomingaccuracy
        else:
            defense = "catch"
            dval = getgauss(defender.catch, defender.pconsist)
            oval = incomingpower
        # apply defense and check for hit
        if oval > dval:
            return defense + "fail"
        else:
            return defense

    else:
        # unaware player gets no chance to defend
        return "unawarehit"


def varyby(stat):
    return random.uniform(1 - ((100 - stat) / 100), 1 + ((100 - stat) / 100))

def getgauss(a, b):
    return random.gauss(a, math.sqrt(100-b) * 1.5)

def calcdev(x):
    return math.sqrt(101-x)



root.wm_state('zoomed')
root.mainloop()
