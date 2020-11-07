import bridge

tr=0
n=0
br_list={}
lan_list={}
tr,n,br_list,lan_list=bridge.take_input(tr,n,br_list,lan_list)
br_list,lan_list=bridge.initialize(tr,n,br_list,lan_list)
br_list=bridge.sortbr(br_list)
for br_id,br_obj in br_list.items():
    br_obj.disp()
br_list,lan_list=bridge.sendpacket(tr,n,br_list,lan_list)
