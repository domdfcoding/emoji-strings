# this package
from emoji_strings import decode

print(decode(b"""

def foo():
	print(g'Starting :package:')
	print(g'Done :rocket:')
"""))
