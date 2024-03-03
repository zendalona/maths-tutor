import sys,os
from PyQt6.QtWidgets import (QApplication,QWidget,QVBoxLayout,QLabel,QLineEdit,QMessageBox, 
                             QComboBox,QMainWindow,QToolBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont,QMovie
from PyQt6.QtWidgets import QFileDialog
import shutil
class MathTutorApp(QMainWindow):  
    def __init__(self):
        super().__init__()
        self.questions=[]
        self.currentQuestionIndex=0
        self.lessonFiles=[]  
        self.initUI()
        self.loadQuestions("addition_easy.txt")  
        self.showFullScreen()
    def initUI(self):        
        centralWidget=QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout=QVBoxLayout(centralWidget)        
        topToolBar=QToolBar("Top Toolbar")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea,topToolBar)
        self.lessonSelector=QComboBox()
        self.lessonSelector.addItem("Addition (Easy)","addition_easy.txt")
        self.lessonSelector.addItem("Addition (Medium)","addition_medium.txt")
        self.lessonSelector.addItem("Add More")
        self.lessonSelector.currentIndexChanged.connect(self.onLessonChange)
        topToolBar.addWidget(self.lessonSelector)  
        self.themeSelector=QComboBox()
        self.themeSelector.addItem("High Contrast")
        self.themeSelector.addItem("Low Contrast")
        self.themeSelector.currentIndexChanged.connect(self.changeTheme)
        topToolBar.addWidget(self.themeSelector)  
        self.centralWidgetLayout=QVBoxLayout()
        self.centralWidgetLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.questionLabel=QLabel("Question will appear here")
        self.questionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.centralWidgetLayout.addWidget(self.questionLabel)
        self.answerInput=QLineEdit()
        self.answerInput.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.answerInput.returnPressed.connect(self.checkAnswer)
        self.centralWidgetLayout.addWidget(self.answerInput)
        self.gifLabel=QLabel()
        self.gifLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.updateGif("welcome-1.gif")
        self.centralWidgetLayout.addWidget(self.gifLabel)
        mainLayout.addLayout(self.centralWidgetLayout)
        self.adjustFontsAndLayout()
    def onLessonChange(self,index):
        if self.lessonSelector.currentText()=="Add More":
            self.addMoreLessons()
            return  
        lessonFile=self.lessonSelector.currentData()
        if lessonFile:
            self.loadQuestions(lessonFile)
            self.updateGif("start.gif")
    def addMoreLessons(self):
        files, _=QFileDialog.getOpenFileNames(self,"Select Lesson Files","","Text Files (*.txt)")
        for file_path in files:
            try:
                base_name=os.path.basename(file_path)
                dest_path=os.path.join("lessons",base_name)
                shutil.copy(file_path,dest_path)
                if base_name not in self.lessonFiles:
                    self.lessonSelector.insertItem(self.lessonSelector.count()-1,base_name.replace(".txt", ""), base_name)
                    self.lessonFiles.append(base_name)
            except Exception as e:
                QMessageBox.critical(self,"Error",f"Failed to add lesson: {e}")
        if files:
            self.lessonSelector.setCurrentIndex(0)
    def loadQuestions(self,filename):
            filePath=os.path.join("lessons",filename)  
            try:
                with open(filePath,"r") as file:
                    self.questions=[line.strip().split('=') for line in file.readlines()]
                self.currentQuestionIndex=0
                self.showQuestion()
            except Exception as e:
                QMessageBox.critical(self,"Error",f"Failed to load questions: {e}")
    def showQuestion(self):
        if self.currentQuestionIndex<len(self.questions):
            question, _=self.questions[self.currentQuestionIndex]
            self.questionLabel.setText(question)
            self.answerInput.clear()
            self.answerInput.setEnabled(True)  
        else:  
            self.questionLabel.setWordWrap(True)
            self.questionLabel.setText("Congratulations, you've completed all the questions!")
            self.updateGif("congratulations.gif")
            self.answerInput.setEnabled(False)  
    def checkAnswer(self):
        if self.currentQuestionIndex < len(self.questions):
            _, correctAnswer=self.questions[self.currentQuestionIndex]
            userAnswer=self.answerInput.text().strip()
            if userAnswer==correctAnswer.strip():
                self.currentQuestionIndex+=1
                self.updateGif("correct.gif" if self.currentQuestionIndex < len(self.questions) else "congratulations.gif")
                self.showQuestion()
            else:
                self.updateGif("wrong.gif")
            self.answerInput.clear()
    def updateGif(self,gifName):
        imagePath=os.path.join("images",gifName)  
        self.gifLabel.setMovie(None)  
        self.gifMovie=QMovie(imagePath)
        self.gifLabel.setMovie(self.gifMovie)
        self.gifMovie.start()
    def keyPressEvent(self,event):     
        if event.key()==Qt.Key.Key_Shift:
            self.readQuestionAloud()
    def readQuestionAloud(self):
        if self.currentQuestionIndex<len(self.questions):
            question, _=self.questions[self.currentQuestionIndex]
            question_to_read=question.split('=')[0].strip()  
            if sys.platform.startswith('darwin'):
                os.system(f'say "{question_to_read}"')
            elif sys.platform.startswith('linux') or sys.platform.startswith('linux2') or sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
                os.system(f'espeak "{question_to_read}"')
    def changeTheme(self,index):
        if index==0:
            self.setStyleSheet("QWidget { background-color: #000000; color: #FFFFFF; }")
        else:
            self.setStyleSheet("QWidget { background-color: #F0F0F0; color: #333333; }")
    def adjustFontsAndLayout(self):
            baseFontSize=max(self.width()//13,24)  
            self.questionLabel.setFont(QFont("Arial",baseFontSize,QFont.Weight.Bold))
            self.answerInput.setFont(QFont("Arial",baseFontSize))
    def resizeEvent(self,event):
        super().resizeEvent(event)
        self.adjustFontsAndLayout()  
if __name__=='__main__':
    app=QApplication(sys.argv)
    mathTutorApp=MathTutorApp()
    mathTutorApp.show()
    sys.exit(app.exec())
