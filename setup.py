from setuptools import setup
import py2app

setup(
    app = ["PyLibViewer.py"],
    version = "0.0.1",
    setup_requires = ["py2app"],
    options = {
        "py2app": {
            "includes":["PyQt5","PyQt5.QtGui","PyQt5.QtCore","PyQt5.QtWidgets","sys","random","time","glob","pickle","os","numpy"]
        }
    }
)