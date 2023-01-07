import os
import sys
import logging
import subprocess
import shutil
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox, QFileDialog, QApplication, QLineEdit, QDialog
from PyQt5.QtCore import pyqtSlot, QModelIndex
from PyQt5.QtGui import QIcon
from support_dictionaries import Supports


class MoveDialog(QDialog):
    def __init__(self, parent, dir_1=None, dir_2=None):
        super(MoveDialog, self).__init__(parent)
        uic.loadUi('../ui/move.ui', self)

        self.setWindowIcon(QIcon('../images/folder.png'))

        if dir_1:
            self.dir1 = dir_1
            self.dir2 = dir_2
            self.fname = os.path.basename(self.dir1)
        else:
            self.dir1 = ''
            self.dir2 = ''
            self.fname = ''

        self.set_up()

    def set_up(self):
        self.move_from_label.setText('Source path')
        self.move_to_label.setText('Destination path')
        self.file_name_label.setText('Destination name')

        self.move_from_edit.setText(self.dir1)
        self.move_to_edit.setText(self.dir2)
        self.file_name_edit.setText(self.fname)

        self.buttonBox.accepted.connect(lambda: self.move_item(self.move_from_edit.text(),
                                                               self.move_to_edit.text(),
                                                               self.file_name_edit.text()))

    @staticmethod
    def move_item(source: str, destination: str, filename: str):
        if not filename:
            filename = os.path.basename(source)

        move_to = os.path.join(destination, filename)

        try:
            os.rename(source, move_to)
            # shutil.move(source, move_to)
            logging.info(f"Moved {source} to {destination} as {filename}")
        # Source is a file, but destination is a directory
        except IsADirectoryError:
            logging.error('Destination only a directory')
        # Source is a directory, but destination is a file
        except NotADirectoryError:
            logging.error('Source a directory and destination a file')
        except PermissionError:
            logging.error('Operation not permitted')
        except OSError as error:
            logging.error(error)


class CopyDialog(QDialog):
    def __init__(self, parent, dir_1=None, dir_2=None):
        super(CopyDialog, self).__init__(parent)
        uic.loadUi('../ui/copy.ui', self)

        self.setWindowIcon(QIcon('../images/copy.png'))

        if dir_1:
            self.dir1 = dir_1
            self.dir2 = dir_2
            self.fname = os.path.basename(self.dir1)
        else:
            self.dir1 = ''
            self.dir2 = ''
            self.fname = ''

        self.set_up()

    def set_up(self):
        self.copy_from_label.setText('Copy from')
        self.copy_to_label.setText('Copy to')
        self.file_name_label.setText('Copied name')

        self.copy_from_edit.setText(self.dir1)
        self.copy_to_edit.setText(self.dir2)
        self.file_name_edit.setText(self.fname)

        self.buttonBox.accepted.connect(lambda: self.copy_item(self.copy_from_edit.text(),
                                                               self.copy_to_edit.text(),
                                                               self.file_name_edit.text()))

    @staticmethod
    def copy_item(copy_source: str, destination: str, copy_name: str):
        copy_destination = os.path.join(destination, copy_name)

        try:
            shutil.copy(copy_source, copy_destination)
            logging.info(f"Copied {copy_source} as {copy_destination}")
        # Source is a file, but destination is a directory
        except IsADirectoryError:
            logging.error('Destination only a directory')
        # Source is a directory, but destination is a file
        except NotADirectoryError:
            logging.error('Source a directory and destination a file')
        except PermissionError:
            logging.error('Operation not permitted')
        except OSError as error:
            logging.error(error)


class PermissionsDialog(QDialog):
    def __init__(self, parent, path: str):
        super(PermissionsDialog, self).__init__(parent)
        uic.loadUi('../ui/permissions.ui', self)

        self.setWindowIcon(QIcon('../images/password.png'))

        self.file_permissions: int = 0
        self.folder_permissions: int = 0

        self.owner_file_dict, self.owner_file_dict_2, self.group_file_dict, self.group_file_dict_2, \
        self.others_file_dict, self.others_file_dict_2 = Supports.dicts(self)

        self.set_up(path)

    def set_up(self, path):
        current = oct(os.stat(path).st_mode)[-3:]
        self.start_boxes(path, current)

        self.item_path_edit.setText(path)

        # self.buttonBox.accepted.connect(self.calculate_permissions)

    def start_boxes(self, path, current):
        boxes = []
        boxes_1 = []
        if os.path.isfile(path):
            boxes = self.owner_file_dict[current[0]]\
                    + self.group_file_dict[current[1]]\
                    + self.others_file_dict[current[2]]

            for box in boxes:
                box.setChecked(True)

            self.file_permissions = current

            location = oct(os.stat(os.path.dirname(path)).st_mode)[-3:]
            boxes_1 = self.owner_file_dict_2[location[0]]\
                      + self.group_file_dict_2[location[1]]\
                      + self.others_file_dict_2[location[2]]

            for box in boxes_1:
                box.setChecked(True)

            self.folder_permissions = location

        elif os.path.isdir(path):
            boxes = self.owner_file_dict_2[current[0]] \
                    + self.group_file_dict_2[current[1]] \
                    + self.others_file_dict_2[current[2]]

            for box in boxes:
                box.setChecked(True)

            self.folder_permissions = current

    def calculate_permissions_file(self):
        """
        This function attempts to create the permission code using the following:

        Binary	Octal	Permission
        000	    0	    —
        001	    1	    –x
        010	    2	    -w-
        011	    3	    -wx
        100	    4	    r–
        101	    5	    r-x
        110	    6	    rw-
        111	    7	    rwx

        :return:
        """
        owner = 0
        if self.owner_read_check.isChecked():
            owner += 4
        if self.owner_write_check.isChecked():
            owner += 2
        if self.owner_exe_check.isChecked():
            owner += 1
        
        group = 0
        if self.group_read_check.isChecked():
            group += 4
        if self.group_write_check.isChecked():
            group += 2
        if self.group_exe_check.isChecked():
            group += 1

        others = 0
        if self.others_read_check.isChecked():
            others += 4
        if self.others_write_check.isChecked():
            others += 2
        if self.others_exe_check.isChecked():
            others += 1

        self.file_permissions = int(f"{owner}{group}{others}")

    def calculate_permissions_folder(self):
        """
        This function attempts to create the permission code using the following:

        Binary	Octal	Permission
        000	    0	    —
        001	    1	    –x
        010	    2	    -w-
        011	    3	    -wx
        100	    4	    r–
        101	    5	    r-x
        110	    6	    rw-
        111	    7	    rwx

        :return:
        """
        owner = 0
        if self.owner_read_check_2.isChecked():
            owner += 4
        if self.owner_write_check_2.isChecked():
            owner += 2
        if self.owner_exe_check_2.isChecked():
            owner += 1

        group = 0
        if self.group_read_check_2.isChecked():
            group += 4
        if self.group_write_check_2.isChecked():
            group += 2
        if self.group_exe_check_2.isChecked():
            group += 1

        others = 0
        if self.others_read_check_2.isChecked():
            others += 4
        if self.others_write_check_2.isChecked():
            others += 2
        if self.others_exe_check_2.isChecked():
            others += 1

        self.folder_permissions = int(f"{owner}{group}{others}")


class RenameDialog(QDialog):
    def __init__(self, parent, dir_1=None):
        super(RenameDialog, self).__init__(parent)
        uic.loadUi('../ui/rename.ui', self)

        self.setWindowIcon(QIcon('../images/edit.png'))

        if dir_1:
            self.dir1 = dir_1
            self.dir2 = dir_1
            self.fname = os.path.basename(self.dir1)
        else:
            self.dir1 = ''
            self.dir2 = ''
            self.fname = ''

        self.set_up()

    def set_up(self):
        self.current_name_label.setText('Current naming')
        self.rename_location_label.setText('Renaming choice')

        self.current_name_edit.setText(self.dir1)
        self.rename_location_edit.setText(self.dir2)

        self.buttonBox.accepted.connect(lambda: self.rename_item(self.current_name_edit.text(),
                                                                 self.rename_location_edit.text()))

    @staticmethod
    def rename_item(source: str, rename_to: str):
        try:
            os.rename(source, rename_to)
            # shutil.move(source, move_to)
            logging.info(f"Renamed {source} to {rename_to}")
        # Source is a file, but destination is a directory
        except IsADirectoryError:
            logging.error('Destination only a directory')
        # Source is a directory, but destination is a file
        except NotADirectoryError:
            logging.error('Source a directory and destination a file')
        except PermissionError:
            logging.error('Operation not permitted')
        except FileExistsError:
            logging.info("File already Exists")
            choice = RenameDialog._remove_dialog()
            if choice:
                try:
                    os.remove(rename_to)
                    logging.info(f"Pre-existing file/folder removed - renaming {source}")
                    os.rename(source, rename_to)
                    logging.info(f"Renamed {source} to {rename_to}")
                except OSError as error:
                    print(error)
        except OSError as error:
            logging.error(error)

    @staticmethod
    def _remove_dialog():
        """
        This function creates a custom dialog to warn the user that the folder to be removed is not empty.

        :return: Boolean response
        """
        remove_check_dialog = QMessageBox()
        icon = QIcon('../images/edit.png')
        remove_check_dialog.setIconPixmap(icon.pixmap(20, 20))
        remove_check_dialog.setWindowTitle("Check Rename Event")
        remove_check_dialog.setText("File already exists with this name - delete existing and rename?")
        remove_check_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)

        returnValue = remove_check_dialog.exec()

        if returnValue == QMessageBox.Yes:
            return True
        else:
            return False
