import codecs

def read_key_section(f):
	lines = []
	for i, line in enumerate(f):
		if len(line) < 3: continue
		lines.append(line)
		if i == 7: break
	return lines

def parse_lines(lines):
	'''
	Parse the keys part of a layout subset
	'''
	def parse_line(line):
		keys = [(line[i : i + 5].strip()) for i in range(1, 86, 6)]
		keys = [s for s in keys if s != "-----"]
		l = len(keys)//2
		left = keys[:l]
		right = keys[l:]
		
		return left, right
	
	left_half = []
	right_half = []
	for line in lines:
		left, right = parse_line(line)				
		left_half.append(left)
		right_half.append(right)
	return left_half, right_half

class Layouts:
	def __init__(self):
		self.sets = {}
	
	def read(self, fname):
		f = codecs.open(fname, "r", encoding = "utf-8")
		for line in f:
			if line.startswith("SET"):
				ks = KeySet(line, f)
				self.sets[ks.name] = ks
		f.close()
		
		for k, v in self.sets.items():
			if v.parent_name: v.parent = self.sets[v.parent_name]

class KeySet:
	def __init__(self, header, f):
		np = header.strip().split()[1].split(":")
		self.name = np[0]
		self.parent_name = None if len(np) < 2 else np[1]
		self.parent = None
		self.subsets = {}
		
		for line in f:
			if len(line) < 3: continue
			if line.startswith("SUBSET"):
				kss = KeySubset(line, f)
				self.subsets[kss.name] = kss
			if line.startswith("END"):
				break
	
	def get_key_info(self, half, row, col):
		res = {}
		for name, subset in self.subsets.items():
			ki = subset.get_key_info(half, row, col)
						
			if (not ki) and self.parent:
				ki = self.parent.subsets[name].get_key_info(half, row, col)
				
			if ki: 
				name, info = ki
				if not name in res.keys():
					res[name] = info
		
		return res


class KeySubset:
	def __init__(self, header, f):
		self.name = header.strip().split()[1]
		self.pos = [int(x) for x in f.readline().strip().split()]
		self.rgb = [int(x) for x in f.readline().strip().split()]
		key_lines = read_key_section(f)
		self.left_half, self.right_half = parse_lines(key_lines)
		self.halves = [self.left_half, self.right_half]
	
	def get_key_info(self, half, row, col):
		key = self.halves[half][row][col]
		if (not key) or (len(key) == 0): return None
		return key, {"pos": (self.pos), "rgb": (self.rgb)}
