import pandas as pd
import Constants

class DataLoader:

	#new_york_times = 'Left Center'
	#breitbart = 'Right'
	#fox_new = 'Right'
	#cnn = 'Left'
	#new_york_post = 'Right Center'
	#vox = 'Left'

	DATA_FILES = ['../articles1.csv', '../articles2.csv', '../articles3.csv']
	COLUMNS = ['title','publication','content']

	publisher_data = {}
	cleaned_articles = None

	def __init__(self):
		imported_data = self.import_data()
		self._partition_by_publisher(imported_data)
		self._assemble_cleaned_articles()

	def import_data(self):
		print('Importing data...\n')
		all_data = pd.DataFrame(columns=self.COLUMNS)
		for file in self.DATA_FILES:
			content = pd.read_csv(file, usecols=self.COLUMNS)
			all_data = pd.concat([all_data, content], ignore_index=True)
		return all_data

	def _partition_by_publisher(self, content):
		self._add_publisher_data(Constants.NY_TIMES, content)
		self._add_publisher_data(Constants.BREITBART, content)
		self._add_publisher_data(Constants.FOX, content)
		self._add_publisher_data(Constants.CNN, content)
		self._add_publisher_data(Constants.NY_POST, content)
		self._add_publisher_data(Constants.VOX, content)

	def _add_publisher_data(self, publisher, content):
		self.publisher_data[publisher] = content[content['publication'] == publisher]
		print('Found {} articles from {}'.format(len(self.publisher_data[publisher]), publisher))


	def _assemble_cleaned_articles(self):
 		articles = list(self.publisher_data[Constants.NY_TIMES].iloc[:,2].values) + \
 								list(self.publisher_data[Constants.BREITBART].iloc[:,2].values) + \
 								list(self.publisher_data[Constants.FOX].iloc[:,2].values) + \
 								list(self.publisher_data[Constants.CNN].iloc[:,2].values) + \
 								list(self.publisher_data[Constants.NY_POST].iloc[:,2].values) + \
 								list(self.publisher_data[Constants.VOX].iloc[:,2].values)
 		self.cleaned_articles = self._clean_articles(articles)

 		print('\nTotal articles loaded: {}'.format(len(self.cleaned_articles)))

	def _clean_articles(self, articles):
		for publisher in self.publisher_data.keys():
			articles = [word.replace(publisher, '') for word in articles]

		return articles
