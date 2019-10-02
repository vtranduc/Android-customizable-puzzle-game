from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup

class CustomizeArt(BoxLayout):

    preview_height_hint=0.5

    def __init__(self,app,**kwargs):
        super(CustomizeArt,self).__init__(**kwargs)

        self.app=app

        self.orientation='vertical'
        self.spacing=round(Window.width*0.01)
        
        self.fl=FileChooserIconView()
        self.fl.bind(selection=self.highlight)
        
        btn1=Button(text='Select')
        btn1.bind(on_release=self.select)
        btn2=Button(text='Default')
        btn2.bind(on_release=self.reset_image)
        btn3=Button(text='Cancel')
        btn3.bind(on_release=self.cancel)

        self.btnlayout=BoxLayout(size_hint_y=0.12,\
                            spacing=round(Window.width*0.01),\
                            orientation='horizontal')
        self.btnlayout.add_widget(btn1)
        self.btnlayout.add_widget(btn2)
        self.btnlayout.add_widget(btn3)

        self.message=Label(text='Preview will be displayed here'+\
                           '\nSupported formats include\n.png\n.jpg\n.jpeg')
        self.message.size_hint_y=self.preview_height_hint
        self.message.valign='middle'
        self.message.halign='center'

        self.size=(Window.width,Window.height)
        self.add_widget(self.message)
        self.add_widget(self.fl)
        self.add_widget(self.btnlayout)
        self.padding=[Window.width*0.01,Window.height*0.005,\
                      Window.width*0.01,Window.height*0.005]

        self.preview=None

    def select(self,instance):
        if self.preview==None:
            self.invalid_selection()
        else:
            self.app.make_selection(self.fl.selection[0])

    def reset_image(self,instance):
        self.app.make_selection('./imageAssets/puzzles/')
        
    def cancel(self,instance):
        self.app.turn_off_selection()

    def invalid_selection(self):
        try:
            self.error_message.open()
        except:
            self.error_message=self.error_popUp()
            self.error_message.open()

    def highlight(self,filechooser,selection):
        try:
            path=selection[0]
            file_type=path[-4]+path[-3]+path[-2]+path[-1]
        
            if file_type=='.png' or file_type=='.jpg' or file_type=='jpeg':
                self.preview=Image(source=path)
                self.preview.size_hint_y=self.preview_height_hint
                self.clear_widgets()
                self.add_widget(self.preview)
                self.add_widget(self.fl)
                self.add_widget(self.btnlayout)
            elif self.preview!=None:
                self.default_display()
        except:
            if self.preview!=None:
                self.default_display()

    def default_display(self):
        self.clear_widgets()
        self.add_widget(self.message)
        self.add_widget(self.fl)
        self.add_widget(self.btnlayout)
        self.preview=None
        
    def error_popUp(self):
        myText=Label(valign='middle',halign='center')
        myText.text='Selected file is not supported\nSupported'+\
                     ' formats include\n.png\n.jpg\n.jpeg'
        myButton=Button(text='Dismiss')
        myButton.bind(on_release=self.error_popUp_dismiss)
        myButton.size_hint_y=0.3
        myBox=BoxLayout(orientation='vertical')
        myBox.add_widget(myText)
        myBox.add_widget(myButton)
        return Popup(title='Please select again',content=myBox,size_hint=(0.9,0.5))

    def error_popUp_dismiss(self,instance):
        self.error_message.dismiss()
