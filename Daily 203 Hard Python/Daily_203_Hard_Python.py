import random

ID_AIR = 0
ID_DIRT = 1
ID_SAND = 2
ID_LAVA = 3
ID_DIAMOND = 4
ID_HERO = 5
DEBUG = True

def log(text):
	if DEBUG:
		print (text)

class World(object):
	def __init__(self, width, depth, height):
		log("Generating World")
		blocktypes = (Air, Dirt, Sand, Lava)
		must_update = []
		self.map = []
		for x in range(width):
			slice = []
			self.map.append(slice)
			for y in range(depth):
				col = []
				slice.append(col)
				for z in range(height-1):
					block = random.choice(blocktypes)(self, x, y, z)
					if block.needs_updated:
						must_update.append(block)
					col.append(block)
				col.append(Dirt(self, x, y, height-1)) # dirt floor of map
		
		log("Updating World")
		for block in must_update:
			block.update()
		
		log("Done")
	
	def get_block(self, x, y, z):
		try:
			return self.map[x][y][z]
		except IndexError:
			return Dirt(self, x, y, z) # silly trick to handle out of bounds
	
	def set_block(self, x, y, z, block):
		self.map[x][y][z] = block # I actually want errors if this happens

class Block(object):
	def __init__(self, world, x, y, z, id):
		self.id = id
		self.world = world
		self.x, self.y, self.z = x, y, z
		self.needs_updated = False
	
	def update(self):
		return
	
	def adjacent_blocks(self):
		# Who needs loops
		return (
			self.world.get_block(self.x-1, self.y, self.z),
			self.world.get_block(self.x, self.y-1, self.z),
			self.world.get_block(self.x, self.y, self.z-1),
			self.world.get_block(self.x, self.y+1, self.z),
			self.world.get_block(self.x+1, self.y, self.z)
		)
	
	def update_adjacent(self):
		for block in self.adjacent_blocks():
			block.update()
	
	def get_block_below(self):
		return self.world.get_block(self.x, self.y, self.z+1)
	
	def move(self, x, y, z, replacement):
		self.world.set_block(self.x, self.y, self.z, replacement)
		self.x, self.y, self.z = x, y, z
		self.world.set_block(x, y, z, self)

class Air(Block):
	def __init__(self, world, x, y, z):
		super(Air, self).__init__(world, x, y, z, ID_AIR)
		self.color = 0xFFFFFF

class Dirt(Block):
	def __init__(self, world, x, y, z):
		super(Dirt, self).__init__(world, x, y, z, ID_DIRT)
		self.color = 0x824E31

class Sand(Block):
	def __init__(self, world, x, y, z):
		super(Sand, self).__init__(world, x, y, z, ID_SAND)
		self.needs_updated = True
		self.color = 0xFFEEBC
	
	def update(self):
		if self.get_block_below().id == ID_AIR:
			must_update = []
			must_update.extend(self.adjacent_blocks())
			while self.get_block_below().id == ID_AIR:
				self.move(self.x, self.y, self.z+1, Air(self.world, self.x, self.y, self.z-1))
				must_update.extend(self.adjacent_blocks())
			for block in must_update:
				block.update()

class Lava(Block):
	def __init__(self, world, x, y, z):
		super(Lava, self).__init__(world, x, y, z, ID_LAVA)
		self.needs_updated = True
		self.color = 0xFF3700
	
	def update(self):
		if self.get_block_below().id == ID_AIR:
			must_update = []
			must_update.extend(self.adjacent_blocks())
			while self.get_block_below().id == ID_AIR:
				self.move(self.x, self.y, self.z+1, Lava(self.world, self.x, self.y, self.z-1))
				must_update.extend(self.adjacent_blocks())
			for block in must_update:
				block.update()

class Diamond(Block):
	def __init__(self, world, x, y, z):
		super(Diamond, self).__init__(world, x, y, z, ID_DIAMOND)
		self.color = 0xC6FFFF

class Hero(Block):
	def __init__(self, world, x, y, z):
		super(Hero, self).__init__(world, x, y, z, ID_HERO)
		self.color = 0xFF00FF

def main():
	world = World(10, 10, 10)
	
	for z in range(10):
		out = ""
		for x in range(10):
			for y in range(10):
				block_id = world.get_block(x, y, z).id
				out += str(block_id) if block_id > 0 else " "
			out += "\n"
		print (out + "\n")

if __name__ == "__main__":
	main()