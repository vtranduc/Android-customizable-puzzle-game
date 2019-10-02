import kivy
kivy.require('1.7.2')

from kivy.uix.widget import Widget
from cropImage import ratioFit, cropFit
from kivy.core.window import Window

from kivy.storage.jsonstore import JsonStore
store = JsonStore('imageCacche.json')
level=JsonStore('levelCacche.json')

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from functools import partial
from customGameOn import CustomGameOn
from kivy.utils import platform

from artInfo import ArtInfo

#from main import Supreme
import time

#print(Supreme.defaultCustomPuzzle)


class CustomMenu(Widget):

    background='./imageAssets/sgegsgegsegs.jpg'
    preview_max_size=[Window.width*0.6,Window.height*0.6]
    preview_height=Window.height*0.35
    #======
    customizableNumber=len(ArtInfo.artist_names) #Must be at least 1
    #============================================================
    preview_min_space=Window.width*0.05
    frame_t=0.01
    animating_speed=1500
    max_speed=5000 #Max speed at which stage selection widget moves. Should be larger than animating speed
    if max_speed<animating_speed:
        max_speed=animating_speed
    swipe_resistance=1.5 #The higher, the harder it is to shift the image. 1 is normal. Must be positive
    shift_speed=Window.width
    lock_opacity=0.8
    lock_image='./imageAssets/locked.png'
    
    def __init__(self,Supreme_class,**kwargs):
        super(CustomMenu,self).__init__(**kwargs)
        self.supreme=Supreme_class

    def init1(self,dt):
        self.add_widget(cropFit(self.background,Window.width,Window.height,0,0))
        self.preview=Widget()
        self.orix=[]
        ori_mid=Window.width*0.5
        self.ori_mid=[ori_mid]
        if store.exists('custom0'):
            imageStr=store.get('custom0')['imageStr']
        else:
            imageStr='./imageAssets/puzzles/1.jpg' #Change image format here
        try:
            preview=ratioFit(imageStr,self.preview_max_size[0],self.preview_max_size[1])
        except:
            print('Image is missing!')
            path='./imageAssets/puzzles/1.jpg' #Change image format here
            store.put('custom0',imageStr=path)
            preview=ratioFit(path,self.preview_max_size[0],self.preview_max_size[1])
        xPos=(Window.width-preview.get_size()[0])/2
        self.orix.append(xPos)
        preview.setPos(xPos,self.preview_height)
        self.preview.add_widget(preview)
        self.preview_widget=[preview]
        self.space=self.preview_max_size[0]+self.preview_min_space
        xPos=(Window.width-self.preview_max_size[0])/2

        self.index=0 #This instance will be used for different purpose later

        try:
            self.loading_increment=float(self.supreme.menu.loading_points[self.supreme.menu.loading_point_index+2]-\
                                    self.supreme.menu.loading_points[self.supreme.menu.loading_point_index+1])/\
                                    float(self.customizableNumber-1)
            Clock.schedule_once(partial(self.supreme.menu.update_progress,\
                                    self.supreme.menu.loading_point(),partial(self.init2,ori_mid)),0)
        except:
            self.add_widget(self.preview)
            self.supreme.menu.loading_point()
            Clock.schedule_once(partial(self.supreme.menu.update_progress,\
                                        self.supreme.menu.loading_point(),self.init3),0)

    def init2(self,ori_mid,dt):

        self.index+=1
        ori_mid+=self.space
        self.ori_mid.append(ori_mid)
        tmpString='custom'+str(self.index)
        if store.exists(tmpString):
            imageStr=store.get(tmpString)['imageStr']
        else:
            imageStr='./imageAssets/puzzles/'+str(self.index+1)+'.jpg' #Change image format here
        try:
            preview=ratioFit(imageStr,self.preview_max_size[0],self.preview_max_size[1])
        except:
            print('Image is missing!')
            path='./imageAssets/puzzles/'+str(self.index+1)+'.jpg' #Change image format here
            store.put(tmpString,imageStr=path)
            preview=ratioFit(path,self.preview_max_size[0],self.preview_max_size[1])
        xPos=ori_mid-float(preview.get_size()[0])/2.
        self.orix.append(xPos)
        preview.setPos(xPos,self.preview_height)
        self.preview.add_widget(preview)
        self.preview_widget.append(preview)

        if self.index==self.customizableNumber-1:
            self.add_widget(self.preview)
            Clock.schedule_once(partial(self.supreme.menu.update_progress,\
                                        self.supreme.menu.loading_point(),self.init3),0)
        else:
            Clock.schedule_once(partial(self.supreme.menu.update_progress,\
                                    self.supreme.menu.loading_points[self.supreme.menu.loading_point_index]+\
                                        self.index*self.loading_increment,partial(self.init2,ori_mid)),0)

    def init3(self,dt):
        self.right_limit=Window.width-float(self.preview_widget[0].get_size()[0])/2.
        self.left_limit=-float(self.preview_widget[self.customizableNumber-1].get_size()[0])/2.
        self.preview_y_range=(self.preview_height,self.preview_height+self.preview_max_size[1])
        self.preview_clicked=False
        self.mid_x=Window.width/2.
        self.index=0
        self.animating=False
        self.postpone=[]
        self.selectedImageList=[]
        Clock.schedule_once(partial(self.supreme.menu.update_progress,\
                                    self.supreme.menu.loading_point(),self.init4),0)
        
    def init4(self,dt):
        if not level.exists('level'):
            level.put('level',level=0)
        self.current_level=current_level=level.get('level')['level']
        self.lock_preview_widget=[]
        self.lock_preview=Widget()
        for index in range(self.customizableNumber-1,level.get('level')['level'],-1):
            locking=cropFit(self.lock_image,self.preview_widget[index].get_size()[0],self.preview_widget[index].get_size()[1])
            locking.opacity=self.lock_opacity
            self.lock_preview_widget.append(locking)
            self.lock_preview.add_widget(locking)
        Clock.schedule_once(partial(self.supreme.menu.update_progress,
                                    self.supreme.menu.loading_point(),self.init5),0)
            

    def init5(self,dt):
            
        self.add_widget(self.lock_preview)
        self.lock_screen_adjust()
        for index in range(0,self.customizableNumber):
            self.postpone.append(False)
            self.selectedImageList.append('')
        self.extra_move=0
        Clock.schedule_once(partial(self.supreme.menu.update_progress,\
                                    self.supreme.menu.loading_point(),self.init_last_stage),0)

    def init_last_stage(self,dt):
        self.supreme.last_stage()
        self.add_widget(self.buttons_generator())
        Clock.schedule_once(partial(self.supreme.menu.update_progress,
                                    self.supreme.menu.loading_point(),self.supreme.supreme_chain_3),0)

    def clear_init_instances(self):
        #del self.supreme
        try:
            del self.loading_increment
        except:
            pass

    def buttons_generator(self):

        box=BoxLayout(orientation='vertical')
        box.size=(Window.width,self.preview_height)
        box.pos=(0,0)
        box.spacing=self.preview_height*0.02
        box.padding=[Window.width*0.2,self.preview_height*0.05,Window.width*0.2,self.preview_height*0.05]
        
        btn=Button(text='Stage Select')
        btn.bind(on_release=self.stage_select_btn)
        box.add_widget(btn)

        btn=Button(text='Customize')
        btn.bind(on_release=self.customize_btn)
        box.add_widget(btn)

        btn=Button(text='Return to menu')
        btn.bind(on_release=self.return_to_menu_btn)
        box.add_widget(btn)

        return box

    def stage_select_btn(self,instance):
        #=============================================================================================================================================
        #=============================================================================================================================================
        if JsonStore('levelCacche.json').get('level')['level']<self.index:
            try:
                self.locked_pop.open()
            except:
                self.locked_pop=self.locked_pop_up()
                self.locked_pop.open()
            return
        self.supreme.customSaveStr='custom'+str(self.index)
        if self.postpone[self.index]:
            self.postpone[self.index]=False
            try:
                saved=JsonStore('puzzledCacche.json').get(self.supreme.customSaveStr)
                self.supreme.customGameList[self.index]=CustomGameOn(self.selectedImageList[self.index],
                                                                    self.index,1,
                                                                    ArtInfo.splitter[self.index][0],
                                                                    ArtInfo.splitter[self.index][1],
                                                                    saved['arrangement'],saved['blank'])
            except:
                self.supreme.customGameList[self.index]=CustomGameOn(self.selectedImageList[self.index],
                                                                    self.index,1,
                                                                    ArtInfo.splitter[self.index][0],
                                                                    ArtInfo.splitter[self.index][1])
                JsonStore('puzzledCacche.json').put(self.supreme.customSaveStr,arrangement=self.supreme.customGameList[self.index].puzzle.tiles,
                         blank=self.supreme.customGameList[self.index].puzzle.blank)

        elif self.supreme.customGameList[self.index]==None:
            if JsonStore('puzzledCacche.json').exists(self.supreme.customSaveStr):
                saved=JsonStore('puzzledCacche.json').get(self.supreme.customSaveStr)
                self.supreme.customGameList[self.index]=CustomGameOn(JsonStore('imageCacche.json').get(self.supreme.customSaveStr)['imageStr'],
                                                                        self.index,1,
                                                                        ArtInfo.splitter[self.index][0],
                                                                        ArtInfo.splitter[self.index][1],
                                                                        saved['arrangement'],saved['blank'])
            elif JsonStore('imageCacche.json').exists(self.supreme.customSaveStr):
                image=JsonStore('imageCacche.json').get(self.supreme.customSaveStr)['imageStr']
                self.supreme.customGameList[self.index]=CustomGameOn(image,self.index,1,
                                                                    ArtInfo.splitter[self.index][0],
                                                                    ArtInfo.splitter[self.index][1])
            else:
                image_str='./imageAssets/puzzles/'+str(self.index+1)+'.jpg' #Change image format here
                self.supreme.customGameList[self.index]=CustomGameOn(image_str,self.index,1,
                                                                    ArtInfo.splitter[self.index][0],
                                                                    ArtInfo.splitter[self.index][1])
                if not JsonStore('imageCacche.json').exists(self.supreme.customSaveStr): 
                    JsonStore('imageCacche.json').put(self.supreme.customSaveStr,imageStr=image_str)
                                    
        self.supreme.screen='custom puzzle'  
        self.supreme.clear_widgets()
        self.supreme.add_widget(self.supreme.customGameList[self.index])

        if JsonStore('stageCacche.json').get('current_stage')['stage']!=self.index:
            if platform=='android':
                if not JsonStore('adCacche.json').exists('ad_count'):
                    JsonStore('adCacche.json').put('ad_count',ad_count=0)
                #THE FOLLOWING IN NOT NECESSARY IF THE GAME IS INITIALZED IN THIS TURN
                self.supreme.customGameList[self.index].ad_count=JsonStore('adCacche.json').get('ad_count')['ad_count']
            JsonStore('stageCacche.json').put('current_stage',stage=self.index)

        #=============================================================================================================================================
        #=============================================================================================================================================

    def customize_btn(self,instance):
        if JsonStore('levelCacche.json').get('level')['level']<self.index:
            try:
                self.locked_pop.open()
            except:
                self.locked_pop=self.locked_pop_up()
                self.locked_pop.open()
        else:
            from kivy.app import App #MAYBE IT CAN BE BETTER THE OTHER WAY?
            App.get_running_app().show_file_options()

    def return_to_menu_btn(self,instance):
        self.supreme.remove_widget(self)
        self.supreme.add_widget(self.supreme.menu)
        self.supreme.screen='menu'
        
    def handle_on_touch_move(self,x):
        if self.preview_clicked:
            displacement=x-self.touch_down
            current_x1=self.orix[0]+displacement
            if current_x1>=self.right_limit:
                return
            current_x=self.orix[self.customizableNumber-1]+displacement
            if current_x<=self.left_limit:
                return
            self.preview_widget[0].setPos(current_x1+self.extra_move,self.preview_height)
            self.preview_widget[self.customizableNumber-1].setPos(current_x+self.extra_move,self.preview_height)
            for index in range(1,self.customizableNumber-1):
                self.preview_widget[index].setPos(self.orix[index]+displacement+self.extra_move,self.preview_height) #=
            #=
            self.x_previous=self.x_current
            self.x_current=x
            self.t_previous=self.t_current
            self.t_current=time.time()
            #=
            self.lock_screen_adjust()

    def handle_on_touch_down(self,x,y):        
        if y>=self.preview_y_range[0] and y<=self.preview_y_range[1]:

            if self.animating:
                Clock.unschedule(self.animate)
                self.animating=False
                self.extra_move=self.preview_widget[0].pos[0]-self.orix[0]
                #return
            elif self.extra_move!=0:
                self.extra_move=0
            
            self.preview_clicked=True
            self.touch_down=x
            self.x_previous=x
            self.x_current=x
            self.t_current=time.time()

    def handle_on_touch_up(self,x):
        
        if self.preview_clicked:
            self.preview_clicked=False
            print('moving now')
            #=
            displacement=self.x_current-self.x_previous
            print(displacement)
            print('extra move='+str(self.extra_move))
            print('displacement='+str(displacement))
            if displacement==0.:

                if self.extra_move==0:
                
                    return
                
            print('where at')
            time_difference=self.t_current-self.t_previous
            if time_difference!=0:
                self.velocity=displacement/(self.t_current-self.t_previous)
            else:
                if displacement>0:
                    self.velocity=self.max_speed
                elif displacement<0:
                    self.velocity=-self.max_speed
                elif displacement==0:
                    self.velocity=0

            if abs(self.velocity)>self.max_speed:
                if self.velocity>0:
                    self.velocity=self.max_speed
                else:
                    self.velocity=-self.max_speed

            displacement2=x-self.touch_down+self.extra_move
            proximity=abs(displacement2+self.ori_mid[0]-self.mid_x)
            self.index=0
            for index in range(1,self.customizableNumber):
                compare=abs(displacement2+self.ori_mid[index]-self.mid_x)
                if compare>proximity:
                    break
                else:
                    proximity=compare
                    self.index=index
            
            if self.velocity>self.shift_speed and self.index>0:
                shift_count=int((self.velocity/self.shift_speed)/self.swipe_resistance)
                if self.index<shift_count:
                    shift_count=self.index
                self.index-=shift_count
            elif self.velocity<-self.shift_speed and self.index<self.customizableNumber-1:
                shift_count=int((-self.velocity/self.shift_speed)/self.swipe_resistance)
                shift_max=self.customizableNumber-self.index-1
                if shift_max<shift_count:
                    shift_count=shift_max
                self.index+=shift_count
                    
            for index in range(0,self.customizableNumber):
                self.ori_mid[index]=(index-self.index)*self.space+self.mid_x
                xPos=self.ori_mid[index]-self.preview_widget[index].get_size()[0]/2.
                self.orix[index]=xPos
            if not self.animating:
                z1=xPos-self.preview_widget[index].pos[0]
                if z1<0:
                    self.multiplier=-1
                elif z1>0:
                    self.multiplier=1
                elif z1==0:
                    return
            print('checke')
            indicator=self.multiplier*self.velocity
            if abs(self.velocity)>self.animating_speed and indicator>0:
                self.impose_accel=True
                self.stepped=0
                self.accel=(self.animating_speed**2-self.velocity**2)/((self.orix[0]-self.preview_widget[0].pos[0])*2)
            else:
                self.impose_accel=False
                
            if not self.animating:
                Clock.schedule_interval(self.animate,self.frame_t)
                self.animating=True
                self.start=time.time()
            self.lock_screen_adjust()

    def animate(self,dt):

        if self.impose_accel==False:
            current_time=time.time()
            distance=self.multiplier*self.animating_speed*(current_time-self.start)
            self.start=current_time #Placement will result in 1 extraneous move, but time will be more accurate
        else:
            t=time.time()-self.start
            distance=self.velocity*t+0.5*self.accel*(t**2.)-self.stepped
            if distance*self.velocity>0:
                self.stepped+=distance
            else: #If widget movement reverses direction due to accel, then we have to fix it
                print('WARNING: distance is reversing direction!')
                self.impose_accel=False
                distance=self.multiplier*self.animating_speed*self.frame_t
                self.start=time.time()

        self.preview_widget[0].setPos(self.preview_widget[0].pos[0]+distance,self.preview_height)
        if (self.multiplier==1 and self.preview_widget[0].pos[0]>=self.orix[0]) or (self.multiplier==-1 and self.preview_widget[0].pos[0]<=self.orix[0]):
            Clock.unschedule(self.animate)          
            self.animating=False
            for index in range(0,self.customizableNumber):
                self.preview_widget[index].setPos(self.orix[index],self.preview_height)
        else:
            for index in range(1,self.customizableNumber):
                self.preview_widget[index].setPos(self.preview_widget[index].pos[0]+distance,self.preview_height)

        self.lock_screen_adjust()

    def stage_readjust(self,stage):

        half_window=Window.width*0.5
        for index in range(0,len(self.preview_widget)):
            current_mid=(index-stage)*self.space+half_window
            self.ori_mid[index]=current_mid
            half_width=self.preview_widget[index].get_size()[0]*0.5
            xPos=current_mid-half_width
            self.orix[index]=xPos
            self.preview_widget[index].setPos(xPos,self.preview_height)
        self.lock_screen_adjust()

    def lock_screen_adjust(self):

        incrementing_index=-1
        for index in range(self.customizableNumber-1,self.customizableNumber-len(self.lock_preview_widget)-1,-1):
            incrementing_index+=1
            self.lock_preview_widget[incrementing_index].setPos(self.preview_widget[index].x,self.preview_widget[index].y)

    def update_level(self):
        if self.current_level<JsonStore('levelCacche.json').get('level')['level']:
            self.current_level+=1
            self.level_up()

    def level_up(self):

        if self.customizableNumber-1==self.index:
            return
        current_lv=level.get('level')['level']
        level.put('level',level=current_lv+1)
        index=len(self.lock_preview_widget)-1
        to_be_removed=self.lock_preview_widget[index]
        self.lock_preview.remove_widget(to_be_removed)
        self.lock_preview_widget.remove(to_be_removed)

        print('LEVELING UP!!!')

    def _customize(self,path):
        self.selectedImageList[self.index]=path
        self.postpone[self.index]=True
        string='custom'+str(self.index)
        store.put(string,imageStr=path)
        self.preview.remove_widget(self.preview_widget[self.index])
        tmpWidget=ratioFit(path,self.preview_max_size[0],self.preview_max_size[1])
        tmpWidget.setPos(self.mid_x-tmpWidget.get_size()[0]/2.,self.preview_height)
        self.orix[self.index]=tmpWidget.pos[0]
        self.ori_mid[self.index]=self.mid_x
        self.preview.add_widget(tmpWidget)
        self.preview_widget[self.index]=tmpWidget

    def locked_pop_up(self):
        #A LOT OF LITERAL

        from kivy.uix.label import Label

        myBox=BoxLayout()
        myBox.orientation='vertical'
        
        myLabel=Label()
        myLabel.text='Clear previous stage\nto unlock this level'
        myLabel.valign='middle'
        myLabel.halign='center'

        button=Button()
        button.text='Dismiss'
        button.size_hint_y=0.3

        myBox.add_widget(myLabel)
        myBox.add_widget(button)
        
        popUp=Popup()
        popUp.title='Level locked'
        popUp.content=myBox
        popUp.size_hint=(0.7,0.5)

        button.bind(on_release=popUp.dismiss)
        
        return popUp

#=====================================================================================
'''
import kivy
kivy.require('1.7.2')

from kivy.app import App

class ClientApp(App):
    
    def build(self):
        self.child=CustomMenu()
        parent=Widget()
        parent.add_widget(self.child)
        return parent

if __name__=='__main__':
    ClientApp().run()

'''
