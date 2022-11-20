#!/usr/bin/python
# -*- coding: utf-8 -*-
# QTableWidget Example @pythonspot.com
from MyPyLib import *
import sys,os,time,random,glob,pickle,numpy

libs={"QtGui":QtGui,"QtCore":QtCore, "QtWidgets":QtWidgets, "os":os,"time":time,"random":random,"glob":glob,"pickle":pickle,"numpy":numpy}

global SelectedLibrary

home_path = os.path.expanduser('~')
directoryName = home_path+"/Library/Application\ Support/PyLibViewer"


class mySearchList(SearchList):
    def __init__(self,name):
        super().__init__(name)
    def listUpdate(self):
        self.list.clear()
        try:
            for k in self.WholeList:
                if k.upper().count(str(self.search.text()).upper())>0:
                    item = QListWidgetItem(k)
                    self.list.addItem(item)
                    path = directoryName.replace('\\','')
                    for s in glob.glob(path+'/*'):
                        for name in s.split('/')[-1].split('.')[0].split(']'):
                            if name==k:
                                item.setBackground(QColor(0xBBAAAAA))
                    
        except:
            pass

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        global SelectedLibrary, currentMemoTo
        SelectedLibrary=QtGui
        self.initUI()
    def loadMEMO(self,name):
        self.memoLabel.setText("MEMO on "+name)
        path = directoryName+'/'+name+'.txt'
        path = path.replace('\\','')
        if len(glob.glob(path))>0:
            f = open(path,'r')
            self.memoEdit.setPlainText(''.join(f.readlines()))
        else:
            self.memoEdit.setPlainText("")
    def editMemo(self):
        if self.memoEdit.toPlainText()!="":
            name = self.memoLabel.text().split(' ')[2]
            path = directoryName+'/'+name+'.txt'
            path = path.replace('\\',"")
                         
            if len(glob.glob(directoryName))<1:
                os.system('mkdir -p '+directoryName)
            if len(glob.glob(path))<1:
                os.system('touch '+path)
            f = open(path,'w')
            f.write(self.memoEdit.toPlainText())
        else:
            name = self.memoLabel.text().split(' ')[2]
            path = directoryName+'/'+name+'.txt'
            if len(glob.glob(path.replace('\\','')))>0:
                os.system('rm '+path)
            
        
        
    def getMemo(self):
        try:
            libname = self.list1.list.currentItem().text()
            objname = self.list2.list.currentItem().text()
            methodname = self.list3.list.currentItem().text()
            #self.memoLabel.setText("MEMO on "+libname+']'+objname+']'+methodname)
            self.loadMEMO(libname+']'+objname+']'+methodname)
        except:
            pass
    def selectLibrary(self):
        try:
            t = self.list1.list.currentItem()
            global SelectedLibrary
            SelectedLibrary=libs[t.text()]
            self.list2.WholeList=dir(SelectedLibrary)
            self.list2.search.setText("")
            self.list3.search.setText("")
            #self.memoLabel.setText("MEMO on "+t.text())
            self.loadMEMO(t.text())
            self.list2.listUpdate()
        except:
            pass
    def selectObject(self):
        try:
            t = self.list2.list.currentItem()
            global SelectedLibrary
            self.list3.WholeList=dir(getattr(SelectedLibrary,t.text()))
            self.list3.listUpdate()
            libname = self.list1.list.currentItem().text()
            objname = t.text()
            #self.memoLabel.setText("MEMO on "+libname+']'+objname)
            self.loadMEMO(libname+']'+objname)
        except:
            pass
    def initUI(self):
        self.resize(1200,800)
        self.layout = QHBoxLayout()
        self.list1=mySearchList("Libraries")
        self.setWindowTitle("PyLibViewer")
        l = list(libs.keys())
        l.sort()
        for lib in l:
            self.list1.WholeList.append(lib)
        self.list1.listUpdate()
        self.list1.list.currentItemChanged.connect(self.selectLibrary)
        self.list2=mySearchList("Classes")
        self.list2.list.currentItemChanged.connect(self.selectObject)        
        self.list3=mySearchList("Components")
        self.list3.list.currentItemChanged.connect(self.getMemo)
        self.layout.addWidget(self.list1)
        self.layout.addWidget(self.list2)
        self.layout.addWidget(self.list3)

        self.mainLayout = QVBoxLayout()
        self.memoEdit = PythonEditor()
        self.memoLabel = QLabel("MEMO")
        self.memoEdit.textChanged.connect(self.editMemo)
        self.mainLayout.addLayout(self.layout)
        self.mainLayout.addWidget(self.memoLabel)
        self.mainLayout.addWidget(self.memoEdit)
        self.setLayout(self.mainLayout)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mwindow = MainWindow()
    mwindow.show()
    app.exec_()