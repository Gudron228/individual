import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QTableWidget, QTableWidgetItem, QDialog,
                               QDialogButtonBox, QFormLayout, QLineEdit, QSpinBox, QInputDialog, QFileDialog,
                               QMessageBox)
from PySide6.QtGui import QAction


class Person:
    def __init__(self, name, age, height):
        self.name = name
        self.age = age
        self.height = height

    def __str__(self):
        return f'{self.name} {self.age} {self.height}'


class PersonDialog(QDialog):
    def __init__(self, parent=None, person=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить/Редактировать Человека')
        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit(self)
        self.age_edit = QSpinBox(self)
        self.age_edit.setMaximum(120)
        self.height_edit = QSpinBox(self)
        self.height_edit.setMaximum(300)

        self.layout.addRow('Имя:', self.name_edit)
        self.layout.addRow('Возраст:', self.age_edit)
        self.layout.addRow('Рост:', self.height_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

        if person:
            self.name_edit.setText(person.name)
            self.age_edit.setValue(person.age)
            self.height_edit.setValue(person.height)

    def get_person(self):
        name = self.name_edit.text()
        age = self.age_edit.value()
        height = self.height_edit.value()
        return Person(name, age, height)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Death Note")
        self.setGeometry(100, 100, 600, 400)

        self.people = []

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        self.table = QTableWidget(0, 3, self)
        self.table.setHorizontalHeaderLabels(['Имя', 'Возраст', 'Рост'])
        self.setCentralWidget(self.table)

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('Файл')
        load_action = QAction('Открыть', self)
        load_action.triggered.connect(self.load_data)
        file_menu.addAction(load_action)

        save_action = QAction('Сохранить', self)
        save_action.triggered.connect(self.save_data)
        file_menu.addAction(save_action)

        exit_action = QAction('Выход', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu('Редактировать')
        add_action = QAction('Добавить', self)
        add_action.triggered.connect(self.add_person)
        edit_menu.addAction(add_action)

        edit_action = QAction('Редактировать', self)
        edit_action.triggered.connect(self.edit_person)
        edit_menu.addAction(edit_action)

        delete_action = QAction('Удалить', self)
        delete_action.triggered.connect(self.delete_person)
        edit_menu.addAction(delete_action)

        filter_menu = menubar.addMenu('Фильтр')
        filter_age_action = QAction('Фильтр по возрасту', self)
        filter_age_action.triggered.connect(self.filter_by_age)
        filter_menu.addAction(filter_age_action)

        filter_height_action = QAction('Фильтр по росту', self)
        filter_height_action.triggered.connect(self.filter_by_height)
        filter_menu.addAction(filter_height_action)

    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "Peoples.txt", "Text Files (*.txt)")
        if file_name:
            with open(file_name, 'r') as file:
                self.people = []
                self.table.setRowCount(0)
                for line in file:
                    name, age, height = line.strip().split()
                    person = Person(name, int(age), int(height))
                    self.people.append(person)
                    self.add_person_to_table(person)

    def save_data(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "Peoples.txt", "Text Files (*.txt)")
        if file_name:
            with open(file_name, 'w') as file:
                for person in self.people:
                    file.write(f'{person.name} {person.age} {person.height}\n')

    def add_person(self):
        dialog = PersonDialog(self)
        if dialog.exec() == QDialog.Accepted:
            person = dialog.get_person()
            self.people.append(person)
            self.add_person_to_table(person)

    def edit_person(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            person = self.people[selected_row]
            dialog = PersonDialog(self, person)
            if dialog.exec() == QDialog.Accepted:
                updated_person = dialog.get_person()
                self.people[selected_row] = updated_person
                self.update_person_in_table(selected_row, updated_person)
        else:
            self.show_message("Человек не выбран", "Выберите человека для редактирования")

    def delete_person(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.people.pop(selected_row)
            self.table.removeRow(selected_row)
        else:
            self.show_message("Человек не выбран", "Выберите человека для удаления")

    def filter_by_age(self):
        min_age, ok1 = QInputDialog.getInt(self, "Фильтр по возрасту", "Минимальный возраст:")
        max_age, ok2 = QInputDialog.getInt(self, "Фильтр по возрасту", "Максимальный возраст:")
        if ok1 and ok2:
            self.apply_filter(lambda person: min_age <= person.age <= max_age)

    def filter_by_height(self):
        min_height, ok1 = QInputDialog.getInt(self, "Фильтр по росту", "Минимальный рост:")
        max_height, ok2 = QInputDialog.getInt(self, "Фильтр по росту", "Максимальный рост:")
        if ok1 and ok2:
            self.apply_filter(lambda person: min_height <= person.height <= max_height)

    def apply_filter(self, filter_func):
        self.table.setRowCount(0)
        for person in self.people:
            if filter_func(person):
                self.add_person_to_table(person)

    def add_person_to_table(self, person):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(person.name))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(person.age)))
        self.table.setItem(row_position, 2, QTableWidgetItem(str(person.height)))

    def update_person_in_table(self, row, person):
        self.table.setItem(row, 0, QTableWidgetItem(person.name))
        self.table.setItem(row, 1, QTableWidgetItem(str(person.age)))
        self.table.setItem(row, 2, QTableWidgetItem(str(person.height)))

    def show_message(self, title, message):
        messagebox = QMessageBox(self)
        messagebox.setWindowTitle(title)
        messagebox.setText(message)
        messagebox.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

