from PyQt5 import QtWidgets as qtw 
from .base_frame import BaseFrame 
from PyQt5 import QtCore as qtc

class PredictionAnalysisFrame(BaseFrame):

    def __init__(self):
        super().__init__()
        self.calibrate_checkbox = qtw.QCheckBox(text="Calibrate setup", checked=True)
        self.choice_checkbox = qtw.QCheckBox(text="Include choice statistics")
        self.threshold_checkbox = qtw.QCheckBox(text="Change flight duration threshold (seconds)")
        self.threshold_incrementor = qtw.QSpinBox(value=5, maximum=20, enabled=False)
        self.spreadsheet_checkbox = qtw.QCheckBox(text="Change spreadsheet name")

        self.spreadsheet_text_edit = self.create_spreadsheet_text_edit()
        self.options_frame = self.create_options_frame()
        main_grid_layout = self.create_main_grid_layout()

        self.setLayout(main_grid_layout)
        self.set_text_edit_placeholder_text()
        self.set_options_signals()
        self.set_run_button_signals()

    def create_spreadsheet_text_edit(self):
        spreadsheet_text_edit = qtw.QLineEdit(self, text="Master", enabled=False)
        spreadsheet_text_edit.setStyleSheet(self.widget_background_color)
        return spreadsheet_text_edit

    def create_options_frame(self):
        options_frame = qtw.QFrame()
        grid_layout = qtw.QGridLayout()
        grid_layout.addWidget(self.calibrate_checkbox, 0, 0, 1, 5)
        grid_layout.addWidget(self.choice_checkbox, 1, 0, 1, 5)
        grid_layout.addWidget(self.threshold_checkbox, 2, 0, 1, 4)
        grid_layout.addWidget(self.threshold_incrementor, 2, 4, 1, 1)
        grid_layout.addWidget(self.spreadsheet_checkbox, 3, 0, 1, 5)
        grid_layout.addWidget(self.spreadsheet_text_edit, 4, 0, 1, 5)
        options_frame.setLayout(grid_layout)
        return options_frame

    def create_main_grid_layout(self):
        main_grid_layout = qtw.QGridLayout()
        main_grid_layout.addWidget(self.file_directory_button, 0, 0, 1, 1)
        main_grid_layout.addWidget(self.file_directory_text_edit, 0, 1, 1, 4)
        main_grid_layout.addWidget(self.save_directory_button, 1, 0, 1, 1)
        main_grid_layout.addWidget(self.save_directory_text_edit, 1, 1, 1, 4)
        main_grid_layout.addWidget(self.options_frame, 2, 0, 4, 5)
        main_grid_layout.addWidget(self.progress_bar, 6, 0, 1, 4)
        main_grid_layout.addWidget(self.progress_text_edit, 6, 0, 1, 4)
        main_grid_layout.addWidget(self.run_button, 6, 4, 1, 1)
        return main_grid_layout

    def set_text_edit_placeholder_text(self):
        self.file_directory_text_edit.setPlaceholderText('Choose prediction file directory...')

    def set_options_signals(self):
        self.threshold_checkbox.stateChanged.connect(self.toggle_threshold_incrementor)
        self.spreadsheet_checkbox.stateChanged.connect(self.toggle_spreadsheet_text_edit)

    @qtc.pyqtSlot()
    def toggle_threshold_incrementor(self):
        if self.threshold_checkbox.isChecked():
            self.threshold_incrementor.setEnabled(True)
        else:
            self.threshold_incrementor.setEnabled(False)

    @qtc.pyqtSlot()
    def toggle_spreadsheet_text_edit(self):
        if self.spreadsheet_checkbox.isChecked():
            self.spreadsheet_text_edit.setEnabled(True)
        else:
            self.spreadsheet_text_edit.setEnabled(False)

    def set_run_button_signals(self):
        self.run_button.clicked.connect(self.emit_widget_info)
        self.run_button.clicked.connect(self.emit_start)

    @qtc.pyqtSlot()
    def emit_widget_info(self):
        # Important info that is used by backend processes (routes to receiveInfo())
        widget_info = {}
        widget_info.setdefault('file_directory', self.file_directory_text_edit.text())
        widget_info.setdefault('save_directory', self.save_directory_text_edit.text())
        widget_info.setdefault('calibrate_setup', self.calibrate_checkbox.isChecked())
        widget_info.setdefault('include_choice_stats', self.choice_checkbox.isChecked())
        widget_info.setdefault('duration_threshold', self.threshold_incrementor.value())
        widget_info.setdefault('name_excel_file', self.spreadsheet_text_edit.text())
        self.info.emit(widget_info)

    @qtc.pyqtSlot()
    def emit_start(self):
        self.start.emit()
                


