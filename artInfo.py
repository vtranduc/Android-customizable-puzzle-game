class ArtInfo:

    #=====THE FOLLOWING ARE THE ARTISTS' FANPAGE WEBSITE=============
    Moriartea='https://www.facebook.com/Moriarteachan/?pnref=lhc'
    tiffany='https://www.facebook.com/zeriru/'
    Shishir='https://www.facebook.com/Dreaming-S-807216569377305/'
    Joan='https://www.facebook.com/Joan-Villocillo-Art-1563819007236807/'
    Sofiya='https://www.facebook.com/Sofiya-915732791845977/?fref=ts'
    #This is yuri madoka & homura
    flickr1='https://www.flickr.com/photos/palma-bernardo-alexius-hutabarat/16041512668/in/photolist-qrwWQC-xkRfbP-f4u67j-9MifR2-58e62s-9YLNCj-ymrsBd-nXqdEn-dgQ7zH-9YLLvS-nXqc2c-oeUsnr-8KGitF-oSAxWn-xq6TbM-xkHgi5-52kwTt-dgQ8rw-9jCgeJ-dgQ7y2-5Qkg6x-y1edoV-oAn2fx-dgQ67x-hwAa5G-3ZQBWz-dgQ7Um-9YLM1Q-9jz6ai-9YHSoK-f4eMyz-dgQ8Bf-dgQ8h5-dgQ7Qs-dgQ763-9YHTqT-cV8BMf-6r2jC-9YHSG6-9YHSeH-9YLM9Y-y5K4Hq-dgQ7Hr-amXiep-9YHTLV-9jz8jX-59siJ9-aKmAkH-9YHSZM-9YHToH'
    #This is ultimate madoka
    flickr2='https://www.flickr.com/photos/palma-bernardo-alexius-hutabarat/15606614604/in/photolist-pM6YN9-f4u3WG-9jz9Zp-dgQ6nu-5hwcJJ-qrwWQC-xkRfbP-f4u67j-9MifR2-58e62s-9YLNCj-ymrsBd-nXqdEn-dgQ7zH-9YLLvS-nXqc2c-oeUsnr-8KGitF-oSAxWn-xq6TbM-xkHgi5-52kwTt-dgQ8rw-9jCgeJ-dgQ7y2-5Qkg6x-y1edoV-oAn2fx-dgQ67x-hwAa5G-3ZQBWz-dgQ7Um-9YLM1Q-9jz6ai-9YHSoK-f4eMyz-dgQ8Bf-dgQ8h5-dgQ7Qs-dgQ763-9YHTqT-cV8BMf-6r2jC-9YHSG6-9YHSeH-9YLM9Y-y5K4Hq-dgQ7Hr-amXiep-9YHTLV'
    #Green hair chick hugging the cat
    flickr3='https://www.flickr.com/photos/palma-bernardo-alexius-hutabarat/16043193217/'
    #Chick holding the camera with a lot of birds around her
    flickr4='https://www.flickr.com/photos/palma-bernardo-alexius-hutabarat/16042884489/in/photostream/'
    #Four chicks in sleeping dress
    #flickr5='https://www.flickr.com/photos/palma-bernardo-alexius-hutabarat/16229019825/in/photostream/'
    #Saten
    flickr6='https://www.flickr.com/photos/palma-bernardo-alexius-hutabarat/16041602450/in/album-72157650175998031/'
    #White hair chick with white princess dress
    flickr7='https://www.flickr.com/photos/palma-bernardo-alexius-hutabarat/16042907619/in/album-72157650175998031/'
    #4 girls under water
    flickr8='https://www.flickr.com/photos/palma-bernardo-alexius-hutabarat/16043147387/in/album-72157650175998031/'
    #Ultimate madoka look up with right hand up
    flickr9='https://www.flickr.com/photos/palma-bernardo-alexius-hutabarat/15609168623/in/album-72157650175998031/'
    

    fanpage_url=[tiffany,Moriartea,tiffany,Shishir,tiffany,
                 Moriartea,flickr1,Moriartea,Shishir,Joan,
                 tiffany,flickr9,tiffany,flickr4,flickr6,
                 tiffany,tiffany,tiffany,tiffany,tiffany,
                 flickr3,tiffany,tiffany,flickr7,flickr8,
                 tiffany,Joan,Sofiya,Moriartea,flickr2]

    #fanpage_url=[tiffany,Moriartea,tiffany] #FIX=================================================================================

    #ANYTHING OBTAINED FROM FLICKR MUST BE 'FLICKR'
    artist_names=[]
    for i in range(0,len(fanpage_url)):
        if fanpage_url[i]==Moriartea:
            artist_names.append('Moriartea')
        elif fanpage_url[i]==tiffany:
            artist_names.append('Tiffany Gao')
        elif fanpage_url[i]==Shishir:
            artist_names.append('S.I.Dew(Shishir)')
        elif fanpage_url[i]==Joan:
            artist_names.append('Joan Villocillo')
        elif fanpage_url[i]==Sofiya:
            artist_names.append('Sofiya')
        elif fanpage_url[i]==flickr1:
            artist_names.append('flickr')
        elif fanpage_url[i]==flickr2:
            artist_names.append('flickr')
        elif fanpage_url[i]==flickr3:
            artist_names.append('flickr')
        elif fanpage_url[i]==flickr4:
            artist_names.append('flickr')
        #elif fanpage_url[i]==flickr5:
         #   artist_names.append('flickr')
        elif fanpage_url[i]==flickr6:
            artist_names.append('flickr')
        elif fanpage_url[i]==flickr7:
            artist_names.append('flickr')
        elif fanpage_url[i]==flickr8:
            artist_names.append('flickr')
        elif fanpage_url[i]==flickr9:
            artist_names.append('flickr')
        else:
            artist_names.append(None)
    #================================================================

    #====ADJUST THE DIFFICULTIES FOR UNLOCKING NEW STAGE HERE========
    goal=[2,3,4,5,6,
          10,15,17,15,15,
          20,25,25,20,20,
          25,25,25,25,25,
          30,30,30,30,30,
          30,30,30,40,50]

    default_shuffling=[30,30,30,30,30,
                       30,30,30,30,30,
                       30,30,30,60,60,
                       60,60,80,80,80]

    splitter=[(3,3),(4,4),(2,3),(5,5),(4,5),
              (5,4),(5,5),(5,5),(6,6),(6,6),
              (5,5),(5,5),(5,5),(5,5),(5,5),
              (5,5),(5,5),(5,5),(5,5),(5,5),
              (5,5),(5,5),(5,5),(5,5),(6,6),
              (6,6),(6,6),(6,6),(6,6),(6,6)]

    sec_per_move=[10,9,8,7,6,
                  6,6,5,8,6,
                  5,5,5,5,5,
                  5,5,5,5,5,
                  5,4,3,2,5,
                  5,4,3,2,1]

    max_score=[10,10,10,10,10,
               20,20,20,20,20,
               30,30,30,30,30,
               50,50,50,50,50,
               None,None,None,None,None,
               None,None,None,None,None]
    #================================================================
