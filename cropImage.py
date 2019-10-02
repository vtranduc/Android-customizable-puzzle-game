import kivy
kivy.require('1.7.2')

from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

#Still experimental. There could still be flaw(s)

class CropImage(Widget):

    def __init__(self,imageStr,*args,**kwargs):
        super(CropImage,self).__init__(**kwargs)
        #Optionally, user can specify 4 elements for args
        #args[0] is x_position of bottom left of portion to be cropped, as ratio of original image's x length
        #args[1] is y_position of bottom left of portion to be cropped, as ratio of original image's y length
        #args[2] is x_length of portion to be croped, as ratio of original image's x length
        #args[3] is y_length of portion to be croped, as ratio of original image's x length
        image=Image(source=imageStr)
        originalSize=image.texture_size
        if len(args)==0:
            subtexture=image.texture
            self.posx=0
            self.posy=0
            self.sizex=originalSize[0]
            self.sizey=originalSize[1]
        elif len(args)==4:
            orix=originalSize[0]
            oriy=originalSize[1]
            self.posx=round(orix*args[0])
            self.posy=round(oriy*args[1])
            self.sizex=round(orix*args[2])
            self.sizey=round(oriy*args[3])
            subtexture=image.texture.get_region(self.posx,self.posy,self.sizex,self.sizey)
        else:
            print('ERROR IN SIDE CROPIMAGE CLASS: args is not used properly!')

        node=Widget(pos=[self.posx,self.posy],size=[self.sizex,self.sizey])
        
        with node.canvas:
            self.rect_bg=Rectangle(size=node.size,texture=subtexture)
        self.add_widget(node)

        with self.canvas:
            self.size=node.size
            self.x=self.posx
            self.y=self.posy
            self.rect_bg.pos=[self.x,self.y]

    def setPos(self,xPos,yPos):
        self.x=xPos
        self.y=yPos
        self.rect_bg.pos=[self.x,self.y]

    def setSize(self,width,height):
        self.size=[width,height]
        self.rect_bg.size=[width,height]

    def get_size(self):
        return self.size

    def scale(self,ratio):
        x=round(self.size[0]*ratio)
        y=round(self.size[1]*ratio)
        self.size=[x,y]
        self.rect_bg.size=[x,y]

def getSize(imageStr):
    return Image(source=imageStr).texture_size

def ratioFit(imageStr,maxWidth,maxHeight,*args):
    #This will stretch to fit just in the box with dimension specified.
    #All aspect ratio will be maintained
    #If you wanna get size for positions and such, do (widget).size
    # or use get_size() function as seen above
    #As an option, you can specifiy x and y coordinates as *args so
    #this thing will fit into that position for you.
    oriSize=getSize(imageStr)
    xScale=float(oriSize[0])/float(maxWidth)
    yScale=float(oriSize[1])/float(maxHeight)
    widget=CropImage(imageStr)
    if xScale<=yScale:
        widget.scale(1./yScale)
        if len(args)==2:
            xPos=(maxWidth-widget.get_size()[0])/2+args[0]
            widget.setPos(xPos,args[1])
        elif len(args)>0:
            print('ERROR: args is not used properly. Read description!')
    elif xScale>yScale:
        widget.scale(1./xScale)
        if len(args)==2:
            yPos=(maxHeight-widget.get_size()[1])/2+args[1]
            widget.setPos(args[0],yPos)
        elif len(args)>0:
            print('ERROR: args is not used properly. Read description!')
    return widget

def cropFit(imageStr,width,height,*args):
    #Crop the widget just to fit the box specified
    #Useful for things like setting background image
    #Optional args allows to set position of background
    oriSize=getSize(imageStr)
    xScale=float(oriSize[0])/float(width)
    yScale=float(oriSize[1])/float(height)
    if xScale<=yScale:
        scale=1./xScale
       	cropRatio=0.5-float(height)/(float(oriSize[1])*scale*2.)
        heightRatio=float(height)/(float(oriSize[1])*scale)
        widget=CropImage(imageStr,0.,cropRatio,1.,heightRatio)
    elif xScale>yScale:
        scale=1./yScale
        cropRatio=0.5-float(width)/(float(oriSize[0])*scale*2.)
        widthRatio=float(width)/(float(oriSize[0])*scale)
        widget=CropImage(imageStr,cropRatio,0.,widthRatio,1.)
    widget.scale(scale)
    if len(args)==2:
        widget.setPos(args[0],args[1])
    elif len(args)>0:
        print('ERROR: args is not used properly. Read description!')
    return widget

def centering_widget(widget,pos_x,pos_y,width,height):
    #This center the widget into the space specified.
    #The widget must've been generated using CropImage class above
    #Last 4 arguments above specifies the space to which widget is centered
    x_pos=pos_x+(width-widget.get_size()[0])/2.
    y_pos=pos_y+(height-widget.get_size()[1])/2.
    widget.setPos(x_pos,y_pos)
    
