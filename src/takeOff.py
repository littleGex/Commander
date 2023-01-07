# -*- coding: utf-8 -*-
import os
import shutil
import sys
import logging
import subprocess
from pathlib import Path
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox, QFileDialog, \
    QApplication, QLineEdit, QDialog, QFileSystemModel
from PyQt5.QtCore import pyqtSlot, QModelIndex, QDir
from PyQt5.QtGui import QIcon, QPixmap
from dialogs import MoveDialog, CopyDialog, PermissionsDialog


class LaunchCommander(QMainWindow):
    def __init__(self, parent=None):
        super(LaunchCommander, self).__init__(parent)
        uic.loadUi('../ui/Main.ui', self)

        self.fileModel = None
        self.hidden_1 = False
        self.hidden_2 = False

        self.active_item: str = None
        self.active_tree: str = None

        self.current_left: str = None
        self.current_right: str = None

        self.header_indices_left: list = []
        self.header_indices_right: list = []

        self.setup_ui()
        self.set_menu()

        # logging.basicConfig(format='%(asctime)s %(message)s')
        # logging.basicConfig(level=logging.INFO)
        # logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        logging.getLogger().setLevel(logging.INFO)

    # ======================================================================
    def setup_ui(self):
        self.header_indices_left = [1, 2, 3]
        path_left = self.directory_line_1.text()
        self.folder_viewer_left(path_left)
        for i in range(1, self.treeView_2.header().length()):
            self.treeView_2.hideColumn(i)
        self.folders_left()

        self.header_indices_right = [1, 2, 3]
        path_right = self.directory_line_2.text()
        self.folder_viewer_right(path_right)
        for i in range(1, self.treeView_2.header().length()):
            self.treeView_4.hideColumn(i)
        self.folders_right()

        self.directory_line_1.textChanged.connect(lambda: self.folder_viewer_left(self.directory_line_1.text()))
        self.directory_line_2.textChanged.connect(lambda: self.folder_viewer_right(self.directory_line_2.text()))
        self.browse_1.released.connect(self.browse_gen)
        self.browse_2.released.connect(self.browse_gen)
        self.move_down_button_1.released.connect(self.move_down_left)
        self.move_down_button_2.released.connect(self.move_down_right)
        self.match_button_1.released.connect(lambda: self.match('left'))
        self.match_button_2.released.connect(lambda: self.match('right'))
        self.home_button_1.released.connect(lambda: self._home(1))
        self.home_button_2.released.connect(lambda: self._home(2))

        self.size_1.released.connect(lambda: self.folder_viewer_left(self.directory_line_1.text(), 1))
        self.kind_1.released.connect(lambda: self.folder_viewer_left(self.directory_line_1.text(), 2))
        self.date_1.released.connect(lambda: self.folder_viewer_left(self.directory_line_1.text(), 3))
        self.size_2.released.connect(lambda: self.folder_viewer_right(self.directory_line_2.text(), 1))
        self.kind_2.released.connect(lambda: self.folder_viewer_right(self.directory_line_2.text(), 2))
        self.date_2.released.connect(lambda: self.folder_viewer_right(self.directory_line_2.text(), 3))
        self.hide_unhide_button_1.released.connect(lambda: self.hide_unhide(1))
        self.hide_unhide_button_2.released.connect(lambda: self.hide_unhide(2))
        self.terminal_button_1.released.connect(lambda: self._terminal('left'))
        self.terminal_button_2.released.connect(lambda: self._terminal('right'))

        self.treeView_2.clicked.connect(self.active_left)
        self.treeView_4.clicked.connect(self.active_right)

        self.move_button.released.connect(self.move_it)
        self.copy_button.released.connect(self.copy_it)
        self.compare_button.released.connect(self.compare_it)
        self.delete_button.released.connect(lambda: self.remove_item(self.active_item))
        self.permission_button.released.connect(self.permission_it)

    def set_menu(self):
        # set up windows menubar
        main_menu = self.menuBar()
        main_menu.setNativeMenuBar(False)  # needed for mac

        file_menu = main_menu.addMenu("File")
        data_menu = main_menu.addMenu("Data")

        settings = file_menu.addMenu("Settings")

        new_session = QAction("New session", self)
        new_session.setShortcut("Ctrl+N")
        new_session.setStatusTip("Click to start new session")
        file_menu.addAction(new_session)
        # new_session.triggered.connect(self.newSession)

        quitz = QAction("Quit", self)
        quitz.setShortcut("Ctrl+Q")
        quitz.setStatusTip("Click to Exit")
        file_menu.addAction(quitz)
        quitz.triggered.connect(self.close_it)

        themes = settings.addMenu('Themes')

        dark_grey = QAction("Dark Grey", self)
        themes.addAction(dark_grey)
        dark_grey.triggered.connect(self.grey_sheet)

        dark_orange = QAction("Dark Orange", self)
        themes.addAction(dark_orange)
        dark_orange.triggered.connect(self.orange_sheet)

        default = QAction("Default", self)
        themes.addAction(default)
        default.triggered.connect(self.default_sheet)

        ctrls = QAction("Create ctrl file", self)
        ctrls.setShortcut("Ctrl+.")
        ctrls.setStatusTip("Click to create ctrl file")
        data_menu.addAction(ctrls)
        # ctrls.triggered.connect(self.ctrls)

    def grey_sheet(self):
        with open('themes/darkGrey.css') as file:
            style = file.read()
        self.setStyleSheet(style)

    def orange_sheet(self):
        with open('themes/darkOrange.css') as file:
            style = file.read()
        self.setStyleSheet(style)

    def default_sheet(self):
        self.setStyleSheet("")

    def move_down_left(self):
        current_path = self.directory_line_1.text()
        moved_down = os.path.split(current_path)[0]

        if os.path.isdir(moved_down):
            self.directory_line_1.clear()
            self.directory_line_1.setText(moved_down)

    def move_down_right(self):
        current_path = self.directory_line_2.text()
        moved_down = os.path.split(current_path)[0]

        if os.path.isdir(moved_down):
            self.directory_line_2.clear()
            self.directory_line_2.setText(moved_down)

    def browse_gen(self):
        QApplication.clipboard().clear()

        folder = QFileDialog.getExistingDirectory(self, "Select Directory")

        QApplication.clipboard().setText(folder)
        if os.path.isfile(folder):
            return folder

    def _home(self, index: int):
        if index == 1:
            self.directory_line_1.setText(str(Path.home()))
        else:
            self.directory_line_2.setText(str(Path.home()))

    def folder_viewer_left(self, path: str, index: int = None):
        self.fileModel_left = QFileSystemModel()
        self.fileModel_left.setReadOnly(False)
        self.fileModel_left.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        self.fileModel_left.setRootPath(QDir.rootPath())
        self.fileModel_left.setResolveSymlinks(True)

        if index:
            headers_remove = self.update_view(index, 'left')
            headers = {1, 2, 3} - set(headers_remove)
        else:
            headers_remove = self.header_indices_left
            headers = {1, 2, 3} - set(headers_remove)

        self.treeView_2.setColumnWidth(0, 200)

        for i in headers:
            self.treeView_2.header().showSection(i)
        for i in headers_remove:
            self.treeView_2.header().hideSection(i)

        self.treeView_2.setModel(self.fileModel_left)
        self.treeView_2.setRootIndex(self.fileModel_left.index(path))
        self.treeView_2.resizeColumnToContents(-1)

    def folders_left(self):
        self.dirModel_left = QFileSystemModel()
        self.dirModel_left.setRootPath(self.directory_line_1.text())
        self.view_left = self.treeView_1
        self.view_left.setModel(self.dirModel_left)
        self.view_left.setRootIndex(self.dirModel_left.index(self.directory_line_1.text()))
        self.view_left.clicked.connect(self.on_tree_view_clicked_left)

        self.treeView_1.setColumnWidth(0, 200)

    @pyqtSlot(QModelIndex)
    def on_tree_view_clicked_left(self, index):
        index_item = self.dirModel_left.index(index.row(), 0, index.parent())

        filename = self.dirModel_left.fileName(index_item)
        filepath = self.dirModel_left.filePath(index_item)

        QApplication.clipboard().setText(filepath)
        if os.path.isdir(filepath):
            self.directory_line_1.clear()
            self.directory_line_1.setText(filepath)
        else:
            self.directory_line_1.clear()
            self.directory_line_1.setText(os.path.dirname(filepath))

    def folder_viewer_right(self, path: str, index: int = None):
        self.fileModel_right = QFileSystemModel()
        self.fileModel_right.setReadOnly(False)
        self.fileModel_right.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        self.fileModel_right.setRootPath(QDir.rootPath())
        self.fileModel_right.setResolveSymlinks(True)

        if index:
            headers_remove = self.update_view(index, 'right')
            headers = {1, 2, 3} - set(headers_remove)
        else:
            headers_remove = self.header_indices_right
            headers = {1, 2, 3} - set(headers_remove)

        self.treeView_4.setColumnWidth(0, 200)

        for i in headers:
            self.treeView_4.header().showSection(i)
        for i in headers_remove:
            self.treeView_4.header().hideSection(i)

        self.treeView_4.setModel(self.fileModel_right)
        self.treeView_4.setRootIndex(self.fileModel_right.index(path))
        self.treeView_4.resizeColumnToContents(-1)

    def folders_right(self):
        self.dirModel_right = QFileSystemModel()
        self.dirModel_right.setRootPath(self.directory_line_2.text())
        self.view_right = self.treeView_3
        self.view_right.setModel(self.dirModel_right)
        self.view_right.setRootIndex(self.dirModel_right.index(self.directory_line_2.text()))
        self.view_right.clicked.connect(self.on_tree_view_clicked_right)

        self.treeView_3.setColumnWidth(0, 200)

    @pyqtSlot(QModelIndex)
    def on_tree_view_clicked_right(self, index):
        index_item = self.dirModel_right.index(index.row(), 0, index.parent())

        filename = self.dirModel_right.fileName(index_item)
        filepath = self.dirModel_right.filePath(index_item)

        QApplication.clipboard().setText(filepath)
        if os.path.isdir(filepath):
            self.directory_line_2.clear()
            self.directory_line_2.setText(filepath)
        else:
            self.directory_line_2.clear()
            self.directory_line_2.setText(os.path.dirname(filepath))

    def update_view(self, num: int, side: str):
        """
        This function checks if a value exists in a list, if so removing it and if not appending the
        number to the list.

        0: Name of file/folder
        1: Kind of file/folder
        2: Size of file/folder
        3: Date modified

        :param num: Number to add/remove from the header list.
        :return: user modified header index list.
        """
        if side == 'left':
            headers = self.header_indices_left
        else:
            headers = self.header_indices_right

        if num in headers:
            headers.remove(num)
            headers.sort()
        else:
            headers.append(num)
            headers.sort()

        return headers

    def hide_unhide(self, index: int):
        if index == 1:
            if self.hidden_1:
                self.treeView_1.show()
                self.hidden_1 = False
            else:
                self.treeView_1.hide()
                self.hidden_1 = True
        else:
            if self.hidden_2:
                self.treeView_3.show()
                self.hidden_2 = False
            else:
                self.treeView_3.hide()
                self.hidden_2 = True

    def _terminal(self, side: str):
        """
        This function attempts to open a terminal from the currently selected folder.

        :param side: String to identify if the left or right explorer where chosen
        """
        if side == 'left':
            os.system(f'open -a Terminal {self.directory_line_1.text()}')
        else:
            os.system(f'open -a Terminal {self.directory_line_2.text()}')

    def match(self, side: str):
        """
        This function attempts to copy the path shown in the neighbouring explorer window.

        :param side: Match left or right identifier
        """
        if side == 'left':
            post = self.directory_line_1
            match = self.directory_line_2.text()
        else:
            post = self.directory_line_2
            match = self.directory_line_1.text()

        post.clear()
        post.setText(match)

    def move_it(self):
        if self.active_item:
            if self.active_tree == 'treeView_2':
                self.move_dialog = MoveDialog(self, self.active_item, self.directory_line_2.text())
            else:
                self.move_dialog = MoveDialog(self, self.active_item, self.directory_line_1.text())
        else:
            self.move_dialog = MoveDialog(self)
            logging.info('No files or directories selected')

        self.move_dialog.show()

    def copy_it(self):
        if self.active_item:
            if self.active_tree == 'treeView_2':
                self.copy_dialog = CopyDialog(self, self.active_item, self.directory_line_2.text())
            else:
                self.copy_dialog = CopyDialog(self, self.active_item, self.directory_line_1.text())
        else:
            self.copy_dialog = CopyDialog(self)
            logging.info('No files or directories selected')

        self.copy_dialog.show()

    def compare_it(self):
        if not self.current_left:
            logging.warning("No item selected in left explorer")
            return
        if not self.current_right:
            logging.warning("No item selected in right explorer")
            return

        item_1 = os.path.abspath(self.current_left)
        item_2 = os.path.abspath(self.current_right)

        logging.info(f"Compaing {item_1} and {item_2}")

        subprocess.Popen(["tkdiff", item_1, item_2])

    def permission_it(self):
        if self.active_item:
            self.permission_dialog = PermissionsDialog(self, os.path.abspath(self.active_item))
        else:
            return

        self.permission_dialog.show()

    def remove_item(self, selected: str):
        item = os.path.abspath(selected)

        if os.path.isfile(item):
            try:
                os.remove(item)
                logging.info(f"{item} removed")
            except OSError as error:
                print(error)
        elif os.path.isdir(item):
            if len(os.listdir(item)) == 0:
                try:
                    os.rmdir(item)
                    logging.info(f"{item} removed")
                except OSError as error:
                    print(error)
            else:
                choice = self._remove_dialog()
                if choice:
                    try:
                        shutil.rmtree(item)
                        logging.info(f"{item} and contents have been removed")
                    except OSError as error:
                        print(error)
        elif os.path.islink(item):
            try:
                os.unlink(item)
                logging.info(f"{item} removed")
            except OSError as error:
                print(error)

    @staticmethod
    def _remove_dialog():
        """
        This function creates a custom dialog to warn the user that the folder to be removed is not empty.

        :return: Boolean response
        """
        remove_check_dialog = QMessageBox()
        icon = QIcon('../images/delete.png')
        remove_check_dialog.setIconPixmap(icon.pixmap(20, 20))
        remove_check_dialog.setWindowTitle("Check Deletion Event")
        remove_check_dialog.setText("Folder is not empty - do you want to continue with delete")
        remove_check_dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = remove_check_dialog.exec()

        if returnValue == QMessageBox.Ok:
            return True
        else:
            return False

    @staticmethod
    def close_it():
        """
        This function attempts to close the main user interface.
        """
        logging.info("Session closing")
        sys.exit()

    @pyqtSlot(QModelIndex)
    def active_left(self, index):
        indexItem = self.fileModel_left.index(index.row(), 0, index.parent())

        filename = self.fileModel_left.fileName(indexItem)
        filepath = self.fileModel_left.filePath(indexItem)

        widget = self.focusWidget()

        self.current_left = filepath
        self.active_item = filepath
        self.active_tree = widget.objectName()

    @pyqtSlot(QModelIndex)
    def active_right(self, index):
        indexItem = self.fileModel_right.index(index.row(), 0, index.parent())

        filename = self.fileModel_right.fileName(indexItem)
        filepath = self.fileModel_right.filePath(indexItem)

        widget = self.focusWidget()

        self.current_right = filepath
        self.active_item = filepath
        self.active_tree = widget.objectName()


# ======================================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('../images/command.png'))
    window = LaunchCommander()
    window.show()
    sys.exit(app.exec_())