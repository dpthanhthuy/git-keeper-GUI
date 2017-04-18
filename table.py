import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, \
    QVBoxLayout, QTableWidget, QToolBar, QAction
from PyQt5.QtGui import QIcon
from json import load
from time import localtime

with open('info.json', 'r') as json_file:
    info = load(json_file)


class JsonFile:

    def __init__(self, info_dict):
        self.info_dict = info_dict

    def class_number(self):
        return len(self.info_dict)

    def class_list(self):
        return self.info_dict

    def class_info(self, class_name):
        return self.info_dict.get(class_name)

    def student_number(self, class_name):
        return len(self.class_info(class_name).get('students'))

    def student_list(self, class_name):
        return self.class_info(class_name).get('students')

    def assignment_number(self, class_name):
        return len(self.class_info(class_name).get('assignments'))

    def assignment_list(self, class_name):
        return self.class_info(class_name).get('assignments')

    def assignment_info(self, class_name, assignment):
        return self.assignment_list(class_name).get(assignment)

    def is_published(self, class_name, assignment):
        return self.assignment_info(class_name, assignment).get('published')

    def assignment_repo(self, class_name, assignment):
        return self.assignment_info(class_name, assignment).get('reports_repo')

    def assignment_hash(self, class_name, assignment):
        return self.assignment_repo(class_name, assignment).get('hash')

    def assignment_path(self, class_name, assignment):
        return self.assignment_repo(class_name, assignment).get('path')

    def student_repo(self, class_name, assignment):
        return self.assignment_info(class_name, assignment).\
            get('students_repos')

    def number_students_submitted(self, class_name, assignment):
        students_submitted = 0
        for student in self.student_list(class_name):
            if self.submission_count(class_name, assignment, student) != 0:
                students_submitted += 1
        return students_submitted

    def list_students_submitted(self, class_name, assignment):
        students_submitted = {}
        for student in self.student_list(class_name):
            if self.submission_count(class_name, assignment, student) != 0:
                students_submitted[student] = self.an_assignment(
                    class_name, assignment, student)
        return students_submitted

    def student_info(self, class_name, username):
        return self.info_dict.get(class_name).get('students').get(username)

    def email_address(self, class_name, username):
        return self.student_info(class_name, username).get('email_address')

    def first_name(self, class_name, username):
        return self.student_info(class_name, username).get('first')

    def home_dir(self, class_name, username):
        return self.student_info(class_name, username).get('home_dir')

    def last_name(self, class_name, username):
        return self.student_info(class_name, username).get('last')

    def student_assignments(self, class_name, username):
        student_assignments = {}
        for an_assignment in self.assignment_list(class_name):
            student_assignment = self.\
                student_repo(class_name, an_assignment).get(username)
            if student_assignment is not None:
                student_assignments[an_assignment] = student_assignment
        return student_assignments

    def an_assignment(self, class_name, assignment, username):
        return self.student_assignments(class_name, username).get(assignment)

    def student_assignment_hash(self, class_name, assignment, username):
        return self.an_assignment(class_name, assignment, username).get('hash')

    def student_assignment_path(self, class_name, assignment, username):
        return self.an_assignment(class_name, assignment, username).get('path')

    def submission_count(self, class_name, assignment, username):
        return self.an_assignment(class_name, assignment, username).\
            get('submission_count')

    def time(self, class_name, assignment, username):
        time = localtime(self.an_assignment(class_name, assignment, username).
                         get('time'))
        return '{0}/{1}/{2} {3}:{4}:{5}'.\
            format(time.tm_mon, time.tm_mday, time.tm_year,
                   time.tm_hour, time.tm_min, time.tm_sec)


class CreateTable(QWidget):

    def __init__(self):
        super().__init__()
        self.left = 550
        self.top = 50
        self.width = 0
        self.height = 0
        self.layout = QVBoxLayout()
        self.class_name = ''
        self.assignment = ''
        self.tableClass = QTableWidget()
        self.tableAssignment = QTableWidget()
        self.tableAssignmentDetails = QTableWidget()
        self.toolbar = QToolBar(self)
        self.layout.addWidget(self.toolbar)
        self.backAction = QAction(QIcon('left_arrow.png'), 'Back', self)
        self.toolbar.addAction(self.backAction)
        self.init_ui()

    def init_ui(self):
        self.setLayout(self.layout)
        self.create_table_class()

    def close_table(self):
        if not self.tableClass.close():
            self.layout.removeWidget(self.tableClass)
            self.tableClass.deleteLater()
            self.tableClass = None
        if not self.tableAssignment.close():
            self.layout.removeWidget(self.tableAssignment)
            self.tableAssignment.deleteLater()
            self.tableAssignment = None
        if not self.tableAssignmentDetails.close():
            self.layout.removeWidget(self.tableAssignmentDetails)
            self.tableAssignmentDetails.deleteLater()
            self.tableAssignmentDetails = None

    def create_table_class(self):
        self.close_table()
        self.backAction.setVisible(False)
        self.tableClass = QTableWidget()
        self.layout.addWidget(self.tableClass)
        self.tableClass.show()
        self.setWindowTitle('Classes')
        self.tableClass.setRowCount(JsonFile(info).class_number())
        self.tableClass.setColumnCount(2)
        self.tableClass.setHorizontalHeaderItem(0, QTableWidgetItem("Name"))
        self.tableClass.\
            setHorizontalHeaderItem(1, QTableWidgetItem("Students"))
        row = 0

        for a_class in JsonFile(info).class_list():
            self.tableClass.setItem(row, 0, QTableWidgetItem(a_class))
            self.tableClass.setItem(row, 1, QTableWidgetItem(
                str(JsonFile(info).student_number(a_class))))
            row += 1

        self.tableClass.move(0, 0)
        self.tableClass.doubleClicked.connect(self.double_click_class)
        self.tableClass.setSortingEnabled(True)
        self.tableClass.setWordWrap(True)
        self.height = self.tableClass.rowHeight(0) * row + 80
        self.width = \
            self.tableClass.columnWidth(0) + \
            self.tableClass.columnWidth(1) + 50
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def create_table_assignments(self, class_name):
        self.close_table()
        self.backAction.setVisible(True)
        self.tableAssignment = QTableWidget()
        self.layout.addWidget(self.tableAssignment)
        self.tableAssignment.show()
        self.setWindowTitle('Assignments for {}'.format(class_name))
        self.tableAssignment.setRowCount(JsonFile(info).
                                         assignment_number(class_name))
        self.tableAssignment.setColumnCount(2)
        self.tableAssignment.\
            setHorizontalHeaderItem(0, QTableWidgetItem('Assignment name'))
        self.tableAssignment.\
            setHorizontalHeaderItem(1, QTableWidgetItem('Submitted'))
        row = 0

        for assignment in JsonFile(info).assignment_list(class_name):
            self.tableAssignment.setItem(row, 0, QTableWidgetItem(assignment))
            self.tableAssignment.setItem(row, 1, QTableWidgetItem(
                str(JsonFile(info).
                    number_students_submitted(class_name, assignment))))
            row += 1

        self.tableAssignment.setColumnWidth(0, 200)
        self.tableAssignment.setColumnWidth(1, 100)
        self.tableAssignment.move(0, 0)
        self.tableAssignment.setSortingEnabled(True)
        self.tableAssignment.doubleClicked.\
            connect(self.double_click_assignment)
        self.backAction.triggered.connect(self.show_table_class)
        self.tableAssignment.setWordWrap(True)
        self.height = self.tableAssignment.rowHeight(0) * row + 110
        self.width = \
            self.tableAssignment.columnWidth(0) + \
            self.tableAssignment.columnWidth(1) + 60
        self.setGeometry(self.left, self.top, self.width, self.height)

    def create_table_assignment_details(self, class_name, assignment):
        self.close_table()
        self.backAction.setVisible(True)
        self.tableAssignmentDetails = QTableWidget()
        self.layout.addWidget(self.tableAssignmentDetails)
        self.tableAssignmentDetails.show()
        self.setWindowTitle('Students for {}'.format(assignment))
        self.tableAssignmentDetails.setRowCount(JsonFile(info).
                                                student_number(class_name))
        self.tableAssignmentDetails.setColumnCount(3)
        self.tableAssignmentDetails.\
            setHorizontalHeaderItem(0, QTableWidgetItem('Name'))
        self.tableAssignmentDetails.setHorizontalHeaderItem(
            1, QTableWidgetItem('Last submission time'))
        self.tableAssignmentDetails.setHorizontalHeaderItem(
            2, QTableWidgetItem('Submission Count'))
        row = 0

        for student in JsonFile(info).student_list(class_name):
            self.tableAssignmentDetails.setItem(
                row, 0, QTableWidgetItem('{0}, {1}'.format(
                    JsonFile(info).last_name(class_name, student),
                    JsonFile(info).first_name(class_name, student))))
            self.tableAssignmentDetails.setItem(
                row, 1, QTableWidgetItem(str(
                    JsonFile(info).time(class_name, assignment, student))))
            self.tableAssignmentDetails.setItem(
                row, 2, QTableWidgetItem(str(JsonFile(info).submission_count(
                    class_name, assignment, student))))
            row += 1

        self.tableAssignmentDetails.setColumnWidth(0, 200)
        self.tableAssignmentDetails.setColumnWidth(1, 200)
        self.tableAssignmentDetails.setColumnWidth(2, 150)
        self.tableAssignmentDetails.move(0, 0)
        self.tableAssignmentDetails.setSortingEnabled(True)
        self.backAction.triggered.connect(self.show_table_assignment)
        self.tableAssignmentDetails.setWordWrap(True)
        self.height = self.tableAssignmentDetails.rowHeight(0) * row + 110
        self.width = \
            self.tableAssignmentDetails.columnWidth(0) + \
            self.tableAssignmentDetails.columnWidth(1) + \
            self.tableAssignmentDetails.columnWidth(2) + 60
        self.setGeometry(self.left, self.top, self.width, self.height)

    def double_click_class(self):
        self.class_name = self.tableClass.currentItem().text()
        self.create_table_assignments(self.class_name)

    def double_click_assignment(self):
        self.assignment = self.tableAssignment.currentItem().text()
        self.create_table_assignment_details(self.class_name, self.assignment)

    def show_table_class(self):
        self.create_table_class()

    def show_table_assignment(self):
        self.create_table_assignments(self.class_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CreateTable()
    sys.exit(app.exec_())
