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

root = Tk()
root.wm_title("Genetic Dodgeball")


freeagents = []
teams = []
usednames = []
curnum = 1


# global variables for decoding genomes
posfactor = 4
divfactor = 4.5
negfactor = 20



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


def all_the_players():
    for team in teams:
        for player in team.roster:
            yield player


def best_player(stat_name):
    return max(all_the_players(), key=operator.attrgetter(stat_name))


sclamp = lambda n: round(max(min(100, n), 1))

class Team:
    def __init__(self, city, name, roster):
        self.name = name
        self.roster = roster
        self.fullname = city + " " + name
        self.id = random.randrange(10, 9999999)

        self.wins = 0
        self.losses = 0
        self.active = True

        self.winpercentage = 0.000

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
            x = 1.000
        else:
            x = round(self.wins/(self.wins + self.losses), 3)
        self.winpercentage = x

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

        # print("the dodge for ", self.name, " is ", str(self.dodge))
        # print("the catch for ", self.name, " is ", str(self.catch))
        # print("the flair for ", self.name, " is ", str(self.flair))

        # all players start alive
        self.alive = True
        self.ingame = True
        self.team = False

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

def newplayers(x):
    freeagents.clear()
    for i in range(1, x):
        freeagents.append(createplayer())

    ticker = 0
    for player in freeagents:
        if player.taccuracy < 45 or player.pconsist or player.awareness < 33:
            ticker += 1
            freeagents.pop(freeagents.index(player))

    print(ticker)

    taccs = []
    for player in freeagents:
        taccs.append(player.taccuracy)

    print(statistics.mean(taccs))


def newteams(x):
    teams.clear()
    filename = open("AnimalNames.txt")
    namelist = [i.strip() for i in filename.readlines()]
    filename.close()

    filename = open("Cities.txt")
    citylist = [i.strip() for i in filename.readlines()]
    filename.close()

    # make x number of teams
    for i in range(0, x):
        teams.append(Team(citylist.pop(random.randint(0, len(citylist)-1)), namelist.pop(random.randint(0, len(namelist)-1)), []))

    for team in teams:
        for i in range(0, 5):
            pick_player = random.randint(0, len(freeagents)-1)
            addplayer(freeagents[pick_player], team)

def remplayer(player, team):
    player.team = False
    freeagents.append(team.roster.pop(team.roster.index(player)))


def addplayer(player, team):
    player.team = team
    team.roster.append(freeagents.pop(freeagents.index(player)))

def newleaguebutton():
    for child in mainbox.winfo_children():
        child.destroy()

    newplayers(500)
    newteams(8)
    pickyourteam()


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

    updatestats()
    leaguestandings()

def leaguestandings():
    for child in mainbox.winfo_children():
        child.destroy()

    tempframe = Frame(mainbox, height=300, width=600)
    tempframe.pack()

    for i in teams:
        words = "%s  %s - %s (%s) [%s]" % (i.fullname, str(i.wins), str(i.losses), ('%.3f' % i.winpercentage), str(i.offrating() +i.defrating()))
        Label(tempframe, text=words).pack()


def playerstats():
    for child in mainbox.winfo_children():
        child.destroy()

    print(theowner.team.fullname)

    tempframe = Frame(mainbox, height=300, width=600)
    tempframe.pack()

    player_with_most_hits = best_player('career_hits')
    words = "League leader in hits - %s of the %s (%s)" % (player_with_most_hits.fullname, player_with_most_hits.team.fullname, player_with_most_hits.career_hits)
    Label(tempframe, text=words).pack()

    player_with_most_catches = best_player('career_catch_succ')
    words = "League leader in catches - %s of the %s (%s)" % (player_with_most_catches.fullname, player_with_most_catches.team.fullname, player_with_most_catches.career_catch_succ)
    Label(tempframe, text=words).pack()

    player_with_most_dodges = best_player('career_dodge_succ')
    words = "League leader in dodges - %s of the %s (%s)" % (player_with_most_dodges.fullname, player_with_most_dodges.team.fullname, player_with_most_dodges.career_dodge_succ)
    Label(tempframe, text=words).pack()

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

    Label(tempframe, text="\nLeague Totals\n").pack()
    words = "%s hits   %s misses   %s dodges   %s catches" % (total_hits, total_misses, total_dodge, total_catch)
    Label(tempframe, text=words).pack()

    words = "%s total throws" % total_throws
    Label(tempframe, text=words).pack()

    words = "%s average throw accuracy" % str(round(statistics.median(accuracies), 1))
    Label(tempframe, text=words).pack()

    words = "%s average throw difficulty" % str(round(statistics.mean(difficulties), 1))
    Label(tempframe, text=words).pack()



def pickteams(x):
    i = 0
    while i < x:
        home = random.choice(teams)
        visitor = home
        while home == visitor:
            visitor = random.choice(teams)
        throwround(home, visitor)
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


def testprint(words):
    print(words)

def begingame(team):
    for child in mainbox.winfo_children():
        child.destroy()

    drawtoolbar()



    # name = get_player_name.get()
    theowner.team = team
    Label(mainbox, text="You are now the owner of the %s" % theowner.team.fullname).grid(row=0, column=0)
    print("%s" % theowner.team.fullname)

# interface

def drawtoolbar():
    toolbar = Frame(root, bg="blue")

    newplayersbutton = Button(toolbar, text="New League", command=newleaguebutton)
    newplayersbutton.pack(side=LEFT, padx=2, pady=2)

    # rosterTestButton = Button(toolbar, text="Show Random Roster", command=randomroster)
    # rosterTestButton.pack(side=LEFT, padx=2, pady=2)

    playseasonbutton = Button(toolbar, text="Play Full Season", command=playseason)
    playseasonbutton.pack(side=LEFT, padx=2, pady=2)

    leaguestandingsbutton = Button(toolbar, text="League Standings", command=leaguestandings)
    leaguestandingsbutton.pack(side=LEFT, padx=2, pady=2)

    playerstatsbutton = Button(toolbar, text="Player Stats", command=playerstats)
    playerstatsbutton.pack(side=LEFT, padx=2, pady=2)

    testtargetbutton = Button(toolbar, text="Random Game", command=lambda: pickteams(10))
    testtargetbutton.pack(side=LEFT, padx=2, pady=2)

    # testTargetButton = Button(toolbar, text="Random Game", command=lambda: throwround(teams[0], teams[1]))
    # testTargetButton.pack(side=LEFT, padx=2, pady=2)

    # testGenomeButton = Button(toolbar, text="Generate Genome", command=creategenome())
    # testGenomeButton.pack(side=LEFT, padx=2, pady=2)

    toolbar.pack(side=TOP, fill=X)

mainbox = Frame(root)
mainbox.pack(side=BOTTOM)

Label(mainbox, text="Owner Name").grid(row=0, column=0)
get_player_name = Entry(mainbox)
get_player_name.grid(row=0, column=1)

Label(mainbox, text="Team City").grid(row=1, column=0)
get_team_city = Entry(mainbox)
get_team_city.grid(row=1, column=1)

newleaguebutton()

# startButton = Button(mainbox, text="START!", command=begingame)
# startButton.grid(row=2, columnspan=2)





def updatestats():
    for i in teams:
        i.winpercent()

    teams.sort(key=lambda x: x.winpercentage, reverse=True)
    # teams.sort(winpercentage, reverse=True)


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

difficulties = []
accuracies = []

def throw(thrower, defender):
    incomingpower = getgauss(thrower.tpower, thrower.pconsist)
    incomingaccuracy = getgauss(thrower.taccuracy, thrower.pconsist)
    throwdifficulty = getgauss(45, 25)
    difficulties.append(throwdifficulty)
    accuracies.append(incomingaccuracy)
    # check to see if throw on target
    if throwdifficulty < incomingaccuracy:
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
