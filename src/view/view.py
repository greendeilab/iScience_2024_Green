from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtCore as qtc   
from .frames.image_extraction_frame import ImageExtractionFrame
from .frames.prediction_analysis_frame import PredictionAnalysisFrame

'''
	This is the main window of the application. It is responsible for showing
	ImageExtractionFrame and PredictionAnalysisFrame. It also handles common events
	such as updating the progress bar.
'''
class View(qtw.QWidget):

	def __init__(self):	
		super().__init__()
		self.extraction_frame = ImageExtractionFrame()
		self.analysis_frame = PredictionAnalysisFrame()
		self.tab_widget = self.create_tab_widget()
		main_layout = self.create_main_layout()
		self.setLayout(main_layout)
		self.setStyleSheet('font-size: 14px;')
		self.set_reset_signals()
		self.show()

	def create_tab_widget(self):
		tab_widget = qtw.QTabWidget()
		tab_widget.insertTab(0, self.extraction_frame, 'Image Extraction')
		tab_widget.insertTab(1, self.analysis_frame, 'Prediction Analysis')
		return tab_widget

	def create_main_layout(self):
		main_layout = qtw.QVBoxLayout()
		main_layout.addWidget(self.tab_widget)
		return main_layout

	def update_progress_bar_value(self, value):
		if self.tab_widget.currentIndex() == 0:
			self.extraction_frame.progress_bar.setValue(value)
		else:
			self.analysis_frame.progress_bar.setValue(value)

	def update_progress_text(self, string):
		if self.tab_widget.currentIndex() == 0:
			self.extraction_frame.progress_text_edit.setText(string)
		else:
			self.analysis_frame.progress_text_edit.setText(string)

	def reset_progress_bar_value(self):
		value = 0
		if self.tab_widget.currentIndex() == 0:
			self.extraction_frame.progress_bar.setValue(value)
		else:
			self.analysis_frame.progress_bar.setValue(value)

	def reset_progress_text(self):
		string = "\tWaiting for program to start...\t\t"
		if self.tab_widget.currentIndex() == 0:
			self.extraction_frame.progress_text_edit.setText(string)
		else:
			self.analysis_frame.progress_text_edit.setText(string)

	def set_reset_signals(self):
		self.extraction_frame.start.connect(self.reset_progress_bar_value)
		self.extraction_frame.start.connect(self.reset_progress_text)
		self.analysis_frame.start.connect(self.reset_progress_bar_value)
		self.analysis_frame.start.connect(self.reset_progress_text)


		



