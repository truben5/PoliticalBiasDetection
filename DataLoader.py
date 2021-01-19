import pandas as pd
import numpy as np
import Constants

class DataLoader:

	DATA_FILES = ['../articles1.csv', '../articles2.csv', '../articles3.csv']
	COLUMNS = ['title','publication','content']

	publisher_data = {}
	cleaned_articles = None
	publisher_classifier = None
	bias_classifier = None

	def load(self):
		raw_data = self.import_data()
		self._partition_by_publisher(raw_data)
		self._assemble_cleaned_articles()
		self._create_publisher_classifier()
		self._create_bias_classifier()

	def import_data(self):
		print('Importing data...\n')
		raw_data = pd.DataFrame(columns=self.COLUMNS)
		for file in self.DATA_FILES:
			content = pd.read_csv(file, usecols=self.COLUMNS)
			raw_data = pd.concat([raw_data, content], ignore_index=True)
		return raw_data


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
		articles = list()
		for publisher in self.publisher_data.keys():
			articles = articles + list(self.publisher_data[publisher].iloc[:,2].values)

		self.cleaned_articles = self._clean_articles(articles)
		print('\nTotal articles loaded: {}'.format(len(self.cleaned_articles)))


	def _clean_articles(self, articles):
		for publisher in self.publisher_data.keys():
			articles = [word.replace(publisher, '') for word in articles]

		return articles


	def _create_publisher_classifier(self):
		classifier_list = []
		identifier = 0
		for publisher in self.publisher_data.keys():
			classifier_list = classifier_list + [identifier for articles in range(len(self.publisher_data[publisher]))]
			identifier = identifier + 1

		self.publisher_classifier = np.asarray(classifier_list)


	def _create_bias_classifier(self):
		self.bias_classifier = np.asarray([Constants.NY_TIMES_BIAS for articles in range(len(self.publisher_data[Constants.NY_TIMES]))] + \
							[Constants.BREITBART_BIAS for articles in range(len(self.publisher_data[Constants.BREITBART]))] + \
							[Constants.FOX_BIAS for articles in range(len(self.publisher_data[Constants.FOX]))] + \
							[Constants.CNN_BIAS for articles in range(len(self.publisher_data[Constants.CNN]))] + \
							[Constants.NY_POST_BIAS for articles in range(len(self.publisher_data[Constants.NY_POST]))] + \
							[Constants.VOX_BIAS for articles in range(len(self.publisher_data[Constants.VOX]))])
