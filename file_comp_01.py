#!/usr/bin/python3

import time 
import sys
import os 

VERSION   = "1.0.0"
APP_NAME  = "File Comp"
VERBOSE   = True
DEBUG     = False
FIRST     = 0
LAST      = -1
ME        = os.path.split(sys.argv[FIRST])[LAST]  # Name of this file
MY_PATH   = os.path.dirname(os.path.realpath(__file__))  # Path for this file

try:
   from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QFrame, QAction, qApp)
   from PyQt5.QtWidgets import (QGridLayout, QVBoxLayout, QHBoxLayout, QBoxLayout, QSplashScreen)
   from PyQt5.QtWidgets import (QLabel, QComboBox, QTabWidget, QTextEdit, QLineEdit, QDialogButtonBox)
   from PyQt5.QtWidgets import (QSlider, QDial, QScrollBar, QListWidget, QListWidgetItem, QPushButton)
   from PyQt5.QtWidgets import (QInputDialog, QLineEdit, QFileDialog, QDialog, QMessageBox)
   from PyQt5.QtGui import (QPixmap, QFont, QIcon, QStatusTipEvent, QColor,  QPalette, QTextCursor)
   from PyQt5.QtCore import (Qt, pyqtSignal, QSize, QUrl, QEvent)
except ModuleNotFoundError:
   sys.stderr.write("ERROR -- Unable to import the 'PyQt5' library\n")
   sys.stderr.write("         try: pip3 install pyqt5 --user\n")
   sys.stderr.flush()
   sys.exit(99)
      
# ======================================================================================= CLASS MainWindow   
class MainWindow(QMainWindow):
   # ------------------------------------------------------------------------------------ __init__()
   def __init__(self, parent=None):
      """ """
      super(MainWindow, self).__init__(parent)
      
      self.folder_a = None                                          # folder a  
      self.folder_b = None                                          # folder b  
      self.folder_a_file_list = []                                  # list of files in folder a 
      self.folder_b_file_list = []                                  # list of files in folder b
      self.output_file        = os.path.join(MY_PATH, "output.csv") # output file  
      
      self.main_widget = QWidget(self)
      self.main_layout = QGridLayout(self.main_widget)
      self.setCentralWidget(self.main_widget)   
      
      self.create_menu_bar()
      
      self.setGeometry(100, 100,  800, 800)
      
      self.folder_a_label = QLabel("Folder A")
      self.folder_a_text  = QLabel(self.folder_a)
      self.folder_b_label = QLabel("Folder B")
      self.folder_b_text  = QLabel(self.folder_b)
      self.process_files_button = QPushButton("Process Files")
      self.process_files_button.clicked.connect(self.process_files) 
      self.process_files_button.setVisible(False) 
      # Place widgets in MainWindow                                    row   col 
      #                           Widget,                    row, col, span, span,      alignment(s)  
      self.main_layout.addWidget( self.folder_a_label,         1,   2,    1,    1, Qt.AlignTop | Qt.AlignRight )
      self.main_layout.addWidget( self.folder_a_text,          1,   3,    1,    1, Qt.AlignTop | Qt.AlignLeft  )
      self.main_layout.addWidget( self.folder_b_label,         2,   2,    1,    1, Qt.AlignTop | Qt.AlignRight ) 
      self.main_layout.addWidget( self.folder_b_text,          2,   3,    1,    1, Qt.AlignTop | Qt.AlignLeft  )
      self.main_layout.addWidget( self.process_files_button,   3,   2,    1,    1                              )
      self.main_layout.addWidget( QLabel(" "),                 6,   1,    1,    1, Qt.AlignTop | Qt.AlignLeft  )
 
      self.main_widget.setLayout(self.main_layout)
     
   # ------------------------------------------------------------------------------------ create_menu_bar()   
   def create_menu_bar(self):
      """ """   
      menu_bar = self.menuBar() 
      # -------------------------------------------------------------- 
      select_folder_a_action = QAction('Folder A', self)
      select_folder_a_action.triggered.connect( self.get_folder_a )
      # -------------------------------------------------------------- 
      select_folder_b_action = QAction('Folder B', self)
      select_folder_b_action.triggered.connect( self.get_folder_b )
      # -------------------------------------------------------------- 
      exit_action = QAction( '&Exit', self)
      exit_action.setShortcut('Ctrl+Q')
      exit_action.setStatusTip('Exit application')
      exit_action.triggered.connect( qApp.quit)
      # -------------------------------------------------------------- 
      fileMenu = menu_bar.addMenu('&File')       
      fileMenu.addAction(select_folder_a_action)
      fileMenu.addAction(select_folder_b_action)       
      fileMenu.addAction(exit_action)
   
   # ------------------------------------------------------------------------------------ get_folder_a()
   def get_folder_a(self):
      """ """
      file_dialog = QFileDialog()
      folder = QFileDialog.getExistingDirectory(self                      , 
                                                "Select folder A"         , 
                                                MY_PATH                   , 
                                                QFileDialog.ShowDirsOnly  )
      self.folder_a = folder    
      self.folder_a_text.setText(self.folder_a) 
      self.folder_a_file_list = [f for f in os.listdir(self.folder_a) if os.path.isfile(os.path.join(self.folder_a, f))]
      if DEBUG: print(self.folder_a_file_list)
      if self.folder_a != None and self.folder_b != None:
         self.process_files_button.setVisible(True) 
      else:
         self.process_files_button.setVisible(False)       
      return folder 

   # ------------------------------------------------------------------------------------ get_folder_b()
   def get_folder_b(self):
      """ """
      file_dialog = QFileDialog()
      folder = QFileDialog.getExistingDirectory(self                      , 
                                                "Select folder B"         , 
                                                MY_PATH                   , 
                                                QFileDialog.ShowDirsOnly  )
      self.folder_b = folder      
      self.folder_b_text.setText(self.folder_b)  
      self.folder_b_file_list = [f for f in os.listdir(self.folder_b) if os.path.isfile(os.path.join(self.folder_b, f))]
      if DEBUG: print(self.folder_b_file_list)
      if self.folder_a != None and self.folder_b != None:
         self.process_files_button.setVisible(True)      
      else:
         self.process_files_button.setVisible(False) 
      return folder 

   def process_files(self):
      """ """
      pass
      # ************************************
      # *** PLACE FILE PROCESS CODE HERE ***
      # ************************************
      """
      For Reference: 
      self.folder_a           # folder a  
      self.folder_b           # folder b  
      self.folder_a_file_list # list of files in folder a (no path)
      self.folder_b_file_list # list of files in folder b (no path)
      self.output_file        # output file  
      """       
      return


      
       
# === MAIN ============================================================================== MAIN
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    windowMain = MainWindow()
    windowMain.show()
    sys.exit(app.exec_())   
   
   
   
