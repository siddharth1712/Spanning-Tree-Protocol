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
tr=int(input())
n=int(input())
br_list=[]
lan_list=[]
temp_bridge_aa=[]

for i in range(0,n):    #1

    inp=input().split(' ')
    br_list.append(bridge())
    br_list[i].id=int(inp[0][1:-1])
    
    for temp_l in inp[1:]:  #2
        br_list[i].conn_lans.update({temp_l:0}) #initialising all connections to DP

        lan_exists=False
        for l in lan_list:  #3
            if l.id==temp_l:
                l.conn_br.update({br_list[i].id:0})
                lan_exists=True
                break

        if not lan_exists:

            lan_list.append(lan())
            lan_list[-1].id=temp_l            
            lan_list[-1].conn_br.update({br_list[i].id:0})
            
''''''
for b in br_list:
    print(b.id,b.conn_lans)
for l in lan_list:
    print(l.id,l.conn_br)
''''''
