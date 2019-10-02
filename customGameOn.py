import kivy
kivy.require('1.7.2')

from kivy.app import App

from kivy.uix.widget import Widget
from kivy.core.window import Window
from puzzleGeneration import PuzzleGeneration
from cropImage import CropImage, getSize, centering_widget
from kivy.clock import Clock
from cropImage import ratioFit, cropFit, centering_widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
from artInfo import ArtInfo
from kivy.utils import platform
import time
import webbrowser

#platform='hello workd'

if platform=="android":
    from jnius import autoclass
    PythonActivity=autoclass("org.renpy.android.PythonActivity")
    AdBuddiz=autoclass("com.purplebrain.adbuddiz.sdk.AdBuddiz")

class CustomGameOn(Widget):

    #edge=0.1
    #=====shuffle_count=20
    re_shuffle_button='./imageAssets/re_shuffle.png'
    #re_shuffle_size=(Window.width*0.2,Window.width*0.2)
    #re_shuffle_pos=(Window.width*0.01,Window.width*0.01)
    winStr='./imageAssets/You Win.png'
    winSize=(Window.width*0.8,Window.height*0.8)

    #backStr='./imageAssets/menu-back.png'
    backStr='./imageAssets/back_button.png'
    #backHeight=Window.height*0.25 #Manual. Note that aspect_ratio is maintained
    #Below, I set back-to-menu button to be right bottom corner
    #=====sec_per_move=1
    #game_over_image='./imageAssets/Psychrometric.png'
    start_timer_image='./imageAssets/start_button.png'
    timer_border_x=Window.width*0.02
    timer_border_y=Window.height*0.02
    first_difficulty=1

    #=-=-=-=-=-=-=-=-=-=-=-=-=-=
    animate_t=0.1
    frame_t=0.001
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=

    background='./imageAssets/wooden_background.jpg'

    puzzle_lower_boundary_y=Window.height*0.1
    puzzle_upper_boundary_y=Window.height*0.9

    button_border_x=Window.width*0.5

    fanpageStr='./imageAssets/artist_fanpage.png'

    scoreBoardStr='./imageAssets/plain_black.png'
    scoreBoardOpacity=0.6

    frameStr='./imageAssets/plain_black.png'
    frame_width=Window.width*0.01 #MUST NOT BE TOO SO THAT IT EXCEEDS THE FRAME OF THE WINDOW
    #THAT IS,self.puzzle_lower_boundary MUST BE LARGER THAN self.frame_width

    art_promotion_bg_str='./imageAssets/plain_black.png'
    art_promotion_min_vertical_border=Window.width*0.5
    art_promotion_opacity=0.85
    art_promo_border=Window.width*0.01
    #profileImage_spacing=Window.width*0.001

    ad_threshold=2 #Number of plays before showing ad
    ad_count_increment_no_timer=0.2
    ad_count_increment_timer=1

    flickr_profile='./imageAssets/gmCropped.png'
    
    def __init__(self,imageStr,puzzle_index,xy_ratio,xnum,ynum,*args,**kwargs):
        #args is there to specify the arrangement of the puzzle
        super(CustomGameOn,self).__init__(**kwargs)

        self.add_widget(cropFit(self.background,Window.width,Window.height,0,0))

        self.shuffle_count=ArtInfo.default_shuffling[puzzle_index]
        self.sec_per_move=ArtInfo.sec_per_move[puzzle_index]
        puzzleHeight=self.puzzle_upper_boundary_y-self.puzzle_lower_boundary_y
        xscale=(Window.width-2*self.frame_width)/xy_ratio
        yscale=puzzleHeight
        if xscale>yscale:
            print('case 1')
            actual_x=yscale*xy_ratio
            left_corner=(Window.width-actual_x)/2.
            bottom_corner=self.puzzle_lower_boundary_y
            self.piece_width=int(actual_x/ynum)
            self.piece_height=int(puzzleHeight/xnum)
        elif xscale<=yscale:
            print('case 2')
            left_corner=self.frame_width
            actual_y=xscale
            bottom_corner=self.puzzle_lower_boundary_y+(puzzleHeight-actual_y)/2.
            self.piece_width=int((Window.width-2*self.frame_width)/ynum)
            self.piece_height=int(actual_y/xnum)
        '''
        elif xscale==yscale:
            print('case 3')
            left_corner=self.frame_width
            bottom_corner=self.puzzle_lower_boundary_y
            self.piece_width=int((Window.width-2*self.frame_width)/ynum)
            self.piece_height=int(puzzleHeight/xnum)
        '''
        self.bottomleft=[left_corner,bottom_corner]

        frame=cropFit(self.frameStr,Window.width-(self.bottomleft[0]-self.frame_width)*2,
                      self.piece_height*xnum+2*self.frame_width,
                      self.bottomleft[0]-self.frame_width,
                      self.bottomleft[1]-self.frame_width)
        self.add_widget(frame)
        
        #self.bottomleft=[0,0]
        #===============================
        self.puzzle=PuzzleGeneration(xnum,ynum)

        if len(args)==0:
            self.puzzle.shuffle(self.shuffle_count)
        else:
            self.puzzle.tiles=args[0]
            self.puzzle.blank=args[1]

        self.xnum=xnum
        self.ynum=ynum
        self.action_list=[]
        for i in range(0,xnum):
            self.action_list.append([])
        self.blank=self.puzzle.blank
        self.imageStr=imageStr
        self.game_widget=Widget()
        self.setUp()
        self.add_widget(self.game_widget)

        half_space=self.button_border_x/2.
        
        self.back_button=ratioFit(self.backStr,half_space,self.puzzle_lower_boundary_y-self.frame_width)
        self.back_button.setPos(0,0)
        self.add_widget(self.back_button)

        self.re_shuffle=ratioFit(self.re_shuffle_button,half_space,self.puzzle_lower_boundary_y-self.frame_width)
        self.re_shuffle.setPos(self.back_button.get_size()[0],0)
        self.add_widget(self.re_shuffle)

        self.timer_activate=None
        #LITERAL BELOW
        print('testing out')
        '''
        print(Window.height-self.puzzle_upper_boundary_y-\
                                   self.frame_width-2*self.timer_border_y)
        print(Window.height)
        print(self.puzzle_upper_boundary_y)
        print(self.frame_width)
        print(self.timer_border)
        '''
        self.start_timing=ratioFit(self.start_timer_image,Window.width-\
                                   self.art_promotion_min_vertical_border-2*self.timer_border_x,
                                   Window.height-self.puzzle_upper_boundary_y-\
                                   self.frame_width-2*self.timer_border_y)
        #self.start_timing.setPos(0,Window.height-self.start_timing.get_size()[1])
        centering_widget(self.start_timing,self.art_promotion_min_vertical_border+self.timer_border_x,
                         self.puzzle_upper_boundary_y+self.frame_width+self.timer_border_y,
                         Window.width-\
                        self.art_promotion_min_vertical_border-2*self.timer_border_x,
                        Window.height-self.puzzle_upper_boundary_y-\
                        self.frame_width-2*self.timer_border_y)
        self.add_widget(self.start_timing)
        self.animating=False
        self.settlement=[]
        for i in range(0,xnum*ynum):
            self.settlement.append(True)
        print(self.settlement)
        self.v_x=float(self.piece_width)/float(self.animate_t)
        self.v_y=float(self.piece_height)/float(self.animate_t)

        if JsonStore('highest_score.json').exists('highest_score'+str(puzzle_index)):
            self.highest_score=JsonStore('highest_score.json').get('highest_score'+str(puzzle_index))['highest_score']
        else:
            JsonStore('highest_score.json').put('highest_score'+str(puzzle_index),highest_score=0)
            self.highest_score=0

        if puzzle_index==JsonStore('levelCacche.json').get('level')['level'] and puzzle_index+1!=len(ArtInfo.artist_names):
            self.critical=True
            self.goal=ArtInfo.goal[puzzle_index]
        else:
            self.critical=False
        self.artist=ArtInfo.artist_names[puzzle_index]
        self.url=ArtInfo.fanpage_url[puzzle_index]
        self.view_art_popUp=self.view_art_popUp()
        self.black=cropFit('./imageAssets/plain_black.png',Window.width,Window.height,0,0)
        self.full_image=ratioFit(imageStr,Window.width,Window.height)
        centering_widget(self.full_image,0,0,Window.width,Window.height)
        self.view_image_mode=False

        if self.artist!=None:

            if self.artist=='flickr':
                print('oh no!')
                flickr=True
            else:
                flickr=False
            
            self.art_promotion_bg=cropFit(self.art_promotion_bg_str,
                                          self.art_promotion_min_vertical_border-2*self.art_promo_border,
                                       Window.height-(self.puzzle_upper_boundary_y+self.frame_width)\
                                          -2*self.art_promo_border,
                                          self.art_promo_border,
                                       self.puzzle_upper_boundary_y+self.frame_width+self.art_promo_border)
            self.add_widget(self.art_promotion_bg)
            self.art_promotion_bg.opacity=self.art_promotion_opacity

            if flickr:
                profileStr=self.flickr_profile
            else:
                profileStr='./imageAssets/artists/'+self.artist+'.jpg' #=
            #from kivy.uix.image import Image
            #profile=Image(source=profileStr)
            self.profile=cropFit(profileStr,self.art_promotion_bg.size[1],self.art_promotion_bg.size[1],
                            self.art_promotion_bg.pos[0],self.art_promotion_bg.pos[1])
            self.add_widget(self.profile)

            self.art_promotion=BoxLayout()
            self.art_promotion.size=(self.art_promotion_bg.size[0]-self.profile.size[0],self.art_promotion_bg.size[1])
            self.art_promotion.pos=(self.art_promotion_bg.pos[0]+self.profile.size[0],self.art_promotion_bg.pos[1])
            self.art_promotion.orientation='horizontal'
            #profile.pos=self.art_promotion_bg.pos
            #profile.
            #profile=CropImage(profileStr)
            myArtist=Label()
            if flickr:
                myArtist.text='License from\nflickr'
            else:
                myArtist.text='Art by\n'+self.artist #=
            #myArtist.size_hint=(0.8,1)
            #self.art_promotion.add_widget(profile)
            self.art_promotion.add_widget(myArtist)
            self.add_widget(self.art_promotion)

        self.puzzle_index=puzzle_index

        self.touch_down=False

        self.disrupt_popUp=self.disrupt_game_popUp()
        self.disrupt_opened=False

        if self.critical:
            self.goal_popUp=self.state_goal_popUp()
        if ArtInfo.max_score[puzzle_index]!=None:
            self.max_reached_popUp=self.max_score_reached_popUp()

        #===========
        #if platform=='android':
        #REMEMBER SELF.AD_THRESHOLD HERE
        if platform=='android':
            if JsonStore('adCacche.json').exists('ad_count'):
                self.ad_count=JsonStore('adCacche.json').get('ad_count')['ad_count']
            else:
                print('PLEASE PLEASE NO')
                self.ad_count=0
                JsonStore('adCacche.json').put('ad_count',ad_count=0)
            AdBuddiz.setPublisherKey("d64d50d6-b371-4516-abe8-22887ea236b5") #replace the key with your app Key
            #AdBuddiz.setTestModeActive() #test mode will be active
            AdBuddiz.cacheAds(PythonActivity.mActivity) #now we are caching the ads 
        #===========

    def show_ad(self):
        #THIS MUST BE CALLED ONLY WHEN PLATFORM=='ANDROID'
        print('BUILD THAT WALL')
        AdBuddiz.showAd(PythonActivity.mActivity) #let's show the ad ;)

    def setUp(self):

        #When changing xnum and ynum, if cacche is not cleared properly, error may result
        splitTiles=self.customPuzzle()
        yAbsPos=self.bottomleft[1]-self.piece_height
        for i in range(self.xnum-1,-1,-1):
            xAbsPos=self.bottomleft[0]-self.piece_width
            yAbsPos+=self.piece_height
            for j in range(0,self.ynum):
                number=self.puzzle.tiles[i][j]
                subtractor=(number+1)%self.ynum
                if subtractor==0:
                    subtractor=self.ynum
                index=(int(number/self.ynum)+1)*self.ynum-subtractor
                xAbsPos+=self.piece_width
                splitTiles[index].setPos(xAbsPos,yAbsPos)
                self.game_widget.add_widget(splitTiles[index])
                self.action_list[i].append(splitTiles[index])

    def update(self,touchx,touchy):

        if self.touch_down!=False:
            i=self.touch_down[5]
            j=self.touch_down[6]

            #self.touch_down=[1,self.action_list[i][j].pos[0],self.action_list[i][j].pos[1],x,y,i,j]

            if self.touch_down[0]==1:
                y_dist=touchy-self.touch_down[4]
                yPos=self.touch_down[2]+y_dist
                if yPos<self.touch_down[8]:
                    self.action_list[i][j].setPos(self.touch_down[7],self.touch_down[8])
                    self.touch_down=False
                    return False
            elif self.touch_down[0]==2:
                y_dist=touchy-self.touch_down[4]
                yPos=self.touch_down[2]+y_dist
                if yPos>self.touch_down[8]:
                    self.action_list[i][j].setPos(self.touch_down[7],self.touch_down[8])
                    self.touch_down=False
                    return False
            elif self.touch_down[0]==3:
                x_dist=touchx-self.touch_down[3]
                xPos=self.touch_down[1]+x_dist
                if xPos<self.touch_down[7]:
                    print('aloha 1')
                    self.action_list[i][j].setPos(self.touch_down[7],self.touch_down[8])
                    self.touch_down=False
                    return False
            elif self.touch_down[0]==4:
                x_dist=touchx-self.touch_down[3]
                print(x_dist)
                xPos=self.touch_down[1]+x_dist
                print(xPos)
                print(self.touch_down[7])
                print([self.frame_width,self.frame_width+self.piece_width,self.frame_width+self.piece_width*2,self.frame_width+self.piece_width*3])
                if xPos>self.touch_down[7]:
                    print('aloha 2')
                    self.action_list[i][j].setPos(self.touch_down[7],self.touch_down[8])
                    self.touch_down=False
                    return False

        #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            index=self.puzzle.tiles[i][j]

            '''
            if self.settlement[index]!=True:
                clicked_widget_pos=[self.settlement[index][1],self.settlement[index][2]]
            else:
                clicked_widget_pos=[self.touch_down[1],self.touch_down[2]]
            '''
            clicked_widget_pos=[self.touch_down[7],self.touch_down[8]]
            
                        
            blank_widget=self.action_list[self.blank[0]][self.blank[1]]
            clicked_widget=self.action_list[i][j]
            self.animate(clicked_widget,self.puzzle.tiles[i][j],blank_widget.pos[0],blank_widget.pos[1])
            self.animating=True
            self.action_list[self.blank[0]][self.blank[1]].setPos(clicked_widget_pos[0],clicked_widget_pos[1])
            self.action_list[i][j]=blank_widget
            self.action_list[self.blank[0]][self.blank[1]]=clicked_widget
            self.blank=[i,j]
            self.puzzle.tiles[self.puzzle.blank[0]][self.puzzle.blank[1]]=self.puzzle.tiles[i][j]
            self.puzzle.tiles[i][j]=0
            self.puzzle.blank=[i,j]

            if self.puzzle.finish():
                if self.timer_activate:
                    self.score+=1
                    if self.difficulty<100: #LITERAL
                        self.difficulty+=1
                    self.re_shuffling(self.difficulty)
                    self.remaining_time=self.sec_per_move*self.difficulty
                    self.score_display.text='Current Score: '+str(self.score)
                    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                    if ArtInfo.max_score[self.puzzle_index]==self.score:
                        self.max_reached_popUp.open()
                        self.stop_timer()

                        if self.score>self.highest_score:
                            JsonStore('highest_score.json').put('highest_score'+str(self.puzzle_index),highest_score=self.score)
                            self.highest_score=self.score
                    #==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                else:
                                #self.win_message()
                    self.view_art_popUp.open()

                    if platform=='android':
                        self.ad_count+=self.ad_count_increment_no_timer
                        JsonStore('adCacche.json').put('ad_count',ad_count=self.ad_count)
                    print('adding '+str(self.ad_count_increment_no_timer))
                    
            self.touch_down=False
            print('Moved using touch_down')
            return True


        #=========================================================The following might be unnecessary
        
        for i in range(0,self.xnum):
            for j in range(0,self.ynum):
                if self.action_list[i][j].collide_point(touchx,touchy):
      
                    if (abs(i-self.blank[0])==1 and abs(j-self.blank[1])==0) or (abs(i-self.blank[0])==0 and abs(j-self.blank[1])==1):
      
                        index=self.puzzle.tiles[i][j]
                        if self.settlement[index]!=True:
                            clicked_widget_pos=[self.settlement[index][1],self.settlement[index][2]]
                        else:
                            clicked_widget_pos=[self.action_list[i][j].pos[0],self.action_list[i][j].pos[1]]
                        
                        blank_widget=self.action_list[self.blank[0]][self.blank[1]]
                        clicked_widget=self.action_list[i][j]
                        self.animate(clicked_widget,self.puzzle.tiles[i][j],blank_widget.pos[0],blank_widget.pos[1])
                        self.animating=True
                        self.action_list[self.blank[0]][self.blank[1]].setPos(clicked_widget_pos[0],clicked_widget_pos[1])
                        self.action_list[i][j]=blank_widget
                        self.action_list[self.blank[0]][self.blank[1]]=clicked_widget
                        self.blank=[i,j]
                        self.puzzle.tiles[self.puzzle.blank[0]][self.puzzle.blank[1]]=self.puzzle.tiles[i][j]
                        self.puzzle.tiles[i][j]=0
                        self.puzzle.blank=[i,j]

                        if self.puzzle.finish():
                            if self.timer_activate:
                                self.score+=1
                                if self.difficulty<100: #LITERAL
                                    self.difficulty+=1
                                self.re_shuffling(self.difficulty)
                                self.remaining_time=self.sec_per_move*self.difficulty
                                self.score_display.text='Current Score: '+str(self.score)
                                #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                                if ArtInfo.max_score[self.puzzle_index]==self.score:
                                    self.max_reached_popUp.open()
                                    self.stop_timer()

                                    if self.score>self.highest_score:
                                        JsonStore('highest_score.json').put('highest_score'+str(self.puzzle_index),highest_score=self.score)
                                        self.highest_score=self.score
        
                            #==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                            else:
                                #self.win_message()
                                self.view_art_popUp.open()
                                
                                #ooooooooooooooo
                                if platform=='android':
                                    self.ad_count+=self.ad_count_increment_no_timer
                                    JsonStore('adCacche.json').put('ad_count',ad_count=self.ad_count)
                                print('adding '+str(self.ad_count_increment_no_timer))

                        return True
                    return False
        return False

    #=-=-=-=-=-=-=-=-=-=-=
    def handle_on_touch_down(self,x,y):

        if self.touch_down!=False:
            self.action_list[self.touch_down[5]][self.touch_down[6]].setPos(self.touch_down[1],self.touch_down[2])
            self.touch_down=False
        
        for i in range(0,self.xnum):
            for j in range(0,self.ynum):
                if self.action_list[i][j].collide_point(x,y):
                    if (abs(i-self.blank[0])==1 and abs(j-self.blank[1])==0) or (abs(i-self.blank[0])==0 and abs(j-self.blank[1])==1):
                        #self.touch_down: 1: up; 2: down; 3: right; 4: left
                        if i-self.blank[0]==1:
                            self.touch_down=[1,self.action_list[i][j].pos[0],self.action_list[i][j].pos[1],x,y,i,j]
                        elif i-self.blank[0]==-1:
                            self.touch_down=[2,self.action_list[i][j].pos[0],self.action_list[i][j].pos[1],x,y,i,j]
                        elif j-self.blank[1]==-1:
                            self.touch_down=[3,self.action_list[i][j].pos[0],self.action_list[i][j].pos[1],x,y,i,j]
                        elif j-self.blank[1]==1:
                            self.touch_down=[4,self.action_list[i][j].pos[0],self.action_list[i][j].pos[1],x,y,i,j]
                            
                        index=self.puzzle.tiles[i][j]
                        if self.settlement[index]!=True:
                            print(self.touch_down)
                            print(self.settlement)
                            print('my settlement is')
                            self.touch_down.append(self.settlement[index][1])
                            self.touch_down.append(self.settlement[index][2])
                            self.settlement[index]=True
                            '''
                            if self.touch_down[1]!=self.touch_down[7] and self.touch_down[2]!=self.touch_down[8]:
                                if self.touch_down[0]==1 or self.touch_down[0]==2:
                                    des_y=self.action_list[self.blank[0]][self.blank[1]].pos[1]
                                    shift=(self.touch_down[7]-self.touch_down[1])/(des_y-self.touch_down[2])
                                    self.touch_down.append(shift)
                            '''
                                    
                        else:
                            self.touch_down.append(self.action_list[i][j].pos[0])
                            self.touch_down.append(self.action_list[i][j].pos[1])                      
                    return

    def handle_on_touch_move(self,x,y):

        #THIS IS NOT ALLOWING SMOOTH DIAGONAL MOVE ATM
        
        if self.touch_down==False:
            return

        #self.touch_down=[1,self.action_list[i][j].pos[0],self.action_list[i][j].pos[1],x,y,i,j]
        if self.touch_down[0]==1:
            print('case up')
            y_dist=y-self.touch_down[4]
            yPos=self.touch_down[2]+y_dist
            if yPos>self.touch_down[8]+self.piece_height or yPos<self.touch_down[8]:
                return
            self.action_list[self.touch_down[5]][self.touch_down[6]].setPos(self.touch_down[7],yPos)
        elif self.touch_down[0]==2:
            print('case down')
            y_dist=y-self.touch_down[4]
            yPos=self.touch_down[2]+y_dist
            if yPos<self.touch_down[8]-self.piece_height or yPos>self.touch_down[8]:
                return
            self.action_list[self.touch_down[5]][self.touch_down[6]].setPos(self.touch_down[7],yPos)
        elif self.touch_down[0]==3:
            x_dist=x-self.touch_down[3]
            xPos=self.touch_down[1]+x_dist
            if xPos<self.touch_down[7] or xPos>self.touch_down[7]+self.piece_width:
                return
            self.action_list[self.touch_down[5]][self.touch_down[6]].setPos(xPos,self.touch_down[8])
        elif self.touch_down[0]==4:
            x_dist=x-self.touch_down[3]
            xPos=self.touch_down[1]+x_dist
            if xPos>self.touch_down[7] or xPos<self.touch_down[7]-self.piece_width:
                return
            self.action_list[self.touch_down[5]][self.touch_down[6]].setPos(xPos,self.touch_down[8])
    
    def animate(self,widget,index,x,y):

        self.settlement[index]=[widget,x,y]
        if not self.animating:
            self.start_t=time.time()
            Clock.schedule_interval(self.animate_block,self.frame_t)

    def animate_block(self,dt):

        index=-1
        check_settlement=False
        elapsed=time.time()-self.start_t
        self.start_t=time.time()
        for settled in self.settlement:
            index+=1
            if settled!=True:
                move_widget=settled[0]
                des_x=settled[1]
                des_y=settled[2]
                xDir=des_x-move_widget.pos[0]
                if xDir>0.:
                    move_x=self.v_x*elapsed
                elif xDir<0.:
                    move_x=-self.v_x*elapsed
                else:
                    move_x=0.
                yDir=des_y-move_widget.pos[1]
                if yDir>0.:
                    move_y=self.v_y*elapsed
                elif yDir<0.:
                    move_y=-self.v_y*elapsed
                else:
                    move_y=0.
                move_widget.setPos(move_widget.pos[0]+move_x,move_widget.pos[1]+move_y)
                stop_x=False
                stop_y=False
                
                if (xDir>=0. and move_widget.pos[0]>=des_x) or (xDir<=0. and move_widget.pos[0]<=des_x):
                    move_widget.setPos(des_x,move_widget.pos[1])
                    stop_x=True
                if (yDir>=0. and move_widget.pos[1]>=des_y) or (yDir<=0. and move_widget.pos[1]<=des_y):
                    move_widget.setPos(move_widget.pos[0],des_y)
                    stop_y=True
                    
                if stop_x and stop_y:
                    self.settlement[index]=True
                    check_settlement=True
        if check_settlement:
            for settled in self.settlement:
                if settled!=True:
                    return
            Clock.unschedule(self.animate_block)
            self.animating=False
        print('animating')

    def customPuzzle(self):
        
        size=getSize(self.imageStr)
        totalWidth=self.piece_width*self.ynum
        totalHeight=self.piece_height*self.xnum
        xScale=float(totalWidth)/float(size[0])
        yScale=float(totalHeight)/float(size[1])
        if xScale>=yScale:
            scale=xScale
            posxRatio=0
            posyRatio=(1-totalHeight/(size[1]*scale))/2
        elif xScale<yScale:
            scale=yScale
            posxRatio=(1-totalWidth/(size[0]*scale))/2
            posyRatio=0
        widthRatio=self.piece_width/(size[0]*scale)
        heightRatio=self.piece_height/(size[1]*scale)
        widgetList=[]
        xPosCrop=posxRatio-widthRatio
        yPosCrop=posyRatio
        columnNumber=0
        for i in range(0,self.xnum*self.ynum):
            xPosCrop+=widthRatio
            columnNumber+=1
            tmpWidget=CropImage(self.imageStr,xPosCrop,yPosCrop,widthRatio,heightRatio)
            tmpWidget.scale(scale)
            if columnNumber==self.ynum:
                xPosCrop=posxRatio-widthRatio
                yPosCrop+=heightRatio
                columnNumber=0
            widgetList.append(tmpWidget)

        #=========================
        #THIS IS UGLY. FIX LATER. SHOULD BE INCORPORATED INTO THE FOR LOOP ABOVE
        widgetList[self.ynum-1]=CropImage('./imageAssets/blank_square.png',0,0,1,1)
        widgetList[self.ynum-1].setSize(self.piece_width,self.piece_height)
        
        #=========================
        return widgetList

    def re_shuffling(self,*args):
        #Optionally, you can specify shuffle count, essentially difficulty
        
        self.puzzle=PuzzleGeneration(self.xnum,self.ynum)
        #======================
        if len(args)==0:
            self.puzzle.shuffle(self.shuffle_count)
        else:
            self.puzzle.shuffle(args[0])

        #============================
        self.blank=self.puzzle.blank
        self.action_list=[]
        for i in range(0,self.xnum):
            self.action_list.append([])
        self.game_widget.clear_widgets()
        self.setUp()

    '''
    def win_message(self):
        
        self.add_widget(self.win_widget)
        self.win=True
    '''

    def add_clock(self):


        if self.timer_activate==False: #MAYBE I CAN JUST MAKE THIS ==FALSE, AND ERASE IF LOOP BELOW
            print('mit timer')
            print(self.timer_activate)
            self.difficulty=self.first_difficulty
            self.remaining_time=self.sec_per_move*self.difficulty
            #self.remove_widget(self.game_over)
            self.re_shuffling(self.difficulty)
            self.timer.text='Remaining time: '+str(self.remaining_time)+' seconds'
            Clock.schedule_interval(self.count_down,1)
            self.win=None
            self.score=0
            self.score_display.text='Current Score: '+str(self.score)
            self.timer_activate=True

            self.remove_widget(self.start_timing)
            self.add_widget(self.score_board)
            '''
            self.add_widget(self.score_display)
            self.add_widget(self.timer)
            print('Non-virgin')
            '''
            self.add_widget(self.timer_score)
            
            self.remove_fanpage()
            
            return
            #======== TO BE DELETED! I DO NOT UNDERSTAND WHEN SELF.TIME_ACTIVATE IS TRUE
            #MAYVE IT'S TRUE WHEN THE GAME IS OVER THEN RESTARTED? CUZ THE SCORE DOES NOT RESET!!! FIX THIS WHEN YOU SEE IT
            '''
            if self.timer_activate:
                while True:
                    print('ERROR: self.timer_activate is True here!')
            '''
            #========================
        '''
        if self.timer_activate==False:
                #self.remove_widget(self.start_timing)
                #self.add_widget(self.score_display)
                #self.add_widget(self.timer)
                #=-=-=-=-=-THIS SHOULD BE PLACED JUST UP THERE, OUTSIDE IF LOOP
                #self.score=0
                #self.score_display.text='Current Score: '+str(self.score)
                #=-=-=-=-=-=-=-=
                #self.add_widget(self.score_display)
                #self.timer_activate=True
            self.remove_widget(self.score_board)
            self.add_widget(self.start_timing)
            print('faulting')
            return
        '''

        self.score_board=cropFit(self.scoreBoardStr,Window.width,Window.height-self.puzzle_upper_boundary_y-self.frame_width,0,self.puzzle_upper_boundary_y+self.frame_width)
        self.score_board.opacity=self.scoreBoardOpacity
        self.add_widget(self.score_board)
            
        #from kivy.uix.label import Label
        self.difficulty=self.first_difficulty
        self.remaining_time=self.sec_per_move*self.difficulty
        
        self.timer=Label()
        self.timer.text='Remaining time: '+str(self.remaining_time)+' seconds'
        '''
        self.timer.size=(Window.width,Window.height*0.07) #LITERAL
        self.timer.pos=0,Window.height-self.timer.size[1]
        self.timer.font_size=Window.width*0.05 #LITERAL
        '''
        
        self.timer_activate=True
        #self.add_widget(self.timer)
        Clock.schedule_interval(self.count_down,1)
        
        self.remove_widget(self.start_timing)
        #=
        #self.game_over=ratioFit(self.game_over_image,Window.width,Window.height,0,0)
        
        self.score=0
        
        self.score_display=Label()
        self.score_display.text='Current Score: '+str(self.score)
        '''
        self.score_display.size=self.timer.size
        self.score_display.font_size=self.timer.font_size
        self.score_display.pos=0,Window.height-2*self.timer.size[1]
        '''

        self.timer_score=BoxLayout()
        self.timer_score.size=self.score_board.size
        self.timer_score.pos=self.score_board.pos
        self.timer_score.orientation='vertical'
        '''
        self.timer_score.add_widget(self.timer)
        self.timer_score.add_widget(self.score_display)
        '''
        self.timer_score.add_widget(self.timer)
        self.timer_score.add_widget(self.score_display)
        self.add_widget(self.timer_score)
        
        
        self.re_shuffling(self.difficulty)

        self.remove_fanpage()


    def reset_timer(self,instance):
        
        #To be called when game_over screen is displayed
        self.game_over_message_popUp.dismiss()
        self.win=None
        #self.remove_widget(self.game_over)
        self.remove_widget(self.score_board)
        self.add_fanpage()
        '''
        self.remove_widget(self.timer)
        self.remove_widget(self.score_display)
        '''
        self.remove_widget(self.timer_score)
        self.add_widget(self.start_timing)

        #oooooooooooooooooooooooooooooooooooooooooooooooooooooooo
        if platform=='android':
            self.ad_count+=self.ad_count_increment_timer
            JsonStore('adCacche.json').put('ad_count',ad_count=self.ad_count)
        print('I have added '+str(self.ad_count_increment_timer))
        
        if self.critical:
            if self.goal<=self.score:
                self.critical=False
                self.level_unlocked_popUp()
                current_lv=JsonStore('levelCacche.json').get('level')['level']
                JsonStore('levelCacche.json').put('level',level=current_lv+1)
                return
        if platform=='android':
            if self.ad_count>=self.ad_threshold:
                self.show_ad()
                self.ad_count=0
                JsonStore('adCacche.json').put('ad_count',ad_count=0)
        print('showing ad here')
        
    def count_down(self,dt):
        self.remaining_time-=1
        self.timer.text='Remaining time: '+str(self.remaining_time)+' seconds'
            
        if self.remaining_time==0:
            #Clock.unschedule(self.count_down)
            #self.add_widget(self.game_over)
            self.win=False
            self.stop_timer()

            if self.score>self.highest_score:
                JsonStore('highest_score.json').put('highest_score'+str(self.puzzle_index),highest_score=self.score)
                self.highest_score=self.score

            if self.disrupt_opened:
                self.disrupt_opened=False
                self.disrupt_popUp.dismiss()

            self.game_over_popUp()
            #self.game_over_popUp.open()
            
    def stop_timer(self):


        if self.timer_activate==True:
            self.timer_activate=False
            Clock.unschedule(self.count_down)
            print('systematic love')
            return

        
        #Can be called only after timer is activated
        Clock.unschedule(self.count_down)
        self.timer_activate=False
        #LITERAL BELOW
        #self.start_timing=ratioFit(self.start_timer_image,Window.width,Window.height*0.15)
        #self.start_timing.setPos(0,Window.height-self.start_timing.get_size()[1])
        self.add_widget(self.start_timing)
        '''
        self.remove_widget(self.score_display)
        self.remove_widget(self.timer)
        '''
        self.remove_widget(self.timer_score)
        self.remove_widget(self.score_board)
        self.add_fanpage()

        
        #self.add_fanpage()

    def game_over_popUp(self):

        myBox=BoxLayout()
        myBox.orientation='vertical'

        myLabel=Label()
        myLabel.text='Your score: '+str(self.score)+'\nHighest score: '+str(self.highest_score)
        if self.critical:
            myLabel.text=myLabel.text+'\nYou must score at least '+str(self.goal)+'\nto unlock next level'

        button=Button()
        button.text='Ok'
        button.size_hint_y=0.3

        myBox.add_widget(myLabel)
        myBox.add_widget(button)
        
        popUp=Popup()
        popUp.title='Result: Level '+str(self.puzzle_index+1)
        popUp.content=myBox
        popUp.size_hint=(0.8,0.5)
        popUp.auto_dismiss=False

        button.bind(on_release=self.reset_timer)

        self.game_over_message_popUp=popUp
        self.game_over_message_popUp.open()


    def artist_unavailable_popUp(self):

        #MOVE THESE TO SOMEWHERE BETTER
        
        myBox=BoxLayout()
        myBox.orientation='vertical'
        
        myLabel=Label()
        myLabel.text='Artist fanpage is\nunavailable at this time'

        button=Button()
        button.text='Dismiss'
        button.size_hint_y=0.3

        myBox.add_widget(myLabel)
        myBox.add_widget(button)
        
        popUp=Popup()
        popUp.title='Level locked'
        popUp.content=myBox
        popUp.size_hint=(0.5,0.5)
        popUp.auto_dismiss=False

        button.bind(on_release=popUp.dismiss)

        popUp.open()

    def level_unlocked_popUp(self):

        #MOVE THESE TO SOMEWHERE BETTER
        
        myBox=BoxLayout()
        myBox.orientation='vertical'
        
        myLabel=Label()
        myLabel.text='Goal has been achieved!\nNew stage is now unlocked!'

        button=Button()
        button.text='Dismiss'
        button.size_hint_y=0.3

        myBox.add_widget(myLabel)
        myBox.add_widget(button)
        
        self.unlockpopUp=Popup()
        self.unlockpopUp.title='New Level Unlocked!'
        self.unlockpopUp.content=myBox
        self.unlockpopUp.size_hint=(0.8,0.5)
        self.unlockpopUp.auto_dismiss=False

        button.bind(on_release=self.level_unlocked_press)

        self.unlockpopUp.open()

    def level_unlocked_press(self,instance):
        self.unlockpopUp.dismiss()
        if platform=='android':
            if self.ad_count>=self.ad_threshold:
                self.show_ad()
                self.ad_count=0
                JsonStore('adCacche.json').put('ad_count',ad_count=0)
        print('showing ad again')
        

    def handle_give_up(self):
        #self.stop_timer()
        self.disrupt_popUp.open()
        self.disrupt_opened=True
        

    def disrupt_yes(self,instance):
        self.stop_timer()
        self.disrupt_popUp.dismiss()
        self.disrupt_opened=False
        if self.score>self.highest_score:
            JsonStore('highest_score.json').put('highest_score'+str(self.puzzle_index),highest_score=self.score)
            self.highest_score=self.score
        self.game_over_popUp()

    def disrupt_no(self,instance):
        self.disrupt_popUp.dismiss()
        self.disrupt_opened=False

    def disrupt_game_popUp(self):

        myBox=BoxLayout()
        myBox.orientation='vertical'
        
        myLabel=Label()
        myLabel.text='This will quit the current game.\nAre you sure?'

        button1=Button()
        button1.text='Yes'
        button1.size_hint_y=0.2

        button2=Button()
        button2.text='No'
        button2.size_hint_y=0.2

        bar=Widget()
        bar.size_hint_y=0.02

        myBox.add_widget(myLabel)
        myBox.add_widget(button1)
        myBox.add_widget(bar)
        myBox.add_widget(button2)
        
        popUp=Popup()
        popUp.title='Stop the game?'
        popUp.content=myBox
        popUp.size_hint=(0.9,0.8)
        popUp.auto_dismiss=False

        #button.bind(on_release=popUp.dismiss)
        button1.bind(on_release=self.disrupt_yes)
        button2.bind(on_release=self.disrupt_no)

        return popUp


    def view_art_popUp(self):

        myBox=BoxLayout()
        myBox.orientation='vertical'
        
        myLabel=Label()
        if self.critical:
            myLabel.text='You have completed the puzzle!\n\nNote: You must win with timer\nto unlock next level'
        else:
            myLabel.text='You have completed the puzzle!'

        if self.artist!=None and self.artist!='flickr':
            button=Button()
            button.text='More arts by '+self.artist
            button.size_hint_y=0.2
            button.bind(on_release=self.open_fanpage)

        button1=Button()
        button1.text='View full image'
        button1.size_hint_y=0.2

        button2=Button()
        button2.text='Replay'
        button2.size_hint_y=0.2

        bar=Widget()
        bar.size_hint_y=0.02
        bar2=Widget(size_hint_y=0.02)

        myBox.add_widget(myLabel)
        myBox.add_widget(button1)
        myBox.add_widget(bar)
        if self.artist!=None and self.artist!='flickr':
            myBox.add_widget(button)
        myBox.add_widget(bar2)
        myBox.add_widget(button2)
        
        popUp=Popup()
        popUp.title='You won!'
        popUp.content=myBox
        popUp.size_hint=(0.9,0.8)
        popUp.auto_dismiss=False

        #button.bind(on_release=popUp.dismiss)
        button1.bind(on_release=self.view_image)
        button2.bind(on_release=self.re_play)

        return popUp

    def re_play(self,instance):
        self.re_shuffling()
        #self.add_fanpage()
        self.view_art_popUp.dismiss()
        print('taking action')

    def view_image(self,instance):
        self.view_art_popUp.dismiss()
        self.add_widget(self.black)
        self.add_widget(self.full_image)
        self.view_image_mode=True

    def open_fanpage(self,instance):
        webbrowser.open(self.url)

    def exit_view_image(self):
        self.remove_widget(self.black)
        self.remove_widget(self.full_image)
        self.view_image_mode=False
        self.view_art_popUp.open()

    def add_fanpage(self):
        if self.artist!=None:
            print('I AM ADDING FANPAGE HERE')
            self.add_widget(self.art_promotion_bg)
            self.add_widget(self.art_promotion)
            self.add_widget(self.profile)

    def remove_fanpage(self):
        if self.artist!=None:
            self.remove_widget(self.art_promotion_bg)
            self.remove_widget(self.art_promotion)
            self.remove_widget(self.profile)

    def state_goal_popUp(self):
        
        myBox=BoxLayout()
        myBox.orientation='vertical'
        
        myLabel=Label()

        if ArtInfo.max_score[self.puzzle_index]!=None:
            myLabel.text='Reach score of '+str(self.goal)+'\nto unlock next stage.\n\
Maximum score: '+str(ArtInfo.max_score[self.puzzle_index])
        else:
            myLabel.text='Reach score of '+str(self.goal)+'\nto unlock next stage.\n\
Maximum score: unlimtied'

        button=Button()
        button.text='Ok!'
        button.size_hint_y=0.3

        myBox.add_widget(myLabel)
        myBox.add_widget(button)
        
        popUp=Popup()
        popUp.title='Mission'
        popUp.content=myBox
        popUp.size_hint=(0.8,0.5)
        popUp.auto_dismiss=False

        button.bind(on_release=self.start_timing_press)

        return popUp

    def start_timing_press(self,instance):
        self.add_clock()
        self.goal_popUp.dismiss()

    def handle_start_timer(self):
        if self.critical:
            self.goal_popUp.open()
        else:
            self.add_clock()
            
    def max_score_reached_popUp(self):
        myBox=BoxLayout()
        myBox.orientation='vertical'
        
        myLabel=Label()
        myLabel.text='Maximum score possible reached\nUnlimited score is allowed in\nhigh level stages'

        button=Button()
        button.text='Dismiss'
        button.size_hint_y=0.3

        myBox.add_widget(myLabel)
        myBox.add_widget(button)
        
        popUp=Popup()
        popUp.title='Max score for level reached'
        popUp.content=myBox
        popUp.size_hint=(0.9,0.5)
        popUp.auto_dismiss=False

        button.bind(on_release=self.handle_max_reached)

        return popUp

    def handle_max_reached(self,instance):
        self.max_reached_popUp.dismiss()
        self.game_over_popUp()
