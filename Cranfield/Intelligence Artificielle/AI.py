import torch
import pydicom
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from pydicom.pixel_data_handlers.util import apply_voi_lut
import time
import sys
import random

from Dataset import CreateDataset, Dataset_config
from Model import NeuralNetwork, Run_model



# Define the function to process DICOM data
def process_data(dicom_path, max_columns, max_rows, voi_lut):

    # Initialize a list to store image padding
    image_padding = []

    # Read the DICOM file located at the specified path
    dicom = pydicom.dcmread(dicom_path)
    # Extract pixel data from DICOM
    data_image = dicom.pixel_array

    # Apply VOI LUT if available
    if voi_lut:
        data_image = apply_voi_lut(dicom.pixel_array, dicom)

    # Adjust pixel data based on Photometric Interpretation
    if dicom.PhotometricInterpretation == "MONOCHROME1":
        data_image = np.amax(data_image) - data_image

    # Normalize pixel data if the number of bits stored is not 16
    if dicom.BitsStored != 16:
        pixel_min = np.min(data_image)
        pixel_max = np.max(data_image)
        pixel_array_normalized = (data_image - pixel_min) / (pixel_max - pixel_min)
        new_bits_stored = 16
        new_pixel_max = (2 ** new_bits_stored) - 1
        data_image = (pixel_array_normalized * new_pixel_max).astype(np.uint16)

    # Resize the image to match the maximum columns and rows
    data_image_resize = data_image

    # Calculate padding dimensions
    padding_height = (max_rows - dicom.Rows) / 2
    padding_width = (max_columns - dicom.Columns) / 2

    # Handle odd padding dimensions
    if padding_height % 2 != 0:
        padding_height_1 = padding_height + 0.5
        padding_height_2 = padding_height_1 - 0.5

    if padding_height % 2 == 0:
        padding_height_1 = padding_height_2 = padding_height

    if padding_width % 2 != 0:
        padding_width_1 = padding_width + 0.5
        padding_width_2 = padding_width_1 - 0.5

    if padding_width % 2 == 0:
        padding_width_1 = padding_width_2 = padding_width

    # Convert padding dimensions to integers
    padding_width_1 = int(padding_width_1)
    padding_width_2 = int(padding_width_2)
    padding_height_1 = int(padding_height_1)
    padding_height_2 = int(padding_height_2)

    # Store padding dimensions in a list
    image_padding = [padding_height_1, padding_height_2, padding_width_1, padding_width_2]

    # Pad the image based on calculated padding dimensions
    data_image_resize = np.pad(data_image_resize, ((padding_height_1, padding_height_2), (padding_width_1, padding_width_2)), mode='constant', constant_values=255)

    # Normalize pixel values between 0 and 255
    data_image = data_image - np.min(data_image)
    data_image = data_image / np.max(data_image)
    data_image = (data_image * 255).astype(np.uint8)

    # Downsample the image to one-fourth of its size
    new_height = data_image_resize.shape[0] // 4
    new_width = data_image_resize.shape[1] // 4
    new_image_array = np.zeros((new_height, new_width), dtype=np.uint8)

    for i in range(new_height):
        for j in range(new_width):
            block = data_image_resize[i*4:(i+1)*4, j*4:(j+1)*4]
            new_pixel_value = np.mean(block)
            new_image_array[i, j] = new_pixel_value

    # Normalize pixel values of the resized image
    data_image_resize = new_image_array - np.min(new_image_array)
    data_image_resize = data_image_resize / np.max(data_image_resize)
    data_image_resize = (data_image_resize * 255).astype(np.uint8)

    # Convert grayscale image to RGB
    data_image_resize = np.repeat(data_image_resize[:, :, np.newaxis], 3, axis=2)

    # Return processed image data, resized image data, and image padding
    return data_image, data_image_resize, image_padding


# Defining the function to find the maximum dimensions in a DICOM file
def max_dimension(dicom_path, max_columns, max_rows):
    # Reading the DICOM file located at the specified path
    dicom = pydicom.dcmread(dicom_path)
    
    # Checking if the number of columns in the DICOM file exceeds the provided maximum columns
    if dicom.Columns > max_columns:
        # If yes, updating the maximum columns to the value in the DICOM file
        max_columns = dicom.Columns
    
    # Checking if the number of rows in the DICOM file exceeds the provided maximum rows
    if dicom.Rows > max_rows:
        # If yes, updating the maximum rows to the value in the DICOM file
        max_rows = dicom.Rows
    
    # Returning the updated maximum columns and rows
    return max_columns, max_rows
  

def create_histo(df,n):
    # Initialize dictionaries to store label counts and label presence verification
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
                  
    # Iterate over DataFrame rows
    for _, row in df.iterrows(): 
        # Check if image ID is not already in the verification dictionary for the corresponding label
        if row[0] not in dict_verif[str(row[2])] :
            # Increment label count
            dict_histo[str(row[2])] +=1
            # Add image ID to verification dictionary for the corresponding label
            dict_verif[str(row[2])].append(row[0])
        
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame.from_dict(dict_histo, orient='index', columns=['Labels'])
    
    # Create a bar plot from the DataFrame
    df.plot(kind='bar')
    
    # Add labels and title
    plt.xlabel('Labels')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    
    # Save the histogram as an image file
    plt.savefig("histogram_train_" + str(n) + ".png")


def create_dataset(PATH, csv_file, n):
    # Initialize dictionaries to store image data, resized image data, and padding information
    dict_data = {}
    dict_data_resize = {}
    dict_padding = {}

    # Define column titles for the DataFrame
    title = ["name", "image", "label", "boxe"]
    # Create an empty DataFrame with specified column titles
    df = pd.DataFrame(columns=title)

    # List all DICOM files in the specified directory
    dicom_list_total = os.listdir(PATH)
    
    # Randomly select n DICOM files from the total list
    dicom_list = random.sample(dicom_list_total, n)

    max_rows = 0
    max_columns = 0
    
    # Iterate over randomly selected DICOM files to find maximum dimensions
    for dicom in dicom_list:
        try:
            max_columns, max_rows = max_dimension(PATH + "/" + dicom, max_columns, max_rows)
        except Exception:
            continue

    # Determine the maximum dimension for resizing
    max_dim = max(max_columns, max_rows)
    max_columns, max_rows = max_dim, max_dim
    
    # Iterate over randomly selected DICOM files to process them
    for dicom in dicom_list:
        name = dicom[:-6]
        try:
            # Process DICOM data and resize images
            dict_data[name], dict_data_resize[name], dict_padding[name] = process_data(PATH + "/" + dicom, max_columns, max_rows, voi_lut=True)
        except Exception as e:
            continue

        # Read CSV file containing labels and bounding boxes
        d_images = pd.read_csv(csv_file)
        d_image = d_images.loc[d_images.iloc[:, 0] == name]

        # Iterate over rows in the CSV file
        for _, row in d_image.iterrows():
            if row[1] != "No finding":
                # Extract padding information
                padding_width_1 = dict_padding[name][2]
                padding_width_2 = dict_padding[name][3]
                padding_height_1 = dict_padding[name][0]
                padding_height_2 = dict_padding[name][1]
                
                # Adjust bounding box coordinates based on padding
                x_min = row[4] + padding_width_1
                x_max = row[6] + padding_width_1
                y_min = row[5] + padding_height_1
                y_max = row[6] + padding_height_1
                try:
                    # Create a dictionary containing image information and append it to the DataFrame
                    row_data = {"name": dicom[:-6], "image": dict_data_resize[dicom[:-6]], "label": row[2], "boxe": [x_min, x_max, y_min, y_max]}
                    df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)
                except Exception:
                    continue
            else:
                try:
                    # Create a dictionary containing image information and append it to the DataFrame
                    row_data = {"name": dicom[:-6], "image": dict_data_resize[dicom[:-6]], "label": 14, "boxe": [0, 0, 0, 0]}
                    df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)
                except Exception:
                    continue
    return df


  
def main():
    # Record the start time of the execution
    start_time = time.time()
    
    # Define the paths to the training data directory and CSV file
    PATH_train = os.getcwd() + "/Train_data"
    csv_file = os.getcwd() + "/train.csv"
    
    # Create the dataset from the training data and CSV file, with the specified number of samples
    df = create_dataset(PATH_train, csv_file, int(sys.argv[1]))
    
    # Generate and save a histogram based on the created dataset
    create_histo(df, sys.argv[1])
    
    # Load the training and validation dataloaders
    train_dataloader, val_dataloader = Dataset_config.load(df)
    
    # Determine the device (CPU, GPU) for training
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )
    print(f"Using {device} device")
    
    # Instantiate the neural network model and move it to the specified device
    model = NeuralNetwork().to(device)
    print(model)
    
    # Define the optimizer for training
    optimizer = torch.optim.Adam(model.parameters(), lr=0.006)
    
    # Train the model using the training and validation dataloaders
    Run_model.train(model, optimizer, train_dataloader, val_dataloader, epochs=10)
    
    # Save the trained model state
    torch.save(model.state_dict(), "model.pth")
    print("Saved PyTorch Model State to model.pth")
    
    # Load the saved model state
    model = NeuralNetwork().to(device)
    model.load_state_dict(torch.load("model_" + str(sys.argv[1]) + ".pth"))
    
    # Record the end time of the execution
    end_time = time.time()
    
    # Calculate the total execution time
    total = end_time - start_time
    
    print("Execution time:", total, "seconds")

    
    
     
if __name__ == "__main__":
    
    main() 