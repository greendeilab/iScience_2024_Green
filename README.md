This repository contains information related to the iScience publication "Modular switches control a shift in monarch butterfly migratory flight behavior at their Mexican overwintering sites" by Delbert A. Green II, Sean Polidori and Samuel Stratton.

<h1>Overview</h1>
The workflow for this project includes four essential parts:
<br/><br/>

<ol>
    <li>Building a training set</li>
    <li>Training a computer vision model</li>
    <li>Processing videos with the trained model</li>
    <li>Extracting descriptive information from the videos (e.g. butterfly heading direction, wingbeat frequency, etc.).</li>
</ol>

To complete Parts 1 & 4, you'll need to use the Python application found in this repository. Note that this can be run on your local machine. Parts 2 & 3 are expected to be run on Google Colab (or a machine with a GPU) using the provided notebook 'AdaptedNeuralNet.ipynb'. Installation and running instructions can be found in the 'INSTALLATION & RUN' file.

The input into AdaptedNeuralNet.ipynb, then, is three sets (folders) of files:
<br/><br/>

<ol>
    <li>images: images to be used for training</li>
    <li>labels: labeled images that are the output of LabelImg </li>
    <li>videos: videos to be analyzed by the model</li>
</ol>

Note that AdaptedNeuralNet.ipynb currently expects three folders with these exact names (images, labels, and videos). Additional details of AdaptedNeuralNet.ipynb function are included as comments within the notebook. The output of AdaptedNeuralNet.ipynb will be one .npy file per input video that contain predictions for specified objects of the model. These files will be input into the Part 4 application.

<h2>Author</h2>
Primary author and maintainer of the code found here is Sean Polidori (seanpolidori0@gmail.com). 

<h2>Licensing</h2>
This project is licensed under the GNU General Public License v.3.0.

<h2>Citation</h2>
If this code is used in work that leads to a scientific publication, we will appreciate acknowledgement of this  by citing the iScience publication (Green II et al. 2024).
