import kivy
kivy.require('1.7.2')


from kivy.config import Config
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '500')



from kivy.app import App
from kivy.uix.widget import Widget
#from kivy.core.window import Window

#from gameOn import GameOn
from menu import Menu

#from filePopup import FilePopup
#from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window

from customMenu import CustomMenu
from customGameOn import CustomGameOn

#from stageSelect import StageSelect
from kivy.storage.jsonstore import JsonStore

#from jnius import autoclass

#from cropImage import ratioFit
from kivy.utils import platform

#=
from cropImage import cropFit
#=

from artInfo import ArtInfo

from kivy.clock import Clock

from functools import partial

import webbrowser

displayAd=False

class Supreme(Widget):

    def __init__(self,**kwargs):
        super(Supreme,self).__init__(**kwargs)
        self.menu=Menu()
        self.add_widget(self.menu)

        Clock.schedule_once(self.initializing,0)

    def initializing(self,dt):
        self.menu.loading_bar.open()
        Clock.schedule_once(self.supreme_chain_1,0)
        
    def supreme_chain_1(self,dt):
        print('initializing')
        Clock.schedule_once(partial(self.menu.update_progress,\
                                    self.menu.loading_point(),self.supreme_chain_2),0)

    def supreme_chain_2(self,dt):
        print('GOOD')
        self.customMenu=CustomMenu(self)
        Clock.schedule_once(partial(self.menu.update_progress,\
                                    self.menu.loading_point(),self.customMenu.init1),0)

    def supreme_chain_3(self,dt):
        self.menu.create_pop_up()
        Clock.schedule_once(partial(self.menu.update_progress,\
                                    self.menu.loading_point(),self.supreme_chain_4),0)

    def supreme_chain_4(self,dt):
        self.menu.create_menu_buttons()
        self.gameList=[]
        for index in range(0,CustomMenu.customizableNumber):
            self.gameList.append(None)
        self.screen='menu'
        Clock.schedule_once(partial(self.menu.update_progress,\
                                    self.menu.loading_point(),self.supreme_chain_5),0)

    def supreme_chain_5(self,dt):
        self.menu.loading_bar.dismiss()
        self.menu.clear_init_instances()
        self.menu.display_buttons()
        self.customMenu.clear_init_instances()

    def last_stage(self):
        if not JsonStore('stageCacche.json').exists('current_stage'):
            print('hello people')
            JsonStore('stageCacche.json').put('current_stage',stage=0)
        else:
            print('loaded')
            self.customMenu.stage_readjust(JsonStore('stageCacche.json').get('current_stage')['stage'])
            self.customMenu.index=JsonStore('stageCacche.json').get('current_stage')['stage']
        self.customGameList=[]
        #---------------
        for i in range(0,CustomMenu.customizableNumber):
            self.customGameList.append(None)
        

    def on_touch_down(self,touch):
        if self.screen=='custom menu':
            self.customMenu.handle_on_touch_down(touch.x,touch.y)
        elif self.screen=='custom puzzle':
            self.customGameList[self.customMenu.index].handle_on_touch_down(touch.x,touch.y)
        super(Supreme, self).on_touch_down(touch) 
            
            
    def on_touch_move(self,touch):
        if self.screen=='custom menu':
            self.customMenu.handle_on_touch_move(touch.x)
        elif self.screen=='custom puzzle':
            self.customGameList[self.customMenu.index].handle_on_touch_move(touch.x,touch.y)
        super(Supreme, self).on_touch_down(touch) 

    def on_touch_up(self,touch):
        if self.screen=='menu':
            if self.menu.button_widget_list[0].collide_point(touch.x,touch.y):
                self.clear_widgets()
                #=============================
                #self.customMenu.update_level() #THIS THING MUST BE CALLED EVERYTIME CUSTOM MENU IS TURNED ON
                self.add_widget(self.customMenu)
                self.screen='custom menu'
                #=================================
            #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            #ALL OF THE FOLLOWING FEATURES WILL BE MADE AVAILABLE IN FUTURE VERSION
            elif self.menu.button_widget_list[1].collide_point(touch.x,touch.y):
                self.menu.achievement_popUp()
            elif self.menu.button_widget_list[2].collide_point(touch.x,touch.y):
                self.menu.unavailable_feature_popUp.open()
            elif self.menu.button_widget_list[3].collide_point(touch.x,touch.y):
                self.menu.unavailable_feature_popUp.open()
            #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            elif self.menu.button_widget_list[4].collide_point(touch.x,touch.y):
                self.menu.exit_popUp.open()
                
        elif self.screen=='custom menu':
            self.customMenu.handle_on_touch_up(touch.x)

        elif self.screen=='custom puzzle':
            
            if self.customGameList[self.customMenu.index].view_image_mode:
                self.customGameList[self.customMenu.index].exit_view_image()
                
            elif self.customGameList[self.customMenu.index].re_shuffle.collide_point(touch.x,touch.y):
                #self.customGameList[self.customMenu.index].re_shuffling()
                #=======-=----------============
                if self.customGameList[self.customMenu.index].timer_activate:
                    self.customGameList[self.customMenu.index].re_shuffling(self.customGameList[self.customMenu.index].difficulty)
                else:
                    self.customGameList[self.customMenu.index].re_shuffling()
                #=======-=----------============
                #==================================
                JsonStore('puzzledCacche.json').put(self.customSaveStr,arrangement=self.customGameList[self.customMenu.index].puzzle.tiles,
                                 blank=self.customGameList[self.customMenu.index].puzzle.blank)
                #====================================
                #print(self.customGameList[self.customMenu.index].puzzle.tiles)
                
            elif self.customGameList[self.customMenu.index].back_button.collide_point(touch.x,touch.y):

                if self.customGameList[self.customMenu.index].timer_activate: #=-=-=-=-=
                    self.customGameList[self.customMenu.index].handle_give_up()
                    return
                
                self.clear_widgets()
                self.customMenu.update_level()
                self.add_widget(self.customMenu)
                self.screen='custom menu'
                
            #THIS SEEMS SKETCHY. THIS WILL WORK ONLY IF PYTHON DOES NOT CHECK FOR SECOND STATEMENT IF FIRST STATEMENT IS TRUE
            elif self.customGameList[self.customMenu.index].artist!=None and self.customGameList[self.customMenu.index].art_promotion_bg.collide_point(touch.x,touch.y):
                if not self.customGameList[self.customMenu.index].timer_activate:
                    to_be_opened=ArtInfo.fanpage_url[self.customMenu.index]
                    if to_be_opened!=None:
                        webbrowser.open(to_be_opened)
                    else:
                            #POP UP IS GENERATED EVERYTIME. THIS IS VERY INEFFICIENT
                        self.customGameList[self.customMenu.index].artist_unavailable_popUp()
                return
                    
            elif self.customGameList[self.customMenu.index].start_timing.collide_point(touch.x,touch.y) and\
                 not self.customGameList[self.customMenu.index].timer_activate:
                print('pressing timeer')
                self.customGameList[self.customMenu.index].handle_start_timer()
            else:
                if self.customGameList[self.customMenu.index].update(touch.x,touch.y):
                    JsonStore('puzzledCacche.json').put(self.customSaveStr,arrangement=self.customGameList[self.customMenu.index].puzzle.tiles,
                                 blank=self.customGameList[self.customMenu.index].puzzle.blank)

        super(Supreme, self).on_touch_down(touch) 
                
                
        
class ClientApp(App):
    
    def build(self):
        self.child=Supreme()
        self.parent=Widget()
        self.parent.add_widget(self.child)
        return self.parent

    def show_file_options(self):
        self.parent.remove_widget(self.child)
        self.child.screen='selection'
        try:
            self.parent.add_widget(self.selection_screen)
        except:
            from customizeArt import CustomizeArt
            self.selection_screen=CustomizeArt(self)
            self.parent.add_widget(self.selection_screen)

    def make_selection(self,path):
        if path=='./imageAssets/puzzles/':
            path=path+str(self.child.customMenu.index+1)+'.jpg'
        try:
            self.child.customMenu._customize(path)
            self.turn_off_selection()
        except:
            self.selection_screen.default_display()
            self.selection_screen.invalid_selection()

    def turn_off_selection(self):
        self.parent.remove_widget(self.selection_screen)
        self.parent.add_widget(self.child)
        self.child.screen='custom menu'
    
    def on_start(self):
        #PERHAPS THIS CAN BE PLACED UP ABOVE SIMPLY
        print('my platfooooooooooorm is '+str(platform))
        if displayAd:
            pass
            AdBuddiz.setPublisherKey("TEST_PUBLISHER_KEY")

        if platform == 'android':
            import android
            android.map_key(android.KEYCODE_BACK, 1000)
            android.map_key(android.KEYCODE_MENU, 1001)
        win = self._app_window
        win.bind(on_keyboard=self._key_handler)
        
    def on_pause(self):
      # Here you can save data if needed
        return True

    def on_resume(self):
      # Here you can check if any data needs replacing (usually nothing)
        pass
    
    def _key_handler(self, *args):
        key = args[1]
        print(key)
        # 1000 is "back" on Android
        # 27 is "escape" on computers
        # 1001 is "menu" on Android
        if key in (1000, 27):
            #OBVIOUSLY,WHATEVER NEEDS TO BE DONE HERE
            if self.child.screen=='menu':
                print('exit here')
                self.child.menu.exit_popUp.open()
            elif self.child.screen=='custom menu':
                self.child.clear_widgets()
                self.child.add_widget(self.child.menu)
                self.child.screen='menu'
            elif self.child.screen=='custom puzzle':
                self.child.clear_widgets()
                self.child.add_widget(self.child.customMenu)
                self.child.customMenu.update_level() #MUST BE CALLED EVERYTIME CUSTOM MENU IS TURNED ON
                self.child.screen='custom menu'
                #-=-
                if self.child.customGameList[self.child.customMenu.index].timer_activate:
                    self.child.customGameList[self.child.customMenu.index].timer_activate='disrupted'
                    self.child.customGameList[self.child.customMenu.index].stop_timer()
            return True
        
        elif key == 1001 or key==49:
            return True


if __name__=='__main__':
    ClientApp().run()
