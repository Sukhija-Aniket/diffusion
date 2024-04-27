from multiprocessing import Pool
import  os
import sqlite3
from dotenv import load_dotenv
from PIL import Image
import torchvision.transforms.functional as TF

import time
from modelCode.model import UNet
from utils import testImage, save_mask
from modelCode.loadModel import model
from database import DBSCHEMA

load_dotenv()



PATHBASE = os.path.abspath(os.path.dirname(__file__))
def process(*file): #TODO: make changes to this function to work with diffusion model. 
    # Apply model here ##############################
    dbconn = sqlite3.connect(os.path.join(PATHBASE, os.getenv('DATABASE_PATH')))
    dbcurs = dbconn.cursor()

    time.sleep(5)
    # TODO: model working to be added here
    # input_file_path = file[2]
    output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'static/generated/{file[0]}.png')
    print(output_file_path)
    # image = Image.open(input_file_path)
    # tensor = testImage(model, image)
    # mask = TF.to_pil_image(tensor)
    # save_mask(mask, output_file_path)
    # time.sleep(1) 
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
