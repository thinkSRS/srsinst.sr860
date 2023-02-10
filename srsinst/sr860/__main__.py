#!/usr/bin/env python3

import sys
from pathlib import Path
from srsgui.ui.qt.QtWidgets import QApplication
from srsgui.ui.taskmain import TaskMain


def main():
    TaskMain.ApplicationName = 'sr860'
    TaskMain.DefaultConfigFile = str(Path(__file__).parent /
        "{}.taskconfig".format(TaskMain.ApplicationName))
    app = QApplication(sys.argv)
    main_window = TaskMain()
    main_window.show()
    app.exec_()


if __name__ == '__main__':
    main()


