from getpass import getpass

class FG:
	black =			"\x1B[30m"
	red =			"\x1B[31m"
	green =			"\x1B[32m"
	yellow =		"\x1B[33m"
	blue =			"\x1B[34m"
	magenta =		"\x1B[35m"
	cyan =			"\x1B[36m"
	white =			"\x1B[37m"
	brightblack =	"\x1B[90m"
	brightred =		"\x1B[91m"
	brightgreen =	"\x1B[92m"
	brightyellow =	"\x1B[93m"
	brightblue =	"\x1B[94m"
	brightmagenta =	"\x1B[95m"
	brightcyan =	"\x1B[96m"
	brightwhite =	"\x1B[97m"

class BG:
	black =			"\x1B[40m"
	red =			"\x1B[41m"
	green =			"\x1B[42m"
	yellow =		"\x1B[43m"
	blue =			"\x1B[44m"
	magenta =		"\x1B[45m"
	cyan =			"\x1B[46m"
	white =			"\x1B[47m"
	brightblack =	"\x1B[100m"
	brightred =		"\x1B[101m"
	brightgreen =	"\x1B[102m"
	brightyellow =	"\x1B[103m"
	brightblue =	"\x1B[104m"
	brightmagenta =	"\x1B[105m"
	brightcyan =	"\x1B[106m"
	brightwhite =	"\x1B[107m"

class Text:
	reset =			"\x1B[0m"
	bold =			"\x1B[1m"
	faint =			"\x1B[2m"
	italic =		"\x1B[3m"
	underline =		"\x1B[4m"
	blink =			"\x1B[5m"
	invert =		"\x1B[7m"
	conceal =		"\x1B[8m"
	strikethrough =	"\x1B[9m"
	franktur =		"\x1B[20m"
	framed =		"\x1B[51m"
	encircled =		"\x1B[52m"
	overlined =		"\x1B[53m"
	clear = 		"\x1B[2J"
	save =			"\x1B[s"
	restore =		"\x1B[u"

class Status:
	DEBUG = FG.magenta + "DEBUG"
	INFO = FG.brightcyan + "INFO"
	SUCCESS = FG.green + "SUCCESS"
	WARN = FG.yellow + "WARN"
	ERROR = FG.red + "ERROR"
	FATAL = BG.red + FG.black + "FATAL"

def cursor(direction, amount, clear):
	"""Moves the cursor in terminal"""
	amount = str(amount)
	if direction == "up" or direction == "u":
		print("\x1B["+amount+"A")
	elif direction == "down" or direction == "d":
		print("\x1B["+amount+"B")
	elif direction == "right" or direction == "r":
		print("\x1B["+amount+"C")
	elif direction == "left" or direction == "l":
		print("\x1B["+amount+"D")
	else:
		raise ValueError("Invalid direction")

	if clear:
		print("\x1B[0J")

def cprint(value):
	"""Safely print with colors"""
	print(value, end=Text.reset + "\n")

def sprint(status, value, fullColor=False):
	"""Print status updates"""
	label = "[" + status + Text.reset + "] "

	value = value.replace("\n", "\n        ")
	
	if fullColor:
		cprint(label + status.split("m")[0]+"m" + value)
	else:
		cprint(label + value)

def choose(*item):
	"""Multiple choice selection system, returns index of answer"""
	for i in range(len(item)):
		cprint(FG.yellow + "[" + str(i+1) + "] " + Text.reset + item[i])
	ans = input()
	try:
		return int(ans)-1
	except:
		return None

def question(question):
	"""Get input with style"""
	cprint(FG.yellow + "[?] " + Text.reset + question)
	return input(FG.yellow + "[→] " + Text.reset)

def password(prompt):
	"""Get password with style"""
	cprint(FG.yellow + "[?] " + Text.reset + prompt)
	return getpass(FG.yellow + "[→] " + Text.reset)

def trueCol(hex):
	if hex:
		r, g, b = hex2RGB(hex)
		return "\x1B[38;2;"+str(r)+";"+str(g)+";"+str(b)+"m"
	else:
		return Text.reset

def hex2RGB(hex):
	return tuple(int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))