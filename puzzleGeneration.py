from random import choice

r='right';l='left';u='up';d='down'

class PuzzleGeneration:

    def __init__(self,xnum,ynum):
		#Here, be cautious enough to make xnum and ynum each equal or bigger than 2, otherwise error will occur somewhere
        self.tiles=[]
        element=xnum*ynum
        self.max=element-1
        for i in range(0,xnum):
            row=[]
            for j in range(0,ynum):
                element-=1
                row.append(element)
            self.tiles.append(row)
        self.blockx=xnum-1
        self.blocky=ynum-1
        self.blank=[self.blockx,self.blocky]
        self.moveList=[l,u]

    def shuffle(self,shuffle_count):

        #shuffle_count=300

        shuffleStep=None
        
        while shuffle_count>0:
            
            for i in range(0,shuffle_count):
                '''
                #=============Here is to make puzzle not go back=============
                if i!=0:
                    picks=self.moveList
                    try:
                        picks.pop(self.moveList.index(shuffleStep))
                    shuffleStep=choice(picks)
                #===========================================
                else:
                    shuffleStep=choice(self.moveList)
                '''
                #=====---========This is so puzzle does not go back
                try:
                    if shuffleStep==r:
                        shuffleStep=l
                    elif shuffleStep==l:
                        shuffleStep=r
                    elif shuffleStep==u:
                        shuffleStep=d
                    elif shuffleStep==d:
                        shuffleStep=u
                    picks=[]
                    for j in range(0,len(self.moveList)):
                        picks.append(self.moveList[j])
                    myIndex=self.moveList.index(shuffleStep)
                    picks.pop(myIndex)
                    shuffleStep=choice(picks)
                except: #This case should be passed in only when i=0
                    shuffleStep=choice(self.moveList)
                    print('did not work = '+str(i))
                
                #shuffleStep=choice(self.moveList)
                #print('I am moving ='+shuffleStep)
                #=========------------======
                
                if shuffleStep==u:
                    tempx=self.blank[0]-1
                    tempy=self.blank[1]
                    temp=self.tiles[tempx][tempy]
                    self.tiles[self.blank[0]][self.blank[1]]=temp
                    self.tiles[tempx][tempy]=0
                    if self.blank[0]==self.blockx:
                        self.moveList.append(d)
                    self.blank[0]-=1
                    if self.blank[0]==0:
                        self.moveList.remove(u)
                
                elif shuffleStep==d:
                    tempx=self.blank[0]+1
                    tempy=self.blank[1]
                    temp=self.tiles[tempx][tempy]
                    self.tiles[self.blank[0]][self.blank[1]]=temp
                    self.tiles[tempx][tempy]=0
                    if self.blank[0]==0:
                        self.moveList.append(u)
                    self.blank[0]+=1
                    if self.blank[0]==self.blockx:
                        self.moveList.remove(d)

                elif shuffleStep==l:
                    tempx=self.blank[0]
                    tempy=self.blank[1]-1
                    temp=self.tiles[tempx][tempy]
                    self.tiles[self.blank[0]][self.blank[1]]=temp
                    self.tiles[tempx][tempy]=0
                    if self.blank[1]==self.blocky:
                        self.moveList.append(r)
                    self.blank[1]-=1
                    if self.blank[1]==0:
                        self.moveList.remove(l)

                elif shuffleStep==r:
                    tempx=self.blank[0]
                    tempy=self.blank[1]+1
                    temp=self.tiles[tempx][tempy]
                    self.tiles[self.blank[0]][self.blank[1]]=temp
                    self.tiles[tempx][tempy]=0
                    if self.blank[1]==0:
                        self.moveList.append(l)
                    self.blank[1]+=1
                    if self.blank[1]==self.blocky:
                        self.moveList.remove(r)
            
            if not self.finish():
            	break

    def finish(self):
        if self.tiles[0][0]!=self.max:
            return False
        compare=self.max
        for j in range(1,self.blocky+1):
            if compare-self.tiles[0][j]!=1:
                return False
            compare=self.tiles[0][j]
        for i in range(1,self.blockx+1):
            for j in range(0,self.blocky+1):
                if compare-self.tiles[i][j]!=1:
                    return False
                compare=self.tiles[i][j]
        return True
