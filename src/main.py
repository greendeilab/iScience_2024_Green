from controller import Controller
from view.view import View
#from orchestrators.image_extractor import ImageExtractor
from orchestrators.prediction_analyzer import PredictionAnalyzer
import sys 
from PyQt5 import QtWidgets as qtw

def main(view):
	#image_extractor = ImageExtractor()
	prediction_analyzer = PredictionAnalyzer()
	controller = Controller(view, None, prediction_analyzer)

if __name__ == "__main__":
	app = qtw.QApplication(sys.argv)
	view = View() # needs to be called here or will be out of scope & destroyed
	main(view)
	sys.exit(app.exec())