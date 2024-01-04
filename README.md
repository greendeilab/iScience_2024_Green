# iScience_2024_Green
This repository contains information related to the iScience publication "Modular switches control a shift in monarch butterfly migratory flight behavior at their Mexican overwintering sites" by Delbert A. Green II, Sean Polidori and Samuel Stratton.

<h1>Overview</h1>
The workflow for this project includes four essential parts:
<br/><br/>

<ol>
    <li>Part 1: Build training and test image sets for model training in LabelImg.</li>
    <li>Part 2: Train a computer vision model to identify the monarch as well as any key characteristics of our setup.</li>
    <li>Part 3: Run the model on input videos (i.e. have our model predict on each frame of our videos).</li>
    <li>Part 4: Extract descriptive information from the videos (e.g. butterfly heading direction, wingbeat frequency, etc.).</li>
</ol>

Parts 1 and 4 are provided as independent applications that are available within this repository. Installation instructions for both applications are found in the INSTALLATION file. Part 1 uses LabelImg to specify objects of interest within videos. Part 4 includes code to generate the flight characteristics (e.g. flight time, direction heading, etc.) using custom algorithms to transform the prediction data into something useful).

Parts 2 and 3 are performed within AdaptedNeuralNet.ipynb (i.e. training a new model and running this model on a set of videos).  The input into AdaptedNeuralNet.ipynb, then, is three sets (folders) of files:
<br/><br/>

<ol>
    <li>images: images to be used for training</li>
    <li>labels: labeled images that are the output of LabelImg </li>
    <li>videos: videos to be analyzed by the model</li>
</ol>

Note that AdaptedNeuralNet.ipynb currently expects three folders with these exact names (images, labels, and videos). Additional details of AdaptedNeuralNet.ipynb function are included as comments within the notebook. The output of AdaptedNeuralNet.ipynb will be one .npy file per input video that contain predictions for specified objects of the model. 

<h1>Licensing</h1>
WORDS

