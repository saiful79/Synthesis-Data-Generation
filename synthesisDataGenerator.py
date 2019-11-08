from PIL import ImageFont, ImageDraw, Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random
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
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

def DataGenerator(img_dir,filename,iteration_number):
	# input_text = "1205 4789 8748 57812"
	file = open(filename,"w")

	for i in range(iteration_number):

		numbers = random.sample(range(10), 4)

		input_text = ''.join([str(elem) for elem in numbers]) 

		# print(len(input_text))

		if len(input_text) > 4:
			width = 450
		else:
			width = 120  

		image = np.zeros((70,width,3), np.uint8)

		# Convert to PIL Image
		cv2_im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		pil_im = Image.fromarray(cv2_im_rgb)

		draw = ImageDraw.Draw(pil_im)

		# Choose a font
		font = ImageFont.truetype("Roboto-Regular.ttf", 40)

		# Draw the text
		draw.text((10, 10),input_text, font=font)

		# Save the image
		cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

		image = 255 - cv2_im_processed

		orginal = img_dir+"/orginal_"+str(i)+".png"

		noise = img_dir+"/noise_"+str(i)+".png"

		if i <=4000:

			cv2.imwrite(orginal, image)
			file.write(orginal+" ok "+input_text+"\n")

		elif i>=4001 and i <=8000:
			noise_img = sp_noise(image,0.05)
			cv2.imwrite(noise, noise_img)
			file.write(noise+" ok "+input_text+"\n")

		elif i>=8001 and i <=12000:
			blurred_image = cv2.GaussianBlur(image,(5, 5), 30)

			blu_img_name = img_dir+"/blurred_"+str(i)+".png"

			cv2.imwrite(blu_img_name, blurred_image)
			file.write(blu_img_name+" ok "+input_text+"\n")
		else:

			noise_img_blur = cv2.GaussianBlur(noise_img,(3, 3), 30)

			blu_noise_img_name = img_dir+"/blurrednoise_"+str(i)+".png"

			cv2.imwrite(blu_noise_img_name, noise_img_blur)
			file.write(blu_noise_img_name+" ok "+input_text+"\n")

		print(i,"Data create DONE")

		# plt.imshow(noise_img_blur)
		# plt.show()
		# plt.imshow(blurred_image)
		# plt.show()
	file.close()
 
if __name__=="__main__":

    iteration_number = 16000

    input_path = "data"
    mapping_file = "sintesis.txt"

    DataGenerator(input_path,mapping_file,iteration_number)