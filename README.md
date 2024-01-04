# iScience_2024_Green
This repository contains information related to the iScience publication "Modular switches control a shift in monarch butterfly migratory flight behavior at their Mexican overwintering sites" by Delbert A. Green II, Sean Polidori and Samuel Stratton.

<h1>Overview</h1>
The workflow for this project/application includes three essential parts:
<br/><br/>

<ol>
    <li>Part1: Build training and test image sets for model training.</li>
    <li>Part 2: Train a computer vision model to identify the monarch as well as any key characteristics of our setup.</li>
    <li>Part 3: Run the model on input videos (i.e. have our model predict on each frame of our videos).</li>
    <li>Part 4: Extract descriptive information from the videos (e.g. butterfly heading direction, wingbeat frequency, etc.).</li>
</ol>

The code included here (AdaptedNeuralNet.ipynb) focuses on the second and third parts, i.e. training a new model and running this model on a set of videos. We performed Part 1 using the LabelImg software as described in the manuscript. The input into AdaptedNeuralNet.ipynb, then, is three sets (folders) of files:
<br/><br/>

<ol>
    <li>images: images to be used for training</li>
    <li>labels: labeled images that are the output of LabelImg </li>
    <li>videos: videos to be analyzed by the model</li>
</ol>

Note that AdaptedNeuralNet.ipynb currently expects three folders with these exact names (images, labels, and videos). Additional details of AdaptedNeuralNet.ipynb function are included as comments within the notebook.

The output of AdaptedNeuralNet.ipynb will be one .npy file per input video that contain predictions for specified objects of the model. Part 4, then, involves using a text processor (e.g. grep, awk) to extract information of interest from .npy files (e.g. flight time, direction heading, etc.).
