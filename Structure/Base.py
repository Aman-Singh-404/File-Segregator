import datetime
import os
import shutil
import smtplib
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import numpy as np
import PyPDF2
from PyQt5 import QtWidgets

from Ui_Help import Ui_MainWindow as uiHelp
from Ui_MailSender import Ui_MainWindow as uiMailSender
from Ui_ResultCalculator import Ui_MainWindow as uiResultCalculator
from Ui_Segregator import Ui_MainWindow as uiSegregator


def calculateResult(data,tos,result):
    com=0
    rang=[]
    rolllist=[]
    marklist=[]
    while 1:
        c=data.find(',',com)
        if c==-1:
            rang.append(data[com:])
            break
        rang.append(data[com:c])
        com=c+1
    for i in rang:
        h=i.find("-")
        if h==-1:
            rolllist.append(i)
        else:
            for t in range(int(i[:3]),int(i[h+1:h+4])+1):
                roll=str(t)+i[h+4:]
                for gt in range(len(i[:h])-len(roll)):
                    roll='0'+roll
                rolllist.append(roll)
    pdfFileObj = open(result, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    for n in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(n)
        a=pageObj.extractText()
        for roll in rolllist:
            if roll in a:
                marks=[]
                k=a.find(roll)
                count=swap=0
                for i in range(len(a)-k):
                    start=end=0
                    if a[k+i]=='\n':
                        count=count+1
                        swap=1
                    if count>8 and count%3==0 and swap:
                        if a[k+i+1]=='A':
                            count=count+1
                            marks.append(0)
                        else:
                            marks.append(int(a[k+i+1:k+i+3]))
                        swap=0
                    if len(marks)==tos:
                        break
                marklist.append((roll,np.round(np.sum(marks)/tos,3),0))
        if len(rolllist)==len(marklist):
            break
    pdfFileObj.close()
    t=[('Roll number','S12'),('Marks',float),('Rank',int)]
    sortlist=np.sort(np.array(marklist,dtype=t),order=['Marks'])
    for i in range(len(sortlist)):
        sortlist[i][2]=len(sortlist)-i
    sortlist=np.sort(sortlist,order=['Roll number'])
    return sortlist

def desegregateFolder(path,parent=None):
    if parent==None:
        parent=path
    for file in os.listdir(path):
        f,e=os.path.splitext(file)
        if e=="":
            desegregateFolder(path+"/"+file,parent)
            os.rmdir(path+"/"+file)
        else:
            if path!=parent:
                shutil.move(path+"/"+file,parent)
    
def segregateFolder(path,desg=False):
    if desg:
        desegregateFolder(path)
    for file in os.listdir(path):
        f,e=os.path.splitext(file)
        if e!="":
            if e[1:].lower() not in os.listdir(path):
                os.mkdir(path+'/'+e[1:])
            shutil.move(path+'/'+file,path+'/'+e[1:].lower())

def sendMails(fromaddr,password,toaddr,body,subject=None,attaches=[]):
    msg=MIMEMultipart()
    msg['From']=fromaddr
    msg['To']=toaddr
    msg['Subject']=subject
    msg.attach(MIMEText(body,'plain'))
    for attachfile in attaches:
        attachment=open(attachfile,'rb')
        p=MIMEBase('application','octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        attachname=attachfile[attachfile.rfind('/')+1:]
        p.add_header('Content-Disposition',"attachment; filename=%s" %attachname)
        msg.attach(p)
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(fromaddr,password)
    text=msg.as_string()
    server.sendmail(fromaddr,toaddr.split(','),text)
    server.quit()

class Help(QtWidgets.QMainWindow,uiHelp):
    def __init__(self,parent=None):
        super(Help,self).__init__(parent)
        self.setupUi(self)
        
        self.sendMailsPB.clicked.connect(self.mail)
        self.segFolderPB.clicked.connect(self.seg)
        self.resCalculatePB.clicked.connect(self.res)
    
    def mail(self):
        self.ms=MailSender()
        self.ms.show()
        self.close()
    
    def seg(self):
        self.s=Segregator()
        self.s.show()
        self.close()
    
    def res(self):
        self.rc=ResultCalculator()
        self.rc.show()
        self.close()

class MailSender(QtWidgets.QMainWindow,uiMailSender):
    def __init__(self,parent=None):
        super(MailSender,self).__init__(parent)
        self.setupUi(self)

        self.attachPB.clicked.connect(self.attach)
        self.sendPB.clicked.connect(self.send)
        self.segFolderPB.clicked.connect(self.seg)
        self.helpPB.clicked.connect(self.help)
        self.resCalculatePB.clicked.connect(self.res)
    
    def help(self):
        self.h=Help()
        self.h.show()
        self.close()
    
    def seg(self):
        self.s=Segregator()
        self.s.show()
        self.close()
    
    def res(self):
        self.rc=ResultCalculator()
        self.rc.show()
        self.close()
    
    def attach(self):
        options=QtWidgets.QFileDialog.Options()
        options |=QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"Select files","","All Files(*)",options=options)
        for file in files:
            self.attachTE.insertPlainText(file+";")
    
    def send(self):
        fromaddr=self.fromLE.text()
        password=self.passwordLE.text()
        toaddr=self.toLE.text()
        subject=self.subjectLE.text()
        body=self.bodyTE.toPlainText()
        attachments=self.attachTE.toPlainText().split(';')
        if fromaddr=="":
            QtWidgets.QMessageBox.warning(self, 'Warning', "Your E-mail-ID cannot be empty.", QtWidgets.QMessageBox.Ok)
            return
        if password=="":
            QtWidgets.QMessageBox.warning(self, 'Warning', "Your password cannot be empty.", QtWidgets.QMessageBox.Ok)
            return
        if toaddr=="":
            QtWidgets.QMessageBox.warning(self, 'Warning', "Receiving E-mail-ID cannot be empty.", QtWidgets.QMessageBox.Ok)
            return
        for attachfile in attachments[:-1]:
            if not os.path.exists(attachfile):
                QtWidgets.QMessageBox.warning(self, 'Warning', "Attacment["+attachfile+"] does not exist.", QtWidgets.QMessageBox.Ok)
                return
            if os.path.isdir(attachfile):
                QtWidgets.QMessageBox.warning(self, 'Warning', "Attacment["+attachfile+"] is a folder.", QtWidgets.QMessageBox.Ok)
                return
        try:
            sendMails(fromaddr,password,toaddr,body,subject,attachments[:-1])
        except:
            QtWidgets.QMessageBox.warning(self, 'Warning', "Incorrect Credentials.", QtWidgets.QMessageBox.Ok)
            self.passwordLE.setText("")
            return
        QtWidgets.QMessageBox.question(self, 'Message Details', "E-mail sent.", QtWidgets.QMessageBox.Ok)

class ResultCalculator(QtWidgets.QMainWindow,uiResultCalculator):
    def __init__(self,parent=None):
        super(ResultCalculator,self).__init__(parent)
        self.setupUi(self)
        
        self.sendMailsPB.clicked.connect(self.mail)
        self.segFolderPB.clicked.connect(self.seg)
        self.helpPB.clicked.connect(self.help)
        self.savePB.clicked.connect(self.save)
        self.browseTB.clicked.connect(self.browse)
        self.calculatePB.clicked.connect(self.calculate)
    
    def mail(self):
        self.ms=MailSender()
        self.ms.show()
        self.close()
    
    def seg(self):
        self.s=Segregator()
        self.s.show()
        self.close()
    
    def help(self):
        self.h=Help()
        self.h.show()
        self.close()
    
    def calculate(self):
        data=self.rangeLE.text()
        result=self.fileLE.text()
        tos=self.tosLE.text()
        if data=="":
            QtWidgets.QMessageBox.warning(self, 'Error', "Roll number range cannot be empty.", QtWidgets.QMessageBox.Ok)
            return
        if tos=="":
            QtWidgets.QMessageBox.warning(self, 'Error', "Number of subject cannot be empty.", QtWidgets.QMessageBox.Ok)
            return
        if not(result!="" and os.path.exists(result) and os.path.isfile(result)):
            QtWidgets.QMessageBox.warning(self, 'Error', "This is not a '.pdf' file", QtWidgets.QMessageBox.Ok)
            return
        self.sortlist=calculateResult(data,int(tos),result)
        self.savePB.setDisabled(False)
        self.resultTW.setRowCount(len(self.sortlist))
        for i in range(len(self.sortlist)):
            self.resultTW.setItem(i,0, QtWidgets.QTableWidgetItem((str(self.sortlist[i][0]))[2:13]))
            self.resultTW.setItem(i,1, QtWidgets.QTableWidgetItem(str(self.sortlist[i][1])))
            self.resultTW.setItem(i,2, QtWidgets.QTableWidgetItem(str(self.sortlist[i][2])))
    
    def save(self):
        resulttxt=open("Result"+str(datetime.datetime.now())[:19]+".txt",'w+')
        resulttxt.write("Roll number\t\tMarks\t\tRank\n\n")
        for i in range(len(self.sortlist)):
            resulttxt.write((str(self.sortlist[i][0]))[2:13]+"\t\t"+str(self.sortlist[i][1])+"\t\t"+str(self.sortlist[i][2])+"\n")
        QtWidgets.QMessageBox.information(self, 'Message Details', "File saved.", QtWidgets.QMessageBox.Ok)
    
    def browse(self):
        options=QtWidgets.QFileDialog.Options()
        options |=QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Select file","","Document(*.pdf)",options=options)
        self.fileLE.setText(files)

class Segregator(QtWidgets.QMainWindow,uiSegregator):
    def __init__(self,parent=None):
        super(Segregator,self).__init__(parent)
        self.setupUi(self)
        
        self.browseTB.clicked.connect(self.onBrowse)
        self.segregatePB.clicked.connect(self.onSeg)
        self.sendMailsPB.clicked.connect(self.mail)
        self.resCalculatePB.clicked.connect(self.res)
        self.helpPB.clicked.connect(self.help)
    
    def mail(self):
        self.s=MailSender()
        self.s.show()
        self.close()

    def help(self):
        self.h=Help()
        self.h.show()
        self.close()
    
    def res(self):
        self.rc=ResultCalculator()
        self.rc.show()
        self.close()
    
    def onSeg(self):
        dirpath=self.pathLE.text()
        if dirpath=="":
            QtWidgets.QMessageBox.warning(self,'Warning','Path location cannot be empty.',QtWidgets.QMessageBox.Ok)
            return
        if not(os.path.exists(dirpath) and os.path.isdir(dirpath)):
            self.pathLE.setText("")
            QtWidgets.QMessageBox.warning(self,'Warning','Path is not a directory.',QtWidgets.QMessageBox.Ok)
            return
        segregateFolder(dirpath,self.desgCB.isChecked())
        QtWidgets.QMessageBox.information(self, 'Message Details', "Folder segregation completed.", QtWidgets.QMessageBox.Ok)
    
    def onBrowse(self):
        self.pathLE.setText(str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")))

app=QtWidgets.QApplication(sys.argv)
toolapp=MailSender()
toolapp.show()
sys.exit(app.exec_())
