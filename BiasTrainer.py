from DataLoader import DataLoader
from Model import Model

def main():
	collector = DataLoader()
	collector.load()
	model = Model()
	
if __name__ == "__main__":
	main()