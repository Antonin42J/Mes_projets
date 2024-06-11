import os 


class Tools :
    
    """
        Class to spread tools to simplify the code and navigate easily in the architecture.
        
        get_the_right_path() -> str
        
            -> return the parent path of "Group_project" folder and avoid problem with os.getcwd() problem
    
    """
    
    def getTheRightPath() -> str:
        
        # Get the absolute path of the current directory
        current_directory = os.getcwd()
        
        index=0
        

        # Navigate to the parent directory until reaching "Group_project"
        while os.path.basename(current_directory) != "Group_project":
            current_directory= os.path.dirname(current_directory)
            index+=1
            
            if index==50:
                print("Error path")
                break
        
        return current_directory
