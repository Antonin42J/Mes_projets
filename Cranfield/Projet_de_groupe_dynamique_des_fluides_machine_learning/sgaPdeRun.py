
import os
import numpy as np

from sgaPdeClasses import SGA,Configure,Setup,Plot
from ToolsClass import Tools


def runSga(problem: str, reynold_number: str, dataset: str,num: int, depth: int, width: int, p_var: float, p_mute: float, p_rep : float, p_cro: float, 
            gen: int, method_pde_find: str) -> tuple[np.array,str]:
    
    """
        Function to run the SGA-PDE method
        
        Parameters :
        
            -`problem` : equation we want     
            -`reynold_number` : reynold number link to the problem  
            -`dataset` : types of dataset we want to work with
            -`num`: number of PDEs to generate
            -`depth`: depth of the tree
            -`width`: width of the tree
            -`p_var`: variation probability
            -`p_mute`: mutation probability
            -`p_rep`: reproduction probabikity
            -`p_cro`: crossover probability
            -`gen`: Number of generations to run (default: 100)
            -`method_pde_find`: method to find the PDEs
        
        Returns :
        
            -`result`: result of the equation
            -`equation`: more lisible equation
            -`path_save_figure`: path where the figure will be saved
            -`path_save_equation`: path where the equation will be saved
    """
    
    # Configure the problem, reynold number, and dataset
    config = Configure(problem, reynold_number, dataset, method_pde_find)

    # Set up the configuration
    setup = Setup(config)

    # Initialize the SGA object with the number of PDEs, depth, width, variation probability, mutation probability, reproduction probability, crossover probability, configuration, and setup
    sga = SGA(num, depth, width, p_var, p_mute, p_rep, p_cro,config=config, setup=setup)

    # Run the SGA and get the result and the more readable equation
    result, equation, mse = sga.run(setup, gen)

    # Determine the type of dataset
    if dataset == "simulation":
        type_dataset = "Simulation"

    if dataset == "dns":
        type_dataset = "DNS"

    # Set the covariance
    covariance = problem[-2] + "'" + problem[-1] + "'"

    # Set the path to save the results
    path_folder = os.path.join(Tools.getTheRightPath(), "models", "sga_pde", problem[-2:], problem[:3])

    # Create the path if it doesn't exist
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)

    # Get the number of files in the path
    number_files = int(len(os.listdir(path_folder)) / 2)

    # Set the path to save the figure
    path_save_figure = os.path.join(path_folder, str(number_files + 1) + "_figure" + ".png")

    # Set the path to save the equation
    path_save_equation = os.path.join(path_folder, str(number_files + 1) + "_equation" + ".txt")

    # Initialize the left side of the equation
    left_side = ""

    # Try to plot the figure
    try:

        # If the problem is eq1, set the left side of the equation to "u''"
        if "eq1" in config.problem:

            left_side = "u''"

            # Plot the figure
            Plot.plotFigure(config.y, setup.uyy, result, "y", left_side, type_dataset, "SGA-PDE", "Model RANS with dp/dx and d(" + covariance + ")/dy", path_save_figure)

        # If the problem is eq2, set the left side of the equation to (covariance)'"
        
        if "eq2" in config.problem : 
            
            left_side = "("+covariance+")'"
            
            # Plot the figure
            Plot.plotFigure(config.y,setup.covy,result,"y",left_side,type_dataset,"SGA-PDE","Model RANS with "+covariance,path_save_figure )
    
    # If there is an exception, print an error message and set the result to zeros
    except Exception :
        
        print("The equation is not good")
        
        result = np.zeros(setup.covy.shape)
        
        Plot.plotFigure(config.y,setup.covy,result,"y",left_side,type_dataset,"SGA-PDE","Model RANS with "+covariance,path_save_figure )
        
        left_side = "The equation is not good\n\n"+left_side
        
        path_save_equation = path_save_equation[:-4] + "_not_good"+path_save_equation[-4:]
        
    #Plot the equation
    data_print = ["MSE : " + mse,
                "\nReynold number : " + reynold_number,
                "\nType of dataset : " + dataset,
                "\nNumber of initial PDE generation : " + str(num),
                "\nDepth : " + str(depth),
                "\nWidth : " + str(width), 
                "\nVariation probability : " + str(p_var),
                "\nMutation probability : "+str(p_mute),
                "\nRepetition probability :"  + str(p_rep),
                "\nCrossover probability :" + str(p_cro),
                "\nNumber of generations : " + str(gen),
                ]
    data_to_print = " ".join(data_print)
    Plot.plotEquation(equation, covariance, left_side, path_save_equation,data_to_print)
    
    return result, equation, path_save_figure, path_save_equation 


def testEquationWithDiffetentDataset(problem: str,reynold: str,dataset: str,method_pde_find: str, equation_number: str) -> None:
    
    """
        Test a equation with a different reynold number dataset. 
        
        Parameters : 
        
            -`problem` : the problem to test
            -`reynold` : the reynold number to test
            -`dataset` : the dataset to test
            -`method_pde_find`: method to find the PDEs
            -`equation_number` : the number of the equation to test
            
    
    """

    path_to_equation = os.path.join(Tools.getTheRightPath(),"models","sga_pde",problem[-2:],problem[:3],equation_number+"_equation.txt")
    
    #Take the right side of the equation
    with open(path_to_equation, "r") as file:
        
        for line in file :

            if "' =" in line :
                
                print(line)
                
                equation = (line.split("=")[-1])[1:]
                
    # Configure the problem, reynold number, and dataset
    config = Configure(problem, reynold, dataset, method_pde_find)

    # Set up the configuration
    setup = Setup(config)

    # Initialize the SGA object with the number of PDEs, depth, width, variation probability, mutation probability, reproduction probability, crossover probability, configuration, and setup
    sga = SGA(num=0, depth=0, width=0, p_var=0.0, p_mute=0.0, p_rep=0.0, p_cro=0.0, config=config, setup=setup)
    
    #Find result
    result,result_print = sga.makeRealTheEquation(equation)
    
    # Determine the type of dataset
    if dataset == "simulation":
        type_dataset = "Simulation"

    if dataset == "dns":
        type_dataset = "DNS"

    # Set the covariance
    covariance = problem[-2] + "'" + problem[-1] + "'"

    # Set the path to save the figure
    path_to_folder = os.path.join(Tools.getTheRightPath(), "models", "sga_pde", "test_equation")
    if not os.path.exists(path_to_folder) :
        os.makedirs(path_to_folder)
    path_save_figure = os.path.join(path_to_folder, problem+"_"+equation_number+"_"+reynold+".png")

    # Initialize the left side of the equation
    left_side = ""

    # If the problem is eq1, set the left side of the equation to "u''"
    if "eq1" in config.problem:

        left_side = "u''"

        # Plot the figure
        Plot.plotFigure(config.y, setup.uyy, result, "y", left_side, type_dataset, "SGA-PDE", "Test of equation "+equation_number+" for model RANS with dp/dx and d(" + covariance + ")/dy", path_save_figure)

    # If the problem is eq2, set the left side of the equation to (covariance)'"
    
    if "eq2" in config.problem : 
        
        left_side = "("+covariance+")'"
        
        # Plot the figure
        Plot.plotFigure(config.y,setup.covy,result, "y", left_side, type_dataset, "SGA-PDE", "Test of equation "+equation_number+" for model RANS with "+covariance,path_save_figure )
    
    

if __name__ == "__main__": 
    
    print("The problems are divided between two types of equations: \n - 'eq1' for the first RANS equation (second derivative of u with respect to y)\n",
          "- 'eq2' for the second RANS equation (derivative of the covariance with respect to y) \n\n Then we have to choose a covariance between",
          "u'u', v'v', w'w', u'v', u'w', v'w'. \n\n Example of problem writing: 'eq2_uv'\n")

    method_pde_find = input("Choose the methode you for the PDE finding ('S' for Strindge and 'L' for Lasso) : ")
    
    problem = input("Choose a problem: ")

    reynold = input("\nChoose a valid Reynolds number (180, 5200): ")

    dataset = input("\nChoose a type of dataset (dns or simulation): ")

    num = int(input("\nChoose the number of random equations you want to generate at the beginning of the SGA-PDE method (recommended number is between 10 and 100): "))

    depth = int(input("\nChoose the number of stages you want in the tree (recommended number is between 4 and 10): "))

    width = int(input("\nChoose the width you want for the tree (recommended number is between 4 and 10): "))

    p_var = float(input("\nChoose a probability of variation during the process (recommended value: 0.6): "))

    p_mute = float(input("\nChoose a probability of mutation during the process (recommended value: 0.5): "))

    p_rep = float(input("\nChoose a probability of repetition during the process (recommended value: 0.4): "))

    p_cro = float(input("\nChoose a probability of crossover during the process (recommended value: 0.6): "))

    gen = int(input("\nChoose the number of generations and tests of equations you want (recommended value between 10 and 100): "))

    path_save_figure, path_save_equation = "", ""

    try:
        result, equation, path_save_figure, path_save_equation = runSga(problem, reynold, dataset, num, depth, width, p_var, p_mute, p_rep, p_cro, gen, method_pde_find)

    except Exception as e:

        print(e)

        if os.path.exists(path_save_figure):
            os.remove(path_save_figure)

        if os.path.exists(path_save_equation):
            os.remove(path_save_equation)

        print("Run SGA failed, let's try again (wait)")
        input("Please type Enter")

        try:

            result, equation, path_save_figure, path_save_equation = runSga(problem, reynold, dataset, num, depth, width, p_var, p_mute, p_rep, p_cro, gen, method_pde_find)

        except Exception:

            print(e)

            if os.path.exists(path_save_figure):
                os.remove(path_save_figure)

            if os.path.exists(path_save_equation):
                os.remove(path_save_equation)

            print("Run SGA failed")
            
    # testEquationWithDiffetentDataset(problem="eq2_uv",reynold="180",dataset="dns",equation_number="1")
    
    list_gen = [10,10,20,20,50,50,100,100]
    
    for element in list_gen :
        
        result, equation, path_save_figure, path_save_equation = runSga("eq2_uv", "5200", "dns", 10, 7, 6, 0.6, 0.5, 0.4, 0.6, element, "S")
        
    
    for element in list_gen : 
        
        result, equation, path_save_figure, path_save_equation = runSga("eq2_uv", "5200", "dns", 50, 7, 6, 0.6, 0.5, 0.4, 0.6, element, "S")
    
    
    # result, equation, path_save_figure, path_save_equation = runSga("eq2_uv", "5200", "simulation", 50, 7, 6, 0.6, 0.5, 0.4, 0.6, 50, "S")
    # result, equation, path_save_figure, path_save_equation = runSga("eq2_vv", "5200", "simulation", 50, 7, 6, 0.6, 0.5, 0.4, 0.6, 50, "S")
    # result, equation, path_save_figure, path_save_equation = runSga("eq2_vv", "5200", "dns", 50, 7, 6, 0.6, 0.5, 0.4, 0.6, 50, "S")
    # result, equation, path_save_figure, path_save_equation = runSga("eq1_uv", "5200", "simulation", 50, 7, 6, 0.6, 0.5, 0.4, 0.6, 50, "S")
    # result, equation, path_save_figure, path_save_equation = runSga("eq1_vv", "5200", "simulation", 50, 7, 6, 0.6, 0.5, 0.4, 0.6, 50, "S")
    
    # result, equation, path_save_figure, path_save_equation = runSga("eq1_uv", "5200", "simulation", 10, 7, 6, 0.6, 0.5, 0.4, 0.6, 10, "S")
    # result, equation, path_save_figure, path_save_equation = runSga("eq1_uw", "5200", "simulation", 10, 7, 6, 0.6, 0.5, 0.4, 0.6, 10, "S")
    
    # testEquationWithDiffetentDataset(problem="eq2_uv",reynold="180",dataset="dns", method_pde_find="S",equation_number="17")
    # testEquationWithDiffetentDataset(problem="eq2_uv",reynold="2000",dataset="dns", method_pde_find="S",equation_number="17")
    # testEquationWithDiffetentDataset(problem="eq2_uv",reynold="1000",dataset="dns", method_pde_find="S",equation_number="17")
    # testEquationWithDiffetentDataset(problem="eq2_uv",reynold="550",dataset="dns", method_pde_find="S",equation_number="17")
    # testEquationWithDiffetentDataset(problem="eq1_uv",reynold="180",dataset="simulation",method_pde_find="S",equation_number="5")
    # testEquationWithDiffetentDataset(problem="eq2_vv",reynold="180",dataset="dns",equation_number="1")
    # testEquationWithDiffetentDataset(problem="eq1_vv",reynold="180",dataset="simulation",equation_number="1")
    
    # result, equation, path_save_figure, path_save_equation = runSga("eq2_uw", "5200", "simulation", 50, 7, 6, 0.6, 0.5, 0.4, 0.6, 50, "S")
    # result, equation, path_save_figure, path_save_equation = runSga("eq2_uw", "5200", "dns", 50, 7, 6, 0.6, 0.5, 0.4, 0.6, 50, "S")
    # result, equation, path_save_figure, path_save_equation = runSga("eq1_uw", "5200", "simulation", 50, 7, 6, 0.6, 0.5, 0.4, 0.6, 50, "S")  
    
    
    