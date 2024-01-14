from controller import Controller
from view.view import View
from orchestrators.image_extraction import ImageExtractionOrchestrator
from orchestrators.prediction_analysis import PredictionAnalysisOrchestrator
import sys 
from PyQt5 import QtWidgets as qtw

def main(view):
	image_extraction = ImageExtractionOrchestrator()
	prediction_analyzer = PredictionAnalysisOrchestrator()
	controller = Controller(view, image_extraction, prediction_analyzer)

if __name__ == "__main__":
	app = qtw.QApplication(sys.argv)
	view = View() # needs to be called here or will be out of scope & destroyed
	main(view)
	sys.exit(app.exec())