
def spot_data(data:dict,result:dict)->None:

    """"
        write spot data to dict for csv DictWriter
    """
    for d in data: 
        result["spot time"]=d
        result["spot vision x"]=data[d]['vision']["x"]
        result["spot vision y"]=data[d]['vision']["y"]
        result["spot vision z"]=data[d]['vision']["z"]
        result["spot vision yaw"]=data[d]["yaw"]
        result["spot vision pitch"]=data[d]["pitch"]
        result["spot vision roll"]=data[d]["roll"]
        # result["spot odom x"]=data['odom'].data.x
        # result["spot odom y"]=data['odom'].data.y
        # result["spot odom z"]=data['odom'].data.z
        # result["spot odom yaw"]=quat_to_Euler(data['odom'].data).yaw
        # result["spot odom pitch"]=quat_to_Euler(data['odom'].data).pitch
        # result["spot odom roll"]=quat_to_Euler(data['odom'].data).roll


def tag_data(data:dict,result:dict)->None:
    """
        write tag data to dict for csv DictWriter

    """
    for d in data: 
        result["tag time"]=d
        result["tag vision x"]=data[d]['vision']["x"]
        result["tag vision y"]=data[d]['vision']["y"]
        result["tag vision z"]=data[d]['vision']["z"]
        result["tag vision yaw"]=data[d]["yaw"]
        result["tag vision pitch"]=data[d]["pitch"]
        result["tag vision roll"]=data[d]["roll"]
   
    # result["tag odom x"]=data['odom'].data.x
    # result["tag odom y"]=data['odom'].data.y
    # result["tag odom z"]=data['odom'].data.z
    # result["tag odom yaw"]=quat_to_Euler(data['odom'].data).yaw
    # result["tag odom pitch"]=quat_to_Euler(data['odom'].data).pitch
    # result["tag odom roll"]=quat_to_Euler(data['odom'].data).roll



