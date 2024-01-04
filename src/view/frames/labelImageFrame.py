# Here should be code for labeling images
from .baseFrame import BaseFrame
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc


class ImageExtractionFrame(BaseFrame):

    def __init__(self):
        super().__init__()
        self.videoIncrementor = self.createVideoIncrementor()
        self.frameIncrementor = self.createFrameIncrementor()
        self.divider = self.createDivider()
        self.problematicFramesCheckbox = self.createProblematicFramesCheckbox()
        self.optionsFrame = self.createOptionsFrame()
        mainGridLayout = self.createMainGridLayout()
        self.setLayout(mainGridLayout)
        self.setTextEditPlaceholderText()
        self.setOptionsSignals()
        self.setRunButtonSignals()

    def createVideoIncrementor(self):
        return qtw.QSpinBox(value=5)

    def createFrameIncrementor(self):
        return qtw.QSpinBox(value=20, maximum=200)

    def createDivider(self):
        line = qtw.QFrame()
        line.setLineWidth(2)
        line.setFrameStyle(qtw.QFrame.Raised)
        line.setStyleSheet("border-top: 1px solid #d6d6d6;")
        return line

    def createProblematicFramesCheckbox(self):
        return qtw.QCheckBox(text="Extract only problematic frames")

    def createPredictionDirectoryButton(self):
        return qtw.QPushButton(text="Open", enabled=False)

    def createPredictionDirectoryTextEdit(self):
        predictionDirectoryTextEdit = qtw.QLineEdit(self, placeholderText="Choose prediction file directory...",
                                                    enabled=False)
        predictionDirectoryTextEdit.setStyleSheet(self.widgetBackgroundColor)
        return predictionDirectoryTextEdit

    def createUniqueObjectsIncrementor(self):
        return qtw.QSpinBox(value=3, maximum=10, minimum=1, enabled=False)

    def createOptionsFrame(self):
        videoIncrementorLabel = qtw.QLabel(text='Max number of videos to process:')
        frameIncrementorLabel = qtw.QLabel(text='Max number of frames to extract per video:')
        problemLabel = qtw.QLabel(text="Choose your problem(s):")
        uniqueObjectsIncrementorLabel = qtw.QLabel(text="Total number of unique objects:")

        optionsFrame = qtw.QFrame()
        gridLayout = qtw.QGridLayout()
        gridLayout.addWidget(videoIncrementorLabel, 0, 0, 1, 4)
        gridLayout.addWidget(self.videoIncrementor, 0, 4, 1, 1)
        gridLayout.addWidget(frameIncrementorLabel, 1, 0, 1, 4)
        gridLayout.addWidget(self.frameIncrementor, 1, 4, 1, 1)
        gridLayout.addWidget(self.divider, 2, 0, 1, 5)
        gridLayout.addWidget(self.problematicFramesCheckbox, 3, 0, 1, 4)
        gridLayout.addWidget(self.predictionDirectoryButton, 4, 0, 1, 1)
        gridLayout.addWidget(self.predictionDirectoryTextEdit, 4, 1, 1, 4)
        gridLayout.addWidget(uniqueObjectsIncrementorLabel, 5, 0, 1, 4)
        gridLayout.addWidget(self.uniqueObjectsIncrementor, 5, 4, 1, 1)
        gridLayout.addWidget(problemLabel, 6, 0, 1, 2)
        gridLayout.addWidget(self.duplicateObjectCheckbox, 6, 3, 1, 1)
        gridLayout.addWidget(self.missingObjectCheckbox, 6, 4, 1, 1)
        optionsFrame.setLayout(gridLayout)
        return optionsFrame

    def createMainGridLayout(self):
        mainGridLayout = qtw.QGridLayout()
        mainGridLayout.addWidget(self.fileDirectoryButton, 0, 0, 1, 1)
        mainGridLayout.addWidget(self.fileDirectoryTextEdit, 0, 1, 1, 5)
        mainGridLayout.addWidget(self.saveDirectoryButton, 1, 0, 1, 1)
        mainGridLayout.addWidget(self.saveDirectoryTextEdit, 1, 1, 1, 5)
        mainGridLayout.addWidget(self.optionsFrame, 2, 0, 2, 6)
        mainGridLayout.addWidget(self.progressBar, 4, 0, 1, 5)
        mainGridLayout.addWidget(self.progressTextEdit, 4, 0, 1, 5)
        mainGridLayout.addWidget(self.runButton, 4, 5, 1, 1)
        return mainGridLayout

    def setTextEditPlaceholderText(self):
        self.fileDirectoryTextEdit.setPlaceholderText('Choose video directory...')

    def setOptionsSignals(self):
        self.problematicFramesCheckbox.stateChanged.connect(self.toggleProblematicFrameWidgets)
        self.problematicFramesCheckbox.stateChanged.connect(self.toggleRunButton)
        self.duplicateObjectCheckbox.stateChanged.connect(self.toggleRunButton)
        self.missingObjectCheckbox.stateChanged.connect(self.toggleRunButton)
        self.predictionDirectoryButton.clicked.connect(self.getPredictionFileDirectory)
        self.predictionDirectoryButton.clicked.connect(self.toggleRunButton)

    @qtc.pyqtSlot()
    def toggleProblematicFrameWidgets(self):
        if self.problematicFramesCheckbox.isChecked():
            self.duplicateObjectCheckbox.setEnabled(True)
            self.missingObjectCheckbox.setEnabled(True)
            self.predictionDirectoryButton.setEnabled(True)
            self.predictionDirectoryTextEdit.setEnabled(True)
            self.uniqueObjectsIncrementor.setEnabled(True)
        else:
            self.duplicateObjectCheckbox.setEnabled(False)
            self.missingObjectCheckbox.setEnabled(False)
            self.predictionDirectoryButton.setEnabled(False)
            self.predictionDirectoryTextEdit.setEnabled(False)
            self.uniqueObjectsIncrementor.setEnabled(False)

    @qtc.pyqtSlot()
    def getPredictionFileDirectory(self):
        try:
            predictionFileDirectory = qtw.QFileDialog.getExistingDirectory(self)
        except ValueError:
            pass
        else:
            self.setPredictionFileDirectory(predictionFileDirectory)

    def setPredictionFileDirectory(self, predictionFileDirectory):
        if predictionFileDirectory:
            self.predictionDirectoryTextEdit.setText(predictionFileDirectory)

    def setRunButtonSignals(self):
        self.runButton.clicked.connect(self.emitWidgetInfo)
        self.runButton.clicked.connect(self.emitStart)

    @qtc.pyqtSlot()
    def emitWidgetInfo(self):
        widgetInfo = {}
        widgetInfo.setdefault('fileDirectory', self.fileDirectoryTextEdit.text())
        widgetInfo.setdefault('saveDirectory', self.saveDirectoryTextEdit.text())
        widgetInfo.setdefault('numVideosToProcess', self.videoIncrementor.value())
        widgetInfo.setdefault('numFramesPerVideo', self.frameIncrementor.value())
        widgetInfo.setdefault('extractProblematicFrames', self.problematicFramesCheckbox.isChecked())
        widgetInfo.setdefault('findDuplicateObjects', self.duplicateObjectCheckbox.isChecked())
        widgetInfo.setdefault('findMissingObjects', self.missingObjectCheckbox.isChecked())
        widgetInfo.setdefault('predictionFileDirectory', self.predictionDirectoryTextEdit.text())
        widgetInfo.setdefault('numUniqueObjects', self.uniqueObjectsIncrementor.value())
        self.info.emit(widgetInfo)

    @qtc.pyqtSlot()
    def emitStart(self):
        self.start.emit()

    @qtc.pyqtSlot()
    def toggleRunButton(self):
        if self.fileDirectoryTextEdit.text() != '' and self.saveDirectoryTextEdit.text() != '':
            if not self.problematicFramesCheckbox.isChecked():
                self.runButton.setEnabled(True)
            elif self.problematicFramesCheckbox.isChecked() and self.problematicInfoGiven():
                self.runButton.setEnabled(True)
            elif self.problematicFramesCheckbox.isChecked() and not self.problematicInfoGiven():
                self.runButton.setEnabled(False)
        else:
            self.runButton.setEnabled(False)

    def problematicInfoGiven(self):
        problematicInfoGiven = False
        if self.predictionDirectoryTextEdit.text() != '':
            if self.duplicateObjectCheckbox.isChecked() or self.missingObjectCheckbox.isChecked():
                problematicInfoGiven = True
        return problematicInfoGiven