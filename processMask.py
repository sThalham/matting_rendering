import os, argparse
import numpy as np
#from scipy.misc import imread, imsave
import render_utils as utils
import cv2

print(np.__version__)

parser = argparse.ArgumentParser()
parser.add_argument('--img_dir', default='.')
args = parser.parse_args()

def threshold(gray):
    img = np.zeros(gray.shape, dtype=np.uint8)
    max_value = gray.max()
    img[gray < max_value * 0.8] = 255
    #img[gray > max_value * 0.8] = 255
    return img

def normalizeRho(gray):
    max_value = gray.max()
    gray = gray.astype(np.float32) / max_value * 255
    return gray.astype(np.uint8)

def processMask():
    file_list = os.listdir(args.img_dir)

    mask_list = [l for l in file_list if l.endswith('_mask.png')]
    print("Transforming mask: %d images" % len(mask_list))
    for mask in mask_list:
        mask_name = os.path.join(args.img_dir, mask)
        img_mask = cv2.imread(mask_name)
        if len(img_mask.shape) <=2: continue
        mask_gray = utils.rgb2gray(img_mask)
        mask_gray = threshold(mask_gray)
        cv2.imwrite(mask_name, mask_gray)

    rho_list =  [l for l in file_list if l.endswith('_rho.png')]
    print("Transforming attenuation mask: %d images" % len(rho_list))
    for rho in rho_list:
        rho_name = os.path.join(args.img_dir, rho)
        img_rho = cv2.imread(rho_name)
        if len(img_rho.shape) <=2: continue
        rho_gray = utils.rgb2gray(img_rho)
        rho_gray = normalizeRho(rho_gray)
        cv2.imwrite(rho_name, rho_gray)

if __name__ == '__main__':
    print('Image dir: %s\n' % args.img_dir)
    processMask()
