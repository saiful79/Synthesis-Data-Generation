from PIL import ImageFont, ImageDraw, Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random
import json
import os
# input_text = "1205 4789 8748 57812"

def sp_noise(image,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 220
            else:
                output[i][j] = image[i][j]
    image = cv2.GaussianBlur(output,(5, 5), 30)
    return image

def DataGenerator(root,img_dir,data):
    # input_text = "1205 4789 8748 57812"
    data_dic = {}
    for i in data.split(" "):
        print(i)
        input_text = i
        if len(input_text) >10:
            width = 450
        else:
            width = 110  
        image = np.zeros((40,width,3), np.uint8)
        image = sp_noise(image,0.05)
        pil_im = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_im)
        font = ImageFont.truetype("font/Siyamrupali.ttf", 32)
        draw.text((1,1),input_text, font=font)
        cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
        image = sp_noise(cv2_im_processed,0.05)
        image = 255 - image
        orginal = root+"/"+img_dir+"/orginal_"+str(i)+".png"
        cv2.imwrite(orginal,image)        
        data_dic[orginal]=input_text
    with open(root+'/annotation.json', 'w',encoding='utf8') as outfile:
        json.dump(data_dic, outfile,ensure_ascii=False)
if __name__ == "__main__":
    root = "dataset"
    data_str="রওশন এরশাদ​ আবারও জাতীয় পার্টিতে (জাপা) জি এম কাদের ও রওশন এরশাদের মধ্যে ক্ষমতার দ্বন্দ্ব দেখা দিয়েছে।"
    if not os.path.isdir(root):
        os.makedirs(root)
    input_path = "data"
    if not os.path.isdir(root+"/"+input_path):
        os.makedirs(root+"/"+input_path)
    DataGenerator(root,input_path,data_str)