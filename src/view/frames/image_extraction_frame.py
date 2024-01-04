from .base_frame import BaseFrame
from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtCore as qtc

class ImageExtractionFrame(BaseFrame):

	def __init__(self):
		super().__init__()
		self.video_incrementor_label = qtw.QLabel(text='Max number of videos to process:')
		self.frame_incrementor_label = qtw.QLabel(text='Max number of frames to extract per video:')
		self.problem_label = qtw.QLabel(text="Choose your problem(s):")
		self.unique_objects_incrementor_label = qtw.QLabel(text="Total number of unique objects:")
		self.problematic_frames_checkbox = qtw.QCheckBox(text="Extract only problematic frames")
		self.duplicate_object_checkbox = qtw.QCheckBox(text="Duplicate objects", enabled=False)
		self.missing_object_checkbox = qtw.QCheckBox(text="Missing objects", enabled=False)
		self.prediction_directory_button = qtw.QPushButton(text="Open", enabled=False)
		self.video_incrementor = qtw.QSpinBox(value=5)
		self.frame_incrementor = qtw.QSpinBox(value=20, maximum=200)
		self.unique_objects_incrementor = qtw.QSpinBox(value=3, maximum=10, minimum=1, enabled=False)

		self.divider = self.create_divider()
		self.prediction_directory_text_edit = self.create_prediction_directory_text_edit()
		self.options_frame = self.create_options_frame()
		main_grid_layout = self.create_main_grid_layout()

		self.setLayout(main_grid_layout)
		self.set_text_edit_placeholder_text()
		self.set_options_signals()
		self.set_run_button_signals()

	def create_divider(self):
		line = qtw.QFrame()
		line.setLineWidth(2)
		line.setFrameStyle(qtw.QFrame.Raised)
		line.setStyleSheet("border-top: 1px solid #d6d6d6;")
		return line 

	def create_prediction_directory_text_edit(self):
		prediction_directory_text_edit = qtw.QLineEdit(self, placeholderText="Choose prediction file directory...", enabled=False)
		prediction_directory_text_edit.setStyleSheet(self.widget_background_color)
		return prediction_directory_text_edit

	def create_options_frame(self):
		options_frame = qtw.QFrame()
		grid_layout = qtw.QGridLayout()
		grid_layout.addWidget(self.video_incrementor_label, 0, 0, 1, 4)
		grid_layout.addWidget(self.video_incrementor, 0, 4, 1, 1)
		grid_layout.addWidget(self.frame_incrementor_label, 1, 0, 1, 4)
		grid_layout.addWidget(self.frame_incrementor, 1, 4, 1, 1)
		grid_layout.addWidget(self.divider, 2, 0, 1, 5)
		grid_layout.addWidget(self.problematic_frames_checkbox, 3, 0, 1, 4)
		grid_layout.addWidget(self.prediction_directory_button, 4, 0, 1, 1)
		grid_layout.addWidget(self.prediction_directory_text_edit, 4, 1, 1, 4)
		grid_layout.addWidget(self.unique_objects_incrementor_label, 5, 0, 1, 4)
		grid_layout.addWidget(self.unique_objects_incrementor, 5, 4, 1, 1)
		grid_layout.addWidget(self.problem_label, 6, 0, 1, 2)
		grid_layout.addWidget(self.duplicate_object_checkbox, 6, 3, 1, 1)
		grid_layout.addWidget(self.missing_object_checkbox, 6, 4, 1, 1)
		options_frame.setLayout(grid_layout)
		return options_frame

	def create_main_grid_layout(self):
		main_grid_layout = qtw.QGridLayout()
		main_grid_layout.addWidget(self.file_directory_button, 0, 0, 1, 1)
		main_grid_layout.addWidget(self.file_directory_text_edit, 0, 1, 1, 5)
		main_grid_layout.addWidget(self.save_directory_button, 1, 0, 1, 1)
		main_grid_layout.addWidget(self.save_directory_text_edit, 1, 1, 1, 5)
		main_grid_layout.addWidget(self.options_frame, 2, 0, 2, 6)
		main_grid_layout.addWidget(self.progress_bar, 4, 0, 1, 5)
		main_grid_layout.addWidget(self.progress_text_edit, 4, 0, 1, 5)
		main_grid_layout.addWidget(self.run_button, 4, 5, 1, 1)
		return main_grid_layout

	def set_text_edit_placeholder_text(self):
		self.file_directory_text_edit.setPlaceholderText('Choose video directory...')

	def set_options_signals(self):
		self.problematic_frames_checkbox.stateChanged.connect(self.toggle_problematic_frame_widgets)
		self.problematic_frames_checkbox.stateChanged.connect(self.toggle_run_button)
		self.duplicate_object_checkbox.stateChanged.connect(self.toggle_run_button)
		self.missing_object_checkbox.stateChanged.connect(self.toggle_run_button)
		self.prediction_directory_button.clicked.connect(self.get_prediction_file_directory)
		self.prediction_directory_button.clicked.connect(self.toggle_run_button)

	@qtc.pyqtSlot()
	def toggle_problematic_frame_widgets(self):
		if self.problematic_frames_checkbox.isChecked():
			self.duplicate_object_checkbox.setEnabled(True)
			self.missing_object_checkbox.setEnabled(True)
			self.prediction_directory_button.setEnabled(True)
			self.prediction_directory_text_edit.setEnabled(True)
			self.unique_objects_incrementor.setEnabled(True)
		else:
			self.duplicate_object_checkbox.setEnabled(False)
			self.missing_object_checkbox.setEnabled(False)
			self.prediction_directory_button.setEnabled(False)
			self.prediction_directory_text_edit.setEnabled(False)
			self.unique_objects_incrementor.setEnabled(False)

	@qtc.pyqtSlot()
	def get_prediction_file_directory(self):
		try:
			prediction_file_directory = qtw.QFileDialog.getExistingDirectory(self)
		except ValueError:
			pass
		else:
			self.set_prediction_file_directory(prediction_file_directory)

	def set_prediction_file_directory(self, prediction_file_directory):
		if prediction_file_directory:
			self.prediction_directory_text_edit.setText(prediction_file_directory)

	def set_run_button_signals(self):
		self.run_button.clicked.connect(self.emit_widget_info)
		self.run_button.clicked.connect(self.emit_start)
		
	@qtc.pyqtSlot()
	def emit_widget_info(self):
		# Important info that is used by backend processes (routes to receiveInfo())
		widget_info = {}
		widget_info.setdefault('file_directory', self.file_directory_text_edit.text())
		widget_info.setdefault('save_directory', self.save_directory_text_edit.text())
		widget_info.setdefault('num_videos_to_process', self.video_incrementor.value())
		widget_info.setdefault('num_frames_per_video', self.frame_incrementor.value())
		widget_info.setdefault('extract_problematic_frames', self.problematic_frames_checkbox.isChecked())
		widget_info.setdefault('find_duplicate_objects', self.duplicate_object_checkbox.isChecked())
		widget_info.setdefault('find_missing_objects', self.missing_object_checkbox.isChecked())
		widget_info.setdefault('prediction_file_directory', self.prediction_directory_text_edit.text())
		widget_info.setdefault('num_unique_objects', self.unique_objects_incrementor.value())
		self.info.emit(widget_info)

	@qtc.pyqtSlot()
	def emit_start(self):
		self.start.emit()

	@qtc.pyqtSlot()
	def toggle_run_button(self):
		# Run button is only accessible after a save and file directory has been chosen
		# Additionally, if the problematic frame checkbox is selected, ensure that more info is given
		if self.file_directory_text_edit.text() != '' and self.save_directory_text_edit.text() != '':
			if not self.problematic_frames_checkbox.isChecked():
				self.run_button.setEnabled(True)
			elif self.problematic_frames_checkbox.isChecked() and self.problematic_info_given():
				self.run_button.setEnabled(True)
			elif self.problematic_frames_checkbox.isChecked() and not self.problematic_info_given():
				self.run_button.setEnabled(False)
		else:
			self.run_button.setEnabled(False)

	def problematic_info_given(self):
		problematic_info_given = False
		if self.prediction_directory_text_edit.text() != '':
			if self.duplicate_object_checkbox.isChecked() or self.missing_object_checkbox.isChecked():
				problematic_info_given = True
		return problematic_info_given