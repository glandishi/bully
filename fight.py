# Fight
def fightstance():
	global player, enemy, dropcons
	trauma = 0
	print("Fight is started!")
	print(
		"--You will hit first since you are more agile" if player.agi > enemy.agi else "--Enemy will hit first since he is more agile")

	def choose():
		print(pnt('green', "YOU [%d/%d]") % (player.hp, player.maxhp))
		print(pnt('red', "%s [%d/%d]") % (enemy.classp, enemy.hp, enemy.maxhp))
		choice = input("Your choice:\n")
		if check() == 1:
			if choice == "k":
				fight()
			elif choice == "d":
				print("Enemy Arm:%d\tLeg:%d\tJaw:%d" % (enemy.brokenarm, enemy.brokenleg, enemy.brokenjaw))
			elif choice == "a":
				print(enemy.aboutEnemy())
			elif choice == "q":
				print(player.about())
			elif choice == 'i':
				print(player.inventory())
			elif choice.startswith("in"):
				invar = choice.split()
				if (len(invar) == 2):
					info('pl', invar[1])
				elif (len(invar) > 2):
					info(invar[1], invar[2])
				else:
					print("Usage - 'info agi' will show player agi")
			elif choice == "b":
				if player.canYouEat():
					print(useItem('beer'))
				else:
					print("--Your jaw is broken. You can't eat, drink or smoke.")
			elif choice == "j":
				if player.canYouEat():
					print(useItem('joint'))
				else:
					print("--Your jaw is broken. You can't eat, drink or smoke.")
			elif choice == "s":
				if player.canYouEat():
					print(useItem('sunseeds'))
				else:
					print("--Your jaw is broken. You can't eat, drink or smoke.")
			elif choice == "ke":
				if player.canYouEat():
					print(useItem('kebab'))
				else:
					print("--Your jaw is broken. You can't eat, drink or smoke.")
			else:
				print("You're in combat. Can't do this")
		elif check() == 2:
			win()
		elif check() == 3:
			lose()

	def check():
		if enemy.hp > 0 and player.hp > 0:
			return 1  # Fight proceed
		elif enemy.hp <= 0 and player.hp > 0:
			return 2  # Player won
		elif player.hp <= 0 and enemy.hp > 0:
			return 3  # Enemy won
		elif enemy.hp <= 0 and player.hp <= 0:
			return 4  # Both dead

	def win():
		global enemy, player, dropcons
		print(pnt('sel', pnt('blue', "You won!")))
		enemy.calculateExp()
		player.exp += enemy.dropexp
		print(pnt('sel', pnt('brown', "You got %d EXP")) % enemy.dropexp + "(%d/%d)" % (player.exp, player.exp4lvl))
		drop = enemy.calculateDrop()
		if drop in (1, 3, 4):
			if drop == 1:
				player.money += enemy.dropmoney
				print(pnt('green', "You searched enemy body and found %d$") % enemy.dropmoney)
			elif drop == 3:
				if list(dropcons)[0] not in player.consumable:
					player.consumable.update(dropcons)
				else:
					player.consumable[list(dropcons)[0]] += 1
				print(pnt('violet', pnt('sel', "Looks like enemy had something in his pockets. %s+1")) % list(dropcons)[
					0])
				dropcons = {}
			elif drop == 4:
				print("You found some " + pnt('ital', 'rocks!'))
		else:
			print("You'd searched enemy body but found nothing useful")
		player.lvlUp()
		enemy = ''
		return 1

	def lose():
		print("You lose, cyka! Cya~")
		time.sleep(5)
		os.system('cls')
		exit()

	def plrdmg():
		crit = player.isCrit()
		# print("crit is %d" % crit)
		plrdmg = int(
			(random.randrange(int(player.mindmg if player.mindmg > 1 else 0), int(player.maxdmg)) - (int(enemy.vit) / 3 + int(enemy.defence))) * (
						1 - enemy.defence / 100)) if crit == 0 else int(
			random.randrange(int(player.mindmg), int(player.maxdmg)) * 1.75) + int(player.critdmg)
		# print("plrdmg is %d" % plrdmg)
		if enemy.hp > 0:
			if crit == 1:
				enemy.hp -= plrdmg
				if enemy.hp > 0:
					traumaChance = random.randrange(1, 11)
					if traumaChance > 6:
						trauma = enemy.isTrauma()
						# print("trauma:",trauma)
						shitChance = random.randrange(1, 11)
						whatBroken = (
							'arm' if trauma == 2 else ('leg' if trauma == 1 else ('jaw' if trauma == 3 else '0')))
						# print("whatBroken:",whatBroken)
						if whatBroken != '0':
							print(pnt("green", "|") + pnt('red',
														  "CRITICAL STRIKE! You broke enemy's %s.") % whatBroken + " Enemy suffers " + pnt(
								'red', "%d DMG. ") % plrdmg + "He still have %d/%d HP" % (enemy.hp, enemy.maxhp))
						else:
							print(pnt("green", "|") + pnt('red', "CRITICAL STRIKE!") + " Enemy suffers " + pnt('red',
																											   "%d DMG. ") % plrdmg + "He still have %d/%d HP" % (
								  enemy.hp, enemy.maxhp))
						if shitChance > 6 and enemy.crap == 0:
							enemy.isCrap()
							print(pnt("green", "|") + pnt("yellow", "Enemy crapped himself. ") + "Nice job!")
					else:
						print(pnt("green", "|") + pnt('red', "CRITICAL STRIKE!!!") + " Enemy suffers " + pnt('red',
																											 "%d DMG ") % plrdmg + "He still have %d/%d HP" % (
							  enemy.hp, enemy.maxhp))
						shitChance = random.randrange(1, 11)
						if shitChance > 6 and enemy.crap == 0:
							enemy.isCrap()
							print(pnt("green", "|") + pnt("yellow", "Enemy crapped himself. ") + "Nice job!")
				else:
					print(pnt("green", "|") + pnt('red',
												  "Wow!") + " You killed your enemy with critical strike - %d DMG" % plrdmg)
					enemy.dead = 1
					win()
			else:
				if isHit():
					enemy.hp -= plrdmg
					if enemy.hp < 0:
						print(pnt("green", "|") + "You hit your opponent for %d DMG. He is dead now" % (plrdmg))
						enemy.dead = 1
						win()
					else:
						traumaChance = random.randrange(1, 101)
						if plrdmg > 0:
							if traumaChance <= (
							player.str / 2 - enemy.vit if player.classP != 2 else player.str / 2 + 7 - enemy.vit):
								trauma = enemy.isTrauma()
								whatBroken = ('arm' if trauma == 2 else (
									'leg' if trauma == 1 else ('jaw' if trauma == 3 else '0')))
								if whatBroken != '0':
									print(pnt("green", "|") + pnt('sel', "You broke enemy's %s" % whatBroken))
									print(pnt("green",
											  "|") + "You hit your opponent for %d DMG. He still have %d/%d HP" % (
										  plrdmg, enemy.hp, enemy.maxhp))
								else:
									print(pnt("green",
											  "|") + "You hit your opponent for %d DMG. He still have %d/%d HP" % (
										  plrdmg, enemy.hp, enemy.maxhp))
							else:
								print(pnt("green", "|") + "You hit your opponent for %d DMG. He still have %d/%d HP" % (
								plrdmg, enemy.hp, enemy.maxhp))
						else:
							print(pnt("green", "|") + "You hit your enemy for no damage. What a pity!")
				else:
					print(pnt("green", "|") + pnt('ital', "You missed"))

	def enmdmg():
		crit = enemy.isCrit()
		enmdmg = ((random.randrange(int(enemy.mindmg if enemy.mindmg > 1 else 0), int(enemy.maxdmg)) - (player.vit / 3 + player.defence)) * (
					1 - player.defence / 100)) if crit == 0 else int(
			random.randrange(int(enemy.mindmg), int(enemy.maxdmg)) * 1.75) + enemy.critdmg
		if enmdmg <= 0:
			print(pnt("red", "|") + "Opponent hit you for no damage. Its only makes you stronger")
		else:
			if crit == 1:
				player.hp -= enmdmg
				if player.hp > 0:
					traumaChance = random.randrange(1, 11)
					if traumaChance > 6:
						trauma = player.isTrauma()
						shitChance = random.randrange(1, 11)
						whatBroken = (
							'arm' if trauma == 2 else ('leg' if trauma == 1 else ('jaw' if trauma == 3 else '0')))
						if whatBroken != '0':
							print(pnt("red", "|") + "%s hit you with " % enemy.classp + pnt('red',
																							"CRITICAL") + " for %d DMG. " % enmdmg + pnt(
								'sel', "He broke your %s") % whatBroken + " You still have %d/%d HP" % (
								  player.hp, player.maxhp))
						else:
							print(pnt("red", "|") + "%s hit you with " % enemy.classp + pnt('red',
																							"CRITICAL") + " for %d DMG. It hurts!!! You still have %d/%d HP" % (
								  enmdmg, player.hp, player.maxhp))
						if shitChance > 6 and player.crap == 0:
							player.isCrap()
							print(pnt("red", "|") + "Huuuuge blow. " + pnt("yellow",
																		   "You'd crapped yourself. ") + "That's gross!\n[" + pnt(
								"green", "FLEE+25% CRIT+5 ") + pnt('red', "HIT-40%") + "]")
					else:
						print(pnt("red", "|") + "%s hit you with " % enemy.classp + pnt('red',
																						"CRITICAL") + " for %d DMG. It hurts!!! You still have %d/%d HP" % (
							  enmdmg, player.hp, player.maxhp))
						shitChance = random.randrange(1, 11)
						if shitChance > 6 and player.crap == 0:
							player.isCrap()
							print(pnt("red", "|") + "Huuuuge blow. " + pnt("yellow",
																		   "You'd crapped yourself. ") + "That's gross!\n[" + pnt(
								"green", "FLEE+25% CRIT+5 ") + pnt('red', "HIT-40%") + "]")
				else:
					print(pnt("red", "|") + "Critical hit to the grave. " + pnt('red', "YOU DIED"))
					player.dead = 1
					lose()
			else:
				if isFlee():
					player.hp -= enmdmg
					if player.hp <= 0:
						print(pnt("red", "|") + "%s hit you for %d DMG." % (enemy.classp, enmdmg) + pnt('red',
																										" YOU DIED"))
						lose()
					else:
						traumachance = random.randrange(1, 101)
						if traumachance <= (
						enemy.str / 2 - player.vit if enemy.classP != 2 else enemy.str / 2 + 7 - player.vit):
							trauma = player.isTrauma()
							whatBroken = (
								'arm' if trauma == 2 else ('leg' if trauma == 1 else ('jaw' if trauma == 3 else '0')))
							if whatBroken != '0': print(pnt('sel', "Enemy broke your %s" % whatBroken))
						print(pnt("red", "|") + "%s hit you for %d DMG. You still have " % (enemy.classp, enmdmg) + (
							pnt('red', "%d/%d HP") % (
							player.hp, player.maxhp) if player.hp <= player.maxhp * .25 else "%d/%d HP" % (
							player.hp, player.maxhp)))
				else:
					print(pnt("red", "|") + pnt('ital', "Enemy missed and you gain some HP"))
					player.regen()

	def isHit():
		rand = random.randrange(1, 101)
		result = (player.hit + 50) - enemy.flee
		if rand < result:
			return 1  # Player scored hit
		else:
			return 0  # Player missed

	def isFlee():
		rand = random.randrange(1, 101)
		result = (enemy.hit + 50) - player.flee
		if rand < result:
			return 1  # Enemy scored hit
		else:
			return 0  # Enemy missed

	def fight():  # brawl
		def playerTurn():
			blows = int(player.speed + 1) if int(player.agi) % 10 > random.randrange(1, 11) else int(player.speed)
			for i in range(blows):
				if i > 0 and enemy != '':
					suff = ("nd" if i == 1 else ("rd" if i == 2 else "th"))
					print(pnt("green", "|") + "Since you are so agile you can make " + pnt('ital', "%d%s") % (
					1 + int(i), suff) + " attack")
					plrdmg()
				elif i > 0 and enemy == '':
					return 0
				else:
					plrdmg()

		def enemyTurn():
			if enemy != '':
				enblows = int(enemy.speed + 1) if enemy.agi % 10 > random.randrange(1, 11) else int(enemy.speed)
				for i in range(enblows):
					if i > 0 and player.hp > 0:
						suff = ("nd" if i == 1 else ("rd" if i == 2 else "th"))
						print(pnt("red", "|") + "Since your enemy is so agile he can make %d%s attack" % (
						1 + int(i), suff))
						enmdmg()
					elif i > 0 and player.hp <= 0:
						lose()
					else:
						enmdmg()

		if player.agi > enemy.agi:
			print(pnt("green", "------------"))
			playerTurn()
			print(pnt("green", "------------"))
			print(pnt("red", "------------"))
			enemyTurn()
			print(pnt("red", "------------"))
		else:
			print(pnt("red", "------------"))
			enemyTurn()
			print(pnt("red", "------------"))
			print(pnt("green", "------------"))
			playerTurn()
			print(pnt("green", "------------"))

	while enemy != '':
		try:
			choose()
		except Exception as e:
			print(e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
	else:
		return 0
