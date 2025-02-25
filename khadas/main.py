import argparse

from config import *
from tools import *
from mqtt import get_client, subscribe

import os
import time
from datetime import datetime
from RNN import RNNPipeline
from get_data import GetDataPipeline

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
current_time = datetime.now()
start_time = time.time()

rnn_pipeline = RNNPipeline()
get_data_pipeline = GetDataPipeline()

config_finger_counter = 0
config_time_counter = 0

def loop_default(client, userdata, msg, config_path:str="default"):
    data = msg.payload.decode()
    #print(data)
    if config_path != "default" : 
        thresholds = read_config(config_path=config_path)
        data = convert_data_str_int(data, thresholds=thresholds)
    else : 
        data = convert_data_str_int(data)
    print(data)

def get_config(client, userdata, msg, config_path:str='default', time_sleep=5):
    global config_finger_counter, config_mode, start_time  
    execution_time = time.time() - start_time
    print(f"Get the {'min' if config_mode != 'min' else 'max'} of {config_finger_counter + 1}'st finger on {time_sleep - execution_time} seconds")
    
    if time_sleep - execution_time <= 0 : 
        config_mode = 'min' if config_mode != 'min' else 'max'
        print("Saving the data")
        
        data = msg.payload.decode()
        data = convert_data_str_int(data)

        os.makedirs('config', exist_ok=True)
        save_data(f"{config_mode} of {config_finger_counter + 1}'st finger : {data.split(', ')[config_finger_counter]}, ", filepath=os.path.join(
            'config', f'{config_path}.txt'))
        if config_mode == 'min': 
            config_finger_counter += 1
        
        if config_finger_counter >=  5 : 
            config_finger_counter = 0
            print("Configuration saved successfully")
            exit()
        
        start_time = time.time()

def get_data(client, userdata, msg, letter:str='a', name='default', id=1, time_get_data=3):
    global start_time  

    execution_time = time.time() - start_time
    data = msg.payload.decode()
    
    data = get_data_pipeline(data, letter, name, id)
    
    print(f'{round(execution_time, 2)} : {data}')
    if execution_time >= time_get_data :
        exit()

def predict(client, userdata, msg, seq_len=20, config_path:str="default"):
    data = msg.payload.decode()
    rnn_pipeline(data)

if __name__ == '__main__':
    # Setup argument parsing
    parser = argparse.ArgumentParser(description='Get data and save it.')
    parser.add_argument(
        '--fn', type=str, default='loop_default', help='Specify the function')
    parser.add_argument('--letter', type=str, default='a',
                        help='Letter used for the directory and filename.')
    parser.add_argument('--id', type=int, default=1,
                        help='ID used for the filename')
    parser.add_argument('--seq_len', type=int, default=20,
                        help='Sequence len gesture data for prediction')
    parser.add_argument('--config_path', type=str, default='default', help='Config path used for saving the configuration')
    parser.add_argument('--name', type=str, default='default', help='Name used for saving the configuration')

    # Parse arguments
    args = parser.parse_args()

    client = get_client(client_id=CLIENT_ID, username=USERNAME,
                        password=PASSWORD, broker=BROKER, port=PORT)

    if (args.fn == 'get_data'):
        print(f'Saving the data into data/{args.letter}-{args.id}.txt')
        subscribe(client, topic=TOPIC, loop=lambda client, userdata, message: get_data(
            client, userdata, message, letter=args.letter, name=args.name, id=args.id))
    
    elif (args.fn =='config'):
        print(f'Saving the configuration into/{args.config_path}.txt')
        start_time = time.time()
        subscribe(client, topic=TOPIC, loop=lambda client, userdata, message: get_config(
            client, userdata, message, config_path=args.config_path))

    elif (args.fn =='predict'):
        print(f'Saving the data into predict-{current_time}.txt')
        subscribe(client, topic=TOPIC, loop=lambda client, userdata, message: predict(
            client, userdata, message, seq_len=args.seq_len, config_path=args.config_path))
    
    else:
        subscribe(client, topic=TOPIC, loop=lambda client, userdata, message: loop_default(
            client, userdata, message, config_path=args.config_path))

    client.loop_forever()
