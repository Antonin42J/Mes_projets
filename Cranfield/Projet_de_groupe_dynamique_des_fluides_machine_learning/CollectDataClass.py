import pandas as pd
import requests
import os

from ToolsClass import Tools

class CollectData:
    """
    Class to extract data from .dat file:
    
    - downloadFile(url : str, folder_name: str) -> None:
        - url: URL to the file to be downloaded
        - folder_name: Path to the folder where the file will be downloaded
        - file_reynold : reynold numbers of the dataset we want to download
        
        -> Downloads the file from the URL
    
    - createFolder(folder_name : str) -> None:
        - folder_name: Name of the folder to be created
        
        -> Creates a folder
    
    - downloadFileUrl(file_url : str, folder_name : str) -> None:
        - file_url: URL to the file to be downloaded
        - folder_name: Path to the folder where the file will be downloaded
        - file_reynold : reynold numbers of the dataset we want to download
        
        -> Creates the folder and downloads the file
    
    - collectDataFile(file_path : str) -> pd.DataFrame:
        - file_path: Path to the file to collect data from
        
        -> Collects data from a file and returns a Pandas DataFrame
    
    - combineDataFrame(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        - df1: First DataFrame to merge
        - df2: Second DataFrame to merge

        -> Creates a new dataframe by making the intersection of the two dataframes

    - combineListDataFrame(dataframes: list) -> pd.DataFrame:
        - dataframes: List of dataframes to merge

        -> Creates a new dataframe by performing successive intersections of the dataframes
        
    - combineListDataFramePath(dataframes_paths: list) -> pd.DataFrame:
        - dataframes: List of paths to merge

        -> Creates a new dataframe by  performing successive creations and intersections of the dataframes
    """
    def __init__(self):
        self.nx = None
        self.ny = None
        self.nz = None
        self.Lx = None
        self.Lz = None
        self.n = None
        self.nu = None
        self.delta = None
        self.U_mean = None
        self.u_tau = None
        self.Re_tau = None

    def updateAttributes(self, variable, value):
        """
        Update the attributes of the class based on the extracted data.
        """
        if variable == 'nx':
            self.nx = value
        elif variable == 'ny':
            self.ny = value
        elif variable == 'nz':
            self.nz = value
        elif variable == 'Lx':
            self.Lx = value
        elif variable == 'Lz':
            self.Lz = value
        elif variable == 'n':
            self.n = value
        elif variable == 'nu':
            self.nu = value
        elif variable == 'delta':
            self.delta = value
        elif variable == 'U_mean':
            self.U_mean = value
        elif variable == 'u_tau':
            self.u_tau = value
        elif variable == 'Re_tau':
            self.Re_tau = value

    def collectDataFile(self, file_path: str) -> pd.DataFrame:
        """
        Collects data from a file and returns a Pandas DataFrame.
        """
        with open(file_path) as file:
            lines = file.readlines()
            index_header = None
            header_line = None

            for i, row in enumerate(lines):
                if row.startswith('%') and ' = ' in row and '**' not in row and 'simulation' not in row:
                    variable, value = row.split('=')  # Split the line by '='
                    variable = variable.strip()[1:].split()[-1]   # Remove '%' and leading/trailing whitespaces
                    value = value.strip()             # Remove leading/trailing whitespaces
                    self.updateAttributes(variable, value)  # Update corresponding attribute
                    
                    print(f"Data retrieved: {variable} = {value}")  # Print the retrieved data
                if "% -----------End of header---------" in row:
                    index_header = i + 2
                if i == index_header:
                    header_line = row[2:].split()  # Remove the leading whitespace and split by whitespace
                    break

        data = pd.read_csv(file_path, names=header_line, comment='%', delim_whitespace=True)
        return data
    
    def collectDataFileDatahead(self, file_path: str) -> dict : 

        dict_variable = {}

        with open(file_path) as file:
            lines = file.readlines()

            for i, row in enumerate(lines):
                if row.startswith('%') and ' = ' in row and '**' not in row and 'Direct' not in row:
                    variable, value = row.split('=')  # Split the line by '='
                    variable = variable.strip()[1:].split()[-1]   # Remove '%' and leading/trailing whitespaces
                    value = value.strip()             # Remove leading/trailing whitespaces
                    self.updateAttributes(variable, value)  # Update corresponding attribute
                    print(f"Data retrieved: {variable} = {value}")  # Print the retrieved data

                    dict_variable[variable] = value

        return dict_variable


  
    @staticmethod
    def downloadFile(url: str, folder_path: str, file_reynold: str) -> None:
        """
        Downloads the file from the given URL to the specified folder.
        """
        local_filename = os.path.join(folder_path, "fluid_data_" + file_reynold, os.path.basename(url))
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(local_filename), exist_ok=True)
            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"File downloaded successfully as '{local_filename}'")
        else:
            print("Error downloading the file.")
            

    @staticmethod
    def createFolder(folder_path: str) -> None:
        """
        Creates a folder if it doesn't already exist.
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    
    @staticmethod
    def downloadFileUrl(file_url: str, folder_path: str, file_reynold: str) -> None:
        """
        Creates the folder if it doesn't exist and downloads the file.
        """
        CollectData.createFolder(folder_path)
        CollectData.downloadFile(file_url, folder_path, file_reynold)
    
    @staticmethod
    def combineDataFrame(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        """
        Combines two Pandas DataFrame and returns a new one.
        """
        df1_header = df1.head()
        df2_header = df2.head()
        duplicated_columns_names = list(set(df1_header) & set(df2_header))

        data = df1.join(df2.drop(duplicated_columns_names, axis=1), how="inner")
        return data
    
    @staticmethod
    def combineListDataFrame(dataframes: list) -> pd.DataFrame:
        """
        Combines all the Pandas DataFrame of the list.
        Returns a new Pandas DataFrame.
        """
        if len(dataframes) == 0:
            raise Exception("List is empty")
        
        data = dataframes[0]
        while len(dataframes) != 1:
            df = dataframes.pop()
            data = CollectData.combineDataFrame(data, df)
        return data
    

    # Which is best: having to separate functions, or having one function we will deal with both cases
    @staticmethod
    def combineListDataFramePath(dataframes_paths: list) -> pd.DataFrame:
        """
        Create a DataFrame from each element of the list to combine it.
        Returns a new Pandas DataFrame.
        """
        if len(dataframes_paths) == 0:
            raise Exception("List is empty")
        
        data = CollectData().collectDataFile(dataframes_paths[0])
        while len(dataframes_paths) != 1:
            df = CollectData().collectDataFile(dataframes_paths.pop())
            data = CollectData.combineDataFrame(data, df)
        return data
    

if __name__ == "__main__":
    file_url = input("Enter the file URL: ")
    file_reynold = input("Enter the Reynolds number of the file: ")
    folder_name = "data"
    CollectData.downloadFileUrl(file_url, folder_name, file_reynold)
    file_path = os.path.join("data", "fluid_data_" + file_reynold, os.path.basename(file_url))
    data = CollectData().collectDataFile(file_path)
    dict = CollectData().collectDataFileDatahead(file_path)
    print(data)
    print(dict)