__author__ = 'Daniel Baker'

# TODO:
#
# Nicknames
# New targeting algorithm
# Add speed/turn order
# Add team creation
# Add time/calender system
# fix bug when last out is visitor's throw being caught


from tkinter import *
import random
import statistics
import operator
import math

root = Tk()


freeagents = []
teams = []
curnum = 1


# global variables for decoding genomes
posfactor = 4
divfactor = 5
negfactor = 4

stats = [["dodge", "A", "C", "D"],
        ["catch", "B", "D", "X"],
        ["tpower", "C", "F", "O"],
        ["taccuracy", "D", "P", "U"],
        ["stamina", "E", "B", "N"],
        ["tricky", "F", "O", "K"],
        ["awareness", "G", "J", "Z"],
        ["tactics", "H", "H", "R"],
        ["pconsist", "J", "N", "P"],
        ["mconsist", "K", "Z", "H"],
        ["leadership", "L", "U", "A"],
        ["flair", "M", "W", "Q"],
        ["speed", "N", "G", "T"],
        ["clutch", "O", "R", "W"],
        ["deflection", "P", "Q", "J"],
        ["ego", "Q", "M", "B"],
        ["coachability", "R", "E", "G"],
        ["nerves", "S", "Y", "E"],
        ["workethic", "T", "T", "F"],
        ["charisma", "U", "X", "C"],
        ["unused", "W", "S", "L"],
        ["patience", "X", "L", "M"],
        ["ethics", "Y", "K", "S"],
        ["winner", "Z", "A", "Y"]]

geneseq = "ABCDEFGHJKLMNOPQRSTUWXYZ"



sclamp = lambda n: round(max(min(100, n), 1))

class Team:
    def __init__(self, name, roster):
        self.name = name
        self.roster = roster
        self.id = -1
        # self.id = random.randrange(10, 9999999)

        troster = []
        for x in self.roster:
            troster.append(x.rating)

        self.consistency = round(statistics.stdev(troster))

        self.wins = 0
        self.losses = 0
        self.winpercent = 0.000
        self.active = True

    def offrating(self):
        troster = []
        for x in self.roster:
            troster.append(x.offense)
        return round(statistics.mean(troster))

    def defrating(self):
        troster = []
        for x in self.roster:
            troster.append(x.defense)
        return round(statistics.mean(troster))

class Player:
    def __init__(self, name, number, genome):
        self.name = name
        self.number = number
        self.nickname = None

        for stat in stats:
            setattr(self, stat[0], sclamp(((((getattr(genome, stat[1]).value + random.uniform(-(math.sqrt(getattr(genome, stat[1]).error)), (math.sqrt(getattr(genome, stat[1]).error)))) *
                        posfactor) + (getattr(genome, stat[2]).value + random.uniform(-(math.sqrt(getattr(genome, stat[2]).error)),
                        (math.sqrt(getattr(genome, stat[2]).error))))) / divfactor) - ((getattr(genome, stat[3]).value +
                        random.uniform(-(math.sqrt(getattr(genome, stat[3]).error)), (math.sqrt(getattr(genome, stat[3]).error)))) / negfactor)))

        # print("the dodge for ", self.name, " is ", str(self.dodge))
        # print("the catch for ", self.name, " is ", str(self.catch))
        # print("the flair for ", self.name, " is ", str(self.flair))

        # all players start alive
        self.alive = True
        self.teamid = 0

        self.offhate = random.randrange(1, 100)
        self.defhate = random.randrange(1, 100)
        self.inthate = random.randrange(1, 100)
        self.pershate = random.randrange(1, 100)

        self.defense = self.awareness + self.dodge + self.catch + self.deflection + self.nerves
        self.offense = self.tpower + self.taccuracy + self.tactics + self.tricky + self.speed
        self.intangibles = self.leadership + self.clutch + self.winner + self.patience + self.workethic
        self.personality = self.flair + self.charisma + self.ego + self.ethics + self.coachability
        self.rating = self.defense + self.offense + self.intangibles + self.personality

        # print("the rating for ", self.name, " is ", str(self.rating))

        self.career_dodge_fail = 0
        self.career_catch_fail = 0
        self.career_deflect_fail = 0
        self.career_dodge_succ = 0
        self.career_catch_succ = 0
        self.career_deflect_succ = 0
        self.career_opp_hits = 0
        self.career_wins = 0
        self.career_losses = 0

    def targetvalue(self, thrower):
        x = ((self.offense * thrower.offhate) + (self.defense * thrower.defhate) +
             (self.intangibles * thrower.inthate) + (self.personality * thrower.pershate)) * varyby(thrower.tactics)
        print(self.name, str(x))
        return x


class Gene:
    def __init__(self):
        self.value = random.randrange(1, 100)
        self.dominance = random.randrange(1, 100)
        self.error = random.randrange(1, 100)


class Genome:
    def __init__(self):
        for x in geneseq:
            setattr(self, x, Gene())




def creategenome():
    mygenome = Genome()
    # for x in "ABCDEFGHJKLMNOPQRSTUWXYZ":
    #    print(getattr(mygenome, x).value, getattr(mygenome, x).dominance, getattr(mygenome, x).error)
    return mygenome

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

    newplayer = Player(tempname, curnum, Genome())

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

    for k in range(0, len(teams)):
        teams[k].id = k
        for m in teams[k].roster:
            m.teamid = teams[k].id


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
        Label(tempframe, text=i.accuracy).grid(row=ticker, column=4)
        Label(tempframe, text=i.power).grid(row=ticker, column=5)
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

toolbar = Frame(root, bg="blue")

newPlayersButton = Button(toolbar, text="New League", command=newleaguebutton)
newPlayersButton.pack(side=LEFT, padx=2, pady=2)

rosterTestButton = Button(toolbar, text="Show Random Roster", command=randomroster)
rosterTestButton.pack(side=LEFT, padx=2, pady=2)

playMatchButton = Button(toolbar, text="Play Random Match", command=randommatch)
playMatchButton.pack(side=LEFT, padx=2, pady=2)

playSeasonButton = Button(toolbar, text="Play Full Season", command=playseason)
playSeasonButton.pack(side=LEFT, padx=2, pady=2)

leagueStandingsButton = Button(toolbar, text="League Standings", command=leaguestandings)
leagueStandingsButton.pack(side=LEFT, padx=2, pady=2)

testTargetButton = Button(toolbar, text="Test Targeting", command=lambda: throwround(teams[0], teams[1]))
testTargetButton.pack(side=LEFT, padx=2, pady=2)

testGenomeButton = Button(toolbar, text="Generate Genome", command=creategenome())
testGenomeButton.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

mainbox = Frame(root, relief=SUNKEN)
mainbox.pack()

def throwround(team1, team2):
    for child in mainbox.winfo_children():
        child.destroy()

    tempframe = Frame(mainbox)
    tempframe.pack()

    text2 = Text(mainbox, height=400, width=200)
    scroll = Scrollbar(root, command=text2.yview)
    text2.configure(yscrollcommand=scroll.set)
    text2.insert(END, 'follow-up\n')
    text2.pack()
    scroll.pack(side=RIGHT, fill=Y)

    home = team1
    visitor = team2

    # print(home.name + " " + ' '.join([str(item.name) for item in home.roster]) + " " + str(home.offrating()) + " " + str(home.defrating()))
    # print(visitor.name + " " + ' '.join([str(item.name) for item in visitor.roster]) + " " + str(visitor.offrating()) + " " + str(visitor.defrating()))

    while len(home.roster) > 0 and len(visitor.roster) > 0:
        for x in home.roster:
            if len(home.roster) and len(visitor.roster) != 0:
                target = selecttarget(x, visitor)
                result = throw(x, target)
                words = (x.name + " throws at " + target.name + " and there is a " + str(result) + "\n")
                text2.insert(END, words)
                if result == "hit":
                    visitor.roster.pop(visitor.roster.index(target))
                if result == "catch":
                    home.roster.pop(home.roster.index(x))
        text2.insert(END, "-- Switch Sides --\n")
        for x in visitor.roster:
            if len(home.roster) and len(visitor.roster) != 0:
                target = selecttarget(x, home)
                result = throw(x, target)
                words = (x.name + " throws at " + target.name + " and there is a " + str(result) + "\n")
                text2.insert(END, words)
                if result == "hit":
                    home.roster.pop(home.roster.index(target))
                if result == "catch":
                    visitor.roster.pop(visitor.roster.index(x))
        text2.insert(END, "-- End of Round --\n")

    if len(home.roster) == 0:
        text2.insert(END, "-- Visitors Win --\n")
    else:
        text2.insert(END, "-- Home Wins --\n")

    text2.insert(END, "-- Remaining Players --\n")
    text2.insert(END, "- Home -\n")
    for y in home.roster:
        text2.insert(END, y.name + "\n")
    text2.insert(END, "- Visitors -\n")
    for y in visitor.roster:
        text2.insert(END, y.name + "\n")


def selecttarget(thrower, opponents):
    # check for panic throw
    target = random.choice(opponents.roster)
    if random.randrange(1, 100) < getgauss(thrower.nerves, thrower.pconsist):
        for x in opponents.roster:
            if target.targetvalue(thrower) < x.targetvalue(thrower):
                target = x
                val = x.targetvalue
    # print(str(thrower.name) + " throws at " + str(target.name))
    return target

def throw(thrower, defender):
    incomingpower = getgauss(thrower.tpower, thrower.pconsist)
    incomingaccuracy = getgauss(thrower.taccuracy, thrower.pconsist)
    # check to see if throw on target
    if random.randrange(1, 100) < incomingaccuracy:
        # check to see if defender notices
        if random.randrange(1, 100) < defender.awareness:
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
                return "hit"
            else:
                return defense

        else:
            # unaware player gets no chance to defend
            return "hit"

    else:
        # throw accuracy was too low
        return "miss"

def varyby(stat):
    return random.uniform(1 - ((101 - stat) / 100), 1 + ((101 - stat) / 100))

def getgauss(a, b):
    return random.gauss(a, math.sqrt(100-b) * 1.5)

def calcdev(x):
    return math.sqrt(101-x)

root.mainloop()
