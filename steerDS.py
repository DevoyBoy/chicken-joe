import numpy as np
from glob import glob
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
import cv2
from glob import glob
from os import path

CUTOFF = 0.2

class SteerDataSet(Dataset):
    
    def __init__(self,root_folder,img_ext = ".jpg" , transform=None):
        self.root_folder = root_folder
        self.transform = transform        
        self.img_ext = img_ext        
        self.filenames = glob(path.join(self.root_folder,"*" + self.img_ext))
        self.totensor = transforms.ToTensor()
        
    def __len__(self):        
        return len(self.filenames)
    
    def __getitem__(self,idx):
        f = self.filenames[idx]       

        # crop top of image
        img = self.crop_and_resize(cv2.imread(f))

        if self.transform == None:
            img = self.totensor(img)
        else:
            img = self.transform(img)

        try:
            steering = f.split("/")[-1].split(self.img_ext)[0][6:]
            steering = np.float32(steering)
        except:
            steering = f.split('\\')[-1].split(self.img_ext)[0][6:]
            steering = np.float32(steering)

        # convert steering angle to classification classes
        if steering < -CUTOFF:
            steer = 0   # left
        elif steering > CUTOFF:
            steer = 1   # right
        else:
            steer = 2   # straight

        sample = {"image":img , "steering":steer}        
        # print(sample)

        return sample

    def crop_and_resize(self, image):
        cropped_im = image[80:,:]
        resized_im = cv2.resize(cropped_im, dsize=(64,64),interpolation=cv2.INTER_CUBIC)
        return resized_im
        
        

def test():
    transform = transforms.Compose(
        [transforms.ToTensor(), 
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    ds = SteerDataSet("data/",".jpg",transform)

    print("The dataset contains %d images " % len(ds))

    ds_dataloader = DataLoader(ds,batch_size=1,shuffle=True)
    for S in ds_dataloader:
        im = S["image"]    
        y  = S["steering"]

        cv2.imshow('image', np.array(im))
        cv2.waitKey(0)

        print(im.shape)
        print(y)
        break



if __name__ == "__main__":
    test()
