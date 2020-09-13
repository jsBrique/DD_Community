def analyse():
    f=open('templates/hanhan.txt','r')
    namelist={}
    hanhantalk=""
    for s in f:
        if ': ' in s:
            timestamp=s[:20]
            line=s[20:]
            a=line.find('] ')
            b=line.find(': ')
            if(a>0):
                tt=a+2
            else:
                tt=0
            bid=line[tt:b]
            talk=line[b+1:]
            if bid not in namelist:
                namelist[bid]=1
            else:
                namelist[bid]=namelist[bid]+1
            if '涵涵_Live2Dモデリング'  in bid:
                hanhantalk=s+'<br>\n'+hanhantalk
 
                 
    f.close()
    # for n in namelist:
    #     print(n,namelist[n])

    ap = sorted(namelist.items(), key=lambda d:d[1], reverse = True)
    res="DD发言排行<br>\n"
    for i,r in enumerate( ap[0:10]):
        res=res+" "+str(i+1)+"  "+r[0]+" "+str(r[1])+"<br>"+"\n"

    return res,hanhantalk

# print(analyse())

