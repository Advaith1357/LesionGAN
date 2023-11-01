# LesionGAN
## Paper: ResearchPaper.pdf
## Project Description:

Computed Tomography (CT) scans are the preferred imaging modality for lesion detection. On average, the daily human error rate of lesion detection by radiologists from CT scans is 4%, and with there being approximately 1 billion scans annually, this means 40 million patients are misdiagnosed annually. To reduce this high error rate of missed lesions, many have turned to deep learning algorithms to assist in automating lesion detection. However, obtaining large-scale annotated datasets in the medical domain is challenging. While traditional data augmentation is a commonly adopted remedy, it often falls short of introducing sufficient variability into the dataset. This research explores the use of a specialized
Wasserstein generative adversarial network with gradient penalty (WGAN-GP) to synthesize artificial CT scans of lesions. The aim is to generate more diverse data points, potentially enhancing the performance of deep learning neural networks in lesion detection compared to traditional augmentation methods. The research methodology encompasses data acquisition, image preprocessing, and the formulation of traditionally augmented, GAN-augmented, and combined datasets. Subsequently, each dataset is evaluated using a deep neural network classifier. Evaluation of the test results indicates that the combined dataset outperformed the others, achieving an accuracy of 78.95% alongside superior average recall and precision metrics.
In contrast, the least effective dataset, which was solely preprocessed without any augmentation, has a test accuracy of 71.93%. Additionally, the traditionally-augmented dataset and the GAN-augmented dataset performed equally well, yielding accuracies of 77.19% and 75.44%. The findings underscore the potential benefits of employing synthetic augmentation in medical imaging tasks, paving the way for more precise lesion detection methodologies.

## Installation
### Dataset
The data used for the experiments was sourced from the DeepLesion Dataset. We used a total of 32000 images to conduct our experiments. The dataset includes eight categories of various lesion types, including bone, abdomen, mediastinum, liver, lung, kidney, soft tissue, and pelvis, which are used in this research. The dataset was split into train, validating, and test subsets. This resulted in 23205, 5775, and 3020 images in the train, validation, and test subsets. To avoid data leakage, the splitting was done before data augmentation on the training dataset. To reduce the large file size of the dataset, the NIHCC compiled the images in a monochrome 64-bit image, resulting in barely defined edges and regions. Within the dataset itself, several steps to re-improve data quality were recommended, from subtracting pixel intensity to upscaling image bits. However, in this research, neither of these methods proved to be effective, as the resulting images were not refined enough for feature extraction using deep learning. Instead, we created an algorithm to contrast the separate shades of gray within the image, and after tuning, this proved to be far more effective in creating higher-quality, sharp-edged images directly from the DeepLesion dataset as compared to the other methods mentioned earlier. The input and output images look like the following:

#
![Preprocessing_Before](https://github.com/Advaith1357/LesionGAN/assets/115594563/05717ab3-e519-4fea-9171-af9f25555515)
![Preprocessing_After](https://github.com/Advaith1357/LesionGAN/assets/115594563/ffdf1000-76dc-411f-b974-d231c485d7b2)

### Data Augmentation Generator
Data augmentation is a set of techniques to artificially increase the amount of data by generating new data points from existing data. This includes making small changes to data or using deep learning models to generate new data points. Data augmentation methods, specifically geometric transformations to images are easy to apply and have been shown to improve deep learning model’s accuracy. Hence, a data augmentation filter was designed for the same. As the processed data passes through the data augmentation filter, the filter performs a randomized series of simple augmentation techniques such as rotation and trimming. This randomized set of operations creates another image, that is typically similar
in structure to the original processed images but can be differentiated by the classification algorithm. The entire dataset of originally processed images is then run through this filter 3 times, creating a dataset 3 times larger than the original dataset. In order to operate, download the file DataAugmentationGenerator.py and open it in Google Colaboratory or any other IDE. Connect the training images to the generator and it will create the new dataset.  

![TA_Before](https://github.com/Advaith1357/LesionGAN/assets/115594563/14202ef4-e682-44c3-87ba-78efad80843a)
![TA_After](https://github.com/Advaith1357/LesionGAN/assets/115594563/b72e2318-16b1-44d5-bb0b-c87457927c40)
###### WARNING:
The data augmentation generator does not limit itself on the size of the dataset created. It is fully capable of crashing both online IDEs and offline IDEs. Google Colaboratory in particular has been notorious for crashing under the processing of the generator. However, when we used Pycharm, the issue subsided, although it took several hours to create the dataset.

### Generative Adversarial Network Training
The actual training of the Generative Adversarial Network is relatively simple. Simply download the file titled ures_ntcppy_of_gan.py, connect the dataset of lesion images to the file and run.

###### WARNING:
It is important to note that GAN training can be computationally intensive and time-consuming. The duration of the training process may vary depending on factors like dataset size, model architecture, and available computational resources. We recommend that users be prepared for potentially extended training times and ensure they have access to a sufficiently powerful computing environment. If mode collapse(Images begin to rapidly drop in quality mid-training so that it is just a black screen) occurs, it is best to end the runtime and restart, as the GAN has previously struggled in recovering its previous gains.

###### The remaining files are used solely by LesionGAN developers for testing. Please do not use these without consulting a moderator prior
