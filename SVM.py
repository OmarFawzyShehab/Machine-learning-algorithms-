import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QFileDialog, QComboBox
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.svm import SVC
from tkinter import *
from PyQt5.QtGui import QIcon

class SVMApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(600, 200, 900, 600)
        self.setWindowTitle('SVM')
        self.setWindowIcon(QIcon('C:\\Users\\Hp\\Downloads\\2857360.png'))

        self.Text1 = QLineEdit(self)
        self.Text1.setGeometry(150, 30, 500, 50)
        self.Text1.setStyleSheet('background-color:#f5cd79;color ; font-size:20px')

        self.Text2 = QLineEdit(self)
        self.Text2.setGeometry(300, 120, 50, 40)
        self.Text2.setText("30")  # Set default test_data size(%)
        self.Text2.setStyleSheet('background-color:#f5cd79;color ; font-size:20px')

        self.Text3 = QComboBox(self)
        self.Text3.setGeometry(300, 200, 100, 40)
        self.Text3.addItems(["rbf", "linear"])
        self.Text3.setStyleSheet('background-color:#f5cd79;color ; font-size:20px')

        self.btn1 = QPushButton('Browse', self)
        self.btn1.setGeometry(700, 30, 100, 50)
        self.btn1.setToolTip('Browse')
        self.btn1.clicked.connect(self.browse_csv)
        self.btn1.setStyleSheet('background-color:#f5cd79;color ; font-size:20px')

        self.btn2 = QPushButton('Run', self)
        self.btn2.setGeometry(700, 400, 100, 50)
        self.btn2.clicked.connect(self.run_svm)
        self.btn2.setEnabled(False)
        self.btn2.setStyleSheet('background-color:#f5cd79;color ; font-size:20px')

        self.name2 = QLabel('  CSV file', self)
        self.name2.setGeometry(30, 30, 100, 50)
        self.name2.setStyleSheet('background-color:#f5cd79;color ; font-size:20px')

        self.name3 = QLabel('   test_data size(%):', self)
        self.name3.setGeometry(30, 120, 185, 50)
        self.name3.setStyleSheet('background-color:#f5cd79;color ; font-size:20px')

        self.name4 = QLabel('   kernal type:', self)
        self.name4.setGeometry(30, 200, 180, 50)
        self.name4.setStyleSheet('background-color:#f5cd79;color ; font-size:20px')

        self.setStyleSheet('background-color:#006266;')

        self.csv_filename = None

    def browse_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        self.setWindowIcon(QIcon('C:\\Users\\Hp\\Downloads\\2857360.png'))

        if filename:
            self.Text1.setText(filename)
            self.csv_filename = filename
            self.btn2.setEnabled(True)

    def run_svm(self):
        if self.csv_filename:
            try:
                test_data_size = float(self.Text2.text())
                if test_data_size > 40:
                    print("Warning: Your test data size is too high.")
                    return
            except ValueError:
                print("Please enter a valid number for the test data size.")
                return

            data = pd.read_csv(self.csv_filename)
            x = data.iloc[:, :-1]
            y = data.iloc[:, -1]

            new_data = SimpleImputer(missing_values=np.nan, strategy="mean")
            new_data = new_data.fit_transform(data)
            new_data = pd.DataFrame(new_data)
            x = new_data.iloc[:, :-1]
            y = new_data.iloc[:, -1]

            scale = StandardScaler()
            x = scale.fit_transform(x)

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_data_size / 100, random_state=0)

            kernel_type = self.Text3.currentText()

            svm_model = SVC(C=2.0, kernel=kernel_type)
            svm_model = svm_model.fit(x_train, y_train)
            y_predict = svm_model.predict(x_test)

            ac = accuracy_score(y_test, y_predict)
            print(ac)

            cr = classification_report(y_test, y_predict)
            print(cr)

            cm = np.array(confusion_matrix(y_test, y_predict, labels=[0, 1]))
            confusion = pd.DataFrame(cm, index=['actual 0', 'actual 1'], columns=['predicted 0', 'predicted 1'])

            sns.heatmap(confusion, center=True)
            plt.show()

            window = Tk()
            window.title("Result")
            window.geometry("1000x500")
            window.configure(bg='#006266')
            result = Label(window, text=f"Accuracy: {metrics.accuracy_score(y_test, y_predict)}",
                           font=("Arial", 20),
                           bg='#ccae62', fg='#fff')
            result.pack()
            classification = Label(window,
                                    text=f"Classification Report: {metrics.classification_report(y_test, y_predict)}",
                                    font=("Arial", 20), bg='#ccae62', fg='#fff')
            classification.pack()
            window.mainloop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = SVMApp()
    myApp.show()
    sys.exit(app.exec_())
