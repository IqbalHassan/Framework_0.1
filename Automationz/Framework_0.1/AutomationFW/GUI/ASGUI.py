"""
import kivy
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from CoreFrameWork.login_info import username
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.animation import Animation
kivy.require('1.8.0')
from CoreFrameWork import DataBaseUtilities as DB
from kivy.app import App

class LoginScreen(Screen):
    username=ObjectProperty(None)
    password=ObjectProperty(None)
    server=ObjectProperty(None)
    error=ObjectProperty(None)
    db_link=StringProperty('')
    def __init__(self, **kwargs):
        super(LoginScreen,self).__init__(**kwargs)
        box_layout=BoxLayout(orientation='vertical',padding=150,spacing=10)
        automation_label=Label(text='Automation Framework',font_size=24,size_hint=(1,.3))
        box_layout.add_widget(automation_label)
        self.username=TextInput(text='Username',multiline=False,size_hint=(1,.1))
        box_layout.add_widget(self.username)
        self.password=TextInput(text='Password',multiline=False,password=True,size_hint=(1,.1))
        box_layout.add_widget(self.password)
        self.server=Spinner(text='Local',values=("Local","Production"),size_hint=(1,.1))
        box_layout.add_widget(self.server)
        login_button=Button(text='Login',size_hint=(1,.1))
        login_button.bind(on_press=self.login)
        box_layout.add_widget(login_button)
        self.error=Label(text='',font_size=16,size_hint=(1,.2))
        box_layout.add_widget(self.error)
        self.add_widget(box_layout)
        if 'username' in kwargs.keys():
            self.username.text=kwargs['username']
        if 'password' in kwargs.keys():
            self.password.text=kwargs['password']
        if 'server' in kwargs.keys():
            self.server.text=kwargs['server']
    
    def login(self,instance):
        if self.server.text=='Local':
            self.db_link="127.0.0.1"
        if self.server.text=='Production':
            self.db_link="135.23.123.206"    
        result=self.check_credential()
        if result['status']:
            #return HomeScreen(username='riz')
            self.parent.user_id=result['user_id']
            self.manager.current='HomeScreen'
        else:
            self.password.text=''
            self.username.text=''
            self.error.text='Authentication Error'
    def check_credential(self):
        Conn=DB.ConnectToDataBase(sHost=self.db_link)
        query="select distinct password,user_id from user_info ui,permitted_user_list pul where username='%s' and pul.user_names = ui.full_name and user_level in ('assigned_tester','manager')"%self.username.text.strip()
        print query
        password_list=DB.GetData(Conn,query,False)
        print password_list
        Conn.close()
        if isinstance(password_list,list) and len(password_list)>0:
            password_got=password_list[0][0]
            user_id=password_list[0][1]
            if self.password.text==password_got:
                dict_status={'username':self.username.text.strip(),'user_id':user_id,'status':True}
                return dict_status
            else:
                dict_status={'status':False}
                return dict_status
        else:
            dict_status={'status':False}
            return dict_status
    pass

class HomeScreen(Screen):
    user_id=StringProperty('')
    def __init__(self,**kwargs):
        super(HomeScreen,self).__init__(**kwargs)
        boxLayout=BoxLayout()
        boxLayout.add_widget(Label(text='Welcome'))
        log_out=Button(text='Log Out')
        log_out.bind(on_press=self.logout)
        boxLayout.add_widget(log_out)
        self.add_widget(boxLayout)
    def logout(self,instance):
        self.manager.current='Login'
        
        
    pass

class RunmanagerApp(App):
    def build(self):
        sm=ScreenManager()
        sm.user_id=''
        sm.add_widget(LoginScreen(name='Login',username='riz',password='.'))
        sm.add_widget(HomeScreen(name='HomeScreen'))
        return sm

if __name__=='__main__':
    runmanager=RunmanagerApp()
    runmanager.run()

"""
from Tkinter import Tk,Frame,BOTH,Button,Entry,Label
from win32api import GetSystemMetrics

def hello_world(username,password,frame2):
    print username
    print password
    print frame2
class MainWindow(Frame):
    def __init__(self,parent,width,height):
        Frame.__init__(self,parent,background="white")
        self.parent = parent
        self.initUI(width,height)
        frame1=Frame(self,height=height,width=(width/2),padx=40)
        frame1.pack(side="left")
        frame2=Frame(self,height=height,width=(width/2),bg="black")
        frame2.pack(side="right")
        #L1 = Label(frame1, text="User Name: ")
        #L1.pack( side = "left")
        username=Entry(frame1,width=50)
        username.pack()
        #L2 = Label(frame1, text="Password: ")
        #L2.pack( side = "left")
        password=Entry(frame1,show="*",width=50)
        password.pack()
        button=Button(frame1,text="login",command=hello_world(username,password,frame2))
        button.pack()

    def center_window(self,w,h):
        #get screen height & width
        sw = (GetSystemMetrics(0)-w)/2
        sh = (GetSystemMetrics(1)-h)/2
        self.parent.geometry("%dx%d+%d+%d"%(w,h,sw,sh))
    def initUI(self,width,height):
        self.parent.title("Simple")
        self.pack(fill=BOTH,expand=1)
        self.center_window(width,height)
def main():
    root = Tk()
    width=800
    height=500
    app=MainWindow(root,width,height)
    root.mainloop()

if __name__=="__main__":
    main()