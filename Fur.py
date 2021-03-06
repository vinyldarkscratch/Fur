title = 'Fur'
author = 'Nightwave Studios'
#Text-based RPG by Kurai Atonitsuka, CEO of Nightwave Studios @ dark.tailed.wolf@gmail.com and Mike Glover @ mglover@pobox.com
#Created May 10, 2013 at 15:14

#Version numbers
version = 455
officialversion = str(version)+" Omega: Tricky Fox"
langversneeded = 0.1

#Import PELT
from pelt import *
from pelt.i18n import m

args = sys.argv[1:]
#Name of the functions says it all
def quit(msg, nosave=False):
	global ios, devplayer
	if nosave:
		pass
	else:
		save()
	makeColor('red')
	#if ios and not devplayer: notification.schedule(m('mailto2'), 15, 'Beep', m('mailto1'))
	if msg:
		sys.exit(msg)
	else:
		sys.exit(0)

def save():
	global loc,gender,player_name,player_last,player_species,frnd_gender,frnd_gndrpn,frnd_nane,scrollspeed,scroll,devplayer
	#with open(reply+'-'+player_name, 'wb') as handle:
	reply = saveload(True)
	if reply:
		with open(reply, 'wb') as handle:
			pickle.dump([loc,gender,player_name,player_last,player_species,frnd_gender,frnd_gndrpn,frnd_nane,scrollspeed,scroll,devplayer], handle)

def load():
	global loc,gender,player_name,player_last,player_species,frnd_gender,frnd_gndrpn,frnd_nane,scrollspeed,scroll,devplayer
	try:
		reply = saveload(False)
		if reply:
			with open(reply, 'rb') as handle:
				file = pickle.load(handle)
				player_name = file[0]
				player_last = file[1]
				loc = file[2]
				gender = file[3]
				player_species = file[4]
				frnd_gender = file[5]
				frnd_gndrpn = file[6]
				frnd_nane = file[7]
				scrollspeed = file[8]
				scroll = file[9]
				devplayer = file[10]
			return True
		else:
			return False
	except IOError:
		output('saveerror')
		return False

#Main menu
def mainmenu():
	global version, scrollspeed, scroll, loc, annoy, msgs, player, friend
	if config.ios:
		temp = m('cancel')
	else:
		temp = m('ok')
	getInput.alert(m('broken1') %temp)
	#show available choices and wait for the user to pick a valid choice
	while True:
		newline()
		choices = [m('start'), m('custom'), m('options'), m('quit')]
		devchoices = ['Developer: Skip Dialogue']
		if config.devplayer:
			for devchoice in devchoices:
				choices.append(devchoice)
		choice = getInput.choice(title, choices)
		newline()
		if choice==m('start'):
			wait_sta = True
			while wait_sta:
				choice_sta = getInput.choice(m('start'), [m('new'), m('load'), m('back')])
				if choice_sta == m('new'):
					start()
				elif choice_sta == m('load'):
					getInput.alert(m('broken3'))
					continue
					i = load()
					if i and devplayer:
						gameplay()
					elif not i:
						continue
					elif not devplayer:
						quit(m('broken4'), nosave=True)
				elif choice_sta == 0:
					wait_sta = False
				else:
					output('inputerror')
		elif choice=='Developer: Skip Dialogue':
			
			player = Ally("", "Moon", "Mist", "Wolf", "Boy", 1)
			friend = Ally("", "Vulpis", "Mist", "Fox", "Girl", 1)
			gameplay('part1', player, [friend])
		elif choice==m('custom'):
			custmenu()
		elif choice==m('options'):
			wait_opt = True
			while wait_opt:
				choice_opt = getInput.choice(m('options'), [m('scroll') %config.scrollspeed, m('annoy'), m('beta'), m('lang'), m('back')])
				if choice_opt == m('scroll' %config.scrollspeed):
					if scrollspeed == m('slow'):
						scrollspeed = m('med')
						scroll=0.03
					elif scrollspeed == m('med'):
						scrollspeed = m('fast')
						scroll=0.01
					else:
						scrollspeed = m('slow')
						scroll=0.05
				elif choice_opt == m('annoy'):
					getInput.alert(m('broken3'))
					continue
					if not annoy:
						getInput.alert(m('annoyon'))
						annoy = True
					else:
						getInput.alert(m('annoyoff'))
						annoy = False
				elif choice_opt==m('beta'):
					if not devplayer:
						getInput.alert(m('betaon'))
						devplayer = True
					else:
						getInput.alert(m('betaoff'))
						devplayer = False
				elif choice_opt == m('lang'):
					language()
				elif choice_opt == 0:
					with open('options.pyp', 'wb') as handle:
						pickle.dump([lang, scrollspeed, annoy, devplayer], handle)
					wait_opt=False
				else:
					output('inputerror')
		elif choice==0:
			quit(m('quitmsg'), nosave=True)
		else:
			output('inputerror')

#Menu for custom levels
def custmenu():
	output('custtitle', s=3)
	#custio.connect()
	while True:
		choice = getInput.choice(m('custtitle'), [m('custstart'), m('custdown'), m('custup'), m('custcreate'), m('back')])
		if choice == m('custstart'):
			pass
		elif choice == m('custdown'):
			pass
		elif choice == m('custup'):
			pass
		elif choice == m('custcreate'):
			custio.custcreate()
		elif choice == 0:
			return False
		else:
			output('inputerror')

#When starting the game, program must ask if the player is a boy or girl.
def start():
	global gender, player, frnd_gender, player_name, player_last, player_species, frnd_gndrpn, species
	waiting=True
	while waiting:
		temp = getInput.choice(m('setupgndr'), [m('boy'), m('girl')])
		if temp == m('boy'):
			gender=m('boy').lower()
			frnd_gender=m('girl').lower()
			frnd_gndrpn=m('she')
		elif temp == m('girl'):
			gender=m('girl').lower()
			frnd_gender=m('boy').lower()
			frnd_gndrpn=m('he')
		else: quit(m('quitmsg'), nosave=True)
		waiting=False
	player_species = getInput.choice(m('setuprace'), species)
	if player_species == 0:
		quit(m('quitmsg'), nosave=True)
	waiting = True
	while waiting:
		temp = getInput.text(m('setupname'))
		temp = temp.title().split(' ')
		try:
			player_name = temp[0]
			player_last = temp[1]
			waiting = False
		except:
			if temp:
				temp = temp[0]
				while waiting:
					temp2 = getInput.text(m('setuplast') %temp)
					temp2 = temp2.title()
					if temp2:
						player_name = temp
						player_last = temp2
						waiting = False
					else:
						output('inputerror')
			else:
				output('inputerror')
	output('setupeyeclose', addon=(player_name, player_last), s=2)
	i = 0
	while i != 3:
		i += 1
		output(str(i)+"...", dict=False, newline=False)
		if not config.instmsg:time.sleep(1)
	newline()
	output('setupeyeopen', addon=(player_species), s=4)
	newline()
	player = Ally(player_name, player_last, player_species, gender, level=1, color='yellow')
	part1()

#part 1
def part1():
	global gender, player_name, player_last, devplayer, player, friend
	playing = True
	friend = Ally('???', player_last, species[4], frnd_gender, level=1, color='blue')
	friend.speak('p1m1', s=2)
	friend.speak('p1m2', s=2)
	friend.speak('p1m3', s=3)
	friend.speak('p1m4', addon=player_species, s=2)
	friend.speak('p1m5', s=2)
	action('p1m6', addon=(frnd_gender, frnd_gender), s=4)
	friend.speak('p1m7', s=3)
	if frnd_gender == m('girl').lower(): temp2 = m('her')
	else: temp2 = m('him')
	action('p1m8', addon=(frnd_gender, frnd_gndrpn.title(), temp2, temp2), s=0.5)
	action('p1m9', s=0.5)
	player.speak('p1m10', s=2)
	friend.speak('p1m11', newline=False, s=1)
	waiting = True
	msg = m('setup9') %(frnd_gndrpn, frnd_gender)
	while waiting:
		frnd_name = getInput.text(msg)
		if frnd_name == None or frnd_name == 0:
			msg = m('nofriendnameerror') %(frnd_gndrpn, frnd_gender)
		else:
			waiting = False
	frnd_name = frnd_name.title()
	friend.speak('p1m12', s=2)
	friend.name = frnd_name
	player.speak('p1m13', s=1)
	friend.speak('p1m14', s=2)
	if player_species == m('fox'):
		temp = m('meyou')
	else:
		temp = m('you')
	friend.speak('p1m15', addon=(player_name, player_species, temp), s=2)
	player.speak('p1m16', s=1)
	if player_species == m('fox'):
		temp = m('foxdesc') %frnd_name
	elif player_species == m('dragon'):
		temp = m('dragondesc')
	else:
		temp = m('p1m18') %frnd_gender+'  '
		if player_species == m('wolf'): temp += m('wolfdesc')
		elif player_species == m('cat'): temp += m('catdesc')
		elif player_species == m('bird'): temp += m('birddesc')
		elif player_species == m('bear'): temp += m('beardesc')
		elif player_species == m('mouse'): temp += m('mousedesc')
		elif player_species == m('otter'): temp += m('otterdesc')
	action('p1m17', addon=temp, s=0.5)
	action('p1m19', s=3)
	friend.speak('p1m20', s=1)
	action('p1m21', addon=player_species, s=2)
	player.speak('p1m22', s=2)
	action('p1m23', s=1)
	friend.speak('p1m24', addon=(player_species, frnd_gndrpn), s=3)
	player.speak('p1m25', s=2)
	friend.speak('p1m26', s=1)
	action('p1m27', addon=frnd_name, s=2)
	player.speak('p1m28', addon=player_species, s=5)
	newline()
	output('helpquit')
	output('helpsave')
	output('helpload')
	output('helphelp')
	output('helpexamine')
	output('helpeat')
	output('helpdrink')
	output('helptake')
	output('helpgo')
	gameplay('part1', player, [friend])
	part2()

def part2():
	output('Next part is in development.', dict=False)

def init():
	global devmode, annoy, gui, species, loc, gender, player_name, player_last, player_species, frnd_gender, frnd_gndrpn, frnd_name, args
	
	try: console.clear() #iOS way to clear the console...
	except: os.system('cls' if config.pc == "Windows" else 'clear')#...but the computer way if not on iOS
	
	try:
		import custio
		
		sync(version, officialversion, langversneeded, title, author, modules=[localio], args=args)

		species = ["Wolf","Cat","Dragon","Bear","Fox","Mouse","Bird","Otter"]
		for i in range(len(species)):
			temp = species[i].lower()
			species[i] = m(temp)
			
		if config.ios:
			choice = getInput.choice(m('iosask'), ['iPhone','iPad'])
			if choice == 0:
				quit(m('iosquit'), nosave=True)
			config.pc = choice
		
		mainmenu()
	except (SystemExit, KeyboardInterrupt): pass
	except:
		output('problem', noscroll=True)
		if config.color:
			temp1 = "[yellow]"
			temp2 = "[red]"
		else: temp1 = temp2 = ""
		tbinfo = "Type: "+str(sys.exc_info()[0])+"\nTraceback: "+str(sys.exc_info()[2])
		output(temp1+"Type: "+str(sys.exc_info()[0])+temp2, noscroll=True, dict=False, newline=False, noreset=True)
		output("\n\n"+tb.format_exc(), noscroll=True, dict=False, ignorecolor=True, noreset=True)

if __name__ in '__main__': init()
