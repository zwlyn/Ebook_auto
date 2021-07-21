cookie = """"""

for line in cookie.split("\n"):
	key = line.split()[0]
	value = line.split()[1]
	msg = "'{key}': '{value}',".format(key=key, value=value)
	print(msg)