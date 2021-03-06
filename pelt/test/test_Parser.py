import parser
import pelt
import unittest

class ParserTest(unittest.TestCase):
	def setUp(self):
		self.level = """Level is "Whatever the Heck" sized 2x3
		
						Dialogue is:
						Finish Dialogue

						Room is:
							Called "Main Room" sized 17x10 placed A20x27
							Door to "Balcony" on Top 1 from Left
							Door to "Hallway" on Top 2 from Right locked with "Rusty Key"
							Door to "Play Room" on Bottom 4 from Right locked with "Silver Key"
							Trapdoor to "Chest Room" 1 from Left 2 from Bottom locked with "Fire Circle" (Hidden)
						Finish Room

						Room is:
							Called "Balcony" sized 8x3 placed A13x23
							Door to "Main Room" on Bottom 2 from Right
							Chest placed 1 from Left 1 from Top facing Bottom with (Rusty Key, $50)
						Finish Room

						Room is:
							Called "Hallway" sized 4x14 placed A32x13
							Door to "Main Room" on Bottom 1 from Left
							Door to "Garden" on Left 0 from Top locked with "Gold Key" (Hidden)
							Chest placed 0 from Right 0 from Top facing Bottom with (Silver Key)
						Finish Room
						"""
	# def testPreprocess(self):
# 		testdata = """Hello
# 		[Hi there]
# 		Goodbye"""
# 		lines = parser.preprocess(testdata)
# 		self.assertEqual(['Hello','Goodbye'], lines)
# 	
# 	def testMultiLineComment(self):
# 		testdata = """Hello
# 		[Hi
# 		there]
# 		Goodbye"""
# 		lines = parser.preprocess(testdata)
# 		self.assertEqual(['Hello','Goodbye'], lines)
# 	
# 	def testMultiCharacterGetBlocks(self):
# 		v = parser.getblocks('Foo', 'bar', ['Foo','baz','bastard','bar'], 1)
# 		self.assertEqual(v, [['baz', 'bastard']])
# 	
# 	def testGetBlocks(self):
# 		r = parser.getblocks('X', 'Y', ['6','X',' ', 'b', 'Y', 'foo', 'X', 'bar', 'baz', 'foobar', 'Y', 'X', 'T', 'Y'], 2)
# 		self.assertEqual(r, [[' ', 'b'], ['bar','baz','foobar']])
	
	def testParseLevel(self):
		l = pelt.Level.fromText(self.level)
		self.assertEqual(l.name, "Whatever the Heck")
		self.assertEqual(l.size, (2,3))
		print l.rooms
	
	def testParseChest1(self):
		t = """Chest placed 0 from Right 0 from Top facing Bottom with (Silver Key)"""
		c = pelt.Chest.fromText(t)
		self.assertEqual(['Silver Key'], c.contents)
	
	def testParseChest2(self):
		t = """Chest placed 1 from Left 1 from Top facing Bottom with (Rusty Key, $50)"""
		c = pelt.Chest.fromText(t)
		self.assertEqual(['Rusty Key', '$50'], c.contents)
		
	def testParseChestEmpty(self):
		t = """Chest placed 1 from Left 1 from Top facing Bottom with ()"""
		self.assertRaises(pelt.ParseError, pelt.Chest.fromText, t)
	
	def testParseChestNoFacing(self):
		t = """Chest placed 6 from Left 1 from Bottom with (Fire Circle, $500)"""
		self.assertRaises(pelt.NoFacingError, pelt.Chest.fromText, t)
	
if __name__ == '__main__':
	unittest.main()