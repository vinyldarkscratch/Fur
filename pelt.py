import time, os, pickle, sys, random, locale, re

try:
	import console, notification
	from scene import *
	pc = 'iphone'
	ios = True
except ImportError:
	import colorama, easygui #, menu, pygame
	colorama.init()
	#pygame.init()
	pc = 'computer'
	ios = False

def sync(vers, debugmode, title):
	global version, debug, gametitle
	version = vers
	debug = debugmode
	gametitle = title

class Door(object):
	def __init__(self, direction, room, key=None):
		self.direction = direction
		self.room = room
		if key:
			self.locked = True
			self.key = key
		else: self.locked = False

	def __str__(self):
		return output('doordesc', r=1, addon=[self.direction,self.room])

#define the attributes of an item
class Item(object):
	name = None
	description = None

	def __init__(self, name, description=None):
		self.name = name
		self.description = description

	def examine(self):
		if self.description: output(self.description, dict=False)
		else: output('itemnormal', addon=self.name)

#define drink item
class Drink(Item):
	def __init__(self, name, description, poison):
		Item.__init__(self, name, description)
		self.poison = poison

	def drink(self):
		if self.poison:
			output('drinkpoisoned', addon=self.name)
			quit('drinkpoisonedmsg', addon=self.name)
		else: output('foodeaten', addon=self.name)

#define food item
class Food(Item):
	def __init__(self, name, description, poison):
		Item.__init__(self, name, description)
		self.poison = poison

	def eat(self):
		if self.poison:
			output('foodpoisoned', addon=self.name)
			quit('foodpoisonedmsg', addon=self.name)
		else: output('foodeaten', addon=self.name)

def getCommand(sentence):
	''' Read a command from the user and parse it.
	This parser understands some simple sentences:
		* just a verb: 'quit'
		* verb followed by a noun: 'eat sandwich'
		* verb noun 'with' noun: 'kill monster with sword'

	Return a dictionary of the parsed words, or None if the
	command couldn't be parsed.
	'''
	cmnd = {}
	words = sentence.lower().split()

	if len(words) == 0: return None

	cmnd['verb'] = words[0].lower()

	if len(words) > 1: cmnd['noun'] = words[1].lower()

	if len(words) > 2:
		if words[2] == output('with', r=1) or words[2] == output('using', r=1):
			if len(words) > 3: cmnd['using'] = words[3]
			else:
				output('usingerror', addon=[verb, noun])
				return None
		else: cmnd['extra'] = words[2:]
	return cmnd

class getinput():
	def __init__(self):
		self.network = False
		self.firstmsg = True
	
	def network(self):
		if ios:
			if self.network:
				console.hide_activity()
				self.network = False
			else:
				console.show_activity()
				self.network = True
		else: pass

	def text(self, msg):
		if ios and __name__ in '__main__': choice = console.input_alert(msg, '', '', 'Ok')
		else: choice = easygui.enterbox(msg=msg, title='PELT Engine - '+gametitle+' V'+str(version))
		return choice
	
	def choice(self, msg, choices, window=False):
		if ios and __name__ in '__main__':
			temp = choices[-1]
			if temp == output('quit', r=1) or temp == output('back', r=1) or temp == output('cancel', r=1): choices.remove(temp)
			try:
				if len(choices) == 1: choice = console.alert(msg, '', choices[0])
				elif len(choices) == 2: choice = console.alert(msg, '', choices[0], choices[1])
				elif len(choices) == 3: choice = console.alert(msg, '', choices[0], choices[1], choices[2])
				else:
					waiting = True
					page = 1
					while waiting:
						try:
							b = 2
							choice = console.alert(msg, '', choices[0+(page-1)*2], choices[1+(page-1)*2], "Next Page")
						except IndexError: 
							b = 1
							try: 
								choice = console.alert(msg, '', choices[0+(page-1)*2], output('next', r=1))
							except IndexError:
								page = 0
								choice = 1+b
							except KeyboardInterrupt: return 0
						except KeyboardInterrupt: return 0
						if choice == 1+b:
							if page <= len(choices) // 2: page += 1
							else: page = 1
						else:
							return choice+(page-1)*2
				return choice
			except KeyboardInterrupt: return 0
		else:
			if not window:
				choice = easygui.buttonbox(msg=msg, title='PELT Engine - '+gametitle+' V'+str(version), choices=choices)
				i = 1
				for c in choices:
					if choice == c: return i
					else: i += 1
			else:
				choice = menu.main(choices)
				time.sleep(0.1)
				return choice

	def alert(self, msg):
			if ios and __name__ in '__main__':
				try: console.alert('',msg)
				except KeyboardInterrupt: pass
			else:
				easygui.msgbox(title='PELT Engine - '+gametitle+' V'+str(version), msg=msg)

getInput = getinput()

def language():
	global lang, msgs
	wait=True
	wait2=True
	while wait:
		while wait2:
			choice = getInput.choice('Language/Idioma', ['English','Espanol (Archivo del Idioma no Esta Presente)','Francais (Fichier de Langue pas present', 'Quit'])
			if choice == 1:
				lang = "English"
				with open('options', 'wb') as handle: pickle.dump([lang, scrollspeed, annoy, devplayer], handle)
				wait2=False
			elif choice == 0 or choice == 4: quit('', nosave=True)
			else: output("Invalid option/Opcion incorrecto/L'option invalide", dict=True)
		if lang == "English":
			with open('english.lang', 'rb') as handle: msgs = pickle.load(handle)
		else: output("Language File Version Incompatible/Version del Archivo del Idioma Incompatible/Version de L'archive du Language Incompatible", dict=True)

def setlang(lang):
	global msgs
	with open('english.lang', 'rb') as handle: msgs = pickle.load(handle)

#Function that prints the messages
def output(msg, dict=True, newline=True, noscroll=False, addon=None, addonfromdict=False, modifier="normal", r=0, s=0):
	global scroll, styles, annoy, msgs
	#modifier = caps, title, lower, normal (when modifier isn't present)
	try:
		if dict: msg = msgs[msg]
	except KeyError:
		if msg == '': pass
		else: msg = "WARNING: "+msg+" is not a valid keyword."
	if addon: 
		try: msg = msg % addon
		except TypeError: msg = 'Hey, this message is broken.  Tried to print "%s" and add "%s".' %(msg, addon)
	if modifier == 'caps': msg = msg.upper()
	elif modifier == 'title': msg = msg.title()
	elif modifier == 'lower': msg = msg.lower()
	if r == 0:
		for c in msg:
			if annoy: color('random')
			sys.stdout.write(styles+c)
			if not noscroll:
				sys.stdout.flush()
				time.sleep(scroll)
		if newline: sys.stdout.write('\n')
		if noscroll: sys.stdout.flush()
		color('reset')
		sys.stdout.write(styles)
		sys.stdout.flush()
	elif r == 1: return msg
	time.sleep(s)

#define what a room is
class Room(object):
	rooms={}
	
	def __init__(self, name, items, doors):
		self.name = name
		self.rooms[name] = self
		self.doors = doors
		self.items = items
	
	@classmethod
	def fromText(cls, text):
		'''Room called "Main Room" sized 532x289 placed A520x357:
			Door to "Balcony" on Top 10 from Left
			Door to "Hallway" on Top 60 from Right
			Door to "Play Room" on Bottom 20 from Right
			Trapdoor to "Chest Room" 15 from Left 20 from Bottom locked with "Wooden Key" (Hidden)
		Finish Room'''
		
		lines = text.split('\n')
		assert(lines[0].startswith('Room'))
		name = re.search('called "\([a-zA-Z ]*\)"')
		
		return cls(name, items, doors)
	
	def findItem(self, name):
		for i in self.items:
			if i.name == name: return i
		return None

	def describe(self):
		output(self.name)
		for i in self.items:
			output('itemhere', addon=i.name)
			time.sleep(0.1)
		for d in self.doors:
			output('doorhere', addon=d.direction)
			time.sleep(0.1)

	def go(self, direction):
		for d in self.doors:
			if d.direction == direction:
				if not d.locked: return d.room
				else: return "locked"
		return None

#Save and load functions
def saveload(save, overwarning, overaddon):
	waiting = True
	while waiting:
		saves = range(10)
		saveslist = list[saves]
		#path = os.path
		#os.listdir(path)
		for s in saves:
			s+=1
			try:
				if pc == 'computer': temp = 'saves/save'
				else: temp='save'
				with open(temp+str(s), 'rb') as handle:
					file = list(pickle.load(handle))
					output('save2', addon=[str(s), file[2]], noscroll=True)
					saveslist[s-1] = output('save2', addon=[str(s), file[2]], r=1)
			except:
				if save: output('save1', addon=str(s), noscroll=True)
				saveslist[s-1] = output('save1', addon=str(s), r=1)
		output('')
		if save: choice = getInput.choice(output('save3', r=1),saveslist)
		else: choice = getInput.choice(output('save4', r=1),saveslist)
		if choice == 'c': return False
		choice = str_to_int(choice)
		if choice > 0 and choice <= len(saves):
			if pc == 'computer': response = 'saves/save'+str(choice)+".save"
			else: response = 'save'+str(choice)+".save"
			try:
				with open(response, 'rb') as handle:
					if handle:
						overwait = True
						handle = pickle.load(handle)
						if save:
							while overwait:
								addon = [file[0], file[1]]
								for o in overaddon: addon.append(o)
								overwrite = getInput.choice(output(overwarning, addon=addon, r=1),[output('yes', r=1),output('no', r=1)])
								if overwrite == 1: return response
								elif overwrite == 2: overwait = False
								else: output('inputerror')
						else: return response
			except: return response
		else:
			output('saveerror')
			output('')

#converts a string to an integer and returns -1 if string is not a number
def str_to_int(text):
	try: response=int(text)
	except ValueError: return -1
	return response

#define an attack
class Attack(object):
	def __init__(self, name, desc, pwr, bonus, type):
		self.name = name
		self.desc = desc
		self.pwr = pwr
		self.bonus = bonus
		self.type = type
	
	def use(attacker, attacked):
		temp = 1.5 if self.type == attacked.type else 1
		#attack.bonus = 4, 2, 1, 5, 2.5, or 0
		damage = (((((((2*attacker.level/5+2)*attacker.attk*self.pwr)/50)+2)*temp)*self.bonus/10)*random.randint(217, 255))/255
		attacked.take_damage(damage)

#define the player and characters
class Character(object):
	def __init__(self, location, name, last, species, gender, level, life=100):
		self.inventory = []
		self.location = location
		self.name = name
		self.last = last
		self.species = species
		self.gender = gender
		self.level = level
		self.life = life
		self.attk = 25
		self.dfns = 25
		self.attacks = [Attack(output('attack1', r=1), output('attack1desc', r=1), 20, 0, output('type1', r=1))]

		def take(self, item_name):
			item = self.location.getItem(item_name)
			self.inventory.append(item)
		
		def take_damage(dmg): self.life -= dmg
		
		def get_var(var):
			if var == 'all': return output('playerdesc', r=1, addon=[self.name, self.last, self.gender, self.species, self.inventory, self.location, self.level, self.attacks])
			else:
				try: return self.__getattribute__(var)
				except AttributeError: return None
		
		def use_attack(): pass
		
		def add_attack(attack):
			if type(attack) == Attack: pass
			else: output('attackerror')
		
		def rem_attack(): pass

def color(color):
	global styles
	styles = ''
	if color == 'red':
		try: console.set_color(1.0, 0.0, 0.0)
		except: styles += colorama.Fore.RED
	elif color == 'green':
		try: console.set_color(0.2, 0.8, 0.2)
		except: styles += colorama.Fore.GREEN
	elif color == 'blue':
		try: console.set_color(0.0, 0.0, 1.0)
		except: styles += colorama.Fore.CYAN
	elif color == 'reset':
		try:
			console.set_color(0.2, 0.2, 0.2)
			console.set_font()
		except: styles += colorama.Fore.RESET
	elif color == 'random':
		try: console.set_color(random.random(),random.random(),random.random())
		except:
			list = [colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.BLUE, colorama.Fore.MAGENTA, colorama.Fore.CYAN, colorama.Fore.WHITE]
			styles += random.choice(list)
	elif color == 'bold':
		try: console.set_font('Helvetica', 32.0)
		except: pass
	else: output('colorerror')

try:
	with open('options', 'rb') as handle:
		handle = pickle.load(handle)
		lang = handle[0]
		scrollspeed = handle[1]
		if scrollspeed == 'Fast': scroll = 0.01
		elif scrollspeed == 'Medium': scroll = 0.03
		elif scrollspeed == 'Slow': scroll = 0.05
		annoy = handle[2]
		devplayer = handle[3]
	if lang == "English": setlang('en')
except:
	scrollspeed='Medium'
	scroll=0.03
	lang=None
	annoy=False
	devplayer=True
	language()

styles = ''