from datetime import datetime
from PySide.QtGui import *
from PySide.QtCore import *
import os, socket
import smtplib
import mimetypes
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
class MySignal(QObject):
    sig = Signal(str)
class MyLongThread(QThread):
    def __init__(self, parent = None,
                 Sender_Email_mail = None,
                 Sender_Password_mail = None,
                 Receiver_Email_mail = None,
                 Subject_mail = None,
                 Body_mail = None,
                 Attachments_mail = None,
                 HTML_mail = None):
        QThread.__init__(self, parent)
        self.signal = MySignal()
        
        self.Sender_Email_mail      = Sender_Email_mail
        self.Sender_Password_mail   = Sender_Password_mail
        self.Receiver_Email_mail    = Receiver_Email_mail.replace(' ','')
        self.Subject_mail           = Subject_mail
        self.Body_mail              = Body_mail
        self.Attachments_mail        = Attachments_mail
        self.HTML_mail              = HTML_mail 

    def run(self):
        self.signal.sig.emit('st:Collecting information to send mail to %s ...'%self.Sender_Email_mail)
        msg = MIMEMultipart()
        msg['From'] = self.Sender_Email_mail
        msg['To'] = self.Receiver_Email_mail
        if self.Subject_mail != None:
            msg['Subject'] = 'Subject'
        if self.Body_mail != None:
            if self.HTML_mail == True:
                msg.attach( MIMEText(self.Body_mail, 'html' ))
            else:
                msg.attach( MIMEText(self.Body_mail, 'plain' ))
        if self.Attachments_mail != None: 
            for f in self.Attachments_mail:
                ctype, encoding = mimetypes.guess_type(r'%s'%f)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                with open(r'%s'%f, 'rb') as fp:
                    Msg = MIMEBase(maintype, subtype)
                    Msg.set_payload(fp.read())
                    encoders.encode_base64(Msg)
                Msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(f))
                msg.attach(Msg)
        self.signal.sig.emit('st:Waiting for %s ...'%self.Sender_Email_mail.split('@')[1])
        try:
            if 'outlook' in self.Sender_Email_mail.lower():
                server_ = '-mail.outlook'
                smtp = smtplib.SMTP("smtp%s.com"%server_ ,25)
            elif 'yahoo' in self.Sender_Email_mail.lower():
                server_ = 'mail.yahoo'
                smtp = smtplib.SMTP("smtp.%s.com"%server_ ,25)
            else:
                smtp = smtplib.SMTP("smtp.%s.com"%self.Sender_Email_mail.split('@')[1].split('.')[0],25)
            self.signal.sig.emit('st:Logging to %s ...'%self.Sender_Email_mail)
            smtp.starttls()
            smtp.login(self.Sender_Email_mail,self.Sender_Password_mail)
            self.signal.sig.emit('st:Sending mail to %s ...'%self.Receiver_Email_mail)
            smtp.sendmail(self.Sender_Email_mail, self.Receiver_Email_mail, msg.as_string())
            self.signal.sig.emit('sst-msg:Email has been sent successfully to %s'%self.Receiver_Email_mail.lower())
            smtp.close()
        except socket.gaierror:
            self.signal.sig.emit('st-msg:Connection Error; We are Unable to connect server, check you Internet Connection')
        except smtplib.SMTPAuthenticationError:
            self.signal.sig.emit('st-msg:Authentication Error; Sender mail or Password is incorrect!')
        except smtplib.SMTPRecipientsRefused:
            self.signal.sig.emit('st-msg:Recipients Refused Error;Please provide valid Receiver Email address.')
        except smtplib.SMTPConnectError:
            self.signal.sig.emit('st-msg:We are expereicing problem while connecting to Server!')
        except smtplib.SMTPServerDisconnected:
            self.signal.sig.emit('st-msg:Server Disconnected; We are experiencing problems while connecting to Server!')
        except Exception, e:
            self.signal.sig.emit('st-msg:Server Disconnected; %s!'%e.message)
    def stop(self):
        self.terminate()
                
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.File_Size = {}
        Form_1 = QFormLayout()
        Form_2 = QFormLayout()
        Form_3 = QFormLayout()
        Form_4 = QFormLayout()
        Grid_1 = QGridLayout()
        Grid_2 = QGridLayout()
        Grid_3 = QGridLayout()
        Horizontal_1 = QHBoxLayout()
        Horizontal_2 = QHBoxLayout()
        Horizontal_3 = QHBoxLayout()
        Horizontal_4 = QHBoxLayout()
        Vertical_1 = QVBoxLayout()
        Vertical_2 = QVBoxLayout()
        Vertical_3 = QVBoxLayout()
        Vertical_4 = QVBoxLayout()
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        ## Defining Widget ...
        self.Sender = QGroupBox('Sender Detail')
        self.Sender.setLayout(Vertical_1)
        self.Receiver = QGroupBox('Email Detail')
        self.Receiver.setLayout(Vertical_2)
        self.sender_mail = QLineEdit("bilalahmadj.110@gmail.com")
        self.sender_mail.setEnabled(False)
        self.sender_mail.setStyleSheet('QLineEdit{padding:2,2,1,12;border:1px solid silver; font-size:9pt}'
                                       'QLineEdit:focus{padding:2,2,1,12;border:1px solid grey; font-size:9pt}')
        self.sender_mail.setFont(QFont('Segoe UI Semibold', 9))
        self.send_pass = QLineEdit("MDMzMzE3MzkwOTUsYUE=\n".decode('base64'))
        self.send_pass.setEnabled(False)
        self.send_pass.setStyleSheet('QLineEdit{padding:2,3,1,12;border:1px solid silver; font-size:9pt}'
                                     'QLineEdit:focus{padding:2,3,1,12;border:1px solid grey; font-size:9pt}')
        self.send_pass.setEchoMode(QLineEdit.Password)
        self.remember_me = QCheckBox('Remember me')
        self.remember_me.setChecked(True)
        self.receiver_mail = QLineEdit()
        self.receiver_mail.setFont(QFont('Segoe UI Semibold', 9))
        self.receiver_mail.setStyleSheet('QLineEdit{padding:2,2,1,12;border:1px solid silver; font-size:9pt}'
                                         'QLineEdit:focus{padding:2,2,1,12;border:1px solid grey; font-size:9pt}')
        completer = QCompleter()
        self.receiver_mail.setCompleter(completer)
        model = QStringListModel()
        completer.setModel(model)
        self.subject = QLineEdit()
        self.subject.focusOutEvent = lambda _:self.subject.setText(self.subject.text().upper())
        self.subject.setStyleSheet('QLineEdit{padding:2,2,1,12;border:1px solid silver; font-size:9pt}'
                                   'QLineEdit:focus{padding:2,2,1,12;border:1px solid grey; font-size:9pt}')
        self.subject.setFont(QFont('Segoe UI Semibold', 9))
        self.body = QTextEdit()
        self.Plain = QRadioButton('Body as plain text')
        self.Plain.setChecked(1)
        self.HTML = QRadioButton('Body as html text')
        self.HTML.toggled.connect(self.Font_2)
        self.Plain.toggled.connect(self.Font_1)
        self.body.setStyleSheet('QTextEdit{padding:2,2,1,12;border:1px solid silver}'
                                'QTextEdit:focus{padding:2,2,1,12;border:1px solid grey}')
        self.body.setFont(QFont('Times New Roman', 11))
        self.body.setTabChangesFocus(True)
        self.attachments = QLabel("<a href=\"http://example.com/\">Show Attachments</a>")
        self.attachments.setCursor(Qt.PointingHandCursor)
        self.Attach = QPushButton('Attach')
        self.attachments_detail = QLabel('No any Attachment added yet! Drop file(s) to add...')
        self.attachments_detail.setFont(QFont('Roboto Lt', 10))
        self.Attach.setIcon(QIcon('attach.png'))
        self.Send = QPushButton(' Send')
        self.Send.setIcon(QIcon('send.png'))
        self.Reset = QPushButton(' Reset')
        self.Reset.setIcon(QIcon('reset.png'))
        self.Cancel = QPushButton(' Cancel')
        self.Cancel.setIcon(QIcon('cross.png'))
        self.Cancel.setIconSize(QSize(12,12))
        self.Table = QTableWidget()
        self.Table.setMinimumSize(450,150)
        self.Table.setColumnCount(4)
        self.Table.setHorizontalHeaderLabels(['Name', 'Size','Location', ''])
        self.Table.itemClicked.connect(self.REMOVE)
        self.Table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Table.setColumnWidth(0, 200)
        self.Table.setColumnWidth(1, 75)
        self.Table.setColumnWidth(2, 275)
        self.Table.setColumnWidth(3, 26)
        self.Table.hide()
        ## Event defining
        self.Attach.clicked.connect(self.ATTACH)
        self.Send.clicked.connect(self.SEND)
        self.attachments.mouseReleaseEvent = lambda _: self.Hide_Show()
        self.Cancel.clicked.connect(self.CANCEL)
        self.Reset.clicked.connect(self.RESET)
        ## First GroupBox Layouts
        Form_1.addRow('Email               ', self.sender_mail)
        Form_1.addRow('Password', self.send_pass)
        Horizontal_1.addStretch(1)
        Horizontal_1.addWidget(self.remember_me)
        ## Second GroupBox Layouts
        Form_3.addRow('Receiver          ', self.receiver_mail)
        Form_3.addRow('Subject', self.subject)
        Horizontal = QHBoxLayout()
        Horizontal.addWidget(self.Plain)
        Horizontal.addWidget(self.HTML)
        Form_3.addRow(QLabel(),Horizontal)
        Form_3.addRow(QLabel('Body'),self.body)
        self.Label_attach = QLabel('Attachment   ')
        Horizontal_2.addWidget(self.Label_attach)
        Horizontal_2.addWidget(self.attachments_detail)
        Horizontal_2.addStretch(1)
        Horizontal_2.addWidget(self.attachments)
        Horizontal_2.addWidget(self.Attach)
        Horizontal_3.addWidget(self.Sender)
        Horizontal_3.addLayout(Vertical_3)
        Vertical_3.addWidget(self.Send)
        Vertical_3.addWidget(self.Reset)
        Vertical_3.addWidget(self.Cancel)
        Vertical_3.addStretch(1)
        self.setAcceptDrops(True)
        Vertical_1.addLayout(Form_1)
        Vertical_1.addStretch(0)
        Vertical_1.addLayout(Horizontal_1)
        Vertical_2.addLayout(Form_3)
        Vertical_2.addLayout(Horizontal_2)
        Vertical_2.addWidget(self.Table)
        self.createActions()
        self.createMenus()
        Vertical_4.addLayout(Horizontal_3)
        Vertical_4.addWidget(self.Receiver)
        self.Loading = QLabel()
        self.Movie = QMovie('loading.gif'); self.Movie.start()
        self.Movie.setScaledSize(QSize(641,10))
        self.Loading.hide()
        self.Loading.setMovie(self.Movie)
        Vertical_4.addStretch(1)
        Vertical_4.addWidget(self.Loading)
        self.Status_Bar = self.statusBar()
        self.Timer = QTimer()
        self.Timer.start(7000)
        self.con = QLabel()
        self.Status_Bar.addPermanentWidget(self.con)
        self.Timer.timeout.connect(self.ICON)
        self.Status_Bar.setFont(QFont('Segoe UI Semibold',10))
        self.attachments_detail.setFont(QFont('Segoe UI Semibold',9))
        self.Status_Bar.setStyleSheet('background-color:#DEE3F3; color:blue')
        self.Table.setFont(QFont('Roboto Lt', 10))
        self.widget.setLayout(Vertical_4)
        self.widget.setTabOrder(self.sender_mail, self.send_pass)
        self.widget.setTabOrder(self.send_pass,self.remember_me)
        self.widget.setTabOrder(self.remember_me,self.receiver_mail)
        self.widget.setTabOrder(self.receiver_mail,self.subject)
        self.widget.setTabOrder(self.subject,self.body)
        self.widget.setTabOrder(self.body, self.Attach)
        ToolTips_Detail = { self.sender_mail:     "Sender mail-address goes here",
                            self.send_pass:       "Password for sender mail goes here",
                            self.remember_me:     "This function will remember your Password and Email for future use.",
                            self.Send:            "Click to send mail! [CTRL + ENTER]",
                            self.Cancel:          "Click to Exit from Application! <br>[ESC]",
                            self.Reset:           "Click to reset! <br>[CTRL + R]",
                            self.Loading:         "Please wait!",
                            self.attachments:     "Click to show your Attachments/files detail in Table form.<br>[Ctrl + Q]",
                            self.body:            "Body is the Explaination",
                            self.subject:         "Subject or Title of Email show at Top in Email",
                            self.Attach:          "Attach files or drop directly onto form <br>[CTRL + T]",
                            self.attachments_detail:"Attachment details"
                          }
        Place_holder = {    self.sender_mail:    "Sender_Email@example.com",
                            self.send_pass:    "**********************",
                            self.subject:      "Subject or Title of Email",
                            self.receiver_mail: "Receiver_Email@example.com "
                       }
        for places in Place_holder:
            self.PLACEHOLDER(places, Place_holder[places])
        for key in ToolTips_Detail:
            self.TOOLTIP(key,ToolTips_Detail[key])
        
        try:
            model.setStringList(self.SAVE()[0])
        except:self.Status_Bar.showMessage('Database not found ... !')
        self.setFont(QFont('Segoe UI Semibold', 9))
        self.setWindowIcon(QIcon('send.png'))
        self.setWindowTitle('SEND MAIL')
        self.resize(659, 473)
    def Enable(self):
        self.Loading.hide()
        self.Send.setEnabled(1)
        self.Reset.setEnabled(1)
        self.Sender.setEnabled(1)
        self.Receiver.setEnabled(1)
    def Disable(self):
        self.Loading.show()
        self.Send.setEnabled(0)
        self.Reset.setEnabled(0)
        self.Sender.setEnabled(0)
        self.Receiver.setEnabled(0)
        self.Cancel.setFocus(Qt.OtherFocusReason)
    def EMIT(self, data):
        if str(data).split(':')[0] == 'st':
            self.Status_Bar.showMessage(data.split(':')[1])
        elif str(data).split(':')[0] == 'sst-msg':
            self.Enable()
            self.Status_Bar.showMessage(data.split(':')[1])
            self.MESSAGE('information', 'Email sent', 'Congratulation, Email has been sent successfully to <b>%s</b>'%self.receiver_mail.text().lower(), False)
            self.SAVE()
            
        elif str(data).split(':')[0] == 'st-msg':
            self.Status_Bar.showMessage(data.split(':')[1].split(";")[1])
            self.Enable()
            self.MESSAGE('critical', 'Message Sent Error', "<b>%s: </b>%s"%(str(data).split(':')[1].split(";")[0],str(data).split(':')[1].split(";")[1]), False)
        else:
            self.MESSAGE('critical', 'Message Sent Error', str(data).split(':')[1], False)
            self.Enable()
    def SAVE(self):
        None
    def CREATE_TABLE(self, Item):
        self.Count = 0; b=0
        self.count = 0
        self.Files = ""; self.files =""
        for item in Item:
            item = str(item).replace('/', '\\')
            if item not in self.File_Size:
                self.Files +=  str(os.path.split(item)[1].split('.')[0]) + str(", ")
                self.Count += 1
                self.File_Size[item] = int(os.stat(item).st_size)
                self.Table.setRowCount(len(self.File_Size))
                self.Table.setItem(len(self.File_Size)-1,0,  QTableWidgetItem('%s'% os.path.split(item)[1]))
                if float(self.File_Size[item]/1024.00/1024.00/1024.00) >= 1:
                    self.Table.setItem(len(self.File_Size)-1,1,  QTableWidgetItem('%.3f GB'% float(self.File_Size[item]/1024.00/1024.00/1024.00)))
                elif float(self.File_Size[item]/1024.00/1024.00) >= 1:
                    self.Table.setItem(len(self.File_Size)-1,1,  QTableWidgetItem('%.2f MB'% float(self.File_Size[item]/1024.00/1024.00)))
                else:
                    self.Table.setItem(len(self.File_Size)-1,1,  QTableWidgetItem('%.1f kB'% float(self.File_Size[item]/1024.00)))
                self.Table.setItem(len(self.File_Size)-1,2,  QTableWidgetItem('%s'%str(item)))
                headerItem = QTableWidgetItem();headerItem.setIcon(QIcon(QPixmap("cancel.png")))
                self.Table.setItem(len(self.File_Size)-1,3,  headerItem)
            else:
                self.count += 1
                self.files +=  str(os.path.split(item)[1].split('.')[0]) + str(", ")
        for values in self.File_Size.values():
            b += values
        if float(b)/1024.00/1024.00/1024.00 >= 1:
            if len(self.File_Size) == 1:
                self.attachments_detail.setText('Total File added: %d  |  Size: %.4f GB'%(len(self.File_Size),float(b/1024.00/1024.00/1024.00)))
            else:
                self.attachments_detail.setText('Total Files added: %d  |  Size: %.4f GB'%(len(self.File_Size),float(b/1024.00/1024.00/1024.00)))
        elif float(b)/1024.00/1024.00 >= 1:
            if len(self.File_Size) == 1:
                self.attachments_detail.setText('Total File added: %d  |  Size: %.3f MB'%(len(self.File_Size),float(b/1024.00/1024.00)))
            else:
                self.attachments_detail.setText('Total Files added: %d  |  Size: %.3f MB'%(len(self.File_Size),float(b/1024.00/1024.00)))
        else:
            if len(self.File_Size) == 1:
                self.attachments_detail.setText('Total File added: %d  |  Size: %.2f kB'%(len(self.File_Size), float(b/1024.00)))
            else:
                self.attachments_detail.setText('Total Files added: %d  |  Size: %.2f kB'%(len(self.File_Size), float(b/1024.00)))
        if self.count == 0:
            if self.Count == 0:
                self.Status_Bar.showMessage('No any file added in this session!')
            elif self.Count == 1:
                self.Status_Bar.showMessage('%d File added successfully: %s'%(self.Count,self.Files[:-2]))
            else:
                self.Status_Bar.showMessage('%d Files added successfully: %s'%(self.Count,self.Files[:-2]))
        elif self.Count == 0:
            if self.count == 1:
                self.Status_Bar.showMessage('%d File already exists: %s'%(self.count,self.files[:-2]))
            else:
                self.Status_Bar.showMessage('%d Files already exists: %s'%(self.count,self.files[:-2]))
        else:
            self.Status_Bar.showMessage('%d File(s) added successfully: %s  |   %d File(s) already exists: %s'%(self.Count,self.Files[:-2],self.count,self.files[:-2]))

    def Font_1(self):
        self.body.setFont(QFont("Times New Roman", 11))
    def Font_2(self):
        self.body.setFont(QFont("Consolas",10))
    def REMOVE(self, item):
        a = 0
        if item.column() == 3:

            if self.File_Size.pop(self.Table.item(item.row(),2).text()) != '':
                self.Status_Bar.showMessage('Attachment "%s" removed!'%self.Table.item(item.row(),0).text())
            for values in self.File_Size.values():
                a += values
            if float(a)/1024.00/1024.00/1024.00 >= 1:
                 self.attachments_detail.setText('Total file(s) added: %d  |  Size: %.4f GB'%(len(self.File_Size),float(a)/1024.00/1024.00/1024.00))  
            elif float(a)/1024.00/1024.00 >= 1:
                 self.attachments_detail.setText('Total file(s) added: %d  |  Size: %.3f MB'%(len(self.File_Size),float(a)/1024.00/1024.00))
            else:
                 self.attachments_detail.setText('Total file(s) added: %d  |  Size: %.2f kB'%(len(self.File_Size), float(a)/1024.00))
            if len(self.File_Size) == 0:
                self.Status_Bar.showMessage('All the attachments have been removed successfully!')
                self.attachments_detail.setText('No any Attachment added yet! Drop files here ...')
                self.File_Size.clear()
            self.Table.removeRow(item.row())
        else:
            self.Status_Bar.showMessage('Selected File: %s | Size: %s '%(self.Table.item(item.row(),0).text(),self.Table.item(item.row(),1).text()))
            
    def createActions(self):
        self.newAct = QAction("&New",
                self, shortcut=QKeySequence.New,statusTip="Create a new file", triggered=None)

        self.openAct = QAction("&Open...", self, shortcut=QKeySequence.Open,
                 triggered=None)

        self.saveAct = QAction("&Save", self, shortcut=QKeySequence.Save,
                statusTip="Save the document to disk", triggered=None)


        self.exitAct = QAction("E&xit", self, shortcut="Alt+F4",
                statusTip="Exit the application",
                triggered=self.close)

        self.about = QAction("About &Qt", self,
                statusTip="Show about developer",
                triggered=None)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.editMenu = self.menuBar().addMenu("&Tools")
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.about)       
    def Hide_Show(self):
        if self.attachments.text() == '<a href="http://example.com/">Show Attachments</a>':
            self.attachments.setCursor(Qt.PointingHandCursor)
            self.attachments.setText("<a href=\"http://example.com/\">Hide Attachments</a>")
            self.Table.show()
        else:
            self.attachments.setCursor(Qt.PointingHandCursor)
            self.attachments.setText("<a href=\"http://example.com/\">Show Attachments</a>")
            self.Table.hide()
    def MESSAGE(self, error_type, heading, body, Button):
        if Button == False:
            try:
                exec('QMessageBox.%s(self, \'%s\',"%s",QMessageBox.Ok)'%(error_type, heading, body))
            except:
                print 'Message Error'
        else:
            exec('Mess = QMessageBox.%s(self, "%s","%s",QMessageBox.Discard|QMessageBox.Save|QMessageBox.Cancel)'%(error_type, heading, body))
            if Mess == QMessageBox.StandardButton.Discard:
                self.longthread.stop()
                self.close()
            elif Mess == QMessageBox.StandardButton.Save:
                self.SAVE()
    def ERROR(self, value):
        if int(value) == 1:
            self.Status_Bar.showMessage('Please check whether you correctly typed the Sender\'s Email address!')
            self.MESSAGE('warning','Sender Mail Error','Please check whether you correctly typed the <b>Sender\'s Email address</b>!', False)
        elif int(value) == 2:
            self.Status_Bar.showMessage('Please check whether you correctly typed the Sender\'s Email address!')
            self.MESSAGE('warning','Password Error','Please specify correct Password for <b>%s</b> '%self.sender_mail.text(), False)
        elif int(value) == 3:
            self.Status_Bar.showMessage('Please specify correct <b>Password</b> for %s ...'%self.sender_mail.text())
            self.MESSAGE('warning','Receiver Mail Error','Please check whether you correctly typed the Receiver\'s Email address!', False)
        elif int(value) == 4:
            self.Status_Bar.showMessage('Please specify atleast Subject, Body or Attachment!')
            self.MESSAGE('warning','Email required Information Error',
                         'You must specify atleast one of following information to send mail.'
                         '<br>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \a &nbsp;&nbsp;<b>Subject of Email.</b>'
                         '<br>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \a &nbsp;&nbsp;<b>Body of Email</b>'
                         '<br>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \a &nbsp;&nbsp;<b>At least on attachment file .</b>', False) 
        else:
            self.Status_Bar.showMessage('Please click Save for future use ...')
            self.MESSAGE('question','Exit from Application','Are you sure to <b>Exit</b> from Application right now?'
                         '<br>Want to save your data <b> click Save </b>', True)
            self.Status_Bar.showMessage('')
    def VALID(self):
        if '@' not in  self.sender_mail.text().lower() or '.com' not in self.sender_mail.text().lower():
            self.ERROR('1')
            self.sender_mail.setFocus(Qt.OtherFocusReason)
        elif self.send_pass.text().replace(' ' ,'') == '':
            self.ERROR('2')
            self.send_pass.setFocus(Qt.OtherFocusReason)
        elif '@' not in  self.receiver_mail.text().lower() or '.com' not in self.receiver_mail.text().lower():
            self.ERROR('3')
            self.receiver_mail.setFocus(Qt.OtherFocusReason)
        elif self.subject.text().replace(' ','') == '' and self.body.toPlainText().replace(' ','') == '' and len(self.File_Size) == 0:
            self.ERROR('4')
            self.body.setFocus(Qt.OtherFocusReason)
        else:
            return True
    def SAVE(self):
        try:
            self.read_from = open('data')
            self.Read_from = self.read_from.read().split("~")
            comp = list([self.Read_from[0]])
            return [comp, self.Read_from[1], self.Read_from[2]]
        except:
            pass    
    def SEND(self):
        if self.VALID():
            self.Disable()
            self.Status_Bar.showMessage('Collecting data, please wait ...')
            if self.subject.text().replace(' ','') != '' and self.body.toPlainText().replace(' ','') == '' and len(self.File_Size.keys()) == 0: ## 1
                
                self.longthread = MyLongThread(Sender_Email_mail      = self.sender_mail.text(),
                    Sender_Password_mail   = self.send_pass.text(),
                    Receiver_Email_mail    = self.receiver_mail.text(),
                    Subject_mail           = self.subject.text(),
                    Body_mail              = None,
                    Attachments_mail       = None,
                    HTML_mail = self.HTML.isChecked())
                self.longthread.start()
                self.longthread.signal.sig.connect(self.EMIT)
            elif self.subject.text().replace(' ','') == '' and self.body.toPlainText().replace(' ','') != '' and len(self.File_Size.keys()) == 0:  ## 2
            
                self.longthread = MyLongThread(Sender_Email_mail      = self.sender_mail.text(),
                    Sender_Password_mail   = self.send_pass.text(),
                    Receiver_Email_mail    = self.receiver_mail.text(),
                    Subject_mail = None,
                    Body_mail        = self.body.toPlainText(),
                    Attachments_mail       = None,
                    HTML_mail = self.HTML.isChecked())
                self.longthread.signal.sig.connect(self.EMIT)
                self.longthread.start()
            elif self.subject.text().replace(' ','') == '' and self.body.toPlainText().replace(' ','') == '' and len(self.File_Size.keys()) != 0: ## 3
               
                self.longthread = MyLongThread(Sender_Email_mail      = self.sender_mail.text(),
                    Sender_Password_mail   = self.send_pass.text(),
                    Receiver_Email_mail    = self.receiver_mail.text(),
                    Subject_mail       = None,
                    Body_mail        = None,
                    Attachments_mail        = self.File_Size.keys(),
                    HTML_mail = self.HTML.isChecked())
                self.longthread.start()
                self.longthread.signal.sig.connect(self.EMIT)
            elif self.subject.text().replace(' ','') != '' and self.body.toPlainText().replace(' ','') != '' and len(self.File_Size.keys()) != 0: ## FULL
                
                self.longthread = MyLongThread(Sender_Email_mail      = self.sender_mail.text(),
                    Sender_Password_mail   = self.send_pass.text(),
                    Receiver_Email_mail    = self.receiver_mail.text(),
                    Attachments_mail        = self.File_Size.keys(),
                    Subject_mail = self.subject.text(),
                    Body_mail = self.body.toPlainText(),
                    HTML_mail = self.HTML.isChecked())
                self.longthread.start()
                self.longthread.signal.sig.connect(self.EMIT)
            elif self.subject.text().replace(' ','') != '' and self.body.toPlainText().replace(' ','') == '' and len(self.File_Size.keys()) != 0: # 1, 3
                
                self.longthread = MyLongThread(Sender_Email_mail      = self.sender_mail.text(),
                    Sender_Password_mail   = self.send_pass.text(),
                    Receiver_Email_mail    = self.receiver_mail.text(),
                    Subject_mail = self.subject.text(),
                    Body_mail = None,
                    Attachments_mail        = self.File_Size.keys(),
                    HTML_mail = self.HTML.isChecked())
                self.longthread.start()
                self.longthread.signal.sig.connect(self.EMIT)
            elif self.subject.text().replace(' ','') != '' and self.body.toPlainText().replace(' ','') != '' and len(self.File_Size.keys()) == 0: # 1, 2
                
                self.longthread = MyLongThread(Sender_Email_mail      = self.sender_mail.text(),
                    Sender_Password_mail   = self.send_pass.text(),
                    Receiver_Email_mail    = self.receiver_mail.text(),
                    Subject_mail = self.subject.text(),
                    Body_mail = self.body.toPlainText(),
                    Attachments_mail        = None,
                    HTML_mail = self.HTML.isChecked())
                self.longthread.start()
                self.longthread.signal.sig.connect(self.EMIT)
            elif self.subject.text().replace(' ','') == '' and self.body.toPlainText().replace(' ','') != '' and len(self.File_Size.keys()) != 0: # 2, 3
                
                self.longthread = MyLongThread(Sender_Email_mail      = self.sender_mail.text(),
                    Sender_Password_mail   = self.send_pass.text(),
                    Receiver_Email_mail    = self.receiver_mail.text(),
                    Subject_mail = None,
                    Body_mail = self.body.toPlainText(),
                    Attachments_mail        = self.File_Size.keys(),
                    HTML_mail = self.HTML.isChecked())
                self.longthread.start()
                self.longthread.signal.sig.connect(self.EMIT)
            else:
                None
        else:
            None
    def RESET(self):
        self.File_Size.clear()
        self.Count = 0
        self.Table.setRowCount(0)
        self.receiver_mail.setText('')
        self.subject.setText('')
        self.body.setPlainText('')
        self.attachments_detail.setText('No any Attachment added yet! Drop file(s) to add...')
        self.Status_Bar.showMessage('Reset, All fields have been reset')
        self.Table.show()
    def CANCEL(self):
        self.ERROR('5')
    def ATTACH(self):
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        names = file_name.getOpenFileNames(self, "Open files", "C\\Desktop")
        if len(names[0]) != 0:
            self.CREATE_TABLE(names[0])
    def resizeEvent(self,resizeEvent):
        x = self.Receiver.frameGeometry().width()
        self.Movie.setScaledSize(QSize(x-10,10))
    def TOOLTIP(self, Widget, Tooltip):
        Widget.setToolTip('<b>%s</b>'%Tooltip)

    def PLACEHOLDER(self, Widg, placeholder):
        Widg.setPlaceholderText(placeholder)
    def dragEnterEvent(self, e):
        tem = []
        if e.mimeData().hasUrls:
            for url in e.mimeData().urls():
                tem.append(os.path.split(url.toLocalFile())[1])
            self.attachments_detail.setStyleSheet('border:3px dashed grey;color:silver; font-size:40pt; font-family:Roboto Lt')
            self.attachments_detail.setText('Drop file here')
            if len(tem) > 1:
                self.Status_Bar.showMessage('Files dragged: %d '%(len(tem)))
            else:
                self.Status_Bar.showMessage('File dragged: %d '%(len(tem)))
            e.accept()
        else:
            e.ignore()
    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()
    def dropEvent(self, e):
        self.resize(659, 400)
        self.attachments_detail.setStyleSheet('font-size:10pt; font-family:Roboto Lt')
        List = []
        if e.mimeData().hasUrls:
            for url in e.mimeData().urls():
                List.append(url.toLocalFile())
            self.CREATE_TABLE(List)
    def dragLeaveEvent(self, e):
        self.Status_Bar.showMessage('No any dropped attachment!')
        self.resize(659, 400)
        self.attachments_detail.setStyleSheet('font-size:10pt; font-family:Roboto Lt')
    def keyPressEvent(self, event):
        MOD_MASK = (Qt.CTRL | Qt.ALT | Qt.SHIFT | Qt.META)
        keyname = ''
        key = event.key()
        modifiers = int(event.modifiers())
        if (modifiers and modifiers & MOD_MASK == modifiers and
            key > 0 and key != Qt.Key_Shift and key != Qt.Key_Alt and
            key != Qt.Key_Control and key != Qt.Key_Meta):
            keyname = QKeySequence(modifiers + key).toString()##print('event.text(): %r' % event.text());print('event.key(): %d, %#x, %s' % (key, key, keyname))
            if keyname == 'Ctrl+Return':
                self.Send.click()
            elif keyname == 'Ctrl+R':
                self.Reset.click()
            elif keyname == 'Ctrl+T':
                self.Attach.click()
            elif keyname == 'Ctrl+Q':
                if self.attachments.text() == '<a href="http://example.com/">Show Attachments</a>':
                    self.attachments.setCursor(Qt.PointingHandCursor)
                    self.attachments.setText("<a href=\"http://example.com/\">Hide Attachments</a>")
                    self.Table.show()
                else:
                    self.attachments.setCursor(Qt.PointingHandCursor)
                    self.attachments.setText("<a href=\"http://example.com/\">Show Attachments</a>")
                    self.Table.hide()
                    self.attachments.releaseMouse
            else:
                print keyname
        else:
            if event.key() == 16777216:
                self.Cancel.click()
    def ICON(self):
        if self.CONNECTION() == True:
            self.con.setPixmap(QPixmap('offline.png'))
            self.con.setToolTip('No Internet access!')
        else:
            self.con.setToolTip('Internet access!')
            self.con.setPixmap(QPixmap('online.png'))
    def CONNECTION(self):
        try:
            if len(socket.gethostbyaddr(socket.gethostname())[2][0]) < 9:
                return True
            else:
                None
        except:
            print 'error'
            None
if __name__ == '__main__':
    app = QApplication([])
    win = Window()
    win.show()
    app.exec_()
