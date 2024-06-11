import torch
import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader


class CreateDataset(Dataset):
    def __init__(self, image, boxe, label):
        self.image = image.values  # Extracts image data as numpy array
        self.boxe = boxe.values  # Extracts bounding box data as numpy array
        self.label = label.values  # Extracts label data as numpy array

    def __len__(self):
        
        return len(self.image)

    def __getitem__(self, idx):
       
        image = self.image[idx]  # Gets the image data at the specified index
        y_label = self.label[idx]  # Gets the label at the specified index
        x, y_boxe = Dataset_config.transformboxe(image, self.boxe[idx])  # Applies transformation to get bounding box
        return x, y_label, y_boxe

class Dataset_config:
    def create_mask(bb, x):
        
        rows, cols, *_ = x.shape  # Extracts rows and columns from the image shape
        Y = np.zeros((rows, cols))  # Initializes an array of zeros with the same shape as the image
        for i in range(len(bb)):
            bb[i] = int(bb[i])  # Converts bounding box coordinates to integers
        Y[bb[0]:bb[2], bb[1]:bb[3]] = 1.  # Sets the region within the bounding box to 1
        return Y

    def mask_to_bb(Y):
        
        cols, rows = np.nonzero(Y)  # Finds the coordinates of nonzero elements in the mask
        if len(cols) == 0:
            return np.zeros(4, dtype=np.float32)  # Returns zeros if no nonzero elements are found
        top_row = np.min(rows)  # Finds the minimum row coordinate
        left_col = np.min(cols)  # Finds the minimum column coordinate
        bottom_row = np.max(rows)  # Finds the maximum row coordinate
        right_col = np.max(cols)  # Finds the maximum column coordinate
        return np.array([left_col, top_row, right_col, bottom_row], dtype=np.float32)  # Returns bounding box coordinates
    
    def transformboxe(image, boxe):
        
        x = image  # Assigns the input image to x
        Y = Dataset_config.create_mask(boxe, x)  # Creates a mask for the bounding box
        return x, Dataset_config.mask_to_bb(Y)  # Returns the transformed image and bounding box
    
    def load(df):
        
        train_df = df.sample(frac=0.8, random_state=42)  # Splits the dataframe into training and validation sets
        val_df = df.drop(train_df.index)
        
        train_df.reset_index(drop=True, inplace=True)  # Resets the index of the training set
        val_df.reset_index(drop=True, inplace=True)  # Resets the index of the validation set

        dataset_train = CreateDataset(train_df["image"], train_df["boxe"], train_df["label"])  # Creates the training dataset
        dataset_val = CreateDataset(val_df["image"], val_df["boxe"], val_df["label"])  # Creates the validation dataset

        batch_size = 10  # Defines the batch size
        shuffle = True  # Shuffles the data at each epoch for better generalization

        train_dataloader = DataLoader(dataset_train, batch_size=batch_size, shuffle=shuffle)  # Creates the training dataloader
        val_dataloader = DataLoader(dataset_val, batch_size=batch_size)  # Creates the validation dataloader
        
        return train_dataloader, val_dataloader  # Returns the training and validation dataloaders
