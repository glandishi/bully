import random,sys,os,time,inspect,curses
class Person(object):
	def __init__(self,name,str,dex,agi,vit,luk,classP,lvl):
 		self.name,self.str,self.dex,self.agi,self.vit,self.luk,self.classP,self.lvl = name,str,dex,agi,vit,luk,classP,lvl
		self.baseStr = self.str
		self.maxhp = self.lvl*2 + self.vit*3 + 10 + self.str
		self.adddmg,self.money,self.buffstat = 0,0,0
		self.brokenArmMINdmg,self.brokenArmMAXdmg,self.brokenArmHit,self.brokenLegFlee = 1,1,1,1
		self.rweaponmindmg=self.lweaponmindmg=self.rweaponmaxdmg=self.lweaponmaxdmg=0 #Weapon DMG init
		self.mindmg = int(((self.str-(self.baseStr-1)) + (self.str/10)*2 + self.adddmg + self.buffstat + self.luk/5 + self.rweaponmindmg + self.lweaponmindmg*0.5)*self.brokenArmMINdmg)
		self.maxdmg = int((self.str + (self.str/10)*3 + self.adddmg + self.buffstat + (self.luk/5) + self.rweaponmaxdmg + self.lweaponmaxdmg*0.5)*self.brokenArmMAXdmg)
		self.statpnt = self.lvl + 20
		self.crit = 1 + self.luk/3
		self.hit = self.dex+10+self.dex/15
		self.flee = self.agi + 5
		self.classp,self.consumable,self.dead,self.exp,self.exp4lvl,self.chancesign,self.critdmg,self.ammo = '',{},0,0,5,'%',0,0
		self.items,self.weapons,self.armor,self.pants,self.hat,self.shoes,self.rweapon,self.lweapon = {},{},{},{},{},{},{},{}
		self.tired = self.vit+3
		self.buffspeed,self.buffhp,self.buffflee,self.buffhit,self.buffcrit = 0,0,0,0,0
		self.speed = (1+self.agi/10)+self.buffspeed
		self.bufftime,self.marketban,self.lucktry,self.defence = 0,0,0,0
		self.lucktolvl = 5*(1+self.luk/10)
		self.brokenjaw,self.brokenleg,self.brokenarm,self.crap,self.crapflee,self.craphit,self.crapcrit = 0,0,0,0,0,0,0
		self.parts2break = ['arm','leg','jaw']
		self.admin = 0
		if self.classP == 1:
			self.classp = "Gangster"
			self.consumable = {'beer':1}
			self.hit += 5
		if self.classP == 2:
			self.classp = "Bull"
			self.maxhp += 10
			self.consumable = {'sunseeds':1}
		if self.classP == 3:
			self.classp = "Hustler"
			self.crit += 10
			self.flee += 5
			self.critdmg += 5
		if self.classP == 4:
			self.classp = "Junkie"
		if self.classP == 5:
			self.classp = "Cop"
		if self.classP == 6:
			self.classp = "Maniac"
		self.hp = self.maxhp
	def lvlUpStatAdd(self):
		rand = random.randrange(1,101)
		if self.classP == 1:
			if rand <= 24:
				self.str+=1
				print(pnt('red',"STR+1"))
			elif rand <=48:
				self.dex+=1
				print(pnt('navy',"DEX+1"))
			elif rand <=72:
				self.agi+=1
				print(pnt('blue',"AGI+1"))
			elif rand <=96:
				self.vit+=1
				print(pnt('violet',"VIT+1"))
			elif rand <=100:
				self.luk+=1
				print(pnt('yellow',"LUK+1"))
		if self.classP == 2:
			if rand <= 40:
				self.str+=1
				print(pnt('red',"STR+1"))
			elif rand <=55:
				self.dex+=1
				print(pnt('navy',"DEX+1"))
			elif rand <=58:
				self.agi+=1
				print(pnt('blue',"AGI+1"))
			elif rand <=98:
				self.vit+=1
				print(pnt('violet',"VIT+1"))
			elif rand <=100:
				self.luk+=1
				print(pnt('yellow',"LUK+1"))
		if self.classP == 3:
			if rand <= 10:
				self.str+=1
				print(pnt('red',"STR+1"))
			elif rand <=25:
				self.dex+=1
				print(pnt('navy',"DEX+1"))
			elif rand <=65:
				self.agi+=1
				print(pnt('blue',"AGI+1"))
			elif rand <=71:
				self.vit+=1
				print(pnt('violet',"VIT+1"))
			elif rand <=100:
				self.luk+=1
				print(pnt('yellow',"LUK+1"))
	def lvlUpConf(self):
		self.updateDmg()
		self.maxhp = self.lvl*2 + self.vit*3 + 10 + self.str + self.buffstat+self.buffhp
		self.crit = (1 + self.luk/3)+self.buffcrit if self.classP != 3 else (1 + self.luk/3 + 10)+self.buffcrit+self.crapcrit
		self.hit = int((self.dex+10+self.dex/15)*self.brokenArmHit)+self.buffhit+self.craphit
		self.flee = int((self.agi + 5)*self.brokenLegFlee)+self.buffflee+self.crapflee if self.classP != 3 else int((self.agi + 10)*self.brokenLegFlee)+self.buffflee+self.crapflee
		self.speed = (1+self.agi/10)+self.buffspeed
		if inspect.stack()[1][3] == 'lvlUp':		
			self.hp = self.maxhp if  self.hp < self.maxhp else self.hp
			self.tired = self.vit+3
			self.statpnt = self.lvl + 20
	def lvlUp(self):
		if self.exp >= self.exp4lvl:
			self.lvl += 1
			self.exp -= self.exp4lvl
			self.exp4lvl += ((self.exp4lvl/2)*1.1)
			print(pnt('green',pnt('sel',"LVL UP! You are LVL %d now")) % self.lvl)
			self.lvlUpStatAdd()
			self.lvlUpConf()
			if self.exp >= self.exp4lvl:
				self.lvlUp()
			else: return 1
	def regen(self):
		if self.hp < self.maxhp:
			self.hp += self.lvl/20 + self.vit/10 + 1
		if self.tired < (self.vit+3):
			self.tired+=1
	def buff(self):
		if self.marketban > 0:
			self.marketban -= 1
			if self.marketban == 0:
				print(pnt('sel',"Seems that you can return to a market - thing are quite there now"))
		if self.crap > 0:
			self.crap -= 1
			if self.crap == 0:
				print(pnt('sel',"You found some puddle and able to clean all those shit stains"))
				self.crapflee = 0; self.crapcrit = 0; self.craphit = 0
				self.lvlUpConf()
		if self.bufftime > 0:
			self.bufftime -= 1
			if self.bufftime == 0:
				player.str-=player.buffstat; player.dex-=player.buffstat; player.agi-=player.buffstat; player.vit-=player.buffstat; player.luk-=player.buffstat
				print(pnt('sel',pnt('grey',"Weed madness worn off")))
	def isCrit(self):
		rand = random.randrange(1,101)
		if rand <= self.crit: return 1
		else: return 0
	def updateHitFlee(self):
		self.hit = int((self.dex+10+self.dex/15)*self.brokenArmHit)+self.buffhit+self.craphit
		self.flee = int((self.agi + 5)*self.brokenLegFlee)+self.buffflee+self.crapflee if self.classP != 3 else int((self.agi + 10)*self.brokenLegFlee)+self.buffflee+self.crapflee
	def updateDmg(self):
		self.mindmg = ((self.str-(self.baseStr-1)) + (self.str/10)*2 + self.adddmg + self.buffstat + self.luk/5 + self.rweaponmindmg + int(self.lweaponmindmg*0.5))*self.brokenArmMINdmg
		self.maxdmg = ((self.str + (self.str/10)*3 + self.adddmg + self.buffstat + self.luk/5 + self.rweaponmaxdmg + int(self.lweaponmaxdmg*0.5))*self.brokenArmMAXdmg)
	def isTrauma(self):
		rand = random.randrange(1,101)
		if self.parts2break != []:
			if rand <= 33:
				if self.brokenleg == 0:
					self.brokenleg = 1
					self.parts2break.remove('leg')
					self.brokenPart()
					if inspect.stack()[1][3] == 'enmdmg': print("[" + pnt('red',"FLEE-50%s") % self.chancesign +"]")
					return 1
			elif rand <= 67:
				if self.brokenarm == 0:
					self.brokenarm = 1
					self.parts2break.remove('arm')
					self.brokenPart()
					if inspect.stack()[1][3] == 'enmdmg': print("[" + pnt('red',"HIT-50%s DMG-45%s") % (self.chancesign,self.chancesign) +"]")
					return 2
			elif rand > 67:
				if self.brokenjaw == 0:
					self.brokenjaw = 1
					self.parts2break.remove('jaw')
					if inspect.stack()[1][3] == 'enmdmg': print("[" + pnt('red',"You can't eat!") +"]")
					return 3
	def brokenPart(self):
		if self.brokenarm == 1:
			self.brokenArmHit = 0.5
			self.brokenArmMINdmg = 0.45
			self.brokenArmMAXdmg = 0.45
			self.updateDmg()
			self.updateHitFlee()
		elif self.brokenleg == 1:
			self.brokenLegFlee = 0.5
			self.updateHitFlee()	
	def isCrap(self):
		self.crap = 20
		self.crapflee += int(self.flee * 0.25); self.crapcrit += 5; self.craphit += int(self.hit*-0.4)
		self.lvlUpConf()
	def equip(self,item,hand):
		def bonus(part,hand,aORd):#weapon or armor, hand, add or deduct bonus
			if part == 'w':#for weapon
				if hand == 'r':
					whatBonus(self.rweapon.values()[0][3].keys()[0].lower(),self.rweapon.values()[0][3].values()[0],'a' if aORd == 'a' else 'd')
				elif hand == 'l':
					whatBonus(self.lweapon.values()[0][3].keys()[0].lower(),self.lweapon.values()[0][3].values()[0],'a' if aORd == 'a' else 'd')
				else:
					whatBonus(self.rweapon.values()[0][3].keys()[0].lower(),self.rweapon.values()[0][3].values()[0],'a' if aORd == 'a' else 'd')
			else:#for armor
				pass
		def whatBonus(what,qty,addOrDed):
			if what == 'hp':
				self.buffhp = self.buffhp + qty if addOrDed == 'a' else self.buffhp - qty
			elif what == 'hit':
				self.buffhit =self.buffhit+qty if addOrDed == 'a' else self.buffhit-qty
			elif what == 'flee':
				self.buffflee=self.buffflee+qty if addOrDed == 'a' else self.buffflee-qty
			elif what == 'crit':
				self.buffcrit=self.buffcrit+qty if addOrDed == 'a' else self.buffcrit-qty
			elif what == 'str':
				self.str=self.str+qty if addOrDed == 'a' else self.str-qty
			elif what == 'dex':
				self.dex=self.dex+qty if addOrDed == 'a' else self.dex-qty
			elif what == 'agi':
				self.agi=self.agi+qty if addOrDed == 'a' else self.agi-qty
			elif what == 'vit':
				self.vit=self.vit+qty if addOrDed == 'a' else self.vit-qty
			elif what == 'luk':
				self.luk=self.luk+qty if addOrDed == 'a' else self.luk-qty
			elif what == 'dmg':
				self.adddmg=self.adddmg+qty if addOrDed == 'a' else self.adddmg-qty
			elif what == 'spd':
				self.buffspeed=self.buffspeed+qty if addOrDed == 'a' else self.buffspeed-qty
			else:
				print("Unknown bonus - %s:%d" % (what,qty))
			self.lvlUpConf()
		if item in self.weapons:
			if hand == 't':
				if self.weapons[item][6] == 1:
					self.rweapon = ({item:self.weapons[item]})
					self.lweapon = ({item:self.weapons[item]})
					self.rweaponmindmg = self.rweapon[item][4]
					self.rweaponmaxdmg = self.rweapon[item][5]
					self.lweaponmindmg = self.lweapon[item][4]
					self.lweaponmaxdmg = self.lweapon[item][5]
					if self.rweapon[item][3] != '': bonus('w','r','a')
					self.updateDmg()
					print("You equipped " + pnt('navy',"%s") % self.weapons[item][1] + " in "+pnt('sel',"two-hand mode") )
				else:
					print("You can't equip this weapon in two-hand mode")
			elif hand == 'l':
				if self.lweapon == {}:
					self.lweapon.update({item:self.weapons[item]})
					self.lweaponmindmg = self.lweapon[item][4]
					self.lweaponmaxdmg = self.lweapon[item][5]
					if self.lweapon[item][3] != '': bonus('w','l','a')
					self.updateDmg()
					print("You equipped " + pnt('navy',"%s") % self.weapons[item][1] + " in the " + pnt('sel',"left hand"))
				else:

					print("You unequipped %s" % self.lweapon.values()[0][1])
					if self.lweapon.values()[0][3] != '': bonus('w','l','d')
					self.lweapon = ({item:self.weapons[item]})
					self.lweaponmindmg = self.lweapon[item][4]
					self.lweaponmaxdmg = self.lweapon[item][5]
					if self.lweapon[item][3] != '': bonus('w','l','a')
					self.updateDmg()
					print("You equipped " + pnt('navy',"%s") % self.weapons[item][1] + " in the " + pnt('sel',"left hand"))		
			else:
				if self.rweapon == {}:
					self.rweapon.update({item:self.weapons[item]})
					self.rweaponmindmg = self.rweapon[item][4]
					self.rweaponmaxdmg = self.rweapon[item][5]
					if self.rweapon[item][3] != '': bonus('w','r','a')
					self.updateDmg()
					print("You equipped " + pnt('navy',"%s") % self.weapons[item][1] + " in the " + pnt('sel',"right hand"))
				else:

					print("You unequipped %s" % self.rweapon.values()[0][1])
					if self.rweapon.values()[0][3] != '': bonus('w','r','d')
					self.rweapon = ({item:self.weapons[item]})
					self.rweaponmindmg = self.rweapon[item][4]
					self.rweaponmaxdmg = self.rweapon[item][5]
					if self.rweapon[item][3] != '': bonus('w','r','a')
					self.updateDmg()
					print("You equipped " + pnt('navy',"%s") % self.weapons[item][1] + " in the " + pnt('sel',"right hand"))
		elif item in self.items:
			if self.items[item][0] == 'a':
				if self.armor == {}:
					self.armor.update({item:self.items[item]})
					self.defence+=self.armor[item][4]
					print("You equipped " + pnt('navy',"%s") % self.armor[item][1] +" DEF+%d" % self.armor[item][4])
				else:
					print("You unequipped %s DEF-%d" % (self.armor.values[0][1],self.armor.values[0][4]))
					self.defence-=self.armor.values()[0][4]
					self.armor = ({item:self.items[item]})
					self.defence+=self.armor[item][4]
					print("You equipped " + pnt('navy',"%s") % self.armor[item][1] +" DEF+%d" % self.armor[item][4])
		else:
			print("There is no such item")
	def canYouEat(self):
		if self.brokenjaw == 1:
			return 0
		else:
			return 1	
	def about(self):
		print("Name:" + pnt('ital',self.name) + " " + pnt('sel',self.classp) + " Level:%d HP:%d/%d " % (self.lvl,self.hp,self.maxhp) + (pnt("green",pnt('sel',"on weed")) if self.bufftime > 0 else '') + " " + (pnt("violet",pnt('sel',"market ban")) if self.marketban > 0 else '') + " " + (pnt("red",pnt('sel',"broken jaw")) if self.brokenjaw == 1 else '') + " " + (pnt("red",pnt('sel',"broken arm")) if self.brokenarm == 1 else '') +  " " + (pnt("red",pnt('sel',"broken leg")) if self.brokenleg == 1 else '')+ " " + (pnt("yellow",pnt('sel',"crapped")) if self.crap > 0 else '')+"\n-------------")
		print("Stats:\nStr:%d  - weapon DMG and HP\t\tDMG: %d-%d\t%d%s attack chance:%d0%s\nDex:%d  - ability to hit opponent\tHIT: %d \nAgi:%d  - evasion rate\t\t\tFLEE:%d\tSPD:%d\nVit:%d  - HP and DMG absorbsion\t\tDEF: %d \nLuck:%d - CRIT & steal chance\t\tCRIT:%d\n--Money %d$\n--Exp %d/%d" % (self.str,self.mindmg,self.maxdmg,(2+self.agi/10),("nd" if self.agi/10 == 0 else ("rd" if self.agi/10 == 1 else "th")),self.agi%10,self.chancesign,self.dex,self.hit,self.agi,self.flee,self.speed,self.vit,self.defence,self.luk,self.crit,self.money,self.exp,self.exp4lvl)
	+ "\n-------------")
		print("Equipment\nHat:%s\nArmor:%s\nRHand:%s\t\tLHand:%s\nPants:%s\nShoes:%s\n" % (pnt('sel',self.hat.values()[0][1]) if self.hat != {} else 'none',pnt('sel',self.armor.values()[0][1]) if self.armor != {} else 'none',pnt('sel',"+%d %s" % (self.rweapon.values()[0][7],self.rweapon.values()[0][1])) if self.rweapon != {} else 'none',pnt('sel',"+%d %s" % (self.lweapon.values()[0][7],self.lweapon.values()[0][1])) if self.lweapon != {} else 'none',pnt('sel',self.pants.values()[0][1]) if self.pants != {} else 'none',pnt('sel',self.shoes.values()[0][1]) if self.shoes != {} else 'none') + pnt('red',"Ammo:%d") % self.ammo)
	def inventory(self):
		print("---Gear---\nWeapons:")
		if self.weapons == {}: print("empty")
		else:
			for i in range(len(self.weapons)):
				if self.weapons.values()[i][0] == 'w':
					print(pnt('sel',"+%d%s:DMG:%d-%d,Effects:%s,Shortcut:%s") % (self.weapons.values()[i][7],self.weapons.values()[i][1],self.weapons.values()[i][4],self.weapons.values()[i][5],self.weapons.values()[i][3],self.weapons.keys()[i]))
		print("Clothing and stuff (type a - armor; p - pants; h - hat; s - shoes):")
		if self.items == {}: print("empty")
		else:
			for i in range(len(self.items)):
				if type(self.items.values()[i]) is list:
					print(pnt('sel',"%s:DEF:%d,Effects:%s,Shortcut:%s,Type:%s") % (self.items.values()[i][1],self.items.values()[i][4],self.items.values()[i][3],self.items.keys()[i],self.items.values()[i][0]))
				else:
					print(pnt('ital',"%s" % self.items.keys()[i] + ":%d" % self.items.values()[i]))
		print("Consumables:")
		if self.consumable == {}: return "empty"
		else:
			for i in range(len(self.consumable)):
				print pnt('sel',"%s:%d") % (self.consumable.keys()[i],self.consumable.values()[i])
		return ""
#Enemy
class Enemy(Person):
	def __init__(self,name,classP,lvl):
		enemyStats = creator(classP,lvl)
		gstr,gdex,gagi,gvit,gluk,gclassP,glvl = enemyStats
		Person.__init__(self,name,gstr,gdex,gagi,gvit,gluk,gclassP,glvl)
		self.drop = random.randrange(1,11)
		self.dropexp,self.addexp,self.dropmoney,self.dropitem,self.dropcons = 0,0,0,0,{}
		self.toughenemy = 0
	def calculateDrop(self):
		chance = 101+player.luk*3
		drop = random.randrange(1,chance)
		if drop <=35+player.luk:
			self.dropmoney += 1 + self.toughenemy + self.lvl+random.randrange(player.luk)+random.randrange(self.lvl*(1+self.lvl/10)+5)
			return 1
		elif drop <=75:
			return 2
		elif drop <=98+player.luk*2:
			calculateCons()
			return 3
		elif drop <= chance:
			if self.lvl < 10:
				self.dropitem = {'rock':1}#{'rock':6,'hard rock':6,'ultra stone':6,'stone3000':1}
			elif self.lvl <25:
				self.dropitem = {'rock':1,'hard rock':1}
			elif self.lvl <50:
				self.dropitem = {'rock':1,'hard rock':1,'ultra stone':1}
			elif self.lvl >50:
				self.dropitem = {'rock':1,'hard rock':1,'ultra stone':1,'stone3000':1}
			return 4
	def calculateExp(self):
		drop = random.randrange(1,11)
		if self.hp < 0:
			self.addexp = -self.hp*1.5 if self.lvl < 10 else -self.hp*2
		if drop < 9:
			self.dropexp = ((self.lvl*(1+self.lvl/7))*1.5+self.addexp) if self.lvl < 10 else ((self.lvl*(self.lvl/5))*2.5+self.addexp*1.5)
		else:
			self.dropexp = ((self.lvl*(1+self.lvl/4))*2.2+self.addexp*1.5) if self.lvl < 10 else (self.lvl*(self.lvl/3))*2.7+self.addexp*1.9
	def aboutEnemy(self):
		return pnt('navy',self.name)+" "+pnt('green',self.classp)+" "+"LVL:%d HP:" % self.lvl + pnt('red',"%d/%d ") % (self.hp,self.maxhp) + (pnt("red",pnt('sel',"broken jaw")) if self.brokenjaw == 1 else '') + " " + (pnt("red",pnt('sel',"broken arm")) if self.brokenarm == 1 else '') +  " " + (pnt("red",pnt('sel',"broken leg")) if self.brokenleg == 1 else '') + " " + (pnt("yellow",pnt('sel',"crapped")) if self.crap > 0 else '') + "\nStats: \nStr:%d  Dex:%d  Agi:%d  Vit:%d  Luck:%d  Drop:%d \nDMG:%d-%d CRIT:%d\nChance to hit:%d%s  Chance to flee:%d%s" % (self.str,self.dex,self.agi,self.vit,self.luk,self.drop,self.mindmg,self.maxdmg,self.crit,(player.hit+50-self.flee) if (player.hit+50-self.flee) < 100 else 100,self.chancesign,((self.hit+50) - player.flee) if ((self.hit+50) - player.flee) > 0 else 100,self.chancesign)
#Consumables - beer(lvl+10hp),sunseeds(lvl+5hp),joint(+2str+2dex+2agi+2vit+(lvl+5hp)),kebab(lvl+20)
def calculateCons():
	global dropcons
	rand = random.randrange(1,101)
	if rand <=45:
		dropcons["sunseeds"] = 1
	elif rand <= 75:
		dropcons["beer"] = 1
	elif rand <= 90:
		dropcons["joint"] = 1
	elif rand > 90:
		dropcons["kebab"] = 1
#Use Item
def useItem(item):
	global player
	if item in player.consumable:
		if item == 'beer':
			if player.consumable[item] > 0: player.hp += player.lvl+10; player.consumable[item] -= 1; print("Bottle of beer gave you %dHP" % (player.lvl+10))
			else: print("You're out of %s" % item)
		elif item == 'sunseeds':
			if player.consumable[item] > 0: player.hp += player.lvl+5; player.consumable[item] -= 1; print("Chowing down those seeds feels so good. +%dHP" % (player.lvl+5))
			else: print("You're out of %s" % item)
		elif item == 'joint':
			if player.consumable[item] > 0: 
				if player.bufftime == 0:
					player.buffstat = 2;  print("Smoke weed every day.All stats+2,+%dHP" % (player.lvl+5)); player.str+=player.buffstat; player.dex+=player.buffstat; player.agi+=player.buffstat; player.vit+=player.buffstat; player.luk+=player.buffstat; player.bufftime = 25; player.lvlUpConf()
				else:
					player.bufftime = 25
					print("Smoked some weed. +%dHP" % (player.lvl+5))
				player.hp += player.lvl+5
				player.consumable[item] -= 1;	
			else: print("You're out of %s" % item)
		elif item == 'kebab':
			if player.consumable[item] > 0: player.hp += player.lvl+20; player.consumable[item] -= 1; print("Mmm food of Gods - glorious kebab. +%dHP" % (player.lvl+20))
			else: print("You're out of %s" % item)
	else:
		print("You dont have that consumable")
	return "\n"
#Creator
def creator(classP,lvl):
	global enemyStats
	str,dex,agi,vit,luk = 0,0,0,0,0
	stats = lvl+20
	classp = ''
	if classP == 1:
		str,dex,agi,vit,luk = int(stats*0.24),int(stats*0.24),int(stats*0.24),int(stats*0.24),int(stats*0.08)
		classp = "Gangster"
		return str,dex,agi,vit,luk,classP,lvl
	elif classP == 2:
		str,dex,agi,vit,luk = int(stats*0.4),int(stats*0.15),int(stats*0.03)+1,int(stats*0.4),int(stats*0.02)+1
		classp = "Bull"
		return str,dex,agi,vit,luk,classP,lvl
	elif classP == 3:
		str,dex,agi,vit,luk = int(stats*0.1),int(stats*0.25),int(stats*0.35),int(stats*0.06),int(stats*0.28)+1
		classp = "Hustler"
		return str,dex,agi,vit,luk,classP,lvl
	elif classP == 4:
		str,dex,agi,vit,luk = int(stats*0.1),int(stats*0.1),int(stats*0.1),int(stats*0.05),int(stats*0.3)
		classp = "Junkie"
		return str,dex,agi,vit,luk,classP,lvl
	elif classP == 5:
		str,dex,agi,vit,luk = int(stats*0.4),int(stats*0.5),int(stats*0.2)+1,int(stats*0.6),int(stats*0.01)+1
		classp = "Cop"
		return str,dex,agi,vit,luk,classP,lvl
	elif classP == 6:
		str,dex,agi,vit,luk = int(stats*0.4),int(stats*0.25),int(stats*0.4),int(stats*0.25),int(stats*0.4)
		classp = "Maniac"
		return str,dex,agi,vit,luk,classP,lvl
	summ = str+dex+agi+vit+luk
#info
def info(who,what):
	attrs = vars(player) if who == 'pl' else vars(enemy)
	if what in attrs:
		if who == 'pl': print("Player " + pnt('ital',what) + " is " + pnt('ital',"%s") % attrs[what])
		else: print("Enemy " + pnt('ital',what) + " is " + pnt('ital',"%d") % attrs[what])
	else:
		print("No such attribute")
#Event
def event():
	choice = raw_input("What do you want to do? Type 'h' for help\n")
	def checkPlaces(place):
		if places[place] != 0: return 1
		else: print("You dont know where is %s located" % place); return 0
	def whatDo(choice):
		global playstats,player,places,enemy,placesToGo
		if choice == "w":
			print("You are walking through the neighborhood")
			playstats.walked+=1
			walk()
		elif choice == 'z':
			print("Jaw:%d\tLeg:%d\tArm:%d" % (player.brokenjaw,player.brokenleg,player.brokenarm))
			print(places)
		elif choice == 'sa':
			player.money+=2000; player.hp = 400; player.crit += 75;
		elif choice == 'va':
			enemy = Enemy("Test Enemy",5,10)
		elif choice == "en":
			player.items.update({'rock':6,'hard rock':6,'ultra stone':6,'stone3000':1}); player.money = 2000; player.weapons = {'kn':['w','Knife',150,{'HIT':3},3,5,0,0],'bk':['w','Brass Knuckles',50,'',2,4,1,0]}; player.equip('kn',1)
		elif choice == "ens":
			print player.items
		elif choice == "wep":
			player.weapons = {'kn':['w','Knife',150,{'HIT':3},3,5,0,0],'bk':['w','Brass Knuckles',50,'',2,4,1,0]}
		elif choice == "t":
			player.isTrauma()
		elif choice == "adm":
			if player.admin == 0: player.admin = 1; print("Admin mode ON")
			else: player.admin = 0; print("Admin mode OFF")
		elif choice == "pl":
			places = {'market':1,'gym':1,'shop':1,'shooting range':1,'vet':1,'workshop':1}
		elif choice == "ch":
			print("--Cheats--")
			player.money+=500
			player.rweapon.update({'ch':['w','Cheat-hand',10,40,'',50,1]})
			player.rweaponmindmg = player.rweapon['ch'][2]
			player.rweaponmaxdmg = player.rweapon['ch'][3]
			player.updateDmg()
			places = {'market':1,'gym':1,'shop':1,'shooting range':1}
		elif choice.startswith("eq"):
			eqvar = choice.split()
			if (len(eqvar) > 2): player.equip(eqvar[1],eqvar[2])
			else: player.equip(eqvar[1],1)
		elif choice.startswith("in"):
			invar = choice.split()
			if (len(invar) > 1): info('pl',invar[1])
			else: print("Usage - 'info agi' will show player agi")
		elif choice == "a":
			if enemy != '':
				print("About enemy")
				print(enemy.aboutEnemy())
			else:
				print("You wanted to look at enemy but only saw your ugly face in the mirroring puddle")
		elif choice == "sh":
			if checkPlaces('shop'):
				print("---Shop---")
				shop()
		elif choice == "br":
			print player.rweapon.values()[0][7]
		elif choice == "ws":
			if checkPlaces('workshop'):
				print("---Workshop---")
				workshop()
		elif choice == "v":
			if checkPlaces('vet'):
				vet()
		elif choice == 'wh':
			placesToGo()
		elif choice == 'hi':
			print(player.hit)
		elif choice == 'gy':
			if checkPlaces('gym'):
				gym()
		elif choice == 'ma':
			if checkPlaces('market'):
				if player.marketban == 0: market()
				else: print("People at market still searching for you - better not go to this place now")
		elif choice == 'sr':
			if checkPlaces('shooting range'):
				print("---Shooting range---\nType 'h' for help")
				shootingRange()
		elif choice == "i":
			print("---Inventory---")
			print(player.inventory())
		elif choice == "b":
			if player.canYouEat(): print(useItem('beer'))
			else: print("Your jaw is broken. You can't eat, drink or smoke.")
		elif choice == "j":
			if player.canYouEat(): print(useItem('joint'))
			else: print("Your jaw is broken. You can't eat, drink or smoke.")
		elif choice == "s":
			if player.canYouEat(): print(useItem('sunseeds'))
			else: print("Your jaw is broken. You can't eat, drink or smoke.")
		elif choice == "ke":
			if player.canYouEat(): print(useItem('kebab'))
			else: print("Your jaw is broken. You can't eat, drink or smoke.")
		elif choice == "t":
			print("---Stats---\n------------")
			print(playstats.showStats())
			print("\n-------")
		elif choice == "q":
			print(player.about())
		#elif choice == "k": print("You're starting to swing your arms and legs. Peaple look at you like on idiot" )
		elif choice in ("f","k"):
			if enemy != '':
				print("You started a fight")
				fightstance()
			else:
				print("Who you want to fight? Air?")
		elif choice == "h":
			print("Help\n---------\n'w' - Walk\t\t\t's' - Go to shop\t\t'sr' - Go to shooting range\n'a' - Look at enemy\t\t'f' - Fight enemy\t\t\'gy' - Go to gym\n't' - Show statistics\t\t'q' - About you\t\t\t'v' - Go to veterinarian")
		elif choice == "exit":
			exit()
	whatDo(choice)
#Walk		
def walk():
	global enemy,player,playstats
	chance = 101+player.luk*3
	rand = random.randrange(1,chance)
	player.regen()
	player.buff()
	if rand <= 7:
		playstats.enemiesmet+=1
		enemy = Enemy("Enemy",random.randrange(1,4),random.randrange(player.lvl+5,player.lvl+16))
		enemy.toughenemy += (enemy.lvl*2)
		if enemy.classP == 1:
			playstats.pats+=1
		elif enemy.classP == 2:
			playstats.bik+=1
		elif enemy.classP == 3:
			playstats.vor+=1
		print(pnt('red',"Tough enemy!!!") + " - "+pnt('sel','%s Lvl:%d') % (enemy.classp,enemy.lvl))
	elif rand <= 70-player.luk:
		print("Nothing happens")
	elif rand <= 90-player.luk:
		enrand = random.randrange(11)
		if enrand < 9:
			enemy = Enemy("Enemy",random.randrange(1,5),random.randrange(player.lvl if player.lvl<=5 else player.lvl-5,player.lvl+6))
		else:
			enemy = Enemy("Enemy",random.randrange(5,7),random.randrange(player.lvl if player.lvl<=5 else player.lvl-3,player.lvl+9))
		playstats.enemiesmet+=1
		if enemy.classP == 1:
			playstats.pats+=1
		elif enemy.classP == 2:
			playstats.bik+=1
		elif enemy.classP == 3:
			playstats.vor+=1
		print("You spotted an enemy - "+pnt('sel','%s LVL:%d') % (enemy.classp,enemy.lvl))
	elif rand <= chance:
		found()
	if enemy != '' and player.admin == 0:#chance to evade fight
		choice = raw_input("Opponent saw you. Fight him or try to run?\n f - fight	r - run	")
		if choice == 'r':
			print("You're trying to run from fight...")
			evade_chance = random.randrange(5)
			if (evade_chance > 1 if player.classP == 3 else evade_chance > 2):
				print(pnt('ital','You succesfully evaded the fight. Nice job, chicken'))
			else:
				print(pnt('ital','~~Can\'t run from me, pussy!'))
				print("You failed to run from opponent")
				fightstance()
		else:
			fightstance()
		return 1
	else:
		return 0
#Found
def found():
	global dropcons,player,places2found,places
	chance = 100+player.luk*3
	rand = random.randrange(1,chance)
	if rand <= 90+player.luk:
		moneyfound = player.lvl + random.randrange(player.luk,player.luk*2)
		player.money += moneyfound
		playstats.moncol += moneyfound
		print(pnt('green','Found money - %d$, now you have %d$') % (moneyfound,player.money))
	elif rand <= 95+player.luk*2:
		print("Found something")
		if places2found != []:
			found = random.randrange(len(places2found))
			place = places2found[found]
			del places2found[found]
			places[place] += 1
			print(pnt('sel',"You found %s" % place))
	elif rand <= 100+player.luk*3:
		calculateCons()
		print(pnt('violet',"Found consumable %s") % dropcons.keys()[0])
		if dropcons.keys()[0] not in player.consumable: player.consumable.update(dropcons)
		else: player.consumable[dropcons.keys()[0]] += 1
#Fight
def fightstance():
	global player,enemy,dropcons
	trauma = 0
	print("Fight is started!")
	print("--You will hit first since you are more agile" if player.agi>enemy.agi else "--Enemy will hit first since he is more agile")
	def choose():	
		choice = raw_input("Your choice:\n")
		if check() == 1:
			if choice == "k":
				fight()
			elif choice == "d":
				print("Enemy Arm:%d\tLeg:%d\tJaw:%d" % (enemy.brokenarm,enemy.brokenleg,enemy.brokenjaw))
			elif choice == "a":
				print(enemy.aboutEnemy())
			elif choice == "q":
				print(player.about())
			elif choice == 'i':
				print(player.inventory())
			elif choice.startswith("in"):
				invar = choice.split()
				if (len(invar) == 2): info('pl',invar[1])
				elif (len(invar) > 2): info(invar[1],invar[2])
				else: print("Usage - 'info agi' will show player agi")
			elif choice == "b":
				if player.canYouEat(): print(useItem('beer'))
				else: print("--Your jaw is broken. You can't eat, drink or smoke.")
			elif choice == "j":
				if player.canYouEat(): print(useItem('joint'))
				else: print("--Your jaw is broken. You can't eat, drink or smoke.")
			elif choice == "s":
				if player.canYouEat(): print(useItem('sunseeds'))
				else: print("--Your jaw is broken. You can't eat, drink or smoke.")
			elif choice == "ke":
				if player.canYouEat(): print(useItem('kebab'))
				else: print("--Your jaw is broken. You can't eat, drink or smoke.")
			else:
				print("You're in combat. Can't do this")
		elif check() == 2:
			win()
		elif check() == 3:
			lose()	
	def check():
		if enemy.hp > 0 and player.hp > 0:
			return 1 #Fight proceed
		elif enemy.hp <= 0 and player.hp > 0:
			return 2 #Player won
		elif player.hp <= 0 and enemy.hp > 0:
			return 3 #Enemy won
		elif enemy.hp <= 0 and player.hp <= 0:
			return 4 #Both dead
	def win():
		global enemy,player,dropcons
		print(pnt('sel',pnt('blue',"You won!")))
		enemy.calculateExp()
		player.exp += enemy.dropexp
		print(pnt('sel',pnt('brown',"You got %d EXP")) % enemy.dropexp + "(%d/%d)" % (player.exp,player.exp4lvl))
		drop = enemy.calculateDrop()
		if drop in (1,3,4):
			if drop == 1:		
				player.money += enemy.dropmoney
				print(pnt('green',"You searched enemy body and found %d$") % enemy.dropmoney)
			elif drop == 3:
				if dropcons.keys()[0] not in player.consumable: player.consumable.update(dropcons)
				else: player.consumable[dropcons.keys()[0]] += 1
				print(pnt('violet',pnt('sel',"Looks like enemy had something in his pockets. %s+1")) % dropcons.keys()[0])
				dropcons = {}
			elif drop == 4:
				print("You found some " + pnt('ital','rocks!'))
		else:
			print("You'd searched enemy body but found nothing useful")
		player.lvlUp()
		enemy = ''
		return 1
	def lose():
		print("You lose, cyka! Cya~")
		time.sleep(5)
		os.system('clear')
		exit()
	def plrdmg():	
		crit = player.isCrit()
		plrdmg = int((random.randrange(int(player.mindmg),int(player.maxdmg)) - (enemy.vit/3+enemy.defence))*(1-enemy.defence/100)) if crit == 0 else int(random.randrange(int(player.mindmg),int(player.maxdmg))*1.75)+player.critdmg
		if enemy.hp > 0:
			if crit == 1: 
				enemy.hp-=plrdmg
				if enemy.hp > 0:
					traumaChance = random.randrange(1,11)
					if traumaChance > 6:
						trauma = enemy.isTrauma()
						shitChance = random.randrange(1,11)
						whatBroken = ('arm' if trauma == 2 else ('leg' if trauma == 1 else ('jaw' if trauma == 3 else 0)))
						if whatBroken > 0:
							print(pnt('red',"CRITICAL STRIKE! You broke enemy's %s.") % whatBroken + " Enemy suffers " + pnt('red',"%d DMG. ") % plrdmg + "He still have %d/%d HP" % (enemy.hp,enemy.maxhp))
						else:
							print(pnt('red',"CRITICAL STRIKE!") + " Enemy suffers " + pnt('red',"%d DMG. ") % plrdmg + "He still have %d/%d HP" % (enemy.hp,enemy.maxhp))
						if shitChance > 6 and enemy.crap == 0:
							enemy.isCrap()
							print(pnt("yellow","Enemy crapped himself. ") + "Nice job!")
					else:
						print(pnt('red',"CRITICAL STRIKE!!!") + " Enemy suffers " + pnt('red',"%d DMG ") % plrdmg + "He still have %d/%d HP" % (enemy.hp,enemy.maxhp))
						shitChance = random.randrange(1,11)
						if shitChance > 6 and enemy.crap == 0:
							enemy.isCrap()
							print(pnt("yellow","Enemy crapped himself. ") + "Nice job!")
				else:
					print(pnt('red',"Wow!") + " You killed your enemy with critical strike - %d DMG" % plrdmg)
					enemy.dead = 1
					win()
			else: 
				if isHit():
					enemy.hp-=plrdmg
					if enemy.hp < 0:
						print("You hit your opponent for %d DMG. He is dead now" % (plrdmg))
						enemy.dead = 1
						win()
					else:
						traumaChance = random.randrange(1,101)
						if plrdmg > 0:
							if traumaChance <= (player.str/2-enemy.vit if player.classP != 2 else player.str/2+7-enemy.vit):
								trauma = enemy.isTrauma()
								whatBroken = ('arm' if trauma == 2 else ('leg' if trauma == 1 else ('jaw' if trauma == 3 else 0)))
								if whatBroken > 0: 
									print(pnt('sel',"You broke enemy's %s" % whatBroken))
									print("You hit your opponent for %d DMG. He still have %d/%d HP" % (plrdmg,enemy.hp,enemy.maxhp))
								else:
									print("You hit your opponent for %d DMG. He still have %d/%d HP" % (plrdmg,enemy.hp,enemy.maxhp))
							else:
								print("You hit your opponent for %d DMG. He still have %d/%d HP" % (plrdmg,enemy.hp,enemy.maxhp))
						else:
							print("You hit your enemy for no damage. What a pity!")
				else:
					print(pnt('ital',"You missed"))
	def enmdmg():
		crit = enemy.isCrit()
		enmdmg = ((random.randrange(int(enemy.mindmg),int(enemy.maxdmg)) - (player.vit/3+player.defence))*(1-player.defence/100)) if crit == 0 else int(random.randrange(int(enemy.mindmg),int(enemy.maxdmg))*1.75)+enemy.critdmg
		if enmdmg <= 0:
			print("Opponent hit you for no damage. Its only makes you stronger")
		else:
			if crit == 1:
				player.hp -= enmdmg
				if player.hp > 0:
					traumaChance = random.randrange(1,11)
					if traumaChance > 6:
						trauma = player.isTrauma()
						shitChance = random.randrange(1,11)
						whatBroken = ('arm' if trauma == 2 else ('leg' if trauma == 1 else ('jaw' if trauma == 3 else 0)))
						if whatBroken != 0: 
							print("%s hit you with " % enemy.classp + pnt('red',"CRITICAL") + " for %d DMG. " % enmdmg + pnt('sel',"He broke your %s") % whatBroken + " You still have %d/%d HP" % (player.hp,player.maxhp))
						else: 
							print("%s hit you with " % enemy.classp + pnt('red',"CRITICAL") + " for %d DMG. It hurts!!! You still have %d/%d HP" % (enmdmg,player.hp,player.maxhp))
						if shitChance > 6 and player.crap == 0:
							player.isCrap()
							print("Huuuuge blow. " + pnt("yellow","You'd crapped yourself. ") + "That's gross!\n[" + pnt("green","FLEE+25% CRIT+5 ") + pnt('red',"HIT-40%") + "]") 
					else: 
						print("%s hit you with " % enemy.classp + pnt('red',"CRITICAL") + " for %d DMG. It hurts!!! You still have %d/%d HP" % (enmdmg,player.hp,player.maxhp))
						shitChance = random.randrange(1,11)
						if shitChance > 6 and player.crap == 0:
							player.isCrap()
							print("Huuuuge blow. " + pnt("yellow","You'd crapped yourself. ") + "That's gross!\n[" + pnt("green","FLEE+25% CRIT+5 ") + pnt('red',"HIT-40%") + "]") 
				else:
					print("Critical hit to the grave. " + pnt('red',"YOU DIED"))
					player.dead = 1
					lose()	
			else: 
				if isFlee():
					player.hp -= enmdmg
					if player.hp <= 0:
						print("%s hit you for %d DMG." % (enemy.classp,enmdmg) +pnt('red'," YOU DIED") )
						lose()
					else:
						traumachance = random.randrange(1,101)
						if traumachance <= (enemy.str/2-player.vit if enemy.classP != 2 else enemy.str/2+7-player.vit):
							trauma = player.isTrauma()
							whatBroken = ('arm' if trauma == 2 else ('leg' if trauma == 1 else ('jaw' if trauma == 3 else 0)))
							if whatBroken != 0: print(pnt('sel',"Enemy broke your %s" % whatBroken))
						print("%s hit you for %d DMG. You still have " % (enemy.classp,enmdmg) + (pnt('red',"%d/%d HP") % (player.hp,player.maxhp) if player.hp <= player.maxhp*.25 else "%d/%d HP" % (player.hp,player.maxhp)) )
				else:
					print(pnt('ital',"Enemy missed and you gain some HP"))
					player.regen()
	def isHit():
		rand = random.randrange(1,101)
		result = (player.hit+50) - enemy.flee
		if rand < result:
			return 1#Player scored hit
		else:
			return 0#Player missed
	def isFlee():
		rand = random.randrange(1,101)
		result = (enemy.hit+50) - player.flee
		if rand < result:
			return 1#Enemy scored hit
		else:
			return 0#Enemy missed
	def fight():#brawl
		def playerTurn():
			blows = int(player.speed+1) if player.agi%10 > random.randrange(1,11) else int(player.speed)			
			for i in range(blows):
				if i > 0 and enemy != '':
					suff = ("nd" if i == 1 else ("rd" if i == 2 else "th"))
					print("Since you are so agile you can make " + pnt('ital',"%d%s") % (1+int(i),suff) + " attack")
					plrdmg()
				elif i > 0 and enemy == '':
					return 0
				else:
					plrdmg()
		def enemyTurn():		
			if enemy !='':
				enblows = int(enemy.speed+1) if enemy.agi%10 > random.randrange(1,11) else int(enemy.speed)
				for i in range(enblows):
					if i > 0 and player.hp > 0:
						suff = ("nd" if i == 1 else ("rd" if i == 2 else "th"))
						print("Since your enemy is so agile he can make %d%s attack" % (1+int(i),suff))
						enmdmg()
					elif i > 0 and player.hp <= 0:
						lose()
					else:
						enmdmg()
		if player.agi > enemy.agi:
			playerTurn()
			print("-----------")
			enemyTurn()
		else:
			enemyTurn()
			print("-----------")
			playerTurn()
	while enemy != '':
		try: choose()
		except Exception as e:
			print(e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
	else:
		return 0
#Shop
def shop():
	global player
	print("List - \'l\'\nBuy - \'buy [item] #\' --Example: to buy 5 beer type 'buy beer 5'\nExit - \'e\'")
	shopitems = {'beer':20,'bk':['w','Brass Knuckles',50,'',2,4,1,0]}#type,name,price,effects,mindmg,maxdmg,twohand?,refine
	def choose():
		choice = raw_input("Your choice: ") 
		if choice == "l":
			print("------\nList\n-------")
			shoplist()
			return 1
		elif choice.startswith("buy"):
			buyvar = choice.split()
			if (len(buyvar) > 2): buy(buyvar[1],buyvar[2])
			else: buy(buyvar[1],1)
			return 1
		else:
			return 0
	def buy(item,qty):
		if item in shopitems:
			if type(shopitems[item]) is int:
				if player.money >= shopitems[item]*int(qty):
					if item not in player.consumable:
						player.consumable.update({item:int(qty)})
					else: player.consumable[item] += int(qty)
					print("You bought " + pnt('violet',"%dx %s") % (int(qty),item))
					player.money-=shopitems[item]*int(qty)
				else: print("You dont have enought money")
			else:
				if shopitems[item][0] == 'w':
					if player.money >= shopitems[item][2]:
						if item not in player.weapons:
							player.weapons.update({item:shopitems[item]})
							player.money-=shopitems[item][2]
						else: print("You already have this item")
						print("You bought " + pnt('violet',"%s") % shopitems[item][1])
					else:
						print("You dont have enought money")
				if qty > 1: print("You dont need more than 1 of that item")
		return 1
	def shoplist():
		for i in range(len(shopitems)):
			if type(shopitems.values()[i]) is int:
				print("%d - %s - %d$" % (i+1,shopitems.keys()[i],shopitems.values()[i]))
			else:
				print("%d - %s(DMG %d-%d) - %d$, shortcut:%s" % (i+1,shopitems.values()[i][1],shopitems.values()[i][4],shopitems.values()[i][5],shopitems.values()[i][2],shopitems.keys()[i]))
	while choose():
		try: choose()
		except Exception as e:
			print(e)
#Gym
gymmenu = {'str':50,'agi':50,'vit':50}
def gym():
	global player,gymmenu
	print("---Gym---\nType 'h' for help")
	def checkmoney(price):
		if player.money >= price: return 1
		else: return 0
	def gymlist():
		print("In gym you can increase your stats for cash\nTo increase specific stat type 'stat [how many times|max]'. Example: 'str 2' will increase your STR 2 times\n------")
		for i in range(len(gymmenu)):
			print("Stat: %s\tCost: %d$" % (gymmenu.keys()[i],gymmenu.values()[i]))
	def choose():
		choice = raw_input("You are in the gym: ")
		if choice == 'h':
			gymlist()
			return 1
		elif choice.startswith("str") or choice.startswith("vit") or choice.startswith("agi"):
			chvar = choice.split()
			qty = 1
			if (len(chvar) > 1): 
				if chvar[1].isdigit():
					qty = int(chvar[1])
				elif type(chvar[1]) is str and chvar[1] == 'max':
					qty = int(player.money/gymmenu[chvar[0]])
				else: qty = 1
			else: 
				qty = 1
			if checkmoney(gymmenu[chvar[0]]*qty):
				if chvar[0] == 'str': 
					print(pnt('red',"You pumped up some iron and got STR+%d" % qty)); player.str += qty
				elif chvar[0] == 'agi': 
					print(pnt('blue',"You runned for hours and got AGI+%d" % qty)); player.agi += qty
				elif chvar[0] == 'vit': 
					print(pnt('violet',"You did crossfit for hours and got VIT+%d" % qty)); player.vit += qty;
				player.money-=gymmenu[chvar[0]]*qty
				gymmenu[chvar[0]]=int((1+float(qty)/10)*gymmenu[chvar[0]])
			else: print("You dont have money for that - " + pnt('red','%d$') % player.money +"/"+ pnt('green','%d$') % int(gymmenu[chvar[0]]*qty))
			player.lvlUpConf()
			return 0
		else:
			return 0
	while choose():
		try: choose()
		except Exception as e:
			print(e)
#Shooting range
def shootingRange():
	global player
	print("Type 'h' for help")
	def choose():
		choice = raw_input("You are on the shooting range: ")
		if choice == 's':
			if player.ammo > 0:
				player.ammo -= 1
				player.dex += 1
				print(pnt('navy',"You started to train at shooting. DEX+1"))
			else:
				print("You dont have ammo to shoot.")
			return 1
		elif choice == 'h':
			print("'s' - to train at shooting. Ammo "+(pnt('red',"%d/1\n") if player.ammo < 1 else "%d/1\n") % player.ammo + "'wa' - try to learn something by looking at the other people shooting")
			return 1
		elif choice == "wa":
			rand = random.randrange(1,101)
			if player.tired > 0:			
				if player.dex < 20 and player.luk >= rand:
					print(pnt('navy',"You are watching how others do shoot and learn something. DEX+1"))
					player.tired -= 3
				else:
					print("You watched at other people but it gives you no experience")
					player.tired -= 1
				return 1
			else:
				print("You are tired. Go home")
				return 0
		else:
			return 0
	while choose():
		try: choose()
		except Exception as e:
			print(e)
#Market
def market():
	global player,enemy
	print("'l' - list of goods\t'buy [what] #' - buy something. Example: to buy 5 sunseeds type 'buy sunseeds 5'\n's' - pickpocket\t'g' - play games of chance")
	shopitems = {'sunseeds':10,'kn':['w','Knife',150,{'HIT':3},3,5,0,0],'ammo':50,'aj':['a','Adidas jacket',500,'',1]}
	def choose():
		choice = raw_input("Your choice: ") 
		if choice == "l":
			print("------List-------")
			shoplist()
			return 1
		elif choice == 's':
			steal()
			return 1
		elif choice == 'g':
			games()
			return 1
		elif choice.startswith("buy"):
			buyvar = choice.split()
			if (len(buyvar) > 2): buy(buyvar[1],int(buyvar[2]))	
			else: buy(buyvar[1],1)
			return 1
		else:
			return 0
	def checkLuck():
		if player.lucktry >= player.lucktolvl:
			player.lucktry -= player.lucktolvl
			player.lucktolvl = 5*(1+player.luk/10)
			print(pnt('yellow',"You become more lucky. LUK+1"))
			player.luk+=1
			player.lvlUpConf()
			return 1
		else:
			return 0
	def games():
		global enemy
		rand = random.randrange(1,101)
		if player.money > player.lvl:
			gamblemoney = player.lvl*(random.randrange(1,player.luk))
			prize = gamblemoney*2
			if rand < player.luk*1.5:
				player.money+=prize
				print(pnt('green',"You played it and won %d$") % prize)
				player.lucktry+=2
				checkLuck()
				return 1
			else:
				player.money-=prize
				if player.money > 0:
					print(pnt('red',"You've lost! -%d$") % prize)
					player.lucktry+=1
					checkLuck()
					return 1
				else:
					if player.money < 0: player.money = 0
					player.marketban = 20
					print(pnt('ital',"~~You dont have money? Well then you should pay your dept with your ass"))
					enemy = Enemy("Enemy",random.randrange(1,4),random.randrange(player.lvl+1,player.lvl+10))
					print("You spotted an enemy - "+pnt('sel','%s Lvl:%d') % (enemy.classp,enemy.lvl))
					player.lucktry+=1
					checkLuck()
					fightstance()
					return 0
		else:
			print("You dont have money to gamble (need at least as much as your LVL)")
			return 0
	def steal():
		global enemy
		rand = random.randrange(1,101)
		chance = player.luk*1.5 if player.classP != 3 else player.luk*1.3+player.luk
		if chance > rand:
			moneystole = int(player.luk*(random.randrange(player.lvl)*1.5))
			print(pnt('sel',pnt('green',"You have gone through the pockets of the people and stole %d$")) % moneystole)
			player.money+=moneystole
			return 1
		else:
			print("You failed at stealing. Someone cought you by the hand")
			player.marketban = 20
			pay = random.randrange(1,101)
			if player.agi/2+player.luk > pay:
				print("Since you are lucky and agile bastard you successfuly run out of angry people\nYou should wait some time until things go quiet in the market")
				return 0
			else:
				print(pnt('ital',"~~Hey, fucker! I will torn your hands so next time you will think twice before steal!"))
				enemy = Enemy("Enemy",random.randrange(1,4),random.randrange(player.lvl+1,player.lvl+10))
				print("You spotted an enemy - "+pnt('sel','%s LVL:%d') % (enemy.classp,enemy.lvl))
				fightstance()
	def buy(item,qty):
		qty = int(qty)
		if item in shopitems:
			if type(shopitems[item]) is int:
				if player.money >= shopitems[item]*qty:
					if item != 'ammo':
						if item not in player.consumable:
							player.consumable.update({item:qty})
							print("You bought " + pnt('violet',"%dx %s") % (qty,item))
						else: 
							player.consumable[item] += qty
							print("You bought " + pnt('violet',"%dx %s") % (qty,item))
					else:
						player.ammo += qty
						print("You bought " + pnt('violet',"%d %s") % (qty,item))
					player.money-=(shopitems[item]*qty)
				else: print("You dont have enought money (" + pnt('red','%d$') % player.money + "/" + pnt('green',"%d$") % (shopitems[item]*qty) + ")")
			else:
				if player.money >= shopitems[item][2]:
					if shopitems[item][0] == 'w':
						if item not in player.weapons:
							player.weapons.update({item:shopitems[item]})
							player.money-=shopitems[item][2]
							print("You bought " + pnt('violet',"%s") % shopitems[item][1])
						else: print("You already have this item")
					else:
						if item not in player.items:
							player.items.update({item:shopitems[item]})
							player.money-=shopitems[item][2]
							print("You bought " + pnt('violet',"%s") % shopitems[item][1])
						else: print("You already have this item")
				else:
					print("You dont have enought money (" + pnt('red','%d$') % player.money + "/" + pnt('green',"%d$") % shopitems[item][2] + ")")
				if qty > 1: print("You dont need more than 1 of that item")
		return 1
	def shoplist():
		for i in range(len(shopitems)):
			if type(shopitems.values()[i]) is int:
				print("%d - %s - %d$" % (i+1,shopitems.keys()[i],shopitems.values()[i]))
			else:
				if shopitems.values()[i][0] == 'w':
					print("%d - %s(DMG %d-%d) - %d$, shortcut:%s" % (i+1,shopitems.values()[i][1],shopitems.values()[i][4],shopitems.values()[i][5],shopitems.values()[i][2],shopitems.keys()[i]))
				else:
					print("%d - %s(DEF %d) - %d$, shortcut:%s" % (i+1,shopitems.values()[i][1],shopitems.values()[i][4],shopitems.values()[i][2],shopitems.keys()[i]))
	while choose():
		try: choose()
		except Exception as e:
			print(e)
#Veterinarian
def vet():
	global player
	print("You came to veterinarian\nVet: " + pnt('ital',"~~Hey, animal! What do you want?"))
	def choose():
		choice = raw_input("Animal want: ") 
		if choice == "h":
			cost = 50*(player.brokenjaw + player.brokenleg + player.brokenarm)
			print("'he' - to heal %d$\t't' - to heal trauma 50$ for each broken part (" % player.maxhp + pnt('green',"%s$") % cost + ")")
			return 1
		elif choice == 'he':
			cost = player.maxhp
			if player.money >= cost:
				if player.hp < player.maxhp:
					player.hp = player.maxhp
					player.money -=  cost
					print(pnt('ital',"~~You seems fine. Go stroll!"))
					return 1
				else:
					print(pnt('ital',"~~You're fine, get the fuck out here!!!"))
					return 0
			else:
				print(pnt('ital',"~~This is not a charity. Go and find some money,animal"))
				return 0
		elif choice == 't':
			cost = 50*(player.brokenjaw + player.brokenleg + player.brokenarm)
			if player.money >= cost:
				if 1 in (player.brokenjaw,player.brokenleg,player.brokenarm):
					player.money -= cost
					player.brokenleg,player.brokenarm,player.brokenjaw = 0,0,0
					player.brokenArmMINdmg,player.brokenArmMAXdmg,player.brokenArmHit,player.brokenLegFlee = 1,1,1,1
					player.updateDmg()
					player.updateHitFlee()
					print(pnt('ital',"~~Your body parts are fixed, be aware next time"))
					player.parts2break = ['arm','leg','jaw']
					return 1
				else:
					print(pnt('ital',"~~You're fine, get the fuck out here!!!"))
					return 0
			else:
				print(pnt('ital',"~~This is not a charity. Go and find some money,animal"))
				return 0
		else:
			return 0
	while choose():
		try: choose()
		except Exception as e:
			print(e)
#Workshop
def workshop():
# 1,2,3 rocks
# 1,2,3 hard rocks
# 1,2,3 ultra stones
# 1 stone3000
	print("You came to workshop")
	def choose():
		choice = raw_input("Workshop ") 
		if choice == "h":
			print("'r [hand]' - to refine your weapon in choosen hand\nTo refine weapon:\n from 0 to +3 - rocks and 200$\n from +3 to +6 - hard rocks and 300$\n from +6 to +9 - ultra stones and 500$\n to +10 - stone300 and 1500$")
			return 1
		elif choice.startswith("r"):
			wsvar = choice.split()
			if (len(wsvar) > 1): refine(wsvar[1])
			else: refine('r')
			return 1 
		else:
			return 0
	def refine(hand):
		if hand == 'r':
			if player.rweapon != {}:	
				cost = (player.rweapon.values()[0][7]+1)*100
				if player.rweapon.values()[0][7] in (0,1,2):
					if 'rock' in player.items and player.money >= cost:
						if player.items['rock']>= player.rweapon.values()[0][7]+1:
							player.rweapon.values()[0][7]+=1
							player.rweapon.values()[0][4]+=1
							player.rweaponmindmg = player.rweapon.values()[0][4]
							player.rweapon.values()[0][5]+=1
							player.rweaponmaxdmg = player.rweapon.values()[0][5]
							player.items['rock']-=(player.rweapon.values()[0][7])
							player.money-=cost
							player.updateDmg()
							print(pnt("ital",'You successfully upgraded your weapon to ') + pnt('sel','+%d') % player.rweapon.values()[0][7])
							return 1
						else:
							print("You dont have enough rocks - %d/%d" % (player.items['rock'],player.rweapon.values()[0][7]+1))
					else:
						print("You dont have enough materials or money:\n--rocks %d/%d\tmoney %d/%d" % (player.items['rock'] if 'rock' in player.items else 0,player.rweapon.values()[0][7]+1,player.money,cost))
						return 0
				elif player.rweapon.values()[0][7] in (3,4,5):
					if 'hard rock' in player.items and player.money >= cost:
						if player.items['hard rock']>= player.rweapon.values()[0][7]%3+1:
							player.rweapon.values()[0][7]+=1
							player.rweapon.values()[0][4]+=2
							player.rweapon.values()[0][5]+=3
							player.rweaponmindmg = player.rweapon.values()[0][4]
							player.rweaponmaxdmg = player.rweapon.values()[0][5]
							if player.rweapon.values()[0][7] != 6:
								player.items['hard rock']-=(player.rweapon.values()[0][7]%3)
							else:
								player.items['hard rock']-=(player.rweapon.values()[0][7]/2)
							player.money-=cost
							player.updateDmg()
							print(pnt("ital",'You successfully upgraded your weapon to ') + pnt('sel','+%d') % player.rweapon.values()[0][7])
							return 1
						else:
							print("You dont have enough hard rocks - %d/%d" % (player.items['hard rock'],player.rweapon.values()[0][7]+1))
					else:
						print("You dont have enough materials or money:\n--hard rocks %d/%d\tmoney %d/%d" % (player.items['hard rock'] if 'hard rock' in player.items else 0,player.rweapon.values()[0][7]%3+1,player.money,cost))
						return 0
				elif player.rweapon.values()[0][7] in (6,7,8):
					if 'ultra stone' in player.items and player.money >= cost:
						if player.items['ultra stone']>= player.rweapon.values()[0][7]%6+1:
							player.rweapon.values()[0][7]+=1
							player.rweapon.values()[0][4]+=3
							player.rweapon.values()[0][5]+=5
							player.rweaponmindmg = player.rweapon.values()[0][4]
							player.rweaponmaxdmg = player.rweapon.values()[0][5]		
							player.items['ultra stone']-=(player.rweapon.values()[0][7]%6)
							player.money-=cost
							player.updateDmg()
							print(pnt("ital",'You successfully upgraded your weapon to ') + pnt('sel','+%d') % player.rweapon.values()[0][7])
							return 1
						else:
							print("You dont have enough ultra stones - %d/%d" % (player.items['ultra stone'],player.rweapon.values()[0][7]+1))
					else:
						print("You dont have enough materials or money:\n--ultra stones %d/%d\tmoney %d/%d" % (player.items['ultra stone'] if 'ultra stone' in player.items else 0,player.rweapon.values()[0][7]%6+1,player.money,cost))
						return 0
				elif player.rweapon.values()[0][7] == 9:
					if 'stone3000' in player.items and player.money >= cost:
						if player.items['stone3000'] >= 1:
							player.rweapon.values()[0][7]+=1
							player.rweapon.values()[0][4]+=4
							player.rweapon.values()[0][5]+=7
							player.rweaponmindmg = player.rweapon.values()[0][4]
							player.rweaponmaxdmg = player.rweapon.values()[0][5]
							player.items['stone3000']-=1
							player.money-=cost
							player.updateDmg()
							print(pnt("ital",'You successfully upgraded your weapon to ') + pnt('sel','+%d') % player.rweapon.values()[0][7])
							return 1
						else:
							print("You dont have enough stone3000 - %d/1" % (player.items['stone3000'],player.rweapon.values()[0][7]+1))
					else:
						print("You dont have enough materials or money:\n--stone3000 %d/1\tmoney %d/%d" % (player.items['stone3000'] if 'stone3000' in player.items else 0,player.money,cost))
				else:
					print("This weapon is fully upgraded")
			else: print("No weapon in the right hand")
		else:
			if hand == 'l':
				if player.lweapon != {}:	
					cost = (player.lweapon.values()[0][7]+1)*100
					if player.lweapon.values()[0][7] in (0,1,2):
						if 'rock' in player.items and player.money >= cost:
							if player.items['rock']>= player.lweapon.values()[0][7]+1:
								player.lweapon.values()[0][7]+=1
								player.lweapon.values()[0][4]+=1
								player.lweaponmindmg = player.lweapon.values()[0][4]
								player.lweapon.values()[0][5]+=1
								player.lweaponmaxdmg = player.lweapon.values()[0][5]
								player.items['rock']-=(player.lweapon.values()[0][7])
								player.money-=cost
								player.updateDmg()
								print(pnt("ital",'You successfully upgraded your weapon to ') + pnt('sel','+%d') % player.lweapon.values()[0][7])
								return 1
							else:
								print("You dont have enough rocks - %d/%d" % (player.items['rock'],player.lweapon.values()[0][7]+1))
						else:
							print("You dont have enough materials or money:\n--rocks %d/%d\tmoney %d/%d" % (player.items['rock'] if 'rock' in player.items else 0,player.lweapon.values()[0][7]+1,player.money,cost))
							return 0
					elif player.lweapon.values()[0][7] in (3,4,5):
						if 'hard rock' in player.items and player.money >= cost:
							if player.items['hard rock']>= player.lweapon.values()[0][7]%3+1:
								player.lweapon.values()[0][7]+=1
								player.lweapon.values()[0][4]+=2
								player.lweapon.values()[0][5]+=3
								player.lweaponmindmg = player.lweapon.values()[0][4]
								player.lweaponmaxdmg = player.lweapon.values()[0][5]
								if player.lweapon.values()[0][7] != 6:
									player.items['hard rock']-=(player.lweapon.values()[0][7]%3)
								else:
									player.items['hard rock']-=(player.lweapon.values()[0][7]/2)
								player.money-=cost
								player.updateDmg()
								print(pnt("ital",'You successfully upgraded your weapon to ') + pnt('sel','+%d') % player.lweapon.values()[0][7])
								return 1
							else:
								print("You dont have enough hard rocks - %d/%d" % (player.items['hard rock'],player.lweapon.values()[0][7]+1))
						else:
							print("You dont have enough materials or money:\n--hard rocks %d/%d\tmoney %d/%d" % (player.items['hard rock'] if 'hard rock' in player.items else 0,player.lweapon.values()[0][7]%3+1,player.money,cost))
							return 0
					elif player.lweapon.values()[0][7] in (6,7,8):
						if 'ultra stone' in player.items and player.money >= cost:
							if player.items['ultra stone']>= player.lweapon.values()[0][7]%6+1:
								player.lweapon.values()[0][7]+=1
								player.lweapon.values()[0][4]+=3
								player.lweapon.values()[0][5]+=5
								player.lweaponmindmg = player.lweapon.values()[0][4]
								player.lweaponmaxdmg = player.lweapon.values()[0][5]		
								player.items['ultra stone']-=(player.lweapon.values()[0][7]%6)
								player.money-=cost
								player.updateDmg()
								print(pnt("ital",'You successfully upgraded your weapon to ') + pnt('sel','+%d') % player.lweapon.values()[0][7])
								return 1
							else:
								print("You dont have enough ultra stones - %d/%d" % (player.items['ultra stone'],player.lweapon.values()[0][7]+1))
						else:
							print("You dont have enough materials or money:\n--ultra stones %d/%d\tmoney %d/%d" % (player.items['ultra stone'] if 'ultra stone' in player.items else 0,player.lweapon.values()[0][7]%6+1,player.money,cost))
							return 0
					elif player.lweapon.values()[0][7] == 9:
						if 'stone3000' in player.items and player.money >= cost:
							if player.items['stone3000'] >= 1:
								player.lweapon.values()[0][7]+=1
								player.lweapon.values()[0][4]+=4
								player.lweapon.values()[0][5]+=7
								player.lweaponmindmg = player.lweapon.values()[0][4]
								player.lweaponmaxdmg = player.lweapon.values()[0][5]
								player.items['stone3000']-=1
								player.money-=cost
								player.updateDmg()
								print(pnt("ital",'You successfully upgraded your weapon to ') + pnt('sel','+%d') % player.lweapon.values()[0][7])
								return 1
							else:
								print("You dont have enough stone3000 - %d/1" % (player.items['stone3000'],player.lweapon.values()[0][7]+1))
						else:
							print("You dont have enough materials or money:\n--stone3000 %d/1\tmoney %d/%d" % (player.items['stone3000'] if 'stone3000' in player.items else 0,player.money,cost))
					else:
						print("This weapon is fully upgraded")
				else: print("No weapon in the left hand")
	while choose():
		try: choose()
		except Exception as e:
			print(e)
#Stats
class Stats(object):
	def __init__(self,enemiesmet,pats,bik,vor,moncol,walked):
 		self.enemiesmet=enemiesmet
		self.pats=pats
		self.bik=bik
		self.vor=vor
		self.moncol=moncol
		self.walked=walked
	def showStats(self):
		return 	"Enemies met:%d\nGangsters:%d Bulls:%d Hustlers:%d\nMoney collected:%d\nWalked:%d" % (self.enemiesmet,self.pats,self.bik,self.vor,self.moncol,self.walked)
def pnt(font,text):
	if font == 'brown': return "\x1b[30;1m" + text + "\x1b[0m"
	elif font == 'red': return "\x1b[31;1m" + text + "\x1b[0m"
	elif font == 'green': return "\x1b[32;1m" + text + "\x1b[0m"
	elif font == 'yellow': return "\x1b[33;1m" + text + "\x1b[0m"
	elif font == 'navy': return "\x1b[34;1m" + text + "\x1b[0m"
	elif font == 'violet': return "\x1b[35;1m" + text + "\x1b[0m"
	elif font == 'blue': return "\x1b[36;1m" + text + "\x1b[0m"
	elif font == 'grey': return "\x1b[37;1m" + text + "\x1b[0m"
	elif font == 'ital': return "\x1b[3;1m" + text + "\x1b[0m"
	elif font == 'undrl': return "\x1b[4;1m" + text + "\x1b[0m"
	elif font == 'sel': return "\x1b[7;1m" + text + "\x1b[0m"
	else: return "WRONG COLOR NAME"
	
#Init
player,enemy='',''
playstats = Stats(0,0,0,0,0,0)
dropcons = {}
places = {'market':0,'gym':0,'shop':0,'shooting range':0,'vet':1,'workshop':1}
places2found = ['market','gym','shop','shooting range']
#Places
def placesToGo():
	global places
	print("You know where is:")
	for i in places:
		if places[i] == 1:
			print(pnt('sel',i))
#Config
def config():
	name = raw_input("Your name? ")
	print("Hello," + name + "!")
	print("Select your class:")
	print
	print("1."+pnt('undrl',"Gangster")+"\nJust an average person in da hood\tStarting gift:"+pnt('blue'," bottle of beer")+"\n-------------")
	print("2."+pnt('undrl',"Bull")+"\nNo need for brain with so much strength\tStarting gift:" +pnt('red'," higher HP&STUN chance")+"\n-------------")
	print("3."+pnt('undrl',"Hustler")+"\nLucky and agile bastard\t\t\tStarting gift:" + pnt('yellow'," higher CRIT&FLEE chance") + "\n-------------")
	def configChoice():
		global player
		print
		choice = raw_input("Your choice? ")
		if int(choice) == 1:
			print(pnt('ital',"You are Gangster"))
			player = Person(name,5,5,5,5,1,1,1)
		elif int(choice) == 2:
			print(pnt('ital',"You are Bull"))
			player = Person(name,8,3,1,8,1,2,1)
		elif int(choice) == 3:
			print(pnt('ital',"You are Hustler"))
			player = Person(name,2,4,7,2,6,3,1)
		else:
			print(pnt('red',"Its too difficult to you - to just choose one of 3?"))
		if int(choice) in (1,2,3):
			print(player.about())
			time.sleep(1)
			os.system('clear')
		else:
			print("Choose again. Wisely!")
			configChoice()
	configChoice()
#Start
os.system('clear')
print("/-------------\\".center(40))
print("|Test  project|".center(40))
print("\-------------/\n".center(40))
config()
#event()
while player.dead != 1:
	try: event()
	except Exception as e:
		print(e)
