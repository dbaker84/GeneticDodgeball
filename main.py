__author__ = 'Daniel Baker'

from tkinter import *
import random
import statistics
import operator

root = Tk()


freeagents = []
teams = []
curnum = 1

sclamp = lambda n: max(min(100, n), 1)

class Team:
    def __init__(self, name, roster):
        self.name = name
        self.roster = roster

        troster = []
        for x in self.roster:
            troster.append(x.rating)

        self.rating = round(statistics.mean(troster))
        self.consistency = round(statistics.stdev(troster))

        self.wins = 0
        self.losses = 0
        self.winpercent = 0.000
        self.active = True

class Player:
    def __init__(self, name, number, ftwitch, stwitch, ndensity, nspeed, lcoord):
        self.name = name
        self.number = number

        # genes

        self.ftwitch = ftwitch
        self.stwitch = stwitch
        self.ndensity = ndensity
        self.nspeed = nspeed
        self.lcoord = lcoord

        # derived stats
        # Physical
        self.dodge = round((nspeed.value + ftwitch.value) / 2)
        self.catch = round((nspeed.value + lcoord.value) / 2)
        self.throwstr = round((ftwitch.value + lcoord.value) / 2)
        self.throwacc = round((lcoord.value + nspeed.value) / 2)
        self.stamina = stwitch.value
        self.size = round((ftwitch.value + stwitch.value))

        # mental
        self.awareness = round((lcoord.value + ndensity.value) / 2)
        self.tactics = round((ndensity.value + nspeed.value) / 2)
        self.pcons = round(random.randrange(1, 100))
        self.mcons = round(random.randrange(1, 100))

        # all players start alive
        self.alive = True

        self.rating = round((self.dodge + self.catch + self.throwstr + self.throwacc + self.stamina + self.awareness + self.tactics) / 7)

        self.hit = 0


class Gene:
    def __init__(self, value, dominance):
        self.value = value
        self.dominance = dominance

def createplayer():
    filename = open("GermanFirst.txt")
    germannames = [i.strip() for i in filename.readlines()]
    filename.close()

    filename = open("JapaneseFirst.txt")
    japanesenames = [i.strip() for i in filename.readlines()]
    filename.close()

    global curnum
    tempreli = round(random.randrange(1, 25))
    if random.randrange(0, 100) > 50:
        tempname = germannames[random.randint(0, len(germannames)-1)]
    else:
        tempname = japanesenames[random.randint(0, len(japanesenames)-1)]

    # Generate Genome

    newplayer = Player(tempname, curnum,
                       Gene(random.randrange(1, 100), random.randrange(1, 100)),
                       Gene(random.randrange(1, 100), random.randrange(1, 100)),
                       Gene(random.randrange(1, 100), random.randrange(1, 100)),
                       Gene(random.randrange(1, 100), random.randrange(1, 100)),
                       Gene(random.randrange(1, 100), random.randrange(1, 100)))

    # for item in newPlayer:
    #     print(item, " ", newPlayer[item])
    curnum += 1

    return newplayer

def newplayers(x):
    freeagents.clear()
    for i in range(1, x):
        freeagents.append(createplayer())

def newteams(x):
    teams.clear()
    filename = open("AnimalNames.txt")
    namelist = [i.strip() for i in filename.readlines()]
    filename.close()

    for i in range(0, x):
        temproster = []
        for j in range(1, 6):
            temproster.append(freeagents.pop(random.randint(0, len(freeagents)-1)))

        teams.append(Team(namelist.pop(random.randint(0, len(namelist)-1)), temproster))


def newleaguebutton():
    newplayers(100)
    newteams(8)

def rostertest():
    for x in teams:
        print(x.name)
        for i in x.roster:
            print(i.number, " ", i.name, " ", i.dodge)
        print('\n')

def randomroster():
    for child in mainbox.winfo_children():
        child.destroy()

    tempframe = Frame(mainbox, height=300, width=600)
    tempframe.pack()

    pick = teams[random.randrange(0, len(teams)-1)]

    Label(tempframe, text=pick.name).grid(row=0, column=0, columnspan=8)
    Label(tempframe, text=pick.rating).grid(row=0, column=8, columnspan=1)
    Label(tempframe, text=pick.consistency).grid(row=0, column=9, columnspan=1)

    ticker = 1
    for i in pick.roster:
        Label(tempframe, text=i.number).grid(row=ticker, column=0)
        Label(tempframe, text=i.name).grid(row=ticker, column=1)
        Label(tempframe, text=i.dodge).grid(row=ticker, column=2)
        Label(tempframe, text=i.catch).grid(row=ticker, column=3)
        Label(tempframe, text=i.throwacc).grid(row=ticker, column=4)
        Label(tempframe, text=i.throwstr).grid(row=ticker, column=5)
        Label(tempframe, text=i.stamina).grid(row=ticker, column=6)
        Label(tempframe, text=i.awareness).grid(row=ticker, column=7)
        Label(tempframe, text=i.tactics).grid(row=ticker, column=8)
        Label(tempframe, text=i.rating).grid(row=ticker, column=9)
        ticker += 1

def playmatch(team1, team2):
    for child in mainbox.winfo_children():
        child.destroy()

    tempframe = Frame(mainbox, height=300, width=600)
    tempframe.pack()

    #team1 = teams[random.randrange(0, len(teams))]
    #team2 = team1
    #while team2 == team1:
    #    team2 = teams[random.randrange(0, len(teams))]

    Label(tempframe, text=team1.name + " (" + str(team1.wins) + "-" + str(team1.losses) + ")  VS. " + team2.name
                          + " ("+ str(team2.wins) + "-" + str(team2.losses) + ")").grid(row=0, column=0, columnspan=10)

    Label(tempframe, text="").grid(row=1, column=0, columnspan=10)

    if random.gauss(team1.rating, team1.consistency) > random.gauss(team2.rating, team2.consistency):
        team1.wins += 1
        team2.losses += 1
        winner = team1.name
    else:
        team1.losses += 1
        team2.wins += 1
        winner = team2.name

    team1.winpercent = team1.wins/(team1.losses+team1.wins)
    team2.winpercent = team2.wins/(team2.losses+team2.wins)

    Label(tempframe, text="The " + winner + " win the match!").grid(row=2, column=0, columnspan=10)
    # Label(tempframe, text=pick.consistency).grid(row=0, column=9, columnspan=1)

def randommatch():
    team1 = teams[random.randrange(0, len(teams))]
    team2 = team1
    while team2 == team1:
        team2 = teams[random.randrange(0, len(teams))]
    playmatch(team1, team2)

def playseason():
    for i in range(0, len(teams)):
        for j in range(0, len(teams)):
            if i != j:
                playmatch(teams[i], teams[j])

    #sort teams by win percent
    teams.sort(key=operator.attrgetter("winpercent"), reverse=True)

def leaguestandings():
    for child in mainbox.winfo_children():
        child.destroy()

    tempframe = Frame(mainbox, height=300, width=600)
    tempframe.pack()

    for i in teams:
        words = i.name + " [" + str(i.rating) + "] (" + str(i.wins) + "-" + str(i.losses) + ") " + ('%.3f' % i.winpercent)
        Label(tempframe, text=words).pack()

# interface

newleaguebutton()

toolbar = Frame(root, bg="blue", width=600)

newPlayersButton = Button(toolbar, text="New League", command=newleaguebutton)
newPlayersButton.pack(side=LEFT, padx=2, pady=2)

rosterTestButton = Button(toolbar, text="Show Random Roster", command=randomroster)
rosterTestButton.pack(side=LEFT, padx=2, pady=2)

playMatchButton = Button(toolbar, text="Play Random Match", command=randommatch)
playMatchButton.pack(side=LEFT, padx=2, pady=2)

playSeasonButton = Button(toolbar, text="Play Full Season", command=playseason)
playSeasonButton.pack(side=LEFT, padx=2, pady=2)

playMatchButton = Button(toolbar, text="League Standings", command=leaguestandings)
playMatchButton.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

mainbox = Frame(root, relief=SUNKEN)
mainbox.pack()





root.mainloop()
