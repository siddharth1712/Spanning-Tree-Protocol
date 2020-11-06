class bridge:
    def __init__(self):
        self.root=-1
        self.rp=['\0',-1]
        self.rootd=-1
        self.id=-1
        self.ftable={}
        self.conn_lans=[]   #second entry is 1 for RP, 0 for DP, -1 for NP
    def disp(self):
        print(self.root,self.rp,self.rootd,self.id,self.conn_lans)
class lan:
    def __init__(self):
        self.dp=-1
        self.id='\0'
        self.conn_br=[]  #second entry is 1 for RP, 0 for DP, -1 for NP
        self.hosts=[]
    def disp(self):
        print(self.dp,self.id,self.conn_br,self.hosts)
class message:
    def __init__(self):
        self.port='\0'
        self.stop=False
        self.src_id=-1
        self.dest_id=-1
        self.root=-1
        self.d=-1
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
            temp_bridge_obj.conn_lans.append(temp_l) #initialising all connections to DP
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
        
    first=True
    while len(sent)>0:
        
        if not first:
            sent.clear()

        for m in recd:
            temp,br_list=fwd(m,br_list,lan_list)
            if not temp.stop:
                sent.append(temp)

        recd.clear()

        for m in sent:
            recd=recd+(send(m,br_list,lan_list))

        new_recd=[]
        for i in recd:
            matched=False
            for elem in new_recd:
                if (i.port==elem.port) & (i.stop==elem.stop) & (i.src_id==elem.src_id) & (i.dest_id==elem.dest_id) & (i.root==elem.root) & (i.d==elem.d):
                    matched=True
                    break
            if not matched:
                new_recd.append(i)
        recd=new_recd

        first=False

    for lan_id,lan_obj in lan_list.items():
        d=br_list[lan_obj.conn_br[0]].rootd
        min_br=lan_obj.conn_br[0]
        for br in lan_obj.conn_br:
            if br_list[br].rootd<d:
                d=br_list[br].rootd
                min_br=br
            else :
                if (br_list[br]==d) & (br<min_br):
                    min_br=br
        lan_obj.dp=min_br
                
    for temp,b in br_list.items():
        b.disp()

    for lanid,lanobj in lan_list.items():
        lanobj.disp()
    
    return br_list,lan_list

    
