import random
import textwrap

def print_bold(msg, end="\n"):
	print("\033[1m" + msg + "\033[0m", end =end)

def print_dotted_lines(width=100):
	print("_"*width)

def occupy_huts(occupants):
	hut = []
	for xc in range(5):
		occupant = random.choice(occupants)
		hut.append(occupant)

	return hut

def game_mission():
	width = 100
	occupants = ["enemy", "native", "no_occupant"]
	print_dotted_lines()
	game_title = "War of Alex and Orchs"
	print_bold(msg = game_title)
	msg = ("The war between humans and Orchs has begun. Alexander was one of"
		" the brave knights gaurding the eastern plains belong to his kingdom."
		" Due to war strategy to defend themselves orchs intruded into huts of the people"
		" Alex doesn't know this he decided to get some water from the occupants"
		" nearby and take rest for sometime. so he went towards village"
		" where 5 huts was their since no one was their he decided to knock at the door.")
	print(textwrap.fill(msg, width= width))
	print("\n")
	print_bold(msg="Mission:")
	print("Choose the hut where Alexander can get some water and rest")
	print_dotted_lines()

	return occupants

def choose_huts():
	msg = "choose a hut number to enter [1-5]: "
	#print_bold(msg=msg)
	input_user = input("\n" + msg)
	idx = int(input_user)

	return idx

def revealing_occupants(hut, idx):
	print("Revealing the occupants")
	msg = ""
	for x in range(len(hut)):
		if x +1 == idx:
			occupant_info = "Hut {} : {}".format(idx, hut[x])
			print_bold(msg=occupant_info)
	print_dotted_lines()

def entering_hut(hut, idx, health_meter):
	msg = "Entering hut..."
	print_bold(msg=msg, end = " ")
	if hut[idx-1] =="enemy":
		print_bold(msg="Enemy Spotted..!!!", end=" ")
		continue_attack = True
		while continue_attack == True:
			user_decision = input("\n Do you wish to fight yes(y)/no(n)? ")
			if user_decision == "n":
				print("Running away with current heath status")
				show_health_meter(health_meter)
				fail = "YOU LOSE :( Better luck next time..."
				print_bold(msg = fail)
				break

			health_meter = attack_function(health_meter)

			if health_meter['orchs'] <=0:
				print_bold(msg = "Good Job..!!! :) You defeated the orchs in this hut {}".format(idx))
				show_health_meter(health_meter)
				print_dotted_lines()
				break

			if health_meter['alex'] <= 0:
				print_bold(msg = "You Lose..!!! :( Better luck next time.")
				print_dotted_lines()
				break
	else:
		passed = "CONGRATULATIONS :) You Win..!!!"
		print_bold(msg = passed)
	print_dotted_lines()

def reset_health_meter():
	health_meter ={}
	health_meter['alex'] = 50
	health_meter['orchs'] = 30

	return health_meter

def show_health_meter(health_meter):
	print("\n")
	print("Alexander Health: " , health_meter['alex'])
	print("Orch's Health: ", health_meter['orchs'])

def attack_function(health_meter):
	# programming attack of alex has a prob of 0.6 and orch have 0.4
	player_rand_choice = ['alex']* 4 + ['orchs']*6
	hit_player = random.choice(player_rand_choice)
	hit_strength = random.choice([5,10,15])
	hit_points = health_meter[hit_player]
	health_meter[hit_player] = max(hit_points - hit_strength, 0)
	show_health_meter(health_meter)

	return health_meter

def run_application():
	keep_playing = "y"
	occupants = game_mission()
	health_meter = reset_health_meter()
	while keep_playing == "y":
		huts = occupy_huts(occupants = occupants)
		user_choice = choose_huts()
		revealing_occupants(hut = huts, idx=user_choice)
		entering_hut(hut=huts, idx = user_choice, health_meter = health_meter)
		keep_playing = input("Play Again? Yes(y), No(n): ")

if __name__ == "__main__":
	run_application()