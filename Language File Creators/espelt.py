msgs = {'title':'%s',
'title2':'%s - Version %s',
'author':'Made by %s',
'version':'[green]Version %s, [blue]Pelt Version %s',
'save1':'Save %s (Unused)',
'save2':'Save %s: %s',
'save3':'Save to File',
'save4':'Load File',
'savewarning':'[red]WARNING: File belongs to %s %s the %s.  Okay to overwrite?',
'saveerror':'[red]Not a valid save file.',
'colorerror':'[red]Color input was invalid.',
'inputerror':'[red]Invalid Input',
'next':'Next Page',
'yes':'[green]Yes',
'no':'[red]No',
'quit':'[red]Quit',
'back':'[red]Back',
'cancel':'[red]Cancel',
'ok':'[green]Ok',
'open':'open',
'closed':'closed',
'med':'Medium',
'fast':'Fast',
'slow':'Slow',
'boy':'Boy',
'girl':'Girl',
'doormissing':"[red]There is no door in that direction.",
'doorlocked':"[red]You try to open the door but the handle won't budge.",
'directionerror':"[red]That's not a proper direction.",
'itemerror':"[red]I don't see any %s here.",
'cmderror':"[red]I don't know how to do that.",
'with':'with',
'using':'using',
'usingerror':"What do you want to %s the %s with?",
'itemnormal':"This %s doesn't seem to be unusual.",
'chestdescopen':"A chest that contains %s and is open.",
'chestdescclosed':'A closed chest.',
'chestopenerror':'[red]The chest is already open!',
'chestopen':'[blue]Opened the chest, %s was inside.',
'chestunlocked':'[blue]Unlocked the chest using %s.',
'chestlocked':'[red]Chest is locked with a key.',
'foodpoisoned':"[red]That %s was covered in fatal poison.  You are now dead.",
'foodpoisonedmsg':'User ate a poisoned %s',
'foodeaten':"That %s was very tasty!",
'drinkpoisoned':"[red]That %s had a fatal poison inside.  You are now dead.",
'drinkpoisonedmsg':'User drank poison from a %s',
'playerdesc':'%s %s the %s %s, carrying %s, at %s, Level %s.  Can use the attacks %s',
'attackerror':'[red]Not a valid attack.',
'itemhere':"[yellow]There is a %s here",
'doorhere':"[yellow]There is a door to the %s",
'doordesc':"[yellow]A door to the %s that leads to the %s.",
'attack1':'Punch',
'attack1desc':'A simple punch',
'type1':'Normal',
'lang':'Language',
'iosask':'Are you on an iPhone or iPad?  This is important for gameplay.',
'iosquit':'User did not choose iPhone or iPad.'
}

import pickle, os.path

rootdir = os.path.dirname(os.path.dirname(__file__))
resourcedir = os.path.join(rootdir, 'resources')
langsdir = os.path.join(resourcedir, 'langs')
langdir = os.path.join(langsdir, 'es')

def compile():
	with open(os.path.join(langdir, "es-pelt.lang"), 'wb') as handle: pickle.dump(msgs, handle)

compile()