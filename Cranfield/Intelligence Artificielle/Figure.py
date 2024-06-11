import pandas as pd
import matplotlib.pyplot as plt
import os

class Figure:
    
    def histo_total(dict_histo, dict_verif):
        # Define the path to the CSV file
        csv_file = os.getcwd() + "/train.csv"
        
        # Read the total dataframe from the CSV file
        df_total = pd.read_csv(csv_file)
        
        # Iterate over each row in the total dataframe
        for _, row in df_total.iterrows():
            if row[0] not in dict_verif[str(row[2])]:
                dict_histo[str(row[2])] += 1
                dict_verif[str(row[2])].append(row[0])
                
        # Convert the dictionary into a DataFrame
        df = pd.DataFrame.from_dict(dict_histo, orient='index', columns=['Labels'])
        
        # Create a histogram from the DataFrame
        df.plot(kind='bar')
        
        # Add labels and a title
        plt.xlabel('Labels')
        plt.ylabel('Frequency')
        plt.title('Histogram')
        
        # Show the histogram
        plt.savefig("histogram_train_total.png")
        
    def histo_2000(dict_histo, dict_verif):
        # Define the path to the directory containing DICOM files and the CSV file
        path = os.getcwd() + "/Train_data"
        csv_file = os.getcwd() + "/train.csv"
        
        # Get the list of DICOM files
        dicom_list = os.listdir(path)
        
        # Read the total dataframe from the CSV file
        df_total = pd.read_csv(csv_file)
        
        print(len(dicom_list))
        
        # Iterate over each DICOM file
        for dicom in dicom_list[:2000]:
            print(dicom[:-6])
            # Select rows corresponding to the current DICOM file
            df_dicom = df_total.loc[df_total.iloc[:, 0] == dicom[:-6]]
            
            # Iterate over each row in the selected dataframe
            for _, row in df_dicom.iterrows(): 
                if row[0] not in dict_verif[str(row[2])]:
                    dict_histo[str(row[2])] += 1
                    dict_verif[str(row[2])].append(row[0])
                    
        # Convert the dictionary into a DataFrame
        df = pd.DataFrame.from_dict(dict_histo, orient='index', columns=['Labels'])
        
        # Create a histogram from the DataFrame
        df.plot(kind='bar')
        
        # Add labels and a title
        plt.xlabel('Labels')
        plt.ylabel('Frequency')
        plt.title('Histogram')
        
        # Show the histogram
        plt.savefig("histogram_2000.png")

    def main():
    # Initialize dictionaries for histograms
      dict_histo = { "0" : 0,
                "1" : 0,
                "2" : 0,
                "3" : 0,
                "4" : 0,
                "5" : 0,
                "6" : 0,
                "7" : 0,
                "8" : 0,
                "9" : 0,
                "10" : 0,
                "11" : 0,
                "12" : 0,
                "13" : 0,
                "14" : 0}
  
      dict_verif = { "0" : [],
                  "1" : [],
                  "2" : [],
                  "3" : [],
                  "4" : [],
                  "5" : [],
                  "6" : [],
                  "7" : [],
                  "8" : [],
                  "9" : [],
                  "10" : [],
                  "11" : [],
                  "12" : [],
                  "13" : [],
                  "14" : []}

      
      # Generate total histogram
      dict_histo_total = dict_histo.copy()
      dict_verif_total = dict_verif.copy()
      Figure.histo_total(dict_histo_total, dict_verif_total)
      
      dict_histo = { "0" : 0,
                "1" : 0,
                "2" : 0,
                "3" : 0,
                "4" : 0,
                "5" : 0,
                "6" : 0,
                "7" : 0,
                "8" : 0,
                "9" : 0,
                "10" : 0,
                "11" : 0,
                "12" : 0,
                "13" : 0,
                "14" : 0}
  
      dict_verif = { "0" : [],
                  "1" : [],
                  "2" : [],
                  "3" : [],
                  "4" : [],
                  "5" : [],
                  "6" : [],
                  "7" : [],
                  "8" : [],
                  "9" : [],
                  "10" : [],
                  "11" : [],
                  "12" : [],
                  "13" : [],
                  "14" : []}
  
      # Generate histogram for the first 2000 DICOM files
      dict_histo_2000 = dict_histo.copy()
      dict_verif_2000 = dict_verif.copy()
      Figure.histo_2000(dict_histo_2000, dict_verif_2000)


    
if __name__ == "__main__":
    
    Figure.main()  