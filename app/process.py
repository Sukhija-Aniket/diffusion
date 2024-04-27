from multiprocessing import Pool
import  os
import sqlite3
from dotenv import load_dotenv
from PIL import Image
import torchvision.transforms.functional as TF
import torch
import time
from modelCode.loadModel import diffusion_alpha, diffusion_animals
from torchvision.utils import save_image
from database import DBSCHEMA

load_dotenv()



animals = []
numbers = []

PATHBASE = os.path.abspath(os.path.dirname(__file__))
def process(*file): #TODO: make changes to this function to work with diffusion model. 
    # Apply model here ##############################
    dbconn = sqlite3.connect(os.path.join(PATHBASE, os.getenv('DATABASE_PATH')))
    dbcurs = dbconn.cursor()

    # TODO: model working to be added here
    modelClass = file[1]
    label = file[2]
    num_images = 1
    if modelClass == 'numbers':
        y = torch.Tensor([numbers[int(label)]] * num_images).long()
        generated_img = diffusion_alpha.sample(True, y).float()
    elif modelClass == 'animals':
        y = torch.Tensor(animals[int(label)] * num_images).long()
        generated_img = diffusion_animals.sample(True, y).float()
    output_file_path = f'static/generated/{file[0]}.png'
    generated_img = generated_img[0]
    save_image(generated_img, output_file_path)
    # TODO: model working to be added here
    
    dbcurs.execute(f"""UPDATE user SET processed_path="{output_file_path}" WHERE user_uuid="{file[0]}"; """)
    dbcurs.execute(f"""UPDATE user SET status="Done" WHERE user_uuid="{file[0]}"; """)

    dbconn.commit()
    dbconn.close()
    #################################################

def generateImage():

    dbconn = sqlite3.connect(os.path.join(PATHBASE, os.getenv('DATABASE_PATH')))
    dbcurs = dbconn.cursor()

    query = dbcurs.execute(f'SELECT * FROM user WHERE status="Pending" ORDER BY created_at').fetchall()
    # print(query)
    dispatcher = []
    for file in query:
        dispatcher.append( [file[DBSCHEMA['user_uuid']], file[DBSCHEMA['model']], file[DBSCHEMA['button']]] )

    dbconn.commit()
    dbconn.close()

    p = Pool(processes=8)
    p.starmap(process, dispatcher)
    p.close()
    p.join()

def main():

    dbconn = sqlite3.connect(os.path.join(PATHBASE, os.getenv('DATABASE_PATH')))
    dbcurs = dbconn.cursor()

    query = dbcurs.execute(f'SELECT * FROM user WHERE status="Pending" ORDER BY created_at').fetchall()
    # print(query)
    dispatcher = []
    for file in query:
        dispatcher.append( [file[DBSCHEMA['file_uuid']], file[DBSCHEMA['name']],
            file[DBSCHEMA['path']]] )

    dbconn.commit()
    dbconn.close()

    p = Pool(processes = 8) #max(len(data),cpu_count())
    result_mult = p.starmap(process, dispatcher)
    p.close()
    p.join()
