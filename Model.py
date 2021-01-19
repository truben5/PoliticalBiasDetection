import tensorflow as tf

from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.regularizers import l1,l2

class Model:

	DNN_model = None

	def __init__(self):
		self._instantiate_model()

	def _instantiate_model(self):
		print('Instantiating Model...')
		optimizer = optimizers.Adam(learning_rate = 0.00015)

		## Base model
		DNN_model = Sequential()
		DNN_model.add(Dense(40, input_dim=512, activation = 'relu', kernel_regularizer=l2(0.1)))
		DNN_model.add(Dropout(0.25)) 
		DNN_model.add(Dense(40, activation='relu',kernel_regularizer=l2(0.1)))
		DNN_model.add(Dropout(0.25))

		## Output Layer
		DNN_model.add(Dense(4, activation='softmax'))

		DNN_model.compile(loss= 'sparse_categorical_crossentropy', optimizer= optimizer, metrics=['acc'])
		print('Completed instantiation')

	def _train_model(self):
		return None