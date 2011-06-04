import pickle

class Database:

	def __init__(self, file):
		self.file = file

	def raw(self):
		f = open(self.file)
		data = pickle.load(f)
		f.close()
		return data

	def getList(self, field):
		data = self.raw()
		data = self.keepLyrics(data)
		field = field.capitalize()
		results = []
		for item in data:
			if field == 'Artist' or field == 'Artists':
				fetched = item['Artist']
				results.append(fetched)

			if field == 'Track' or field == 'Name' or field == "Title":
				fetched = item['Name']
				results.append(fetched)

		return results

	def keepLyrics(self, old):
		new = []
		for item in old:
			lyrics = item['Lyrics']
			if lyrics != None:
				new.append(item)
		return new