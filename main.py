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
        self.id = random.randrange(10, 9999999)

        troster = []
        for x in self.roster:
            troster.append(x.rating)

        self.consistency = round(statistics.stdev(troster))

        self.wins = 0
        self.losses = 0
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

    def playersleft(self):
        ticker = 0
        for x in self.roster:
            if x.ingame:
                ticker += 1
        return ticker

    def winpercent(self):
        if self.losses == 0:
            return 1.000
        else:
            return round(self.wins/(self.wins + self.losses), 3)

class Player:
    def __init__(self, name, number, genome):
        self.formalname = name
        self.firstname = self.formalname.split()[0]
        self.lastname = self.formalname.split()[1]
        self.fullname = name
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
        self.ingame = True
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
        self.career_hits = 0
        self.career_misses = 0
        self.career_wasdodged = 0
        self.career_wascaught = 0
        self.career_blindsided = 0
        self.career_assassinations = 0
        self.career_wins = 0
        self.career_losses = 0

    def targetvalue(self, thrower):
        x = ((self.offense * thrower.offhate) + (self.defense * thrower.defhate) +
             (self.intangibles * thrower.inthate) + (self.personality * thrower.pershate)) * varyby(thrower.tactics)
        # print(self.name, str(x))
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
            print(i.number, " ", i.fullname, " ", i.dodge)
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
        Label(tempframe, text=i.fullname).grid(row=ticker, column=1)
        Label(tempframe, text=i.dodge).grid(row=ticker, column=2)
        Label(tempframe, text=i.catch).grid(row=ticker, column=3)
        Label(tempframe, text=i.accuracy).grid(row=ticker, column=4)
        Label(tempframe, text=i.power).grid(row=ticker, column=5)
        Label(tempframe, text=i.stamina).grid(row=ticker, column=6)
        Label(tempframe, text=i.awareness).grid(row=ticker, column=7)
        Label(tempframe, text=i.tactics).grid(row=ticker, column=8)
        Label(tempframe, text=i.rating).grid(row=ticker, column=9)
        ticker += 1

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
                throwround(teams[i], teams[j])

    # sort teams by win percent
    # teams.sort(key=operator.attrgetter("winpercent"), reverse=True)

def leaguestandings():
    for child in mainbox.winfo_children():
        child.destroy()

    tempframe = Frame(mainbox, height=300, width=600)
    tempframe.pack()

    for i in teams:
        words = "%s  %s - %s (%s) [%s]" % (i.name, str(i.wins), str(i.losses), ('%.3f' % i.winpercent()), str(i.offrating() +i.defrating()))
        Label(tempframe, text=words).pack()


def playerstats():
    for child in mainbox.winfo_children():
        child.destroy()

    tempframe = Frame(mainbox, height=300, width=600)
    tempframe.pack()

    xyz = []

    k = random.choice(random.choice(teams).roster)

    for i in teams:
        for j in i.roster:
            if j.career_hits > k.career_hits:
                k = j

    words = "League leader in hits - %s of Team %s (%s)" % (k.fullname, findteamname(k), k.career_hits)
    Label(tempframe, text=words).pack()


def findteamname(z):
    for x in teams:
        if x.id == z.teamid:
            return x.name
            break

def pickteams(x):
    i = 0
    while i < x:
        home = random.choice(teams)
        visitor = home
        while home == visitor:
            visitor = random.choice(teams)
        throwround(home, visitor)
        i += 1

# interface

newleaguebutton()

toolbar = Frame(root, bg="blue")

newPlayersButton = Button(toolbar, text="New League", command=newleaguebutton)
newPlayersButton.pack(side=LEFT, padx=2, pady=2)

# rosterTestButton = Button(toolbar, text="Show Random Roster", command=randomroster)
# rosterTestButton.pack(side=LEFT, padx=2, pady=2)

playSeasonButton = Button(toolbar, text="Play Full Season", command=playseason)
playSeasonButton.pack(side=LEFT, padx=2, pady=2)

leagueStandingsButton = Button(toolbar, text="League Standings", command=leaguestandings)
leagueStandingsButton.pack(side=LEFT, padx=2, pady=2)

playerStatsButton = Button(toolbar, text="Player Stats", command=playerstats)
playerStatsButton.pack(side=LEFT, padx=2, pady=2)

testTargetButton = Button(toolbar, text="Random Game", command=lambda: pickteams(10))
testTargetButton.pack(side=LEFT, padx=2, pady=2)

# testTargetButton = Button(toolbar, text="Random Game", command=lambda: throwround(teams[0], teams[1]))
# testTargetButton.pack(side=LEFT, padx=2, pady=2)

# testGenomeButton = Button(toolbar, text="Generate Genome", command=creategenome())
# testGenomeButton.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

mainbox = Frame(root, relief=SUNKEN)
mainbox.pack()



def throwround(team1, team2):
    for child in mainbox.winfo_children():
        child.destroy()
    #
    # tempframe = Frame(mainbox)
    # tempframe.pack()

    # text2 = Text(mainbox, height=40, width=60)
    # scroll = Scrollbar(mainbox, command=text2.yview)
    # text2.configure(yscrollcommand=scroll.set)
    # text2.pack(side=LEFT)
    # scroll.pack(side=RIGHT, fill=Y)

    text2 = Text(mainbox, height=40, width=60)
    scroll = Scrollbar(mainbox, command=text2.yview)
    text2.configure(yscrollcommand=scroll.set)
    text2.pack(side=LEFT)
    scroll.pack(side=RIGHT, fill=Y)

    home = team1
    visitor = team2

    text2.insert(END, "%s [%soff %sdef] vs. %s [%soff %sdef]\n" % (home.name, home.offrating(), home.defrating(),
                                                                   visitor.name, visitor.offrating(), visitor.defrating()))
    text2.insert(END, "- Home -\n")
    for y in home.roster:
        text2.insert(END, y.fullname + "\n")
    text2.insert(END, "- Visitors -\n")
    for y in visitor.roster:
        text2.insert(END, y.fullname + "\n")

    text2.insert(END, "Start Game!\n")

    # self.career_dodge_fail = 0
    # self.career_catch_fail = 0
    # self.career_deflect_fail = 0
    # self.career_dodge_succ = 0
    # self.career_catch_succ = 0
    # self.career_deflect_succ = 0
    # self.career_hits = 0
    # self.career_blindsided = 0
    # self.career_wins = 0
    # self.career_losses = 0

    # check to make sure no team is depleted to 0 players
    while home.playersleft() > 0 and visitor.playersleft() > 0:
        for x in home.roster:
            if x.ingame:
                target = selecttarget(x, visitor)
                if not target:
                    break
                result = throw(x, target)
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
                if result == "miss":
                    text2.insert(END, "%s's throw at %s goes wide!\n" % (x.fullname, target.fullname))
                    x.career_misses += 1

        text2.insert(END, "-- Switch Sides --\n")
        for x in visitor.roster:
            if x.ingame:
                target = selecttarget(x, home)
                if not target:
                    break
                result = throw(x, target)
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
                if result == "miss":
                    text2.insert(END, "%s's throw at %s goes wide!\n" % (x.fullname, target.fullname))
                    x.career_misses += 1

        text2.insert(END, "-- End of Round --\n")

    if home.playersleft() == 0:
        text2.insert(END, "-- Visitors Win --\n")
        visitor.wins += 1
        home.losses += 1
    else:
        text2.insert(END, "-- Home Wins --\n")
        home.wins += 1
        visitor.losses += 1

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

# def processthrow(x, y):
#     if x.ingame:
#         target = selecttarget(x, visitor)
#         if not target:
#             break
#         result = throw(x, target)
#         if result == "unawarehit":
#             text2.insert(END, "%s sees that %s unaware and hits him!\n" % (x.name, target.name))
#             target.career_blindsided += 1
#             x.career_hits += 1
#             target.ingame = False
#         if result == "catchfail":
#             text2.insert(END, "%s tries to catch a throw by %s but can't hold on!\n" % (target.name, x.name))
#             target.career_catch_fail += 1
#             x.career_hits += 1
#             target.ingame = False
#         if result == "dodgefail":
#             text2.insert(END, "%s fails to dodge a throw by %s!\n" % (target.name, x.name))
#             target.career_dodge_fail += 1
#             x.career_hits += 1
#             target.ingame = False
#         if result == "catch":
#             text2.insert(END, "%s's throw is caught by %s!\n" % (x.name, target.name))
#             target.career_catch_succ += 1
#             x.career_wascaught += 1
#             x.ingame = False
#         if result == "dodge":
#             text2.insert(END, "%s dodges a throw by %s!\n" % (target.name, x.name))
#             target.career_dodged_succ += 1
#             x.career_wasdodged += 1
#         if result == "miss":
#             text2.insert(END, "%s's throw at %s goes wide!\n" % (x.name, target.name))
#             x.career_misses += 1


def selecttarget(thrower, opponents):
    if opponents.playersleft() > 0:
        target = random.choice(opponents.roster)
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
    incomingpower = getgauss(thrower.tpower, thrower.pconsist)
    incomingaccuracy = getgauss(thrower.taccuracy, thrower.pconsist)
    throwdifficulty = getgauss(50, 25)
    # print("%s taccuracy %s incomingaccuracy %s throwdiff %s" % (thrower.name, thrower.taccuracy, incomingaccuracy, throwdifficulty))
    # check to see if throw on target
    if throwdifficulty < incomingaccuracy:
        # check to see if defender notices
        if getgauss(50, 25) < defender.awareness:
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

    else:
        # throw accuracy was too low
        return "miss"

def varyby(stat):
    return random.uniform(1 - ((101 - stat) / 100), 1 + ((101 - stat) / 100))

def getgauss(a, b):
    return sclamp(random.gauss(a, math.sqrt(100-b) * 1.5))

def calcdev(x):
    return math.sqrt(101-x)

root.mainloop()
