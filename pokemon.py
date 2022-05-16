import random
random.seed(a=None, version=2)

type_multipliers={"normal>normal":1,"normal>fire":1,"normal>water":1,"normal>grass":1,"normal>electric":1,"normal>fighting":1,"fire>normal":1,"fire>fire":0.5,"fire>water":0.5,"fire>grass":2,"fire>electric":1,"fire>fighting":1,"water>normal":1,"water>fire":2,"water>water":0.5,"water>grass":0.5,"water>electric":1,"water>fighting":1,"grass>normal":1,"grass>fire":0.5,"grass>water":2,"grass>grass":0.5,"grass>electric":1,"grass>fighting":1,"electric>normal":1,"electric>fire":1,"electric>water":2,"electric>grass":0.5,"eletric>electric":0.5,"electric>fighting":1,"fighting>normal":2,"fighting>fire":1,"fighting>water":1,"fighting>grass":1,"fighting>electric":1,"fighting>fighting":1}
#damage multiplier in the format attacking_move_type>defender_type:X

move_list={"Pokemon_switched_out":(10000,100,"normal",0,"n/a"),"Quick Attack":(200,100,"normal",40,"n/a"),"Strength":(0,100,"normal",80,"n/a"),"Hydro Pump":(0,80,"water",120,"n/a"),"Protect":(1000,100,"normal",0,"movedmgtopoke",lambda x: x*0),"Aqua Ring":(0,100,"water",0,"movedmgtopoke",lambda x: x-100),"Headbutt":(1000,100,"normal",70,"movedmgtopoke",lambda x: x*(random.choice([1,1,1,1,1,1,1,0,0,0]))),"Low Sweep":(0,100,"fighting",60,"speeddmgfrompoke",lambda x: x+5),"Bubble":(0,100,"water",40,"speeddmgfrompoke",lambda x: x+8),"Electroweb":(0,95,"electric",55,"speeddmgfrompoke",lambda x: x+6),"Low Kick":(1000,100,"fighting",50,"movedmgtopoke",lambda x: x*(random.choice([1,1,1,1,1,0,0,0,0,0]))),"Thunder Fang":(1000,100,"electric",80,"movedmgtopoke",lambda x: x*(random.choice([1,1,1,1,1,1,1,1,1,0]))),"Fire Blast":(-2,85,"fire",110,"n/a"),"Flamethrower":(0,100,"fire",90,"n/a"),"Wood Hammer":(0,100,"grass",120,"movedmgtopoke",lambda x: x+40),"Self-Destruct":(0,100,"normal",300,"movedmgtopoke",lambda x: x+10000),"Giga Drain":(0,100,"grass",70,"movedmgtopoke",lambda x: x-35),"Razor Leaf":(0,100,"grass",30*random.choice([1,1,4]),"n/a")}
#{"name":(priority,accuracy,type,dmg,optional secondary variable,optiional secondary effect outcome)}
pokedex={"Pikachu":(300,5,"electric","Quick Attack","Thunder Fang","Headbutt","Protect"),"Galvantula":(400,4,"electric","ElectroWeb","Thunder Fang","Self-Destruct","Strength"),"Machop":(400,5,"fighting","Low Kick","Strength","Low Sweep","Headbutt"),"Lucario":(350,6,"fighting","Low Sweep","Quick Attack","Protect","Thunder Fang"), "Oshowatt":(250,6,"water","Hydro Pump","Protect","Bubble","Low Kick"),"Milotic":(400,3,"water","Aqua Ring","Bubble","Quick Attack","Headbutt"),"Ninetails":(350,4,"fire","Fire Blast","Flamethrower","Headbutt","Protect"),"Infernape":(300,5,"fire","Fire Blast","Low Kick","Self-Destruct","Quick Attack"),"Snivy":(250,6,"grass","Razor Leaf","Protect","Wood Hammer","Headbutt"),"Cacturne":(400,4,"grass","Wood Hammer","Giga Drain","Strength","Low Sweep"),"Snorlax":(550,1,"normal","Headbutt","Strength","Wood Hammer","Low Sweep"),"Farfetch’d":(350,5,"normal","Low Kick","Razor Leaf","Quick Attack","Strength")}
#{"name":(hp,speed,type,move1,move2,move3,move4)}

active_pokemon_team1=""
active_pokemon_team2=""
#initializing active_pokemon_teamX, will be changed later

#the following is a function to resolve turns given poke1 (the pokemon of team 1), poke2, and the queued moves for each
def resolve_turns(poke1,move1,poke2,move2):
    global current_turn
    global team1
    global team2
    global active_pokemon_team1
    global active_pokemon_team2
    
    #determining incoming damage
    poketype1=team1[poke1][2]
    poketype2=team2[poke2][2]
    movetype1=move_list[move1][2]
    movetype2=move_list[move2][2]
    movedmgtopoke1=(type_multipliers[movetype2+">"+poketype1])*(move_list[move2][3])
    movedmgtopoke2=(type_multipliers[movetype1+">"+poketype2])*(move_list[move1][3])
    #initializing speed damage, a modifier that may be invoked later depending on the queued moves
    speeddmgfrompoke1=0
    speeddmgfrompoke2=0
    
    #if speed of pokemon1 + priority of move1 is greater than that of pokemon2 and move2, move1 gets resolved first
    if team1[poke1][1] + move_list[move1][0]>=team2[poke2][1] + move_list[move2][0]:
        #special effects:
        if move_list[move1][4]!="n/a":
            locals()[str(move_list[move1][4])+"1"]=move_list[move1][5](locals()[str(move_list[move1][4])+"1"])
        if move_list[move2][4]!="n/a":
            locals()[str(move_list[move2][4])+"1"]=move_list[move2][5](locals()[str(move_list[move2][4])+"2"])
        #now we calculate damage and if move1 hits:
        if random.randrange(99)<move_list[move1][1]:
            team2.update({poke2:(team2[poke2][0]-movedmgtopoke2,team2[poke2][1]-speeddmgfrompoke1,team2[poke2][3],team2[poke2][4],team2[poke2][5],team2[poke2][5])})
            if team2[poke2][1]<=0:
                movedmgtopoke1=0
                del team2[poke2]
                if len(team2)>0:
                    active_pokemon_team2=input("Player 2: your pokémon has fainted. Choose one of the following to send in. " + " ".join(team2.keys()) + ": ")
                else:
                    print("Player 2, all your pokemon have now fainted. Player 1 wins!")
                    quit()
        #now we calculate damage and if move2 hits:
        if random.randrange(99)<move_list[move2][1]:
            team1.update({poke1:(team1[poke1][0]-movedmgtopoke1,team1[poke1][1]-speeddmgfrompoke2,team1[poke1][3],team1[poke1][4],team1[poke1][5],team1[poke1][5])})
            if team1[poke1][1]<=0:
                del team1[poke1]
                if len(team1)>0:
                    active_pokemon_team1=input("Player 1: your pokémon has fainted. Choose one of the following to send in. " + " ".join(team1.keys()) + ": ")
                else:
                    print("Player 1, all your pokemon have now fainted. Player 2 wins!")
                    quit()
    #if speed of pokemon2 + priority of move2 is greater than that of pokemon1 and move1, move2 gets resolved first
    else:
        #special effects:
        if move_list[move2][4]!="n/a":
            locals()[str(move_list[move2][4])+"1"]=move_list[move2][5](locals()[str(move_list[move2][4])+"2"])
        if move_list[move1][4]!="n/a":
            locals()[str(move_list[move1][4])+"1"]=move_list[move1][5](locals()[str(move_list[move1][4])+"1"])
        #now we calculate damage and if  move2 hits:
        if random.randrange(99)<move_list[move2][1]:
            team1.update({poke1:(team1[poke1][0]-movedmgtopoke1,team1[poke1][1]-speeddmgfrompoke2,team1[poke1][3],team1[poke1][4],team1[poke1][5],team1[poke1][5])})
            if team1[poke1][1]<=0:
                movedmgtopoke2=0
                del team1[poke1]
                if len(team1)>0:
                    active_pokemon_team1=input("Player 1: your pokémon has fainted. Choose one of the following to send in. " + " ".join(team1.keys()) + ": ")
                else:
                    print("Player 1, all your pokemon have now fainted. Player 2 wins!")
                    quit()
        #now we calculate damage and if move1 hits:
        if random.randrange(99)<move_list[move1][1]:
            team2.update({poke2:(team2[poke2][0]-movedmgtopoke2,team2[poke2][1]-speeddmgfrompoke1,team2[poke2][3],team2[poke2][4],team2[poke2][5],team2[poke2][5])})
            if team2[poke2][1]<=0:
                del team2[poke2]
                if len(team2)>0:
                    active_pokemon_team2=input("Player 2: your pokémon has fainted. Choose one of the following to send in. " + " ".join(team2.keys()) + ": ")
                else:
                    print("Player 2, all your pokemon have now fainted. Player 1 wins!")
                    quit()
    print("Player 1: " + active_pokemon_team1 + " took " + str(movedmgtopoke1) + " damage and has " + str(team1[active_pokemon_team1][0]) + "/" + str(pokedex[active_pokemon_team1][0]) + " hp left. Its speed was decreased by " + str(speeddmgfrompoke2) + ".")
    print("Player 2: " + active_pokemon_team2 + " took " + str(movedmgtopoke2) + " damage and has " + str(team2[active_pokemon_team2][0]) + "/" + str(pokedex[active_pokemon_team2][0]) + " hp left. Its speed was decreased by " + str(speeddmgfrompoke1) + ".")
    print("A new round begins.")
    current_turn="turn1"

# -----------

choices=input("Player 1: choose your team of 6 pokémon (seperated by spaces) from the following list: " + " ".join(pokedex.keys()) + " // ")
choices=choices.split()
#choosing pokemon

team1={choices[0]:pokedex.get(choices[0]),choices[1]:pokedex.get(choices[1]),choices[2]:pokedex.get(choices[2]),choices[3]:pokedex.get(choices[3]),choices[4]:pokedex.get(choices[4]),choices[5]:pokedex.get(choices[5])}
#making new dictionary for team1

choices=input("Player 2: choose your team of 6 pokémon (seperated by spaces) from the following list: " + " ".join(pokedex.keys()) + " // ")
choices=choices.split()
#choosing pokemon

team2={choices[0]:pokedex.get(choices[0]),choices[1]:pokedex.get(choices[1]),choices[2]:pokedex.get(choices[2]),choices[3]:pokedex.get(choices[3]),choices[4]:pokedex.get(choices[4]),choices[5]:pokedex.get(choices[5])}
#making new dictionary for team2

# -----------

active_pokemon_team1=str(input("Player1: Choose pokémon to send in. " + " // ".join(team1.keys()) + ": "))
t1move1=team1[active_pokemon_team1][3]
t1move2=team1[active_pokemon_team1][4]
t1move3=team1[active_pokemon_team1][5]
t1move4=team1[active_pokemon_team1][6]

active_pokemon_team2=str(input("Player2: Choose pokémon to send in. " + " // ".join(team2.keys()) + ": "))
t2move1=team2[active_pokemon_team2][3]
t2move2=team2[active_pokemon_team2][4]
t2move3=team2[active_pokemon_team2][5]
t2move4=team2[active_pokemon_team2][6]

#starting combat
combat="ongoing"
while combat=="ongoing":
    
    current_team=team1
    #this means it is turn1
    
    turn1=input("Player1: 'Swap' or 'Fight'? ")
    if turn1=="Fight" or turn1=="F":
        queued_move_team1=input("Player1: pick a move. " + t1move1 + " // " + t1move2 + " // " + t1move3 + " // " + t1move4 + ": ")
    if turn1=="Swap" or turn1=="S":
        active_pokemon=input("Player1: Choose pokémon to send in. " + " // ".join(team1.keys()) + ": ")
        
        t1move1=team1[active_pokemon_team1][3]
        t1move2=team1[active_pokemon_team1][4]
        t1move3=team1[active_pokemon_team1][5]
        t1move4=team1[active_pokemon_team1][6]
        
        queued_move_team1="Pokemon_switched_out"
    
    current_team=team2
    #this means it is turn2
    
    turn2=input("Player2: 'Swap' or 'Fight'? ")
    if turn2=="Fight" or turn2=="F":
        queued_move_team2=input("Player2: pick a move. " + t2move1 + " // " + t2move2 + " // " + t2move3 + " // " + t2move4 + ": ")
    if turn2=="Swap" or turn2=="S":
        active_pokemon=active_pokemon_team2=input("Player2: Choose pokémon to send in. " + " // ".join(team2.keys()) + ": ")
        
        t2move1=team2[active_pokemon_team2][3]
        t2move2=team2[active_pokemon_team2][4]
        t2move3=team2[active_pokemon_team2][5]
        t2move4=team2[active_pokemon_team2][6]
        
        queued_move_team2="Pokemon_switched_out"
        
    resolve_turns(active_pokemon_team1,queued_move_team1,active_pokemon_team2,queued_move_team2)


#  :)
