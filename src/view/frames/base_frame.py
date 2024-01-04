from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtCore as qtc

'''
    Contains widgets and functionalities that are shared between 
    ImageExtractionFrame and PredictionAnalysisFrame
'''
class BaseFrame(qtw.QFrame):

    # These will inform the controller of the current window's  
    # widget info and if the corresponding process should start
    info = qtc.pyqtSignal(dict)
    start = qtc.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.widget_background_color = 'background-color: rgb(255, 255, 255);' 
        self.file_directory_button = qtw.QPushButton(text='Open')
        self.save_directory_button = qtw.QPushButton(text='Open')
        self.run_button = qtw.QPushButton(text="Run", enabled=False)
        self.progress_text_edit = qtw.QLabel(text="\tWaiting for program to start...\t\t")

        self.file_directory_text_edit = self.create_file_directory_text_edit()
        self.save_directory_text_edit = self.create_save_directory_text_edit()
        self.progress_bar = self.create_progress_bar()
        
        self.set_directory_signals()

    def create_file_directory_text_edit(self):
        file_directory_text_edit = qtw.QLineEdit(self)
        file_directory_text_edit.setStyleSheet(self.widget_background_color)
        return file_directory_text_edit

    def create_save_directory_text_edit(self):
        save_directory_text_edit = qtw.QLineEdit(self, placeholderText='Choose save directory...')
        save_directory_text_edit.setStyleSheet(self.widget_background_color)
        return save_directory_text_edit

    def create_progress_bar(self):
        progress_bar = qtw.QProgressBar(self, minimum=0, maximum=100, value=0, textVisible=False)
        progress_bar.setStyleSheet(f'border: 1px solid grey; border-radius: 5px; {self.widget_background_color}')
        return progress_bar

    def set_directory_signals(self):
        self.file_directory_button.clicked.connect(self.get_file_directory)
        self.file_directory_button.clicked.connect(self.toggle_run_button)
        self.save_directory_button.clicked.connect(self.get_save_directory)
        self.save_directory_button.clicked.connect(self.toggle_run_button)
    
    @qtc.pyqtSlot()
    def get_file_directory(self):
        try:
            file_directory = qtw.QFileDialog.getExistingDirectory(self)
        except ValueError:
            pass
        else:
            self.set_file_directory(file_directory)

    @qtc.pyqtSlot()
    def get_save_directory(self):
        try:
            save_directory = qtw.QFileDialog.getExistingDirectory(self)
        except ValueError:
            pass
        else:
            self.set_save_directory(save_directory)

    def set_file_directory(self, file_directory):
        if file_directory:
            self.file_directory_text_edit.setText(file_directory)

    def set_save_directory(self, save_directory):
        if save_directory:
            self.save_directory_text_edit.setText(save_directory)

    @qtc.pyqtSlot()
    def toggle_run_button(self):
        # Run button is only accessible after a save and file directory has been chosen
        if self.save_directory_text_edit.text() != '' and self.file_directory_text_edit.text() != '':
            self.run_button.setEnabled(True)
        else:
            self.run_button.setEnabled(False)
    
