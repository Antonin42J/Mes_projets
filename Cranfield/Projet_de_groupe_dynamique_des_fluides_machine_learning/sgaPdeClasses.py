import numpy as np
import os
import random
import sys
from inspect import isfunction
import pandas as pd
import copy
import matplotlib.pyplot as plt
import math

from CollectDataClass import CollectData
from ToolsClass import Tools


""" 
    This file difine the classes : 
    
    `Node` : Class to define the node type for the tree structure
    
    `Configure` : Class to define the starting value for the project
    
    `PDEFind`: Class to define the tools to find PDE
    
    `Setup`: Class to setup the value for the creation of PDE
    
    `Tree`: Define the Tree architecture
    
    `PDE`: Class to evaluate PDE
    
    `SGA`: Class used to initialise and run the SGA analysis
    
    `Plot`: Class to plot and save figure and equation

    This file and classes are based on the work of Yuntian Chen
    GitHub : https://github.com/YuntianChen/SGA-PDE
_
"""

PATH_DATA = os.path.join(Tools.getTheRightPath(), "data")

PATH_SIMULATION_FILE = os.path.join(Tools.getTheRightPath(), "1D_Channel_Flow_simulations", "1D_Channel_Flow-ReynoldsStressTransportModel")

class Node:
    
    """
        Class to define the nodes structure for the tree architecture
        
        - __init__(self, depth : int, idx : int, parent_idx : int, name : str, full, child_num : int, child_st: int, var : int) -> None :
        
            Define to value to initialise the node
            
            Parameters : 
                -`depth` : required depth 
                -`idx` : index, 
                -`parent_idx` : index, 
                -`name` : name of the node, 
                -`full` : signification of the node, 
                -`child_num` : number of the child, 
                -`child_st`: state, 
                -`var` : value of the node
        
        - __str__(self) -> str : 
            
            return the name of the value attribute to the node
        
        - reset_status(self) -> None :
        
            Define the status of the node 
    
    """
    
    def __init__(self, depth : int, idx : int, parent_idx : int, name : str, full, child_num : int, child_st: int, var : int) -> None:
        
        """
            Define to value to initialise the node
            
            Parameters : 
                -`depth` : required depth 
                -`idx` : index, 
                -`parent_idx` : index, 
                -`name` : name of the node, 
                -`full` : signification of the node, 
                -`child_num` : number of the child, 
                -`child_st`: state, 
                -`var` : value of the node
            
        """
        
        self.depth = depth
        self.idx = idx
        self.parent_idx = parent_idx

        self.name = name
        self.child_num = child_num
        self.child_st = child_st
        self.status = self.child_num
        self.var = var
        self.full = full
        self.cache = copy.deepcopy(var)

    def __str__(self) -> str: 
        
        """
            return the name of the value attribute to the node
            
            Returns : 
            
                -`name` : name of the value attribute to the node
        """
        return self.name

    def reset_status(self) -> None: 
        
        """
            Define the status of the node
        """
        
        self.status = self.child_num
        
        
class Configure : 
    
    """
        Class to Configure value and function of the project
        
        - __init__(self, problem: str, reynold_number: str) -> None :
        
            Define value usefull for the project like : 
                
                -working variables
            
            Parameters :
        
                -`problem` : equation we want, 
                
                -`reynold_number` : reynold number on what we work
                
                -`dataset` : types of dataset we want to work with
                
                -`method_pde_find` : method we want to use for PDE finding
        
                
        - getValueConfigure(self) -> tuple[np.array]:
        
            return the working values
            
            Returns : 
            
                -`y`: y coordinate
                -`cov`: covariance data
                -`dp_y`: derivative of the pression about y 
                -`dp_x`: derivative of the pression about x
                -`u` : velocity
                -`du`: dericative of the velocity about y
                
        - get_y(self) -> np.array :
        
            retunr y value
            
            Returns :
            
                -`y`: y coordinate
            
        - getProblem(self) -> str :
        
            return the problem on what we working
            
            Returns : 
                
                -`problem`: name of the problem

            
        - getDevice(self) -> str : 
        
            return the availble device
            
            Returns : 
            
                -`divice`: available device
                
        - getDataset(self) -> str :
        
            return the availble device
            
            Returns : 
            
                -`divice`: available device
                
                
        - getMethod_train(self) -> str :
        
            return the method for pde finding
            
            Returns : 
            
                -`method_pde_find`: method we want to use
                
            
        - divide(up : float, down :float, eta=1e-10) -> float :

            return the division between two numbers
            
            Parameters : 
        
                -`up`: numerator 
                -`down`: denominator
                
            Returns : 
            
                - up/down : division between up and down
        
        Possible problem :
        
            "eq1_" : First RANS equation  
            
            "eq2_" : Second RANS equation 
            
        Possible covariances : 
        
            - u'u'
            - v'v'
            - w'w'
            - u'v'
            - u'w' -> derivative equal to 0
            - v'w' -> derivative equal to 0 
    """
    
    def __init__(self, problem: str, reynold_number: str, dataset: str, method_pde_find: str) -> None : 
        
        """
            Define value usefull for the project like : 
            
                -device 
                
                -working variables
            
            Parameters :
        
                -`problem` : equation we want, 
                
                -`reynold_number` : reynold number on what we work
                
                -`dataset` : types of dataset we want to work with
                
                -`method_pde_find` : method we want to use for PDE finding
                
        """
        
        self.problem = problem
        
        self.reynold_number = reynold_number
        
        self.dataset = dataset
        
        # self.method_pde_find = input("What method do you want to use for PDE finding ? ('S' for STRidge and 'L' for Lasso): ")
        
        self.method_pde_find = method_pde_find
        
        # Adapt reynold number to find the data for example 180 to 0180 
        if len(reynold_number) < 4 : 
        
            l = 0
            
            reynold_number_2 = reynold_number
            
            while l < 4 : 
                
                reynold_number_2 = "0" + reynold_number_2
                
                l = len(reynold_number_2)
            
        else : 
            
            reynold_number_2 = reynold_number
            
            
        #Find the data for the different types of dataset   
        if self.dataset == "simulation" :
            list_files = []
            for root, dirs, files in os.walk(PATH_SIMULATION_FILE):
                for file in files:
                    if "1DChannelFlow_RSTM_Re-"+reynold_number+"_Data" in file:
                        file_path = os.path.join(root, file)            
                
            data = pd.read_csv(file_path)
            
            data.columns = ['nodenumber', 'x-coordinate', 'y-coordinate','z-coordinate', 'velocity-magnitude', 'x-velocity','y-velocity', 'z-velocity', 
                            'lambda2-criterion','turb-kinetic-energy', 'turb-intensity', 'uu-reynolds-stress','vv-reynolds-stress', 'ww-reynolds-stress', 
                            'uv-reynolds-stress','vw-reynolds-stress', 'uw-reynolds-stress', 'turb-diss-rate','production-of-k', 'viscosity-turb', 'y-star',
                            'y-plus', 'turb-reynolds-number-rey', 'wall-shear','x-wall-shear', 'y-wall-shear', 'skin-friction-coef','x-coordinate.1', 
                            'y-coordinate.1', 'cell-wall-distance','strain-rate-mag', 'dx-velocity-dx', 'dx-velocity-dy','dx-velocity-dz', 'dp-dx', 'dp-dy', 'dp-dz']
        
        if self.dataset == "dns" : 
            dataframe_path_1 = os.path.join(PATH_DATA, "fluid_data_" + str(reynold_number), "LM_Channel_"+ reynold_number_2+"_mean_prof.dat")
            dataframe_path_2 = os.path.join(PATH_DATA, "fluid_data_" + str(reynold_number), "LM_Channel_" + reynold_number_2+"_vel_fluc_prof.dat")
            data = CollectData.combineDataFrame(CollectData().collectDataFile(dataframe_path_1), CollectData().collectDataFile(dataframe_path_2))
     
        
        # Initialise the value  
        self.y= 0
        self.u = 0
        self.du= 0
        self.cov= 0
        self.dp_x= 0
        self.dp_y = 0
        
        
        # Exit the case where is imposible to find the equations with the specific dataset
        if "eq1" in self.problem and self.dataset == "dns" :
            
            print("For this kind of dataset the finding of the firs RANS equation is impossible")
            
            sys.exit()
            
        
        
        #Define the value of configuration in function of the problem
        if self.problem == 'eq1_uv':
            
            y_o = data["y-coordinate"]
            u_o = data["x-velocity"]
            du_o = data["dx-velocity-dy"]
            cov_o = data["uv-reynolds-stress"]
            dp_x_o = data["dp-dx"]
        
            self.y= y_o.to_numpy().reshape(-1,1)
            self.u = u_o.to_numpy().reshape(-1,1)
            self.du= du_o.to_numpy().reshape(-1,1)
            self.cov= cov_o.to_numpy().reshape(-1,1)
            self.dp_x= dp_x_o.to_numpy().reshape(-1,1)
            
        if self.problem == 'eq2_uv':
            
            if self.dataset == "dns" :
                
                y_o = data["y^+"]
                cov_o = data["u'v'"]
                dp_y_o = data["P"]
                
            elif self.dataset == "simulation" :
                
                y_o = data["y-coordinate"]
                cov_o = data["uv-reynolds-stress"]
                dp_y_o = data["dp-dy"]
            
            self.y= y_o.to_numpy().reshape(-1,1)
            self.cov= cov_o.to_numpy().reshape(-1,1)
            self.dp_y= dp_y_o.to_numpy().reshape(-1,1)
            
            
        if self.problem == 'eq1_uu':
            
            y_o = data["y-coordinate"]
            u_o = data["x-velocity"]
            du_o = data["dx-velocity-dy"]
            cov_o = data["uu-reynolds-stress"]
            dp_x_o = data["dp-dx"]
            
            self.y= y_o.to_numpy().reshape(-1,1)
            self.u = u_o.to_numpy().reshape(-1,1)
            self.du= du_o.to_numpy().reshape(-1,1)
            self.cov= cov_o.to_numpy().reshape(-1,1)
            self.dp_x= dp_x_o.to_numpy().reshape(-1,1)
            
        if self.problem == 'eq2_uu':
            
            if self.dataset == "dns" :
                
                y_o = data["y^+"]
                cov_o = data["u'u'"]
                dp_y_o = data["P"]
                
            elif self.dataset == "simulation" :
                
                y_o = data["y-coordinate"]
                cov_o = data["uu-reynolds-stress"]
                dp_y_o = data["dp-dy"]
            
            self.y= y_o.to_numpy().reshape(-1,1)
            self.cov= cov_o.to_numpy().reshape(-1,1)
            self.dp_y= dp_y_o.to_numpy().reshape(-1,1)
            
        if self.problem == 'eq1_vv':
            
            y_o = data["y-coordinate"]
            u_o = data["x-velocity"]
            du_o = data["dx-velocity-dy"]
            cov_o = data["vv-reynolds-stress"]
            dp_x_o = data["dp-dx"]
            
            self.y= y_o.to_numpy().reshape(-1,1)
            self.u = u_o.to_numpy().reshape(-1,1)
            self.du= du_o.to_numpy().reshape(-1,1)
            self.cov= cov_o.to_numpy().reshape(-1,1)
            self.dp_x= dp_x_o.to_numpy().reshape(-1,1)
            
        if self.problem == 'eq2_vv':
            
            
            if self.dataset == "dns" :
                
                y_o = data["y^+"]
                cov_o = data["v'v'"]
                dp_y_o = data["P"]
                
            elif self.dataset == "simulation" :
                
                y_o = data["y-coordinate"]
                cov_o = data["vv-reynolds-stress"]
                dp_y_o = data["dp-dy"]
            
            
            self.y= y_o.to_numpy().reshape(-1,1)
            self.cov= cov_o.to_numpy().reshape(-1,1)
            self.dp_y= dp_y_o.to_numpy().reshape(-1,1)
            
            
        if self.problem == 'eq1_ww':
            
            y_o = data["y-coordinate"]
            u_o = data["x-velocity"]
            du_o = data["dx-velocity-dy"]
            cov_o = data["ww-reynolds-stress"]
            dp_x_o = data["dp-dx"]
            
            self.y= y_o.to_numpy().reshape(-1,1)
            self.u = u_o.to_numpy().reshape(-1,1)
            self.du= du_o.to_numpy().reshape(-1,1)
            self.cov= cov_o.to_numpy().reshape(-1,1)
            self.dp_x= dp_x_o.to_numpy().reshape(-1,1)
            
        if self.problem == 'eq2_ww':
            
            if self.dataset == "dns" :
                
                y_o = data["y^+"]
                cov_o = data["w'w'"]
                dp_y_o = data["P"]
                
            elif self.dataset == "simulation" :
                
                y_o = data["y-coordinate"]
                cov_o = data["ww-reynolds-stress"]
                dp_y_o = data["dp-dy"]
            
            self.y= y_o.to_numpy().reshape(-1,1)
            self.cov= cov_o.to_numpy().reshape(-1,1)
            self.dp_y= dp_y_o.to_numpy().reshape(-1,1)
            
            
        if problem == 'eq1_uw':
            
            y_o = data["y-coordinate"]
            u_o = data["x-velocity"]
            du_o = data["dx-velocity-dy"]
            cov_o = data["uw-reynolds-stress"]
            dp_x_o = data["dp-dx"]
            
            self.y= y_o.to_numpy().reshape(-1,1)
            self.u = u_o.to_numpy().reshape(-1,1)
            self.du= du_o.to_numpy().reshape(-1,1)
            self.cov= cov_o.to_numpy().reshape(-1,1)
            self.dp_x= dp_x_o.to_numpy().reshape(-1,1)
            
        if problem == 'eq2_uw':
            
            
            if self.dataset == "dns" :
                
                y_o = data["y^+"]
                cov_o = data["u'w'"]
                dp_y_o = data["P"]
                
            elif self.dataset == "simulation" :
                
                y_o = data["y-coordinate"]
                cov_o = data["uw-reynolds-stress"]
                dp_y_o = data["dp-dy"]
            
            self.y= y_o.to_numpy().reshape(-1,1)
            self.cov= cov_o.to_numpy().reshape(-1,1)
            self.dp_y= dp_y_o.to_numpy().reshape(-1,1)
            
        if problem == 'eq1_vw':
            
            y_o = data["y-coordinate"]
            u_o = data["x-velocity"]
            du_o = data["dx-velocity-dy"]
            cov_o = data["vw-reynolds-stress"]
            dp_x_o = data["dp-dx"]
            
            self.y= y_o.to_numpy().reshape(-1,1)
            self.u = u_o.to_numpy().reshape(-1,1)
            self.du= du_o.to_numpy().reshape(-1,1)
            self.cov= cov_o.to_numpy().reshape(-1,1)
            self.dp_x= dp_x_o.to_numpy().reshape(-1,1)
            
        if problem == 'eq2_vw':
            
            
            if self.dataset == "dns" :
                
                y_o = data["y^+"]
                cov_o = data["v'w'"]
                dp_y_o = data["P"]
                
            elif self.dataset == "simulation" :
                
                y_o = data["y-coordinate"]
                cov_o = data["vw-reynolds-stress"]
                dp_y_o = data["dp-dy"]
            
            self.y= y_o.to_numpy().reshape(-1,1)
            self.cov= cov_o.to_numpy().reshape(-1,1)
            self.dp_y= dp_y_o.to_numpy().reshape(-1,1)
            
            
            
    def getValueConfigure(self) -> tuple[np.array]:
        
        """
            return the working values
            
            Returns : 
            
                -`y`: y coordinate
                -`cov`: covariance data
                -`dp_y`: derivative of the pression about y 
                -`dp_x`: derivative of the pression about x
                -`u` : velocity
                -`du`: dericative of the velocity about y
        """
        
        return self.y,self.cov,self.dp_y,self.dp_x,self.u,self.du
    
    def get_y(self) -> np.array : 
        
        """
            retunr y value
            
            Returns :
            
                -`y`: y coordinate
        """
        
        return self.y
    
    def getProblem(self) -> str :
        
        """
            return the problem on what we working
            
            Returns : 
                
                -`problem`: name of the problem
        """
        
        return self.problem  
    
    def getDevice(self) -> str :
        
        """
            return the availble device
            
            Returns : 
            
                -`divice`: available device
        """
        
        return self.device
    
    def getDataset(self) -> str :
        
        """
            return the type dataset choosen
            
            Returns : 
            
                -`dataset`: dataset choosen
        """
        
        return self.dataset
    
    def getMethodTrain(self) -> str :
        
        """
            return the method for pde finding
            
            Returns : 
            
                -`method_pde_find`: method we want to use
        """
        
        if self.method_pde_find == "S" : 
            
            method = "STR"
            
        elif self.method_pde_find == "L" :
            
            method = "Lasso"
        
        return method
       
    def divide(up : float, down :float, eta=1e-10) -> float:
        
        """
            return the division between two numbers
            
            Parameters : 
        
                -`up`: numerator 
                -`down`: denominator
                
            Returns : 
            
                -up/down : division between up and down
        """
        
        while np.any(down == 0):
            down += eta
        return up/down
    

class PDEFind : 
    
    """
        Classes to define the PDE 
        
        
        - derivative(x: np.array,y : np.array) -> np.array : 

            return the derivative of x about y
            
            Parameters : 
            
                -`x`: nominator
                -`y`: denominator 
                
            Returns : 
                -`d` : derivative of x about y
            
            
            
        - derivative2(x: np.array,y : np.array) -> np.array 
        
            return the second derivative of x about y
            
            Parameters :
        
                -`x`: nominator
                -`y`: denominator 
            
            Returns : 

                -`d2`: second derivative of x about y
            
            
        - AIC(w, err, AIC_ratio) 
        
            return the AIC number
            
            Parameters :
        
                -`w` : array of weights 
                
                -`err` : error 
                
                -`AIC_ratio` : AIC ratio
        
            
        - train(configure: Configure, R : np.array, W : np.array, lam : int, d_tol: int, AIC_ratio=1, maxit=10, STR_iters=10, l0_penalty=1, split=0.8, sparse='STR') 
        -> tuple[float] : 
        
            Train to find the best PDE
            
            Parameters : 

                -`config`: instance of Configure class
                -`R`: array of data
                -`W` : arrau of targets 
                -`lam` : regulation parameter
                -`d_tol` : tolerance 
                -`AIC_ratio` : AIC ratio
                -`maxit`  : maximal number of iterations
                -`STR_iters` : STRiges algorithms iterations
                -`l0_penalty` : Penalty coefficient
                -`slipt` : split training percentage
                -`sparse` : method type (STRidge, Lasso)
                
            Returns: 
                -`w_best`: best coefficient 
                -`data_err_best`: error from the best dataset
                -`mse_best`: best mse
                -`aic_best`: best aic
                
                
        - STRidge(X: np.array, y : np.array, lam: int, maxit :int , tol: int) -> np.array:
        
            return the weights of coefficients with STRidge method
        
            Parameters :
                
                -`X` : data 
                -`y` : targets
                -`lam` : regulation parameter
                -`maxit`: maximal number of iterations
                -`tol` : tolerance
            
            Retunrs : 
            
                -`w` : array of coeficients weights
                
        - lasso(X: np.array, Y: np.array, lam: int, w=np.array([0]), maxit=100) -> np.array:
            
            return the weights coefficients with Lasso method
            
            Parameters :
                
                -`X` : data 
                -`y` : targets
                -`lam` : regulation parameter
                -`w`: array of weights coefficients 
                -`maxit` : max iterations
            
            Retunrs : 
            
                -`w` : array of weights coeficients 
            
            Uses accelerated proximal gradient (FISTA) to solve Lasso
            argmin (1/2)*||Xw-Y||_2^2 + lam||w||_1
    """
    
    def derivative(x: np.array,y : np.array) -> np.array: 
        
        """
            return the derivative of x about y
            
            Parameters : 
            
                -`x`: nominator
                -`y`: denominator 
                
            Returns : 
                -`d` : derivative of x about y
        """
        
        n=x.size 
        
        d = [] 
    
        for i in range(1,n-1) : 
            
            dx = x[i+1] - x[i-1] 
            dy = y[i+1] - y[i-1]
            
            d.append(dx/dy) 
        d.append(np.array(0.0))
        d.insert(0,np.array(0.0))
        
        return np.vstack(d)
    
    
    def derivative2(x: np.array,y : np.array) -> np.array : 
        
        """
            return the second derivative of x about y
            
            Parameters :
        
                -`x`: nominator
                -`y`: denominator 
            
            Returns : 

                -`d2`: second derivative of x about y
        """
        
        n = x.size 
        
        d1 = PDEFind.derivative(x,y)
        
        d2 =[] 
        
        for i in range(2,n-2) :
            
            d2x = d1[i+1] - d1[i-1]
            
            d2y = y[i+1] - y[i-1]
            
            d2.append(d2x / d2y) 
            
        d2.append(np.array(0.0))
        d2.append(np.array(0.0))
        d2.insert(0,np.array(0.0))
        d2.insert(1,np.array(0.0))
            
        return np.array(d2)
    
    
    def AIC(w : np.array, err : float, AIC_ratio : float) -> float:
        
        """
            return the AIC number
            
            Parameters :
        
                -`w` : array of weights 
                
                -`err` : error 
                
                -`AIC_ratio` : AIC ratio
        """
        
        k = 0
        for item in w:
            if abs(item) != 0:
                k += 1
        return AIC_ratio*2*k+2*np.log(err)
    
    
    def train(config: Configure, R : np.array, W : np.array, lam : int, d_tol: int, AIC_ratio=1, maxit=10, STR_iters=10, l0_penalty=1, split=0.8) -> tuple[float]:
        """
            Train to find the best PDE
            
            Parameters : 
        
                -`config`: instance of Configure class
                -`R`: array of data
                -`W` : arrau of targets 
                -`lam` : regulation parameter
                -`d_tol` : tolerance 
                -`AIC_ratio` : AIC ratio
                -`maxit`  : maximal number of iterations
                -`STR_iters` : STRiges algorithms iterations
                -`l0_penalty` : Penalty coefficient
                -`slipt` : split training percentage
                
            Returns: 
                -`w_best`: best coefficient 
                -`data_err_best`: error from the best dataset
                -`mse_best`: best mse
                -`aic_best`: best aic
            

            This function trains a predictor using STRidge or Lasso.
            It runs over different values of tolerance and trains predictors on a training set, then evaluates them
            using a loss function on a holdout set.
        """
        
        sparse = config.getMethodTrain()

        # Split data into training and test sets
        n, _ = R.shape
        train = np.random.choice(n, int(n * split), replace=False)
        test = [i for i in np.arange(n) if i not in train]
        TrainR = R[train]
        TestR = R[test]
        TrainY = W[train]
        TestY = W[test]
        D = TrainR.shape[1]

        # Set up the initial tolerance and l0 penalty
        d_tol = float(d_tol)
        tol = d_tol
        if l0_penalty == None:
            l0_penalty = 0.001 * np.linalg.cond(R)

        try:
            # Try to compute initial coefficients
            w_best = np.linalg.lstsq(TrainR, TrainY)[0]

        except Exception:

            # Handle exceptions and ensure data type consistency
            if TrainR.dtype != np.float64:
                TrainR = TrainR.astype(np.float64)
                TestR = TestR.astype(np.float64)
            if TrainY.dtype != np.float64:
                TrainY = TrainR.astype(np.float64)
                TestY = TestR.astype(np.float64)
            w_best = np.linalg.lstsq(TrainR, TrainY)[0]

        # Calculate errors based on w_best, including data_error_best and AIC_best
        data_err_best = np.linalg.norm(TestY - TestR.dot(w_best), 2)
        err_best = np.linalg.norm(TestY - TestR.dot(w_best), 2) + l0_penalty * np.count_nonzero(w_best)
        mse_best = np.mean((TrainY - TrainR.dot(w_best)) ** 2)
        aic_best = PDEFind.AIC(w_best[:, 0], mse_best, AIC_ratio)
        tol_best = 0

        if sparse == 'STR':
            
            # Now increase tolerance until test performance decreases
            for iter in range(maxit):
                # Get a set of coefficients and error
                w = PDEFind.STRidge(R, W, lam, STR_iters, tol)
                err = np.linalg.norm(TestY - TestR.dot(w), 2) + l0_penalty * np.count_nonzero(w)
                
                # Calculate data error and MSE
                data_err = np.linalg.norm(TestY - TestR.dot(w), 2)
                mse = np.mean((TrainY - TrainR.dot(w)) ** 2)

                # Calculate AIC
                if type(w) == type(int):
                    aic = PDEFind.AIC(w, mse, AIC_ratio)
                else:
                    aic = PDEFind.AIC(w[:, 0], mse, AIC_ratio)
                    
                # Update if AIC is better
                if aic <= aic_best:
                    aic_best = aic
                    err_best = err
                    mse_best = mse
                    w_best = w
                    data_err_best = data_err
                    tol = tol + d_tol
                else:
                    # Adjust tolerance
                    tol = max([0, tol - 2 * d_tol])
                    d_tol = 2 * d_tol / (maxit - iter)
                    tol = tol + d_tol

        elif sparse == 'Lasso':
            # Use Lasso method
            w = PDEFind.lasso(R, W, lam, w=np.array([0]), maxit=maxit * 10)
            err = np.linalg.norm(W - R.dot(w), 2) + l0_penalty * np.count_nonzero(w)
            data_err_best = np.linalg.norm(W - R.dot(w), 2)
            mse_best = np.mean((TrainY - TrainR.dot(w)) ** 2)
            aic_best = PDEFind.AIC(w[:, 0], mse_best, AIC_ratio)

        return w_best, data_err_best, mse_best, aic_best
    
    
    def STRidge(X: np.array, y : np.array, lam: int, maxit :int , tol: int) -> np.array:
        """
        
        return the weights of coefficients with STRidge method
        
        Parameters :
            
            -`X` : data 
            -`y` : targets
            -`lam` : regulation parameter
            -`maxit`: maximal number of iterations
            -`tol` : tolerance
        
        Retunrs : 
        
            -`w` : array of coeficients weights
        
        Sequential Threshold Ridge Regression algorithm for finding (hopefully) sparse
        approximation to X^{-1}y.  The idea is that this may do better with correlated observables.
        This assumes y is only one column
        """
        # Get the number of samples and features
        n, d = X.shape

        # Ensure X is float64
        if X.dtype != np.float64 :
           X = X.astype(np.float64)
        
        # Ensure y is float64
        if y.dtype != np.float64 :
            y = y.astype(np.float64)
        
        # If regularization parameter is not zero, perform ridge regression
        if lam != 0:
            w = np.linalg.lstsq(X.T.dot(X) + lam * np.eye(d), X.T.dot(y))[0]
        else:
            # If regularization parameter is zero, perform simple least squares
            X = np.nan_to_num(X, nan=0)
            w = np.linalg.lstsq(X, y)[0]
        
        num_relevant = d
        biginds = np.where(abs(w) > tol)[0]
        
        # Threshold and continue
        for j in range(maxit):
            # Figure out which items to cut out
            smallinds = np.where(abs(w) < tol)[0]
            new_biginds = [i for i in range(d) if i not in smallinds]
            # If nothing changes then stop
            if num_relevant == len(new_biginds):
                break
            else:
                num_relevant = len(new_biginds)
            # Also make sure we didn't just lose all the coefficients
            if len(new_biginds) == 0:
                if j == 0:
                    return w
                else:
                    break
            biginds = new_biginds
            # Otherwise get a new guess
            w[smallinds] = 0
            if lam != 0:
                w[biginds] = np.linalg.lstsq(X[:, biginds].T.dot(X[:, biginds]) + lam * np.eye(len(biginds)), X[:, biginds].T.dot(y))[0]
            else:
                w[biginds] = np.linalg.lstsq(X[:, biginds], y)[0]
        
        # Now that we have the sparsity pattern, use standard least squares to get w
        try : 
            if biginds != []: 
                w[biginds] = np.linalg.lstsq(X[:, biginds], y)[0]
        except Exception :
            w = np.linalg.lstsq(X, y)[0]

        return w
    

    def lasso(X: np.array, Y: np.array, lam: int, w=np.array([0]), maxit=100) -> np.array:
        """
        return the weights coefficients with Lasso method
        
        Parameters :
            
            -`X` : data 
            -`y` : targets
            -`lam` : regulation parameter
            -`w`: array of weights coefficients 
            -`maxit` : max iterations
        
        Retunrs : 
        
            -`w` : array of weights coeficients 
        
        Uses accelerated proximal gradient (FISTA) to solve Lasso
        argmin (1/2)*||Xw-Y||_2^2 + lam||w||_1
        """
        # Obtain size of X
        n, d = X.shape
        Y = Y.reshape(n, 1)
        # Create w if none is given
        if w.size != d:
            w = np.zeros((d, 1))
        w_old = np.zeros((d, 1))
        X = X
        # Lipschitz constant of gradient of smooth part of loss function
        L = np.linalg.norm(X.T.dot(X), 2)
        # Now loop until converged or max iterations
        for iters in range(0, maxit):
            # Update w
            z = w + iters / float(iters + 1) * (w - w_old)
            w_old = w
            z = z - X.T.dot(X.dot(z) - Y) / L
            for j in range(d):
                w[j] = np.multiply(np.sign(z[j]), np.max([abs(z[j]) - lam / L, np.zeros_like(abs(z[j]) - lam / L)]))
        # Now that we have the sparsity pattern, used least squares.
        biginds = (np.where(w != 0)[0]).reshape(-1,1)
        if biginds != []:
            w[biginds] = np.linalg.lstsq(X[:, biginds], Y)[0]
        # Finally, reverse the regularization so as to be able to use with raw data
        return w
    

class Setup : 
    
    """
        Class to setup the value for the creation of PDE
        
        - _init_(self) -> None : 
        
            Define the dictionnary to complete PDE
            
            Parameters : 
            
                -`config`: Instance of Configure class
            
        - getDict(self) -> tuple[dict] :
        
            return the dictionnary of values 
            
            Returns : 
            
                -`ALL` : all the value of the other dictionnary
                -`OPS`: possible operation
                -`OP1`: first type of operations
                -`OP2` : second type of operations
                -`VARS`: Varibale possible to include in the PDE 
                -`den`: denominator possible
        
        - getLib(self) -> tuple[list] : 
        
            return useful library 
            
            Returns : 

                -`pde_lib`: list to stock the diffirent pde 
                -`err_lib`: list to stock the error
                
        - getResultVariable(self) -> tuple[np.array] :

            return possible target variables 
            
            Returns : 

                -`covy`: derivative of the covariance about y 
                -`uyy`: second derivative of u about y
                
                
        - getResultDerivative(self) -> tuple[np.array] : 
        
            return derivative and nu 
            
            Returns : 

                -`dpx`: derivative of the pressure about x
                -`dpy`: derivative of the pressure about y
                -`covy`: derivative of the covariance about y 
                

        
        - getDefault(self) -> tuple[np.array, np.array, int] :
            return default elements 
            
            Returns : 

                -`default_terms`: default terms of variable in pde
                -`default_names`: names of the default variable
                -`num_default` : number of default names
            
    """
    
    def __init__(self,config) -> None:
        
        """
            Define the dictionnary to complete PDE
            
            Parameters : 
            
                -`config`: Instance of Configure class
        """
        
        self.y,self.cov,self.dp_y,self.dp_x,self.u,self.du = config.getValueConfigure()
        
        self.problem = config.getProblem()
        
        self.dataset = config.getDataset()
        
                
        self.covy = np.zeros(self.y.shape)
        self.uyy= np.zeros(self.y.shape)
        
        self.dpy = np.zeros(self.y.shape)
        self.dpx = np.zeros(self.y.shape)
        
        self.default_terms = np.zeros(self.y.shape)
        self.default_names = ""
        self.num_default = 0
        
        if self.problem == "eq1_uu" :
        
            n, m = self.cov.shape
            
            ones = (np.ones(self.cov.shape).flatten()).reshape(-1,1)
                    
            self.covy = (PDEFind.derivative(self.cov, self.y)).reshape(-1,1)
            
            self.dpx = (self.dp_x).reshape(-1,1)
                
            
            self.uyy = (PDEFind.derivative(self.du, self.y)).reshape(-1,1)
            
            
            default_covy = np.reshape(self.covy, (self.covy.shape[0]*self.covy.shape[1], 1))
            default_dpx = np.reshape(self.dpx, (self.dpx.shape[0]*self.dpx.shape[1], 1))
            default_y = np.reshape(self.y, (self.y.shape[0]*self.y.shape[1], 1))
            default_uyy = np.reshape(self.uyy,(self.uyy.shape[0],1))
            self.default_terms = np.hstack((default_dpx,default_covy))
            self.default_names = ["dp/dx","(u'u')'"]
            self.num_default = self.default_terms.shape[1]
            
            
            self.ALL = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
                "dp/dx": {'0': 0, '1': self.dpx},
                "(u'u')'": {'0': 0, '1': self.covy},
                '1': {'0': 0, '1': ones},
            }

            self.OPS = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.ROOT = {
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.OP1 = {
                '1': {'0': 0, '1': 1}
            }

            self.OP2 = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.VARS = {
                "dp/dx": {'0': 0, '1': self.dpx},
                "(u'u')'": {'0': 0, '1': self.covy}
            }

            self.den = {
                '1': {'0': 0, '1': ones}   
            }
    
        if self.problem == "eq1_vv" :
        
            n, m = self.cov.shape
            
            ones = (np.ones(self.cov.shape).flatten()).reshape(-1,1)
                    
            self.covy = (PDEFind.derivative(self.cov, self.y)).reshape(-1,1)
            
            self.dpx = (self.dp_x).reshape(-1,1)    
            
            self.uyy = (PDEFind.derivative(self.du, self.y)).reshape(-1,1)
            
            
            default_covy = np.reshape(self.covy, (self.covy.shape[0]*self.covy.shape[1], 1))
            default_dpx = np.reshape(self.dpx, (self.dpx.shape[0]*self.dpx.shape[1], 1))
            default_y = np.reshape(self.y, (self.y.shape[0]*self.y.shape[1], 1))
            default_uyy = np.reshape(self.uyy,(self.uyy.shape[0],1))
            self.default_terms = np.hstack((default_dpx,default_covy))
            self.default_names = ["dp/dx","(u'v')'"]
            self.num_default = self.default_terms.shape[1]
            
            
            self.ALL = {
            '+': {'0': 2, '1': np.add},
            '-': {'0': 2, '1': np.subtract},
            '*': {'0': 2, '1': np.multiply},
            '/': {'0': 2, '1': Configure.divide},
            "dp/dx": {'0': 0, '1': self.dpx},
            "(v'v')'": {'0': 0, '1': self.covy},
            '1': {'0': 0, '1': ones},
            }

            self.OPS = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.ROOT = {
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.OP1 = {
                '1': {'0': 0, '1': 1}
            }

            self.OP2 = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.VARS = {
                "dp/dx": {'0': 0, '1': self.dpx},
                "(v'v')'": {'0': 0, '1': self.covy}
            }

            self.den = {
                '1': {'0': 0, '1': ones}   
            }
            
        if self.problem == "eq1_ww" :
        
            n, m = self.cov.shape
            
            ones = (np.ones(self.cov.shape).flatten()).reshape(-1,1)
                    
            self.covy = (PDEFind.derivative(self.cov, self.y)).reshape(-1,1)
            
            self.dpx = (self.dp_x).reshape(-1,1)    
            
            self.uyy = (PDEFind.derivative(self.du, self.y)).reshape(-1,1)

            
            default_covy = np.reshape(self.covy, (self.covy.shape[0]*self.covy.shape[1], 1))
            default_dpx = np.reshape(self.dpx, (self.dpx.shape[0]*self.dpx.shape[1], 1))
            default_y = np.reshape(self.y, (self.y.shape[0]*self.y.shape[1], 1))
            default_uyy = np.reshape(self.uyy,(self.uyy.shape[0],1))
            self.default_terms = np.hstack((default_dpx,default_covy))
            self.default_names = ["dp/dx","(u'v')'"]
            self.num_default = self.default_terms.shape[1]
            
            
            ALL = {
            '+': {'0': 2, '1': np.add},
            '-': {'0': 2, '1': np.subtract},
            '*': {'0': 2, '1': np.multiply},
            '/': {'0': 2, '1': Configure.divide},
            "dp/dx": {'0': 0, '1': self.dpx},
            "(w'w')'": {'0': 0, '1': self.covy},
            '1': {'0': 0, '1': ones},
            }

            self.OPS = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.ROOT = {
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.OP1 = {
                '1': {'0': 0, '1': 1}
            }

            self.OP2 = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.VARS = {
                "dp/dx": {'0': 0, '1': self.dpx},
                "(w'w')'": {'0': 0, '1': self.covy}
            }

            self.den = {
                '1': {'0': 0, '1': ones},  
            }
            
        if self.problem == "eq1_uv" :
        
            n, m = self.cov.shape
            
            ones = (np.ones(self.cov.shape).flatten()).reshape(-1,1)
                    
            self.covy = (PDEFind.derivative(self.cov, self.y)).reshape(-1,1)
            
            self.dpx = (self.dp_x).reshape(-1,1)
            
            self.uyy = (PDEFind.derivative(self.du, self.y)).reshape(-1,1)
            
            
            default_covy = np.reshape(self.covy, (self.covy.shape[0]*self.covy.shape[1], 1))
            default_dpx = np.reshape(self.dpx, (self.dpx.shape[0]*self.dpx.shape[1], 1))
            default_y = np.reshape(self.y, (self.y.shape[0]*self.y.shape[1], 1))
            default_uyy = np.reshape(self.uyy,(self.uyy.shape[0],1))
            self.default_terms = np.hstack((default_dpx,default_covy))
            self.default_names = ["dp/dx","(u'v')'"]
            self.num_default = self.default_terms.shape[1]
            
            
            self.ALL = {
            '+': {'0': 2, '1': np.add},
            '-': {'0': 2, '1': np.subtract},
            '*': {'0': 2, '1': np.multiply},
            '/': {'0': 2, '1': Configure.divide},
            "dp/dx": {'0': 0, '1': self.dpx},
            "(u'v')'": {'0': 0, '1': self.covy},
            '1': {'0': 0, '1': ones}
            }

            self.OPS = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.ROOT = {
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.OP1 = {
                '1': {'0': 0, '1': 1}
            }

            self.OP2 = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.VARS = {
                "dp/dx": {'0': 0, '1': self.dpx},
                "(u'v')'": {'0': 0, '1': self.covy}
            }

            self.den = {
                '1': {'0': 0, '1': ones} 
            }


        if self.problem == "eq1_vw" :
        
            n, m = self.cov.shape
            
            ones = (np.ones(self.cov.shape).flatten()).reshape(-1,1)
                    
            self.covy = (PDEFind.derivative(self.cov, self.y)).reshape(-1,1)
            
            self.dpx = (self.dp_x).reshape(-1,1) 
            
            self.uyy = (PDEFind.derivative(self.du, self.y)).reshape(-1,1)
            
            
            default_covy = np.reshape(self.covy, (self.covy.shape[0]*self.covy.shape[1], 1))
            default_dpx = np.reshape(self.dpx, (self.dpx.shape[0]*self.dpx.shape[1], 1))
            default_y = np.reshape(self.y, (self.y.shape[0]*self.y.shape[1], 1))
            default_uyy = np.reshape(self.uyy,(self.uyy.shape[0],1))
            self.default_terms = np.hstack((default_dpx,default_covy))
            self.default_names = ["dp/dx","(v'w')'"]
            self.num_default = self.default_terms.shape[1]
            
            
            self.ALL = {
            '+': {'0': 2, '1': np.add},
            '-': {'0': 2, '1': np.subtract},
            '*': {'0': 2, '1': np.multiply},
            '/': {'0': 2, '1': Configure.divide},
            "dp/dx": {'0': 0, '1': self.dpx},
            "(v'w')'": {'0': 0, '1': self.covy},
            '1': {'0': 0, '1': ones},
            }

            self.OPS = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.ROOT = {
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.OP1 = {
                '1': {'0': 0, '1': 1}
            }

            self.OP2 = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.VARS = {
                "dp/dx": {'0': 0, '1': self.dpx},
                "(v'w')'": {'0': 0, '1': self.covy}
            }

            self.den = {
                '1': {'0': 0, '1': ones},  
            }
            
        
        if self.problem == "eq1_uw" :
        
            n, m = self.cov.shape
            
            ones = (np.ones(self.cov.shape).flatten()).reshape(-1,1)
                    
            self.covy = (PDEFind.derivative(self.cov, self.y)).reshape(-1,1)
            
            self.dpx = (self.dp_x).reshape(-1,1)  
            
            self.uyy = (PDEFind.derivative(self.du, self.y)).reshape(-1,1)
            
            
            default_covy = np.reshape(self.covy, (self.covy.shape[0]*self.covy.shape[1], 1))
            default_dpx = np.reshape(self.dpx, (self.dpx.shape[0]*self.dpx.shape[1], 1))
            default_y = np.reshape(self.y, (self.y.shape[0]*self.y.shape[1], 1))
            default_uyy = np.reshape(self.uyy,(self.uyy.shape[0],1))
            self.default_terms = np.hstack((default_dpx,default_covy))
            self.default_names = ["dp/dx","(u'w')'"]
            self.num_default = self.default_terms.shape[1]
            
            self.ALL = {
            '+': {'0': 2, '1': np.add},
            '-': {'0': 2, '1': np.subtract},
            '*': {'0': 2, '1': np.multiply},
            '/': {'0': 2, '1': Configure.divide},
            "dp/dx": {'0': 0, '1': self.dpx},
            "(u'w')'": {'0': 0, '1': self.covy},
            '1': {'0': 0, '1': ones},
            }

            self.OPS = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.ROOT = {
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.OP1 = {
                '1': {'0': 0, '1': 1}
            }

            self.OP2 = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.VARS = {
                "dp/dx": {'0': 0, '1': self.dpx},
                "(u'w')'": {'0': 0, '1': self.covy}
            }

            self.den = {
                '1': {'0': 0, '1': ones},   
            }
            
            
        if "eq2" in self.problem :
        
            n, m = self.cov.shape
            
            ones = (np.ones(self.cov.shape).flatten()).reshape(-1,1)
                    
            self.covy = (PDEFind.derivative(self.cov, self.y)).reshape(-1,1)
            
            if self.dataset == "simulation " :
            
                self.dpy = (self.dp_y).reshape(-1,1)  
            
            elif self.dataset =="dns":
            
                self.dpy =  (PDEFind.derivative(self.dp_y, self.y)).reshape(-1,1)  
                
            
            default_covy = np.reshape(self.covy, (self.covy.shape[0]*self.covy.shape[1], 1))
            default_py = np.reshape(self.dpy, (self.dpy.shape[0]*self.dpy.shape[1], 1))
            default_y = np.reshape(self.y, (self.y.shape[0]*self.y.shape[1], 1))
            self.default_terms = np.hstack((default_py)).reshape(-1,1)
            self.default_names = ["dp/dy"]
            self.num_default = self.default_terms.shape[1]
            
            
            self.ALL = {
            '+': {'0': 2, '1': np.add},
            '-': {'0': 2, '1': np.subtract},
            '*': {'0': 2, '1': np.multiply},
            '/': {'0': 2, '1': Configure.divide},
            "dp/dy": {'0': 0, '1': self.dpy},
            '1': {'0': 0, '1': ones},
            }

            self.OPS = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.ROOT = {
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.OP1 = {
                '1': {'0': 0, '1': ones},
            }

            self.OP2 = {
                '+': {'0': 2, '1': np.add},
                '-': {'0': 2, '1': np.subtract},
                '*': {'0': 2, '1': np.multiply},
                '/': {'0': 2, '1': Configure.divide},
            }

            self.VARS = {
                "dp/dy": {'0': 0, '1': self.dpy},
                "1" : {'0': 0, '1': ones},
            }

            self.den = {
                "1" : {'0': 0, '1': ones}    
            }
        
    
    def getDict(self) -> tuple[dict] :
        
        """
            return the dictionnary of values 
            
            Returns : 
            
                -`ALL` : all the value of the other dictionnary
                -`OPS`: possible operation
                -`ROOT`: root operations
                -`OP1`: first type of operations
                -`OP2` : second type of operations
                -`VARS`: Varibale possible to include in the PDE 
                -`den`: denominator possible
        """
        
        return self.ALL, self.OPS, self.ROOT, self.OP1, self.OP2, self.VARS, self.den
    
    
    def setLib(self,element_pde_lib,element_err_lib) -> None :
        
        self.pde_lib.append(element_pde_lib)
        self.err_lib.append(element_err_lib)
    
    
    def getResultVariable(self) -> tuple[np.array] :
        
        """
            return possible target variables 
            
            Returns : 

                -`covy`: derivative of the covariance about y 
                -`uyy`: second derivative of u about y
        """
        
        return self.covy, self.uyy
    
    def getResultDerivative(self) -> tuple[np.array] : 
        
        """
            return derivative
            
            Returns : 

                -`dpx`: derivative of the pressure about x
                -`dpy`: derivative of the pressure about y
                -`covy`: derivative of the covariance about y 
                -`nu`: kinematic viscosity
        """
        
        return self.dpx,self.dpy,self.covy
    
    def getDefault(self) -> tuple[np.array, np.array, int] :
        
        """
            return default elements 
            
            Returns : 

                -`default_terms`: default terms of variable in pde
                -`default_names`: names of the default variable
                -`num_default` : number of default names
        """
        
        return self.default_terms, self.default_names, self.num_default
    
    
class Tree : 
    
    """
        Define the Tree architecture
        
        - __init__(self, max_depth : int, p_var: float, setup: Setup) -> None:
        
            Initializes a tree with specified parameters and generates nodes based on certain rules.

            Parameters:
                - `max_depth`: Maximum depth of the tree.
                - `p_var`: Probability of generating a variable node instead of an operation node.
                - `setup`: instance of Setup class.
                
                
        - dfs(ret : list, a_tree : list, depth : int, idx: int) -> None:
        
            Performs an auxiliary pre-order traversal of the tree.

            Parameters:
                - `ret`: List to store the pre-order traversal sequence.
                - `a_tree`: The tree structure containing nodes.
                - `depth`: The depth of the current node.
                - `idx`: The index of the current node at its depth.
                
                
        - tree2strMerge(a_tree: list) -> str:
        
            Converts the tree structure into a string representation.

            Parameters:
                -`a_tree`: List representing the tree structure.

            Returns:
                -`str`: String representation of the tree.
                
        
        - mutate(self, p_mute : float, VARS: dict, OP1: dict, OP2: dict, den: dict) -> None:
        
            Mutates nodes in the original tree with a certain probability.

            Parameters:
                -`p_mute`: Probability of mutation.
                -`VARS`: Dictionary containing variable.
                -`OP1`: Dictionary containing unary operator.
                -`OP2`: Dictionary containing binary operator.
                -`den`: Dictionary containing denominator.

    """
    
    
    def __init__(self, max_depth : int, p_var: float, setup: Setup) -> None:
        """
            Initializes a tree with specified parameters and generates nodes based on certain rules.

            Parameters:
                - `max_depth`: Maximum depth of the tree.
                - `p_var`: Probability of generating a variable node instead of an operation node.
                - `setup`: instance of Setup class.
        """
        # Initialize class attributes
        self.max_depth = max_depth
        self.tree = [[] for i in range(max_depth)]  # List of lists to store tree nodes at each depth
        self.preorder, self.inorder = None, None  # Initialize preorder and inorder representations of the tree
        
        # Extract setup data
        self.ALL, self.OPS, self.ROOT, self.OP1, self.OP2, self.VARS, self.den = setup.getDict()
        
        
        # Randomly generate the initial root (an operation)
        root_key = random.choice(list(self.ROOT.keys()))
        root = self.ROOT[root_key]
        # Set initial node
        node = Node(depth=0, idx=0, parent_idx=None, name=root_key, var=root['1'], full=root,
                    child_num=int(root['0']), child_st=0)
        # Add initial node to the tree
        self.tree[0].append(node)

        depth = 1
        while depth < max_depth:
            next_cnt = 0  # child_st=next_cnt: the starting point of the current child node in the next layer
            # Generate child nodes for each parent node
            for parent_idx in range(len(self.tree[depth - 1])):
                parent = self.tree[depth - 1][parent_idx]  # Extract parent node
                # Skip if the parent node has no child nodes
                if parent.child_num == 0:
                    continue
                # Generate child nodes based on rules
                for j in range(parent.child_num):
                    if depth == max_depth - 1:  # Rule 1: Bottom layer must be var, not op
                        node_key = random.choice(list(self.VARS.keys()))
                        node = self.VARS[node_key]
                        node = Node(depth=depth, idx=len(self.tree[depth]), parent_idx=parent_idx, name=node_key,
                                    var=node['1'], full=node, child_num=int(node['0']), child_st=None)
                        self.tree[depth].append(node)
                    else:
                        # Rule 2: Generate var or op based on probability
                        if np.random.random() <= p_var:
                            node_key = random.choice(list(self.VARS.keys()))
                            node = self.VARS[node_key]
                            node = Node(depth=depth, idx=len(self.tree[depth]), parent_idx=parent_idx, name=node_key,
                                        var=node['1'], full=node, child_num=int(node['0']), child_st=None)
                            self.tree[depth].append(node)
                        else:
                            node_key = random.choice(list(self.OPS.keys()))
                            node = self.OPS[node_key]
                            node = Node(depth=depth, idx=len(self.tree[depth]), parent_idx=parent_idx, name=node_key,
                                        var=node['1'], full=node, child_num=int(node['0']), child_st=next_cnt)
                            next_cnt += node.child_num
                            self.tree[depth].append(node)
            depth += 1

        # Perform depth-first search to construct preorder representation of the tree
        ret = []
        Tree.dfs(ret, self.tree, depth=0, idx=0)
        self.preorder = ' '.join([x for x in ret])
        # Deep copy the tree and construct inorder representation
        model_tree = copy.deepcopy(self.tree)
        self.inorder = Tree.tree2strMerge(model_tree)

        
        
    def dfs(ret : list, a_tree : list, depth : int, idx: int) -> None:
        """
            Performs an auxiliary pre-order traversal of the tree.

            Parameters:
                - `ret`: List to store the pre-order traversal sequence.
                - `a_tree`: The tree structure containing nodes.
                - `depth`: The depth of the current node.
                - `idx`: The index of the current node at its depth.

        """
        node = a_tree[depth][idx]  # Get the current node
        ret.append(node.name)  # Append the name of the current node to the pre-order traversal sequence
        # Traverse the children of the current node
        for ix in range(node.child_num):
            if node.child_st is None:
                continue
            # Recursively traverse the tree starting from the next child node
            Tree.dfs(ret, a_tree, depth+1, node.child_st + ix)
            
    
    def tree2strMerge(a_tree: list) -> str:
        """
            Converts the tree structure into a string representation.

            Parameters:
                -`a_tree`: List representing the tree structure.

            Returns:
                -`str`: String representation of the tree.
        """
        
        # Traverse the tree in reverse order
        for i in range(len(a_tree) - 1, 0, -1):
            for node in a_tree[i]:
                # Check if the node is not processed yet
                if node.status == 0:
                    # Check the status of the parent node
                    if a_tree[node.depth-1][node.parent_idx].status == 1:
                        # If the parent node has one child, append the current node's name to it
                        if a_tree[node.depth-1][node.parent_idx].child_num == 2:
                            a_tree[node.depth-1][node.parent_idx].name = a_tree[node.depth-1][node.parent_idx].name + ' ' + node.name + ')'
                        else:
                            a_tree[node.depth-1][node.parent_idx].name = '( ' + a_tree[node.depth-1][node.parent_idx].name + ' ' + node.name + ')'
                    # If the parent node has more than one child, prepend the current node's name to it
                    elif a_tree[node.depth-1][node.parent_idx].status > 1:
                        a_tree[node.depth-1][node.parent_idx].name = '(' + node.name + ' ' + a_tree[node.depth-1][node.parent_idx].name
                    # Decrement the status of the parent node
                    a_tree[node.depth-1][node.parent_idx].status -= 1
        # Return the string representation of the root node
        return a_tree[0][0].name


    def mutate(self, p_mute : float) -> None:
        """
            Mutates nodes in the original tree with a certain probability.

            Parameters:
                -`p_mute`: Probability of mutation.
                -`VARS`: Dictionary containing variable.
                -`OP1`: Dictionary containing unary operator.
                -`OP2`: Dictionary containing binary operator.
                -`den`: Dictionary containing denominator.

        """
        # Deep copy of the original tree for visualization
        global see_tree
        see_tree = copy.deepcopy(self.tree)
        
        # Start mutation process
        depth = 1
        while depth < self.max_depth:
            next_cnt = 0
            idx_this_depth = 0  # Index of the node at this depth
            for parent_idx in range(len(self.tree[depth - 1])):
                parent = self.tree[depth - 1][parent_idx]
                if parent.child_num == 0:
                    continue
                for j in range(parent.child_num):  # Iterate over children of the parent
                    # Decide whether to mutate the current node based on the mutation probability
                    not_mute = np.random.choice([True, False], p=([1 - p_mute, p_mute]))
                    
                    # Skip if not mutated
                    if not_mute:
                        next_cnt += self.tree[depth][parent.child_st + j].child_num
                        continue
                    
                    # Retrieve information about the current node
                    current = self.tree[depth][parent.child_st + j]
                    temp = self.tree[depth][parent.child_st + j].name
                    num_child = current.child_num  # Number of child nodes of the current node
                    
                    # Mutate leaf node (variable)
                    if num_child == 0:
                        node_key = random.choice(list(self.VARS.keys()))
                        node = self.VARS[node_key]
                        new_node = Node(depth=depth, idx=idx_this_depth, parent_idx=parent_idx, name=node_key,
                                        var=node['1'], full=node, child_num=int(node['0']), child_st=None)
                        self.tree[depth][parent.child_st + j] = new_node
                    
                    # Mutate non-leaf node (operator)
                    else:
                        if num_child == 1:
                            node_key = random.choice(list(self.OP1.keys()))
                            node = self.OP1[node_key]
                            while node_key == temp:  # Avoid repetition
                                node_key = random.choice(list(self.OP1.keys()))
                                node = self.OP1[node_key]
                        elif num_child == 2:
                            node_key = random.choice(list(self.OP2.keys()))
                            node = self.OP2[node_key]
                            right = self.tree[depth + 1][current.child_st + 1].name
                            while node_key == temp or (node_key in {'d', 'd^2'} and right not in list(Setup.den.keys())):
                                node_key = np.random.choice(list(self.OP2.keys()))
                                node = self.OP2[node_key]
                        else:
                            raise NotImplementedError("Error occurs!")

                        # Create new node with mutated operator
                        new_node = Node(depth=depth, idx=idx_this_depth, parent_idx=parent_idx, name=node_key,
                                        var=node['1'], full=node, child_num=int(node['0']), child_st=next_cnt)
                        next_cnt += new_node.child_num
                        self.tree[depth][parent.child_st + j] = new_node
                    idx_this_depth += 1
            depth += 1

        # Generate preorder and inorder representations of the mutated tree
        ret = []
        Tree.dfs(ret, self.tree, depth=0, idx=0)
        self.preorder = ' '.join([x for x in ret])
        model_tree = copy.deepcopy(self.tree)
        self.inorder = Tree.tree2strMerge(model_tree)
    
    
class PDE:
    
    """
        Class to evaluate PDE
        
        - __init__(self, depth : int, max_width : int, p_var: float, setup : Setup, config: Configure) ->None : 
        
            Initializes PDE evaluation with the creation of tree architecture.

            Parameters:
                -`depth`: depth of the tree.
                -`max_width`: maximum width of the tree.
                -`p_var`: probability of selecting a variable node during mutation.
                -`setup`: instance of Setup class.
                -`config`: instance of Configure class.
                
        - mutate(self, p_mute: float) -> None:
        
            Mutates each element of the tree with a certain mutation probability.

            Parameters:
                -`p_mute`: probability of mutation for each node
                
        
        - replace(self) -> None:
        
            Replaces a randomly selected element of the tree with a new Tree object.
            
        
        - visualize(self) -> str : 
        
            Generates a representation of the terms produced by the Simple Genetic Algorithm (SGA),
            including all generated terms without removing those with small coefficients.

            Returns:
                -`name`: string representing the generated terms.
                
                
        - conciseVisualize(self, config: Configure) -> str:
        
            Generates a concise representation of all terms, including those from the fixed candidate set and SGA.
            
            Parameters: 
            
                -`config`: instance of Configure class

            Returns:
                -`name`:string representing all terms, including coefficients and their sources.
                
                
        - evaluateMse(self,config: Configure, a_pde: float, is_term=False) -> tuple[np.array] : 
        
            Evaluates the mean squared error (MSE) of the provided partial differential equation (PDE) terms.

            Parameters:
            
                -`config`: instance of Configure class
                -`PDE_terms`: list of PDE terms.
                -`is_term`: indicates whether the input is a list of PDE terms. Defaults to False.

            Returns:
                tuple or float: If 'is_term' is True, returns a tuple containing the processed PDE terms, optimal weights, and MSE.
                                If 'is_term' is False, returns AIC, optimal weights, and MSE.
    """
    
    def __init__(self, depth : int, max_width : int, p_var: float, setup : Setup, config: Configure) ->None:
        """
            Initializes PDE evaluation with the creation of tree architecture.

            Parameters:
                -`depth`: depth of the tree.
                -`max_width`: maximum width of the tree.
                -`p_var`: probability of selecting a variable node during mutation.
                -`setup`: instance of Setup class.
                -`config`: instance of Configure class.
        """
        # Initialize the tree structure setup dictionaries
        self.ALL, self.OPS, self.ROOT, self.OP1, self.OP2, self.VARS, self.den = setup.getDict()
        
        
        # Get the problem type from the configuration
        self.problem = config.getProblem()
        
        # Get result variables (covy and uyy) from the setup
        self.covy, self.uyy = setup.getResultVariable()
        
        # Define Setup instance
        self.setup= setup 
        self.config= config
        
        # Get default terms, names, and number of default terms from the setup
        self.default_terms, self.default_names, self.num_default = setup.getDefault()
        
        # Set depth, probability of selecting a variable node, and random width
        self.depth = depth
        self.p_var = p_var
        self.W = np.random.randint(max_width) + 1  # Random width from 1 to max_width
        
        # Initialize elements of the tree using recursion
        self.elements = [Tree(depth, p_var, setup) for _ in range(self.W)]


    def mutate(self, p_mute: float) -> None:
        """
            Mutates each element of the tree with a certain mutation probability.

            Parameters:
                -`p_mute`: probability of mutation for each node.
        """
        
        for i in range(0, self.W):  # Loop through each element of the tree
            # Mutate the current element with the given mutation probability
            self.elements[i].mutate(p_mute)
            

    def replace(self) -> None:
        """
            Replaces a randomly selected element of the tree with a new Tree object.
        """
        if self.W == 0:  # If the tree has no elements
            w = 1  # Set the number of elements to 1
        else: 
            w = self.W  # Otherwise, use the current number of elements

        # Randomly select an index within the range of the number of elements
        ix = np.random.randint(w)
        
        # Replace the selected element with a new Tree object with the same depth and probability of selecting a variable node
        self.elements[ix] = Tree(self.depth, self.p_var, self.setup)

    
    def visualize(self) -> str:
        """
            Generates a representation of the terms produced by the Simple Genetic Algorithm (SGA),
            including all generated terms without removing those with small coefficients.

            Returns:
                -`name`: string representing the generated terms.
        """
        name = ''  # Initialize an empty string to store the generated terms
        for i in range(len(self.elements)):  # Iterate through all generated elements
            if i != 0:
                name += '+'  # Add a '+' sign between terms, except for the first term
            name += self.elements[i].inorder  # Add the generated term to the string
        return name 


    def conciseVisualize(self) -> str:
        """
            Generates a concise representation of all terms, including those from the fixed candidate set and SGA.
            
            Parameters: 
            
                -`config`: instance of Configure class 

            Returns:
                -`name`:string representing all terms, including coefficients and their sources.
        """
        name = ''  # Initialize an empty string to store the concise representation
        elements = copy.deepcopy(self.elements)  # Create a deep copy of the generated elements
        elements, coefficients, mse = PDE.evaluateMse(elements,config=self.config,setup=self.setup, is_term=True)  # Evaluate mean squared error and coefficients
        coefficients = coefficients[:, 0]  # Extract coefficients
        
        for i in range(len(coefficients)):  # Iterate through all coefficients
            if np.abs(coefficients[i]) < 1e-4 and self.problem != "eq2_uw" and self.problem != "eq2_vw" and "eq1" not in self.problem:
                # Ignore coefficients that are too small under certain conditions
                continue
            if i != 0 and name != '':  # Add a '+' sign between terms, except for the first term
                name += ' + '
            name += str(round(np.real(coefficients[i]), 4))  # Add the coefficient to the string
            
            if i < self.num_default:  # Check if the term comes from the preset candidate set
                
                name += self.default_names[i]  # Add the preset candidate name
            else:
                
                name += elements[i - self.num_default].inorder  # Add the SGA-generated candidate term using 'inorder'
                
        return name

    
    def evaluateMse(a_pde,config: Configure, setup, is_term=False) -> tuple[np.array]:
        """
            Evaluates the mean squared error (MSE) of the provided partial differential equation (PDE) terms.

            Parameters:
            
                -`config`: instance of Configure class
                -`PDE_terms`: list of PDE terms.
                -`is_term`: indicates whether the input is a list of PDE terms. Defaults to False.

            Returns:
                tuple or float: If 'is_term' is True, returns a tuple containing the processed PDE terms, optimal weights, and MSE.
                                If 'is_term' is False, returns AIC, optimal weights, and MSE.

        """
        if is_term == True:
            terms = a_pde  # Use the provided PDE terms
        else:
            terms = a_pde.elements  # Use the PDE elements from the PDE
        # Initialize terms_values array based on the problem type
        if "eq2" in config.problem:
            terms_values = np.zeros((setup.covy.shape[0], len(terms)))
        elif "eq1" in config.problem:
            terms_values = np.zeros((setup.uyy.shape[0], len(terms)))
        else:
            NotImplementedError("Unknown problem type!")

        delete_ix = []  # Initialize a list to store indices of terms to be deleted

        # Iterate through each term in the provided PDE terms
        for ix, term in enumerate(terms):
            tree_list = term.tree
            max_depth = len(tree_list)

            # Traverse the tree from bottom to top, processing each node's cache
            for i in range(2, max_depth + 1):
                if len(tree_list[-i + 1]) == 0:
                    continue
                else:
                    for j in range(len(tree_list[-i])):
                        if tree_list[-i][j].child_num == 0:
                            continue
                        elif tree_list[-i][j].child_num == 1:
                            try:
                                child_node = tree_list[-i + 1][tree_list[-i][j].child_st]
                                tree_list[-i][j].cache = tree_list[-i][j].cache(child_node.cache)
                                child_node.cache = child_node.var
                            except:
                                continue
                        elif tree_list[-i][j].child_num == 2:
                            child1 = tree_list[-i + 1][tree_list[-i][j].child_st]
                            child2 = tree_list[-i + 1][tree_list[-i][j].child_st + 1]
                            if isfunction(child1.cache) or isfunction(child2.cache):
                                continue
                            tree_list[-i][j].cache = tree_list[-i][j].cache(child1.cache, child2.cache)
                            child1.cache, child2.cache = child1.var, child2.var
                        else:
                            NotImplementedError()

            # Check if the term has converged (all zeros in cache)
            if not any(tree_list[0][0].cache.reshape(-1)):
                delete_ix.append(ix)
                tree_list[0][0].cache = tree_list[0][0].var  # Reset cache
            else:
                # Store the merged term in terms_values
                terms_values[:, ix:ix + 1] = tree_list[0][0].cache.reshape(-1, 1)
                tree_list[0][0].cache = tree_list[0][0].var  # Reset cache

        move = 0  # Counter to adjust indices after deletion
        for ixx in delete_ix:
            if is_term == True:
                terms.pop(ixx - move)
            else:
                a_pde.elements.pop(ixx - move)
                a_pde.W -= 1  # Decrease actual width by one
            terms_values = np.delete(terms_values, ixx - move, axis=1)
            move += 1  # Shift indices after deletion

        # Check for infinity, NaN, or empty terms_values
        if False in np.isfinite(terms_values) or terms_values.shape[1] == 0:
            error = np.inf
            aic = np.inf
            w = 0
            mse = np.inf
        else:
            # Concatenate default terms with the processed terms_values
            if "eq1" in config.problem:
                terms_values = np.hstack((setup.default_terms, terms_values))
                w, loss, mse, aic = PDEFind.train(config,terms_values, setup.uyy, 0, 1)
            if "eq2" in config.problem:
                terms_values = np.hstack((setup.default_terms, terms_values))
                w, loss, mse, aic = PDEFind.train(config,terms_values, setup.covy, 0, 1)

        
        if is_term:
            return terms, w, mse
        else:
            return aic, w , mse
        

class SGA :
    
    """
        Class used to initialise and run the SGA analysis
        
        - __init__(self, num: int, depth: int , width: int, p_var: float, p_mute: float, p_rep: float, p_cro: float, problem: str, reynold_number: int, 
                dataset: str) -> None:
                
            Initialise the SGA analysis
            
            Parameters : 
                -`num`: number of PDEs to generate
                -`depth`: depth of the tree
                -`width`: width of the tree
                -`p_var`: variation probability
                -`p_mute: mutation probability
                -`p_rep`: reproduction probabikity
                -`p_cro`: crossover probability
                -`problem`: problem we want to solve
                -`reynold_number`: reynold number of the data we use
                -`dataset`: type of data we want use
                
        - run(self, gen=100) -> tuple[np.array, str] : 
        
            Run the SGA method.
            
            Parameters:
                - `gen`: Number of generations to run (default: 100)
                
            Returns:
                
                -`result`: result of the equation
                -`equation`: more lisible equation
                
        - stringToFunction(expression: str) -> function :
        
            Converts a string expression into a function.

            Parameters:
                - `expression`: string representation of the mathematical expression.

            Returns:
                A NumPy universal function (ufunc) representing the function obtained from the expression.
                
        - makeRealTheEquation(self, equation: str) -> tuple[np.array, str] : 
        
            Converts the equation into a real equation and more lisible one.

            Parameters:
            
                - `equation`: result equation from SGA method

            Returns:
                
                -`result`: result of the equation
                -`equation`: more lisible equation
                
        - theBest(self) -> tuple[PDE, float] :
        
            Find the best equation with it mse
            
            Returns : 
            
                Equation and MSE
                
        - crossOver(self, percentage=0.5) -> None :
        
            Performs crossover operation on a portion of the population.

            Parameters:
                - `percentage`: The percentage of the population to perform crossover on.
                
        
        - change(self, p_mute=0.05, p_rep=0.3) -> None : 
        
            Performs mutation and replacement operations on a portion of the population.

            Parameters:
                - `p_mute`: The probability of mutation.
                - `p_rep`: The probability of replacement.
    """
    
    
    def __init__(self, num: int, depth: int , width: int, p_var: float, p_mute: float, p_rep: float, p_cro: float, config: Configure,setup: Setup) -> None:
        
        """
            Initialise the SGA analysis
            
            Parameters : 
            
                -`num`: number of PDEs to generate
                -`depth`: depth of the tree
                -`width`: width of the tree
                -`p_var`: variation probability
                -`p_mute: mutation probability
                -`p_rep`: reproduction probabikity
                -`p_cro`: crossover probability
                -`problem`: problem we want to solve
                -`reynold_number`: reynold number of the data we use
                -`dataset`: type of data we want use
                -`config`: instance of Configure class
                -`setup`: instance of Setup class
                
        """
        
        # Setting instance variables with provided parameters
        self.num = num
        self.p_mute = p_mute
        self.p_cro = p_cro
        self.p_rep = p_rep
        self.eqs = []  # List to store generated PDEs
        self.mses = []  # List to store MSEs of generated PDEs
        self.ratio = 1
        self.repeat_cross = 0
        self.repeat_change = 0

        # Instance of Configure class
        self.config = config

        # Instance of Setup class
        self.setup = setup
        
        # self.pde_lib, self.err_lib = setup.get_pde_lib(), setup.get_err_lib()
        
        self.pde_lib, self.err_lib = [],[]
        
        self.y = config.get_y()
        
        self.dpx,self.dpy,self.covy = setup.getResultDerivative()
        
        self.covy,self.uyy= setup.getResultVariable()
        
        self.problem = config.getProblem()
        

        # Generating original PDEs in the pool
        print('Creating the original pdes in the pool ...')
        for i in range(num*self.ratio): # Loop to generate num PDEs
            a_pde = PDE(depth, width, p_var, self.setup, self.config)  # Creating a new PDE
            a_err, a_w, a_mse = PDE.evaluateMse(a_pde,config=self.config,setup=self.setup)  # Evaluating the MSE of the PDE
            self.pde_lib.append(a_pde)  # Adding the PDE to the library
            self.err_lib.append((a_err, a_w))  # Adding the MSE and weights to the error library
            # setup.setLib(a_pde,(a_err, a_w))
            
            # Re-generating PDE if MSE is too small to avoid certain conditions
            while a_err < -100 or a_err == np.inf:
                a_pde = PDE(depth, width, p_var, self.setup, self.config)  # Creating a new PDE
                a_err, a_w, a_mse = PDE.evaluateMse(a_pde,config=self.config,setup=self.setup)  # Evaluating the MSE of the PDE
                self.pde_lib.append(a_pde)  # Adding the PDE to the library
                self.err_lib.append((a_err, a_w))  # Adding the MSE and weights to the error library
                # setup.setLib(a_pde,(a_err, a_w))
                
            print('Creating the ith pde, i=', i)
            print('a_pde.visualize():',a_pde.visualize())  # Visualizing the PDE
            print('evaluate_aic:',a_err)  # Printing the evaluated AIC
            self.eqs.append(a_pde)  # Storing the generated PDE
            self.mses.append(a_mse)  # Storing the MSE of the generated PDE

        # Sorting the generated PDEs based on their MSE
        new_eqs, new_mse = copy.deepcopy(self.eqs), copy.deepcopy(self.mses)
        sorted_indices = np.argsort(new_mse)
        for i, ix in enumerate(sorted_indices):
            self.mses[i], self.eqs[i] = new_mse[ix], new_eqs[ix]
        self.mses, self.eqs = self.mses[0:num], self.eqs[0:num]
        

    def getSet(self) :
        
        return self.setup



    def run(self, setup, gen=100) -> tuple[np.array, str]:
        """
            Run the SGA method.
            
            Parameters:
                - `gen`: Number of generations to run (default: 100)
                
            Returns:
                
                -`result`: result of the equation
                -`equation`: more lisible equation
                -`mse` : MSE of the equation
                
        """
        # List to store the best equations and their MSEs
        list_best = []
        
        # Iterate through each generation
        for i in range(1, gen+1):
            # Perform crossover operation
            self.crossOver(setup,self.p_cro)
            # Perform mutation and reproduction operations
            self.change(setup,self.p_mute, self.p_rep)
            # Get the best equation and its MSE
            best_eq, best_mse = self.theBest()
            
            # Print the best equation, its MSE, and its visual representation
            print('{} generation best_aic, best_mse & best Eq: {}, {}'.format(i, best_mse, best_eq.visualize()))
            # Print the concise representation of the best equation
            print('best concise Eq: {}'.format(best_eq.conciseVisualize()))
            
            # Check if the MSE is negative (close to the answer)
            if best_mse < 0:
                print('We are close to the answer, pay attention')
            
            # Print the number of times crossover and mutation were repeated in this generation
            print('{} generation repeat cross over {} times and mutation {} times'.
                format(i, self.repeat_cross, self.repeat_change))
            
            # Reset the counters for crossover and mutation repetitions
            self.repeat_cross, self.repeat_change = 0, 0
            
            # Append the best equation and its MSE to the list
            list_best.append(["{}".format(best_eq.conciseVisualize()), best_mse])
        
        # Initialize the best equation and its MSE to infinity
        best = [np.inf, np.inf]
        
        # Iterate through the list of best equations and MSEs
        for element in list_best:
            # Update the best equation and its MSE if a better one is found
            if element[1] <= best[1]:
                best = element
                
        # Print the best equation and its MSE
        print("\n\nBest equation is", best[0], "with mse", best[1])
        
        # Make the best equation real
        result, equation = self.makeRealTheEquation(best[0])
        
        # Return the result
        mse = str(best[1])
        return result, equation, mse

            
    
    def stringToFunction(expression: str):
        """
            Converts a string expression into a function.

            Parameters:
                - `expression`: string representation of the mathematical expression.

            Returns:
                A NumPy universal function (ufunc) representing the function obtained from the expression.
        """
        # Define a function that evaluates the expression using the given dictionary of variables
        def function(dict_variable):
            return eval(expression)
        
        # Return a NumPy universal function (ufunc) that wraps the function above
        # The ufunc takes one input argument and returns one output
        return np.frompyfunc(function, 1, 1)

        
        
    def makeRealTheEquation(self, equation: str) -> tuple[np.array, str]:
        """
            Converts the equation into a real equation and more lisible one.

            Parameters:
            
                - `equation`: result equation from SGA method

            Returns:
                
                -`result`: result of the equation
                -`equation_print`: more lisible equation
        """
        
        # Initialize variables to store the result and modified equation
        result_eq = ""
        equation_print = ""
        
        # List of valid operators not before a multiplication
        value_ok = ["(", "/", "+", "-", "*"]
        
        # Dictionary of variables
        variable = []
        dict_variable = {
            "dpy": self.dpy,
            "dpx": self.dpx,
            "dcov": self.covy,
            "y": self.y
        }
        
        i = 0
        
        # Loop through each character in the equation
        while i < len(equation):
            # Check if the substring represents "dp/dy"
            if equation[i:i+5] == "dp/dy":
                # Define the corresponding value and print value
                value = "dict_variable['dpy']"
                value_print = equation[i:i+5]
                # Adjust value if needed
                if (equation[i-1] not in value_ok and equation[i-1] != " ") or (equation[i-2] not in value_ok and equation[i-2].isdigit() == False and equation[i-2] != " "):
                    value = "*" + value
                    value_print = "*" + value_print
                result_eq += value
                equation_print += value_print
                if value not in variable:
                    variable.append(value)
                i += 5
            # Check if the substring represents "dp/dx"
            elif equation[i:i+5] == "dp/dx":
                # Define the corresponding value and print value
                value = "dict_variable['dpx']"
                value_print = equation[i:i+5]
                # Adjust value if needed
                if (equation[i-1] not in value_ok and equation[i-1] != " ") or (equation[i-2] not in value_ok and equation[i-2].isdigit() == False and equation[i-2] != " "):
                    value = "*" + value
                    value_print = "*" + value_print
                result_eq += value
                equation_print += value_print
                if value not in variable:
                    variable.append(value)
                i += 5
            # Check if the substring represents "(dcov)"
            elif equation[i] == "(" and equation[i+4:i+7] == "')'":
                # Define the corresponding value and print value
                value = "dict_variable['dcov']"
                value_print = equation[i:i+7]
                # Adjust value if needed
                if (equation[i-1] not in value_ok and equation[i-1] != " ") or (equation[i-2] not in value_ok and equation[i-2].isdigit() == False and equation[i-2] != " "):
                    value = "*" + value
                    value_print = "*" + value_print
                result_eq += value
                equation_print += value_print
                if value not in variable:
                    variable.append(value)
                i += 7
            # Check if the substring represents "y"
            elif equation[i] == "y":
                # Define the corresponding value and print value
                value = "dict_variable['y']"
                value_print = equation[i]
                # Adjust value if needed
                if (equation[i-1] not in value_ok and equation[i-1] != " ") or (equation[i-2] not in value_ok and equation[i-2].isdigit() == False and equation[i-2] != " "):
                    value = "*" + value
                    value_print = "*" + value_print
                result_eq += value
                equation_print += value_print
                if value not in variable:
                    variable.append(value)
                i += 1
            # Check if the substring represents a numerical value followed by '('
            elif equation[i].isdigit() == True and (equation[i+1] == "(" or (equation[i+1] == " " and equation[i+2] == "(")) and equation[i+3] != "'":
                result_eq += equation[i] + "*"
                equation_print += equation[i] + "*"
                i += 1
            # Default case: append the character to the result
            else:
                result_eq += equation[i]
                equation_print += equation[i]
                i += 1
                
        # Create a NumPy universal function from the modified equation
        result_function = SGA.stringToFunction(result_eq)
        
        try:
            # Try evaluating the function with the given variables
            result = result_function(dict_variable)
        except Exception:
            result = 0
            # Split the equation by '+' and evaluate each part separately
            result_list = result_eq.split("+")
            for element in result_list:
                result_function = SGA.stringToFunction(element)
                try:
                    result += result_function(dict_variable)
                except Exception as e:
                    pass
                
        # If "eq1" is in the problem, handle NaN and inf values
        if "eq1" in self.problem:
            liste_r = []
            for element in result:
                if np.isnan(element[0]) or math.isinf(element[0]):
                    try:
                        liste_r.append(liste_r[-1])
                    except Exception:
                        liste_r.append(0)
                else:
                    liste_r.append(element[0])
            result = np.array(liste_r).reshape(-1, 1)
            
        return result, equation_print, 

        
    def theBest(self) -> tuple[PDE, float]:
        """
            Find the best equation with it mse
            
            Returns : 
            
                Equation and MSE
        """
        # Find the index of the equation with the minimum MSE
        argmin = np.argmin(self.mses)
        # Return the best equation and its MSE as a tuple
        return self.eqs[argmin], self.mses[argmin]
    

    def crossOver(self,setup, percentage=0.5) -> None:
        """
            Performs crossover operation on a portion of the population.

            Parameters:
                - `percentage`: The percentage of the population to perform crossover on.

        """
        def crossIndividual(pde1, pde2):
            """
                Crosses over two PDEs to create new individuals.

                Parameters:
                    - `pde1`: The first parent PDE.
                    - `pde2`: The second parent PDE.

                Returns:
                    Two new PDEs resulting from crossover.
            """
            new_pde1, new_pde2 = copy.deepcopy(pde1), copy.deepcopy(pde2)
            w1, w2 = len(pde1.elements), len(pde2.elements)
            ix1, ix2 = np.random.randint(w1), np.random.randint(w2)
            new_pde1.elements[ix1] = pde2.elements[ix2]
            new_pde2.elements[ix2] = pde1.elements[ix1]
            return new_pde1, new_pde2

        # Select top-performing individuals for crossover
        num_ix = int(self.num * percentage)
        new_eqs, new_mse = copy.deepcopy(self.eqs), copy.deepcopy(self.mses)
        sorted_indices = np.argsort(new_mse)
        for i, ix in enumerate(sorted_indices):
            self.mses[i], self.eqs[i] = new_mse[ix], new_eqs[ix]
        copy_mses, copy_eqs = self.mses[0:num_ix], self.eqs[0:num_ix]  # Top percentage samples

        # Perform crossover on top-performing individuals
        new_eqs, new_mse = copy.deepcopy(copy_eqs), copy.deepcopy(copy_mses)
        reo_eqs, reo_mse = copy.deepcopy(copy_eqs), copy.deepcopy(copy_mses)
        random.shuffle(reo_mse)
        random.shuffle(reo_eqs)

        for a, b in zip(new_eqs, reo_eqs):
            new_a, new_b = crossIndividual(a, b)
            #if new_a.visualize() in setup.getPdeLib() :
            if new_a.visualize() in self.pde_lib :
                self.repeat_cross += 1
            else:  # If crossover produces a new PDE, add it to the library and the current population
                a_err, a_w, a_mse = PDE.evaluateMse(new_a,config=self.config,setup=self.setup)
                self.pde_lib.append(new_a.visualize())
                self.err_lib.append((a_err, a_w))
                # setup.setLib(new_a.visualize(),(a_err, a_w))
                self.mses.append(a_mse)
                self.eqs.append(new_a)

            if new_b.visualize() in self.pde_lib:
                self.repeat_cross += 1
            else:  # If crossover produces a new PDE, add it to the library and the current population
                b_err, b_w, b_mse = PDE.evaluateMse(new_b,config=self.config, setup=self.setup)
                self.pde_lib.append(new_b.visualize())
                self.err_lib.append((b_err, b_w))
                # setup.setLib(new_a.visualize(),(b_err, b_w))
                self.mses.append(b_mse)
                self.eqs.append(new_b)

        # Select the best individuals from the current population
        new_eqs, new_mse = copy.deepcopy(self.eqs), copy.deepcopy(self.mses)
        sorted_indices = np.argsort(new_mse)[0:self.num]
        for i, ix in enumerate(sorted_indices):
            self.mses[i], self.eqs[i] = new_mse[ix], new_eqs[ix]

        
    def change(self, setup,p_mute=0.05, p_rep=0.3) -> None:
        """
            Performs mutation and replacement operations on a portion of the population.

            Parameters:
                - `p_mute`: The probability of mutation.
                - `p_rep`: The probability of replacement.
        """
        # Create copies of the population for mutation and replacement
        new_eqs, new_mse = copy.deepcopy(self.eqs), copy.deepcopy(self.mses)
        # Sort the population based on MSE
        sorted_indices = np.argsort(new_mse)
        for i, ix in enumerate(sorted_indices):
            self.mses[i], self.eqs[i] = new_mse[ix], new_eqs[ix]
        new_eqs, new_mse = copy.deepcopy(self.eqs), copy.deepcopy(self.mses)

        # Iterate through the population
        for i in range(self.num):
            # Preserve the best-performing individuals, only perform crossover
            if i < 1:  # Preserve the best 1 individual, no mutation or replacement
                continue
            # Mutate the individual with a certain probability
            new_eqs[i].mutate(p_mute)
            # Decide whether to replace the individual with a new one
            replace_or_not = np.random.choice([False, True], p=([1 - p_rep, p_rep]))
            if replace_or_not:
                new_eqs[i].replace()
            # Check for duplicates
            # if new_eqs[i].visualize() in setup.get_pde_lib():
            if new_eqs[i].visualize() in self.pde_lib:
                self.repeat_change += 1
            else:
                # Evaluate the MSE of the new individual
                a_err, a_w, a_mse = PDE.evaluateMse(new_eqs[i],config=self.config, setup = self.setup)
                # Add the new individual to the library and the current population
                self.pde_lib.append(new_eqs[i].visualize())
                self.err_lib.append((a_err, a_w))
                # setup.setLib(new_eqs[i].visualize(),(a_err, a_w))
                self.mses.append(a_mse)
                self.eqs.append(new_eqs[i])

        # Update the population with the best individuals after mutation and replacement
        new_eqs, new_mse = copy.deepcopy(self.eqs), copy.deepcopy(self.mses)
        sorted_indices = np.argsort(new_mse)[0:self.num]
        for i, ix in enumerate(sorted_indices):
            self.mses[i], self.eqs[i] = new_mse[ix], new_eqs[ix]
            
            
class Plot : 
    
    """
        Class to plot and save figure and equation
        
        - plotFigure(x: np.array,y1: np.array,y2: np.array,title_x : str,title_y: str,name_y1: str,name_y2: str,title: str,save_path: str) -> None :
        
            Plot the figure 
            
            Parameters : 
            
                -`x` : x-axis values
                -`y1` : y-axis values for y1
                -`y2` : y-axis values for y2
                -`title_x` : title for x-axis
                -`title_y` : title for y-axis
                -`name_y1` : label name for y1
                -`name_y2` : label name for y2
                -`title` : title of the figure
                -`save_path` : path to save the figure
                
        - plotEquation(equation: str, covariance: str, left_side : str, save_path: str) -> None
        
            Plot the equation
            
            Parameters : 
            
                -`equation`: equation to print
                -`covariance` : covariance used
                -`left_side` : left side of the equation
                -`save_path` : path to save the figure
    """
    
    def plotFigure(x: np.array,y1: np.array,y2: np.array,title_x : str,title_y: str,name_y1: str,name_y2: str,title: str,save_path: str) -> None :
        
        """
            Plot the figure 
            
            Parameters : 
            
                -`x` : x-axis values
                -`y1` : y-axis values for y1
                -`y2` : y-axis values for y2
                -`title_x` : title for x-axis
                -`title_y` : title for y-axis
                -`name_y1` : label name for y1
                -`name_y2` : label name for y2
                -`title` : title of the figure
                -`save_path` : path to save the figure
        """
        
         # Create a figure
        fig = plt.figure()

        # Create a subplot
        ax = fig.subplots()

        # Plot y1 and y2 against x
        ax.plot(x, y1, label=name_y1)
        ax.plot(x, y2, label=name_y2)

        # Add a legend to the plot
        ax.legend()

        # Set the title of the figure
        plt.title(title)

        # Set the x-axis and y-axis labels
        ax.set_xlabel(title_x)
        ax.set_ylabel(title_y)

        # Save the figure to the specified path
        plt.savefig(save_path)

        # Show the figure
        plt.show(block=False)
        
        
    def plotEquation(equation: str, covariance: str, left_side : str, save_path: str, data_print: str) -> None:
        
        """
            Plot the equation
            
            Parameters : 
            
                -`equation`: equation to print
                -`covariance` : covariance used
                -`left_side` : left side of the equation
                -`save_path` : path to save the figure
                -`data_print`: data to print
        """
        
        # Set the title of the equation
        title = "Equation for "

        # If the save path contains "eq1", set the title to "first RANS equations problem with"
        if "eq1" in save_path:
            title += "first RANS equations problem with "

        # If the save path contains "eq2", set the title to "second RANS equations problem with"
        if "eq2" in save_path:
            title += "second RANS equations problem with "

        # Add the covariance to the title
        title += covariance + " :"
        
        text_to_print = ["======================\n",
                        "-------Equation-------\n\n",
                        title + "\n\n",
                        left_side + " = " + equation,
                        "\n\n----------END----------\n",
                        "=======================\n\n",
                        data_print
                        ]

        # Open the file in write mode
        with open(save_path, "w") as file:
            for element in text_to_print :
                
                file.write(element)
        
        with open(save_path, "r") as file :
            for row in file :
                print(row,end="")
