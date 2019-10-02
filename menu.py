import kivy
kivy.require('1.7.2')

from kivy.uix.widget import Widget
from cropImage import CropImage, cropFit, ratioFit, centering_widget
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.uix.scrollview import ScrollView
from artInfo import ArtInfo
from kivy.clock import Clock

class Menu(Widget):
    start_button_str='./imageAssets/gmbuttonstart.png'
    score_button_str='./imageAssets/gmbuttonscore.png'
    gallery_button_str='./imageAssets/gmbuttonsgallery.png'
    configure_button_str='./imageAssets/gmbuttonsconfigure.png'
    exit_button_str='./imageAssets/gmbuttonsEXIT.png'

    #Put the strings of buttons into the list, so we can use for loop later
    button_paths=[start_button_str,score_button_str,gallery_button_str,
                  configure_button_str,exit_button_str]
    
    top_edge=0.5 #Manual
    left_edge=0.3 #Manual
    
    background='./imageAssets/bg.png'
    #Background image's position will be computed to center
    
    #customize_button_str='./imageAssets/CUSTOMIZE_BUTTON.png'

    #Here, we define the horizontal borders for buttons, from the top
    horizontal_borders=[float(Window.height)*(5./5.),float(Window.height)*(4./5.),
                        float(Window.height)*(3./5.),float(Window.height)*(2./5.),float(Window.height)*(1./5.),0.]
    #The vertical borders are there to limit the size of buttons. BUTTONS ARE ON THE LEFT HAND SIDE OF THESE BORDERS
    vertical_borders=[float(Window.width)*(1./2.),float(Window.width)*(1./2.),float(Window.width)*(1./2.),
                      float(Window.width)*(1./2.),float(Window.width)*(1./2.)]

    loading_points=[0,5,15,20,70,75,80,85,90,95,100];
    loading_bar_interval=0.001
    loading_increment=2.5
    
    def __init__(self,**kwargs):
        super(Menu,self).__init__(**kwargs)
        bg=cropFit(self.background,Window.width,Window.height,0,0)
        self.add_widget(bg)

        self.loading_bar()

    def create_menu_buttons(self):

        self.button_widget_list=[]
        for index in range(0,len(self.button_paths)):
            button=ratioFit(self.button_paths[index],self.vertical_borders[index],
                            self.horizontal_borders[index]-self.horizontal_borders[index+1])
            centering_widget(button,0,self.horizontal_borders[index+1],self.vertical_borders[index],
                             self.horizontal_borders[index]-self.horizontal_borders[index+1])
            self.button_widget_list.append(button)
            #self.add_widget(button)
            
    def display_buttons(self):
        for button in self.button_widget_list:
            self.add_widget(button)

    def create_pop_up(self):

        #THESE WILL BE WORKED ON IN THE FUTURE VERSION
        self.unavailable_feature_popUp=self.unvailable_feature_popUp_creator()
        #This is fine
        self.exit_popUp=self.are_you_sure_exit()

    def loading_point(self):
        self.loading_point_index+=1
        return self.loading_points[self.loading_point_index]

    def update_progress(self,next_stat,next_action,dt):
        current_stat=self.pb.value
        if current_stat>=next_stat or next_stat>self.pb.max:
            raise Exception('You have to specify next_stat between current_stat and max possible value')
        Clock.schedule_interval(self.update_progress_accessory,self.loading_bar_interval)
        self.next_stat=next_stat
        self.next_function=next_action

    def update_progress_accessory(self,dt):
        #To be accessed by update_progress method in the same class only
        self.pb.value+=self.loading_increment
        if self.pb.value<self.next_stat:
            return
        elif self.pb.value>self.next_stat:
            self.pb.value=self.next_stat
        Clock.unschedule(self.update_progress_accessory)
        Clock.schedule_once(self.next_function,0)


    def clear_init_instances(self):
        del self.pb
        del self.loading_point_index
        del self.next_stat
        del self.next_function
        del self.loading_bar

    def loading_bar(self):

        from kivy.uix.progressbar import ProgressBar
        self.loading_bar=Popup()
        self.loading_bar.auto_dismiss=False
        self.loading_bar.title='Initializing'
        self.loading_bar.size_hint=(0.8,0.2)
        self.pb=ProgressBar()
        self.pb.max=self.loading_points[-1]
        self.loading_bar.add_widget(self.pb)

        self.loading_point_index=0
        self.pb.value=self.loading_points[0]
        
    def unvailable_feature_popUp_creator(self):

        #I WILL MAKE THE FEATURES SIMPLE UNAVAILABLE FOR NOW

        myBox=BoxLayout()
        myBox.orientation='vertical'
        
        myLabel=Label()
        myLabel.text='This feature will be\navailable in future version'

        button=Button()
        button.text='Dismiss'
        button.size_hint_y=0.3

        myBox.add_widget(myLabel)
        myBox.add_widget(button)
        
        popUp=Popup()
        popUp.title='Feature not yet available'
        popUp.content=myBox
        popUp.size_hint=(0.8,0.5)

        button.bind(on_release=popUp.dismiss)

        return popUp

    def are_you_sure_exit(self):

        myBox=BoxLayout()
        myBox.orientation='vertical'
        
        myLabel=Label()
        myLabel.text='Are you sure\nyou wanna exit the game?'

        button=Button()
        button.text='No'
        button.size_hint_y=0.2

        button1=Button()
        button1.text='Yes'
        button1.size_hint_y=0.2

        bar=Widget()
        bar.size_hint_y=0.02

        myBox.add_widget(myLabel)
        myBox.add_widget(button1)
        myBox.add_widget(bar)
        myBox.add_widget(button)
        
        popUp=Popup()
        popUp.title='Exiting the game'
        popUp.content=myBox
        popUp.size_hint=(0.8,0.8)

        button.bind(on_release=popUp.dismiss)
        button1.bind(on_release=self.exit_application)

        return popUp

    def exit_application(self,instance):
        from kivy.app import App
        App.get_running_app().stop()

    def achievement_update(self):
        if JsonStore('highest_score.json').exists('highest_score0'):
            score=JsonStore('highest_score.json').get('highest_score0')['highest_score']
        else:
            score=0
        achievement='Stage 1: '+str(score)
        if score>=ArtInfo.max_score[0] and ArtInfo.max_score[0]!=None:
            achievement=achievement+' (Max reached)'
        for index in range(1,len(ArtInfo.fanpage_url)):
            what_to_get='highest_score'+str(index)
            if JsonStore('highest_score.json').exists(what_to_get):
                score=JsonStore('highest_score.json').get(what_to_get)['highest_score']
                achievement=achievement+'\nStage '+str(index+1)+': '+str(score)
                if score>=ArtInfo.max_score[index] and ArtInfo.max_score[index]!=None:
                    achievement=achievement+' (Max reached)'
            else:
                #THIS SHOULD BE UNNECESSARY. IT IS HERE FOR SAFETY REASON
                if not JsonStore('levelCacche.json').exists('level'):
                    JsonStore('levelCacche.json').put('level',level=0)
                myLevel=JsonStore('levelCacche.json').get('level')['level']
                if myLevel<index:
                    for index2 in range(index,len(ArtInfo.fanpage_url)):
                        achievement=achievement+'\nStage '+str(index2+1)+': Locked'
                    return achievement
                else: #THIS SHOULD NEVER BE CALLED IN THE APP
                    achievement=achievement+'\nStage '+str(index+1)+': 0'
        return achievement

    def achievement_popUp(self):
        #MUST BE CALLED AFTER CALLING self.achievement_update() above

        myBox=BoxLayout()
        myBox.orientation='vertical'
        
        myLabel=Label()
        myLabel.text=self.achievement_update()
        myLabel.size_hint_y=len(ArtInfo.fanpage_url)*0.07

        myScroll=ScrollView()
        myScroll.add_widget(myLabel)

        button=Button()
        button.text='Dismiss'
        button.size_hint_y=0.15

        myBox.add_widget(myScroll)
        myBox.add_widget(button)
        
        popUp=Popup()
        popUp.title='Highest scores'
        popUp.content=myBox
        popUp.size_hint=(0.9,0.8)

        button.bind(on_release=popUp.dismiss)

        popUp.open() 
