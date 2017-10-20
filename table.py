import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, \
    QVBoxLayout, QTableWidget, QToolBar, QAction, QPushButton
from PyQt5.QtGui import QIcon
from json import load
from time import localtime

with open('info.json', 'r') as json_file:
    info = load(json_file)


class JsonInfo:
    """Provides methods for extracting information from the info dictionary."""

    def __init__(self, info_dict: dict):
        """
        Create the object
        :param info_dict: dictionary of info
        """

        self.info_dict = info_dict

    def class_count(self) -> int:
        """
        Get the number of classes.

        :return: number of classes
        """

        return len(self.info_dict)

    def class_list(self) -> list:
        """
        Get the list of classes.

        :return: list of classes
        """

        return list(self.info_dict.keys())

    def student_count(self, class_name: str) -> int:
        """
        Get the number of students in a class.

        :param class_name: name of a class
        :return: number of students in the class
        """

        return len(self.info_dict[class_name]['students'])

    def student_list(self, class_name: str) -> list:
        """
        Get the list of the students in a class.

        :param class_name: name of a class
        :return: list of students in the class
        """

        return list(self.info_dict[class_name]['students'])

    def assignment_count(self, class_name: str) -> int:
        """
        Get the number of assignments for a class.

        :param class_name: name of a class
        :return: number of assignments for the class
        """

        return len(self.info_dict[class_name]['assignments'])

    def assignment_list(self, class_name: str) -> list:
        """
        Get the info dictionary of assignments for a class.

        :param class_name: name of a class
        :return: info dictionary of assignments for a class
        """

        return list(self.info_dict[class_name]['assignments'])

    def is_published(self, class_name: str, assignment: str) -> bool:
        """
        Determine if an assignment is published.

        :param class_name: name of a class
        :param assignment: name of an assignment
        :return: True if the assignment is published, False otherwise
        """

        return self.info_dict[class_name][assignment]['published']

    def assignment_hash(self, class_name: str, assignment: str) -> str:
        """
        Get the hash of an assignment.

        :param class_name: name of a class
        :param assignment: name of an assignment
        :return: assignment's hash
        """

        return self.info_dict[class_name][assignment]['hash']

    def assignment_path(self, class_name: str, assignment: str) -> str:
        """
        Get the path of an assignment.

        :param class_name: name of a class
        :param assignment: name of an assignment
        :return: assignment's path
        """

        return self.info_dict[class_name][assignment]['path']

    def student_submitted_count(self, class_name: str, assignment: str) -> int:
        """
        Get the number of students who submitted an assignment.

        :param class_name: name of a class
        :param assignment: name of an assignment
        :return: number of students who submitted the assignment
        """

        students_submitted = 0
        for student in self.student_list(class_name):
            if self.submission_count(class_name, assignment, student) != 0:
                students_submitted += 1
        return students_submitted

    def students_submitted_list(self, class_name: str, assignment: str) \
            -> list:
        """
        Get the info dictionary of students who submitted an assignment.

        :param class_name: name of a class
        :param assignment: name of an assignment
        :return: info dictionary of students who submitted an assignment
        """

        students_submitted = []
        for student in self.student_list(class_name):
            if self.submission_count(class_name, assignment, student) != 0:
                students_submitted.append(student)
        return students_submitted

    def email_address(self, class_name: str, username: str) -> str:
        """
        Get the email address of a student.

        :param class_name: name of a class
        :param username: username of a student
        :return: student's email address
        """

        return self.info_dict[class_name]['students'][username][
            'email_address']

    def first_name(self, class_name: str, username: str) -> str:
        """
        Get the first name of a student.

        :param class_name: name of a class
        :param username: username of a student
        :return: student's first name
        """

        return self.info_dict[class_name]['students'][username]['first']

    def home_dir(self, class_name: str, username: str) -> str:
        """
        Get the home directory of a student.

        :param class_name: name of a class
        :param username: username of a student
        :return: student's home directory
        """

        return self.info_dict[class_name]['students'][username]['home_dir']

    def last_name(self, class_name: str, username: str) -> str:
        """
        Get the last name of a student.

        :param class_name: name of a class
        :param username: username of a student
        :return: student's last name
        """

        return self.info_dict[class_name]['students'][username]['last']

    def assignments_by_student_list(self, class_name: str, username: str) \
            -> list:
        """
        Get all the assignments for a student.

        :param class_name: name of a student
        :param username: username of a student
        :return: an info dict of all the assignments for a student
        """

        student_assignments = []
        for an_assignment in self.assignment_list(class_name):
            student_assignment = self.info_dict[class_name]['assignments'][
                an_assignment]['students_repos'][username]
            if student_assignment is not None:
                student_assignments.append(an_assignment)
        return student_assignments

    def assignment_by_student_hash(self, class_name: str, assignment: str,
                                   username: str) -> str:
        """
        Get the hash of a student's assignment.

        :param class_name: name of a class
        :param assignment: name of an assignment
        :param username: username of a student
        :return: the hash of a student's assignment
        """
        return self.info_dict[class_name]['assignments'][assignment][
            'students_repos'][username]['hash']

    def assignment_by_student_path(self, class_name: str, assignment: str,
                                   username: str) -> str:
        """
        Get the path of a student's assignment.

        :param class_name: name of a class
        :param assignment: name of an assignment
        :param username: username of a student
        :return: the path of a student's assignment
        """

        return self.info_dict[class_name]['assignments'][assignment][
            'students_repos'][username]['path']

    def submission_count(self, class_name: str, assignment: str,
                         username: str) -> int:
        """
        Get the submission count of a student for an assignment.

        :param class_name: name of a class
        :param assignment: name of an assignment
        :param username: username of a student
        :return: student's submission count for an assignment
        """

        return self.info_dict[class_name]['assignments'][assignment][
            'students_repos'][username]['submission_count']

    def time(self, class_name: str, assignment: str, username: str):
        """
        Get the Unix time a student last submitted an assignment.

        :param class_name: name of a class
        :param assignment: name of an assignment
        :param username: username of a student
        :return: the Unix time a student last submitted an assignment.
        """

        return self.info_dict[class_name]['assignments'][assignment][
            'students_repos'][username]['time']

    def time_converted(self, class_name: str, assignment: str, username: str)\
            -> str:
        """
        Get a string of the time a student last submitted an assignment
        (month/day/year hour:min:second)

        :param class_name: name of a class
        :param assignment: name of an assignment
        :param username: username of a student
        :return: a string of the time a student last submitted an assignment
        """

        time = localtime(self.time(class_name, assignment, username))
        return '{0}/{1}/{2} {3}:{4}:{5}'.\
            format(time.tm_mon, time.tm_mday, time.tm_year,
                   time.tm_hour, time.tm_min, time.tm_sec)

    def get_username_from_name(self, class_name: str, name: str) -> str:
        """
        Get the username of a student from his/her full name.

        :param class_name: name of a class
        :param name: a student's full name in the format
        "last name, first name"
        :return: student's username
        """

        for username in self.student_list(class_name):
            name_form = '{0}, {1}'.format(
                self.last_name(class_name, username),
                self.first_name(class_name, username))
            if name_form == name:
                return username

    def last_first_username(self, class_name: str, username: str) -> str:
        """
        Get the last name, first name, and username of a student.

        :param class_name: name of a class
        :param username: username of a student
        :return: a string in the format "last name, first name, username"

        """
        return self.info_dict[class_name]['students'][username][
            'last_first_username']


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
        self.username = ''
        self.tableClass = QTableWidget()
        self.tableAssignment = QTableWidget()
        self.tableAssignmentDetails = QTableWidget()
        self.tableStudent = QTableWidget()
        self.toolbar = QToolBar(self)
        self.layout.addWidget(self.toolbar)
        self.fetchSubmissionButton = QPushButton("Fetch", self.toolbar)
        self.backAction = QAction(QIcon('left_arrow.png'), 'Back', self)
        self.toolbar.addAction(self.backAction)
        self.init_ui()

    def init_ui(self):
        self.setLayout(self.layout)
        self.create_table_class()

    def close_table(self, table):
        if not table.close():
            self.layout.removeWidget(table)
            table.deleteLater()
            table = None

    def close_all_tables(self):
        self.close_table(self.tableClass)
        self.close_table(self.tableAssignment)
        self.close_table(self.tableAssignmentDetails)
        self.close_table(self.tableStudent)

    def create_table_class(self):
        self.close_all_tables()
        self.backAction.setVisible(False)
        self.fetchSubmissionButton.setVisible(False)
        self.tableClass = QTableWidget()
        self.layout.addWidget(self.tableClass)
        self.tableClass.show()
        self.setWindowTitle('Classes')
        self.tableClass.setRowCount(JsonInfo(info).class_count())
        self.tableClass.setColumnCount(2)
        self.tableClass.setHorizontalHeaderItem(0, QTableWidgetItem("Name"))
        self.tableClass.\
            setHorizontalHeaderItem(1, QTableWidgetItem("Students"))
        row = 0

        for a_class in JsonInfo(info).class_list():
            self.tableClass.setItem(row, 0, QTableWidgetItem(a_class))
            self.tableClass.setItem(row, 1, QTableWidgetItem(
                str(JsonInfo(info).student_count(a_class))))
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
        self.close_all_tables()
        self.backAction.setVisible(True)
        self.fetchSubmissionButton.setVisible(False)
        self.tableAssignment = QTableWidget()
        self.layout.addWidget(self.tableAssignment)
        self.tableAssignment.show()
        self.setWindowTitle('Assignments for {}'.format(class_name))
        self.tableAssignment.setRowCount(JsonInfo(info).
                                         assignment_count(class_name))
        self.tableAssignment.setColumnCount(2)
        self.tableAssignment.\
            setHorizontalHeaderItem(0, QTableWidgetItem('Assignment name'))
        self.tableAssignment.\
            setHorizontalHeaderItem(1, QTableWidgetItem('Submitted'))
        row = 0

        for assignment in JsonInfo(info).assignment_list(class_name):
            self.tableAssignment.setItem(row, 0, QTableWidgetItem(assignment))
            self.tableAssignment.setItem(row, 1, QTableWidgetItem(
                str(JsonInfo(info).
                    student_submitted_count(class_name, assignment))))
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
        self.close_all_tables()
        self.backAction.setVisible(True)
        self.fetchSubmissionButton.setVisible(False)
        self.tableAssignmentDetails = QTableWidget()
        self.layout.addWidget(self.tableAssignmentDetails)
        self.tableAssignmentDetails.show()
        self.setWindowTitle('Students for {}'.format(assignment))
        self.tableAssignmentDetails.setRowCount(JsonInfo(info).
                                                student_count(class_name))
        self.tableAssignmentDetails.setColumnCount(3)
        self.tableAssignmentDetails.\
            setHorizontalHeaderItem(0, QTableWidgetItem('Name'))
        self.tableAssignmentDetails.setHorizontalHeaderItem(
            1, QTableWidgetItem('Last submission time'))
        self.tableAssignmentDetails.setHorizontalHeaderItem(
            2, QTableWidgetItem('Submission Count'))
        row = 0

        for student in JsonInfo(info).student_list(class_name):
            self.tableAssignmentDetails.setItem(
                row, 0, QTableWidgetItem('{0}, {1}'.format(
                    JsonInfo(info).last_name(class_name, student),
                    JsonInfo(info).first_name(class_name, student))))
            self.tableAssignmentDetails.setItem(
                row, 1, QTableWidgetItem(str(
                    JsonInfo(info).time_converted(class_name, assignment, student))))
            self.tableAssignmentDetails.setItem(
                row, 2, QTableWidgetItem(str(JsonInfo(info).submission_count(
                    class_name, assignment, student))))
            row += 1

        self.tableAssignmentDetails.setColumnWidth(0, 200)
        self.tableAssignmentDetails.setColumnWidth(1, 200)
        self.tableAssignmentDetails.setColumnWidth(2, 150)
        self.tableAssignmentDetails.move(0, 0)
        self.tableAssignmentDetails.setSortingEnabled(True)
        self.tableAssignmentDetails.doubleClicked.connect(self.double_click_student)
        self.backAction.triggered.connect(self.show_table_assignment)
        self.tableAssignmentDetails.setWordWrap(True)
        self.height = self.tableAssignmentDetails.rowHeight(0) * row + 110
        self.width = \
            self.tableAssignmentDetails.columnWidth(0) + \
            self.tableAssignmentDetails.columnWidth(1) + \
            self.tableAssignmentDetails.columnWidth(2) + 60
        self.setGeometry(self.left, self.top, self.width, self.height)

    def create_table_student(self, class_name, username):
        self.close_all_tables()
        self.backAction.setVisible(True)
        self.fetchSubmissionButton.setVisible(True)
        self.tableStudent = QTableWidget()
        self.layout.addWidget(self.tableStudent)
        self.tableStudent.show()
        self.setWindowTitle('{0}, {1}'.format(
            JsonInfo(info).last_name(class_name, username),
            JsonInfo(info).first_name(class_name, username)))
        self.tableStudent.setRowCount(len(JsonInfo(info).assignments_by_student_list(class_name, username)))
        self.tableStudent.setColumnCount(3)
        self.tableStudent.setHorizontalHeaderItem(0, QTableWidgetItem('Assignment'))
        self.tableStudent.setHorizontalHeaderItem(1, QTableWidgetItem('Last submission time'))
        self.tableStudent.setHorizontalHeaderItem(2, QTableWidgetItem('Submission count'))
        row = 0

        for assignment in JsonInfo(info).assignments_by_student_list(class_name, username):
            self.tableStudent.setItem(row, 0, QTableWidgetItem(assignment))
            self.tableStudent.setItem(row, 1, QTableWidgetItem(JsonInfo(info).time_converted(class_name, assignment, username)))
            self.tableStudent.setItem(row, 2, QTableWidgetItem(str(JsonInfo(info).submission_count(class_name, assignment, username))))
            row += 1

        self.tableStudent.setColumnWidth(0, 200)
        self.tableStudent.setColumnWidth(1, 200)
        self.tableStudent.setColumnWidth(2, 150)
        self.tableStudent.move(0, 0)
        self.tableStudent.setSortingEnabled(True)
        self.backAction.triggered.connect(self.show_table_assignment_details)
        self.tableStudent.setWordWrap(True)
        self.height = self.tableStudent.rowHeight(0) * row + 110
        self.width = self.tableStudent.columnWidth(0) + self.tableStudent.columnWidth(1) + self.tableStudent.columnWidth(2) + 60
        self.fetchSubmissionButton.move(self.width - 130, 0)
        self.fetchSubmissionButton.clicked.connect(self.fetch_student_submission)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def double_click_class(self):
        self.class_name = self.tableClass.currentItem().text()
        self.create_table_assignments(self.class_name)

    def double_click_assignment(self):
        self.assignment = self.tableAssignment.currentItem().text()
        self.create_table_assignment_details(self.class_name, self.assignment)

    def double_click_student(self):
        self.username = self.tableAssignmentDetails.currentItem().text()
        self.username = JsonInfo(info).get_username_from_name(self.class_name, self.username)
        self.create_table_student(self.class_name, self.username)

    def show_table_class(self):
        self.create_table_class()

    def show_table_assignment(self):
        self.create_table_assignments(self.class_name)

    def show_table_assignment_details(self):
        self.create_table_assignment_details(self.class_name, self.assignment)

    def fetch_student_submission(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CreateTable()
    sys.exit(app.exec_())
