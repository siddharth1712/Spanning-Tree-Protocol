class bridge:
    def __init__(self):
        self.id=-1
        self.ftable={}
        self.conn_lans={}   #second entry is 1 for RP, 0 for DP, -1 for NP
class lan:
    def __init__(self):
        self.id='\0'
        self.conn_br={}  #second entry is 1 for RP, 0 for DP, -1 for NP
        self.hosts=[]
        
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
        
        for temp_l in inp[1:]:  #2
            temp_bridge_obj.conn_lans.update({temp_l:0}) #initialising all connections to DP
            
            if temp_l not in lan_list:
                temp_lan_obj=lan()
                temp_lan_obj.id=temp_l
                lan_list.update({temp_l:temp_lan_obj})

            lan_list[temp_l].conn_br.update({br_id:0})

        br_list.update({br_id:temp_bridge_obj})
        
    
    for i in range(len(lan_list)):
        inp=input().split(' ')
        lan_id=inp[0][0]
        for host in inp[1:]:
            lan_list[lan_id].hosts.append(int(host[1:]))

    ''''''
    for bridge_id,brobj in br_list.items():
        print(brobj.id,brobj.conn_lans)
    for lan_id,lanobj in lan_list.items():
        print(lanobj.id,lanobj.conn_br,lanobj.hosts)
    ''''''
    
    
    
    return tr,n,br_list,lan_list

