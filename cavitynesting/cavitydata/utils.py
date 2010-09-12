import sys

def debug(str):
	sys.stderr.write('%s\n' % str)

def shorten_string(str, width=50):
	if len(str) > width-3:
		str = str[0:width-3] + '...'
	return str

def htmlify_string(str):
	lines = str.split('\n')
	htmlstring= ''
	if len(lines) > 0:
		htmlstring = lines[0]
		for line in lines[1:]:
			htmlstring += '<br>%s' % line
	return htmlstring

def new_csv_string(str):
	return str.split('\n')[0]

def csv_string(str):
	csvstring= str.replace('\n', ' ')
	csvstring= csvstring.replace('\t', ' ')
	csvstring= csvstring.replace('\r', ' ')
	csvstring= csvstring.replace('\"', '\\\"')
	return csvstring

def float_clean(strval):
	if strval == None or strval == 'None': 
		return None
	else:
		return strval

def str_to_float(strval):
	try:
		return float(strval)
	except TypeError:
		return None
	except ValueError:
		return None

def str_to_int(strval):
	try:
		return int(strval)
	except TypeError:
		return None
	except ValueError:
		return None

def stringify_dict(dict):
	sdict = {}
	for k in dict.keys():
		sdict[k] = str(dict[k])
	return sdict

def as_dict(obj):
	keys = [x for x in dir(obj) if not x.startswith('__')]
	dict = {}
	for k in keys:
		try:
			dict[k] = getattr(obj, k)
		except AttributeError:
			debug('Cannnot access %s' % k)		
	return dict
