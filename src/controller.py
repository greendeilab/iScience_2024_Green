from PyQt5 import QtCore as qtc

'''
	The main purpose of the controller is to act an intermediary between the
	frontend and backend. Whenever user input is received by the view which 
	requires some logic to be performed, this class will be responsible for 
	calling the correct functions. Additionally, any progress that is logged 
	by the backend, will be sent to the view through this class. 
'''
class Controller(qtc.QObject):
	def __init__(self, view, image_extraction, prediction_analyzer):
		super().__init__()
		self.view = view 
		self.image_extraction = image_extraction
		self.prediction_analyzer = prediction_analyzer

		self.analyzer_thread = qtc.QThread()
		self.extractor_thread = qtc.QThread()
		
		self.set_up_threads()
		self.connect_view_to_extractor()
		self.connect_view_to_analyzer()

	def set_up_threads(self):
		# Major processes need to be moved into a separate thread (from the main thread)
		# to prevent the GUI from freezing up
		self.prediction_analyzer.moveToThread(self.analyzer_thread)
		self.image_extraction.moveToThread(self.extractor_thread)
		self.extractor_thread.started.connect(self.image_extraction.run)
		self.analyzer_thread.started.connect(self.prediction_analyzer.run)

	def connect_view_to_extractor(self):
		# Lambdas need to be used to connect View's signals with ImageExtractor's slots. Not sure why
		# but this is the only way I got it to work
		self.view.extraction_frame.info.connect(lambda widget_info: self.image_extraction.receive_info(widget_info))
		self.view.extraction_frame.start.connect(lambda: self.image_extraction.reset())
		self.view.extraction_frame.start.connect(lambda: self.extractor_thread.start())
		self.image_extraction.progress_value.connect(lambda value: self.view.update_progress_bar_value(value))
		self.image_extraction.progress_text.connect(lambda text: self.view.update_progress_text(text))
		self.image_extraction.finished.connect(lambda: self.extractor_thread.quit())
		

	def connect_view_to_analyzer(self):
		# Lambdas need to be used to connect View's signals with PredictionAnalyzer's slots. Not sure why
		# but this is the only way I got it to work
		self.view.analysis_frame.info.connect(lambda widget_info: self.prediction_analyzer.receive_info(widget_info))
		self.view.analysis_frame.start.connect(lambda: self.prediction_analyzer.reset())
		self.view.analysis_frame.start.connect(lambda: self.analyzer_thread.start())
		self.prediction_analyzer.progress_value.connect(lambda value: self.view.update_progress_bar_value(value))
		self.prediction_analyzer.progress_text.connect(lambda text: self.view.update_progress_text(text))
		self.prediction_analyzer.finished.connect(lambda: self.analyzer_thread.quit())



