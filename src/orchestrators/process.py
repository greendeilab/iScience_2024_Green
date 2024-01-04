from PyQt5 import QtCore as qtc

'''
	This class contains functions that are used for logging information about 
	the current process. The data that is logged is ultimately sent to the view.
'''
class Process(qtc.QObject):
	
	finished = qtc.pyqtSignal()
	progress_value = qtc.pyqtSignal(int)
	progress_text = qtc.pyqtSignal(str)

	def __init__(self):
		super().__init__()
		self.num_tasks_completed = 0
		self.total_tasks = 0

	def task_completed(self):
		self.num_tasks_completed += 1
		self.progress_value.emit(int(self.num_tasks_completed / self.total_tasks * 100))

	def next_step(self, text):
		self.progress_text.emit(text)

	def finished_process(self):
		self.progress_text.emit("\tFinished.")
		self.finished.emit()

	def reset(self):
		self.num_tasks_completed = 0