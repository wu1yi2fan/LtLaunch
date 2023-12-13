from typing import Optional
from PySide6.QtGui import QIcon, QAction,QAbstractFileIconProvider
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget, QApplication, QGridLayout, QPushButton, QSystemTrayIcon, QMenu,QFileDialog,QInputDialog
from PySide6.QtCore import Qt,QFileInfo,QSize
from PySide6.QtWidgets import QMessageBox
#from BlurWindow.blurWindow import GlobalBlur
#from aero_window import WindowEffect as GlobalBlur
from win32mica import MicaTheme
from win32mica import ApplyMica, MicaStyle
from json import load as json_load
from json import dump as json_dump
from win32api import ShellExecute
from win32api import MessageBox
from win32con import MB_OK
from functools import partial
from sys import exit, executable, argv
from os import execl
#from pyautogui import position as pag_position

qt_style = '''
    QPushButton {
        background-color: rgba(255,255,255,0); 
        width:64px; 
        height:24px; 
        border:none;
        }
    QPushButton#AppButton {
        height:48px; 
        }
    QPushButton::hover{
        background-color: rgba(255,255,255,0.6); 
    }
    #Title {
        background-color: rgba(255,255,255,0);
        text-align: left;
    }
    #Close_btn{
        height:16px;
        width:16px;
        background-color: rgba(0,0,0,0);
    }
    #Close_btn::hover{
        background-color: rgba(212,25,32,0.6);
    }
    #Window {
        background-color: rgba(255,255,255,0);
        border-radius: 8px;
    }
    #Grid {
        padding:0;
    }
    QMenu {
        background-color: rgba(255,255,255,0.8);
        margin: 1px;
        border: 0px;
        width: 120px;
    }
    QMenu::item {
        background-color: transparent;
    }
    QMenu::item:selected { 
        color: rgb(0,0,0);
        background-color: rgba(0,0,0,0.1);
    }

'''

hotboot = 0

class Main(QWidget):

    def showEvent(self, event):
        if hotboot == 1:
            self.showwindow()
        if hotboot == 0:
            widget.show()

    def showwindow(self):
        self.set_position()
        #self.Globalblur = GlobalBlur()
        #self.Globalblur.setAcrylicEffect(int(self.winId()))
        #GlobalBlur(self.winId(),Acrylic=True)
        ApplyMica(HWND=self.winId(), Theme=MicaTheme.LIGHT, Style=MicaStyle.DEFAULT)
        widget.showNormal()    

    def exitwindow(self):
        QApplication.quit()

    def reboot(self):
        p = executable
        execl(p,p,*argv)

    def generate_config(self):
        the_new_item = [{"name":"记事本", "src":"notepad.exe"}]
        new_config = {"softlist": the_new_item}
        with open('config.json' ,'w' , encoding='utf-8') as f_new :
            json_dump(new_config, f_new)

    def __init__(self):
        super().__init__()
        self.initTray()

        self.initWindow()
    
    def set_position(self):
        #window_x, window_y = pag_position()
        window_x = QCursor.pos().x()
        window_y = QCursor.pos().y()
        the_x = window_x - widget.width()/2
        the_y = window_y - widget.height() - 60
        widget.move(int(the_x),int(the_y))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
    
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()
    
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False

    def trayclicked(self,t):
        if t == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isHidden() == False and self.isMinimized() == False:
                self.hide()
            else:
                self.showwindow()

    def addItem(self):
        the_new_item = QFileDialog().getOpenFileName(self,"选择文件","/","*.*")
        the_new_item_url = the_new_item[0].replace('/',r'\\')
        input_dialog = QInputDialog()
        
        the_item_name, is_ok = input_dialog.getText(self,"请输入名称","路径:\n"+the_new_item[0]+"\n名称:")
        input_dialog.setStyleSheet("QPushButton { height: 24px; }")
        if is_ok and the_item_name:
            the_item_config = {"name":the_item_name, "src":the_new_item_url}
            MessageBox(0,str(the_item_config),'提示', MB_OK)
            thetype.append(the_item_config)
            new_config = {"softlist": thetype}
            with open('config.json' ,'w' , encoding='utf-8') as f_new :
                json_dump(new_config, f_new)
                f_new.close()
            MessageBox(0,'添加成功！点击确定立刻重载程序', '提示', MB_OK)
            self.reboot()

    def initTray(self):
        self.add_Item = QAction("添加")
        self.show_window = QAction("显示")
        self.exit_window = QAction("退出")
        self.tray_list = QMenu()
        self.tray_list.addAction(self.add_Item)
        self.add_Item.triggered.connect(self.addItem)
        self.tray_list.addAction(self.show_window)
        self.show_window.triggered.connect(self.showwindow)
        self.tray_list.addAction(self.exit_window)
        self.exit_window.triggered.connect(self.exitwindow)
        self.trayicon = QSystemTrayIcon()
        self.trayicon.setContextMenu(self.tray_list)
        self.trayicon.setIcon(QIcon("app.ico"))
        self.trayicon.setToolTip("显示面板")
        self.trayicon.activated.connect(self.trayclicked)
        self.tray_list.setStyleSheet(qt_style)
        self.trayicon.show()
        


    def initWindow(self):
        
        self.setObjectName("Window")
        self.resize(100,30)
        Window_Title = "Pad"
        Window_Icon = QIcon("app.ico")
        self.setWindowTitle(Window_Title)
        self.setWindowIcon(Window_Icon)
        self.setStyleSheet(qt_style)
        #GlobalBlur(self.winId(),Acrylic=True)
        #self.Globalblur = GlobalBlur()
        #self.Globalblur.setAcrylicEffect(int(self.winId()))
        ApplyMica(HWND=self.winId(), Theme=MicaTheme.LIGHT, Style=MicaStyle.DEFAULT)

        #变量初始化
        try:
            with open('config.json', encoding='utf-8') as f :
               configs = json_load(f)
               f.close()
        except IOError:
            MessageBox(0,'配置文件不存在，继续将新建配置文件', '错误', MB_OK)
            self.generate_config()
            self.reboot()

        def get_icon(src):
            file_src = src.replace(r'\\','/')
            the_file = QFileInfo(file_src)
            the_icon_object = QAbstractFileIconProvider()
            the_icon = the_icon_object.icon(the_file)
            return the_icon


        names = locals()
        global thetype
        thetype = configs['softlist']
        def run_proc(src):
            try:
                ShellExecute(0, 'open', src,'','', 1)
            finally:
                return

        def get_xy(n):
            n_i = n+2
            if (n_i % 3) == 0:
                x = 1
                y = int((n_i-3)/3+1)
            if (n_i % 3) == 2:
                x = 0
                y = int((n_i-1)/3+1)
            if (n_i % 3) == 1:
                x = 2
                y = int((n_i-2)/3+1)
            return x,y

        grid = QGridLayout()
        grid.setObjectName("Grid")
        self.setLayout(grid)
        grid.setColumnMinimumWidth(0,64)
        grid.setColumnMinimumWidth(1,64)
        grid.setColumnMinimumWidth(2,64)
        grid.setSpacing(1)
        grid.setContentsMargins(4,1,4,4)
        '''
        title_btn = QPushButton("Pad")
        title_btn.setIcon(Window_Icon)
        title_btn.setObjectName("Title")
        title_btn.setFixedSize(64,24)
        title_btn.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        grid.addWidget(title_btn,0,0,alignment=Qt.AlignLeft)

        close_btn = QPushButton("")
        close_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton))
        close_btn.setIconSize(QSize(10,10))
        close_btn.setObjectName("Close_btn")
        close_btn.setFixedSize(24,24)
        grid.addWidget(close_btn,0,2,alignment=Qt.AlignRight)
        close_btn.clicked.connect(partial(self.hide,))
        '''
        n = 0
        for soft_n in thetype:
            thesrc = soft_n['src']
            icon = get_icon(thesrc)
            names['btn_%s' % n] = QPushButton(icon,soft_n['name'])
            names['btn_%s' % n].setObjectName('AppButton')
            x,y = get_xy(n)
            grid.addWidget(names['btn_%s' % n],y,x)
            names['btn_%s' % n].clicked.connect(partial(run_proc,thesrc))
            n = n+1


if __name__ == "__main__":
    app = QApplication([])
    QApplication.setQuitOnLastWindowClosed(False)
    widget = Main()
    #widget.setWindowFlags(Qt.Window|Qt.FramelessWindowHint|Qt.WindowSystemMenuHint|Qt.WindowMinimizeButtonHint|Qt.WindowMaximizeButtonHint)
    
    widget.show()
    widget.setFixedSize(widget.width(),widget.height())
    hotboot = 1
    exit(app.exec())