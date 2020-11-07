class bridge:
    def __init__(self):
        self.root=-1
        self.rp=['\0',-1]
        self.rootd=-1
        self.id=-1
        self.ftable={}
        self.conn_lans=[]
        self.lans=[]
    def disp(self):
        #print(self.root,self.rp,self.rootd,self.id,self.conn_lans,self.lans,self.ftable)
        stri="B{}:".format(self.id)
        for l in self.conn_lans:
            if l==self.rp[0]:
                stri+=" {}-RP".format(l)
            else:
                if l in self.lans:
                    stri+=" {}-DP".format(l)
                else:
                    stri+=" {}-NP".format(l)
        print(stri)
    def printftable(self):
        print("B{}:".format(self.id))
        print("HOST ID | FORWARDING PORT")
        for h,p in self.ftable.items():
            print("H{} | {}".format(h,p))
        
class lan:
    def __init__(self):
        self.dp=-1
        self.id='\0'
        self.conn_br=[]  
        self.hosts=[]
        self.br=[]
    def disp(self):
        print(self.dp,self.id,self.conn_br,self.hosts,self.br)
        
class message:
    def __init__(self):
        self.port='\0'
        self.stop=False
        self.src_id=-1
        self.dest_id=-1
        self.root=-1
        self.d=-1

class data:
    def __init__(self):
        self.src_host=-1
        self.dest_host=-1
        self.lan='\0'
        self.bridge=-1
        
#-------------------------------------------------
def take_input(tr,n,br_list,lan_list):
    tr=int(input())
    n=int(input())
    #br_list=[]
    #lan_list=[]

    for i in range(0,n):    #1

        inp=input().split(' ')
        temp_bridge_obj=bridge()
        br_id=int(inp[0][1:-1])
        temp_bridge_obj.id=br_id
        temp_bridge_obj.root=br_id
        
        for temp_l in inp[1:]:  #2
            temp_bridge_obj.conn_lans.append(temp_l) 
            temp_bridge_obj.conn_lans=list(set(temp_bridge_obj.conn_lans))
            
            if temp_l not in lan_list:
                temp_lan_obj=lan()
                temp_lan_obj.id=temp_l
                lan_list.update({temp_l:temp_lan_obj})

            lan_list[temp_l].conn_br.append(br_id)
            lan_list[temp_l].conn_br=list(set(lan_list[temp_l].conn_br))

        br_list.update({br_id:temp_bridge_obj})
        
    
    for i in range(len(lan_list)):
        inp=input().split(' ')
        lan_id=inp[0][0]
        for host in inp[1:]:
            lan_list[lan_id].hosts.append(int(host[1:]))

    '''
    for bridge_id,brobj in br_list.items():
        brobj.disp()
    for lan_id,lanobj in lan_list.items():
        lanobj.disp()
    '''
    
    
    
    return tr,n,br_list,lan_list

def send(m,br_list,lan_list):
    #print(m.d,m.src_id,m.root)
    received=[]
    for lan_id in br_list[m.src_id].conn_lans:
        for br_id in lan_list[lan_id].conn_br:
            if(br_id!=m.src_id):
                received.append(message())
                received[-1].root=m.root
                received[-1].d=m.d
                received[-1].src_id=m.src_id
                received[-1].dest_id=br_id
                received[-1].port=lan_id
    return received                    

def fwd(m,br_list,lan_list):
    m1=message()
    m1.root=m.root
    m1.d=m.d+1
    m1.src_id=m.dest_id
    c1=  (m.root < br_list[m1.src_id].root)
    c2= (m.root == br_list[m1.src_id].root) & (br_list[m1.src_id].rootd > m.d+1)
    c3= (m.root == br_list[m1.src_id].root) & (br_list[m1.src_id].rootd == m.d+1) & (br_list[m1.src_id].rp[1] > m.src_id)
    if c1|c2|c3:
        br_list[m1.src_id].root=m.root
        br_list[m1.src_id].rp=[m.port,m.src_id]
        br_list[m1.src_id].rootd=m.d+1
    else:
        m1.stop=True
    return m1,br_list

def initialize(tr,n,br_list,lan_list):
    sent=[]
    recd=[]
    for bridge_id,br_obj in br_list.items():
        m=message()
        m.d=0
        m.src_id=br_obj.id
        m.root=br_obj.id
        sent.append(m)
        
    while len(sent)>0:
        for m in sent:
            recd=recd+(send(m,br_list,lan_list))
        #if not first:
        sent.clear()

        for m in recd:
            temp,br_list=fwd(m,br_list,lan_list)
            if not temp.stop:
                sent.append(temp)

        recd.clear()

        
    for lan_id,lan_obj in lan_list.items():
        d=br_list[lan_obj.conn_br[0]].rootd
        min_br=lan_obj.conn_br[0]
        for br in lan_obj.conn_br:
            if br_list[br].rootd<d:
                d=br_list[br].rootd
                min_br=br
            else :
                if (br_list[br].rootd==d) & (br<min_br):
                    min_br=br
        lan_obj.dp=min_br

    for br_id,br_obj in br_list.items():
        for l in br_obj.conn_lans:
            if (l==br_obj.rp[0]) | (lan_list[l].dp==br_obj.id):
                lan_list[l].br.append(br_obj.id)
                br_obj.lans.append(l)
                
    
    return br_list,lan_list

def sortbr(br_list):
    tempbr=[]
    for br_id,br in br_list.items():
        br.conn_lans.sort()
        br.lans.sort()
        temp=[]
        for temp1,temp2 in br.ftable.items():
            temp.append(temp1)
        temp.sort()
        tempft={}
        for t in temp:
            tempft.update({t:br.ftable[t]})
        br.ftable=tempft

        tempbr.append(br.id)
    tempbr.sort()
    new_br_list={}
    for br in tempbr:
        new_br_list.update({br:br_list[br]})
    br_list=new_br_list
    return br_list


def sendpacket(tr,n,br_list,lan_list):
    sent=[]
    recd=[]
    t=int(input())
    for i in range(t):
        inp=input().split(' ')
        m=data()
        m.src_host=int(inp[0][1:])
        m.dest_host=int(inp[1][1:])
        for lan_id,l in lan_list.items():
            if m.src_host in l.hosts:
                m.lan=l.id
        sent.append(m)
        
        while len(sent)>0:
            for m in sent:
                for b in lan_list[m.lan].br:
                    if b!=m.bridge:
                        m1=data()
                        m1.bridge=b
                        m1.src_host=m.src_host
                        m1.dest_host=m.dest_host
                        m1.lan=m.lan
                        recd.append(m1)
            sent.clear()
            
            for m in recd:
                if (m.dest_host in br_list[m.bridge].ftable):
                    if m.lan!=br_list[m.bridge].ftable[m.dest_host]:
                        m1=data()
                        m1.bridge=m.bridge
                        m1.src_host=m.src_host
                        m1.dest_host=m.dest_host
                        m1.lan=br_list[m.bridge].ftable[m.dest_host]
                        sent.append(m1)
                else:
                    for l in br_list[m.bridge].lans:
                        if l!=m.lan:
                            m1=data()
                            
                            m1.bridge=m.bridge
                            m1.src_host=m.src_host
                            m1.dest_host=m.dest_host
                            m1.lan=l
                            sent.append(m1)
                br_list[m.bridge].ftable.update({m.src_host:m.lan})
            recd.clear()
        br_list=sortbr(br_list)
        for br_id,br_obj in br_list.items():
            br_obj.printftable()

        if i!=t-1:
            print("")
    return br_list,lan_list
