# Mask Detection 
This is a mask detector deployed as a telegram bot.

It classifies human faces in an image into either:
- mask
- no-mask

with their respective bounding boxes and class probabilities. 

## Contents
- [How to use](#h2u)
- [Data](#data)
- [Training and inference](#train)
- [Deployment](#deploy)
- [Future Improvements](#todo)

## <a name="h2u"></a> How to use
Telegram web/app on desktop: [link](https://t.me/AK_Mask_bot)

Telegram app on mobile: search for @AK_Mask_bot

## <a name="data"></a> Data
Data is provided by Roboflow under the public domain license and shared by Joseph Nelson.

After augmentation of rotation and brightness adjustments, we have 349 images with 70/20/10 train/valid/test split.

Source: https://public.roboflow.com/object-detection/mask-wearing/4

#### Overview
The Mask Wearing dataset is an object detection dataset of individuals wearing various types of masks and those without masks. The images were originally collected by Cheng Hsun Teng from Eden Social Welfare Foundation, Taiwan and relabled by the Roboflow team.

Example image (some with masks, some without):

![alt text](https://github.com/LeKwee/Mask_Detection/blob/master/images/readme_pic1.PNG?raw=true)

## <a name="train"></a> Training
This detector is trained using AlexeyAB's darknet/YoloV4 [(git)](https://github.com/AlexeyAB/darknet)

It trained for about ~2000 epochs achieving:
- mean average precision (mAP@0.50) = 97.85 % 
- class mask, ap = 99.11%
- class no-mask, ap = 96.59%  

Notebook for training can be found [here](https://github.com/LeKwee/Mask_Detection/tree/master/Mask_detection_yolov4_darknet/notebooks/Training)

Notebook for inference can be found [here](https://github.com/LeKwee/Mask_Detection/tree/master/Mask_detection_yolov4_darknet/notebooks/Inference)

## <a name="deploy"></a> Deployment
Deployment was made using the telegram bot api using webhooks and host through heroku using it free services.

To deploy:
- git add (everything in telegram_bot folder)
- git commit
- git push heroku master 
  
you will have to first get your telegram token and a heroku link and update in a config.ini file.
 
## <a name="todo"></a> Future Improvements
- [ ] Improvements to be made on the inference speed. Maybe try a smaller model like tiny-yolo.

- [ ] To provid mask detection on videos on top of current image capabilities.

- [x] Frequently wrongly predicts images where there is a single person with no mask on. (seems like it requires both classes to be in image to predict no-mask class). This maybe due to imbalanced data set consisting of 1.9k mask vs 300 no-mask labels. To collect more no-mask data to balance training dataset.

     - Collected more no-mask data. The ratio now is ~1300 mask to ~900 no-mask
      
     - With new no-mask data balancing, model achieved:

       - mean average precision (mAP@0.50) = 98.59 % 

       - class mask, ap = 98.65% 

       - class no-mask, ap = 98.53%
     - Personal testing, seems to perform better now on single person focus images with no mask on.
