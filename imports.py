import os
import random
from torch.utils.data import DataLoader, Dataset
# from torch.utils.tensorboard import SummaryWriter
import cv2
import torch
import pandas as pd
import torch.nn as nn
import torch.optim as optim
from PIL import Image
from torchvision import transforms
from sklearn.model_selection import train_test_split

main_dir = "C:\\Users\\sveta\\Documents\\People_detection2.0"

dataset_path = f"{main_dir}\\drone_dataset\\train"
csv_path = f"{main_dir}\\drone_dataset\\_annotations.csv"


imgs_train_path = "\\images\\train"
imgs_val_path = "\\images\\val"
imgs_test_path = "\\images\\test"

annotations_train_path = "\\labels\\train"
annotations_val_path = "\\labels\\val"
annotations_test_path = "\\labels\\test"