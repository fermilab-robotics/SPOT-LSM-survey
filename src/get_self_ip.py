""" This script is used to get the host_ip of host that runs the gRPC server """

import os
from bosdyn.client.common import get_self_ip

spot_host=os.getenv("spot_host")

if __name__=="__main__":
	
   host_ip=get_self_ip(spot_host)
   assert host_ip!=None, "host ip is NULL"
   print(host_ip)
    

   
    
