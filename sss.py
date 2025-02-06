import os
import datetime
import hashlib
import pandas as pd
from glob import glob
from tqdm import tqdm
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import paramiko
import shutil
from argparse import ArgumentParser
import logging
import sys
from scipy import interpolate as scipy_interpolate

import torch
import numpy as np
# from umap import UMAP

# from src.tables import eqp_table
# from src.inference import Inference

# from src.misc import set_dir, mode, get_fname, mode, set_dir, save_json, load_json

# from src.build import read_data_file
# from src.datas import TrainDataset
from torch.utils.data import DataLoader
# from src.models import get_attn
# from src.misc import load_yaml
# from src.build import *

import warnings
warnings.filterwarnings(action='ignore')




parser = ArgumentParser()
parser.add_argument('--date', type=str)
args = parser.parse_args()


today_date = datetime.today().strftime("%Y_%m_%d")[2:]
check_last_month = False

if int(today_date[-2:]) < 7:
    check_last_month = True

#####################################################
 #   Get X filenames
#####################################################
host = "10.150.9.121" 
port = 22 
SSH_Client = paramiko.SSHClient()
# transprot = paramiko.transport.Transport(host,port)
userId = "sksl_ds02"  # example
password = 'sksl_ds02!' # example
SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
SSH_Client.connect(hostname=host,
                port=port,
                username=userId,
                password=password,
                look_for_keys=False)
sftp_client = SSH_Client.open_sftp()


remote_x_path = f'/home/sksl_ds02/ANALYSIS_DATA_SET/X_TEMP/3200_WIRE_SAW/{today_date[:5]}'
x_dir_list = sftp_client.listdir(remote_x_path)

if check_last_month:
    last_month = datetime.strptime(today_date, '%y_%m_%d') - timedelta(weeks=1)
    last_month = last_month.strftime('%y_%m_%d')
    remote_x_path = f'/home/sksl_ds02/ANALYSIS_DATA_SET/X_TEMP/3200_WIRE_SAW/{last_month[:5]}'
    x_dir_list.extend(sftp_client.listdir(remote_x_path))

sftp_client.close()
SSH_Client.close() 


usage: ipykernel_launcher.py [-h] [--date DATE]
ipykernel_launcher.py: error: unrecognized arguments: --f=c:\Users\SKsiltron\AppData\Roaming\jupyter\runtime\kernel-v324ab0c7b101ffde14d9a9966ff050e95fea44d1c.json
An exception has occurred, use %tb to see the full traceback.

SystemExit: 2
