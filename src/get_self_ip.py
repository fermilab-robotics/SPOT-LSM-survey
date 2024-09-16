import os
from bosdyn.client.common import get_self_ip

spot_host=os.getenv("spot_host")

if __name__=="__main__":
   self_ip=get_self_ip(spot_host)
   path=os.path.dirname(__file__)
   path_to_env=os.path.join(path,"../.devcontainer/.env")
   with open(path_to_env,"w") as f:
    to_be_written=f"test_ip={self_ip}"
    f.write(to_be_written)
   
   assert open(path_to_env,"r").read()!=None, "host ip is not provided"
    

   
    