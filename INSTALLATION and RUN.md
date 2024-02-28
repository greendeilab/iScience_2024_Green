<h1>Table of Contents</h1>
<ol>
    <li><a href="#p1">Building a Training Set</a></li>
    <li><a href="#p2">Training a Computer Vision Model</a></li>
    <li><a href="#p3">Processing Videos with the Trained Model</a></li>
    <li><a href="#p4">Extracting Descriptive Information</a></li>
</ol>

<h1>Prerequisites</h1>
Before you can start the workflow below, you'll need to setup your local environment. Thankfully, all you need is a version of anaconda and git (miniconda works as well). You can download anaconda at the following <a href="https://www.anaconda.com/download" target="_blank">link</a>. Additionally, you can install git from <a href="https://git-scm.com/downloads" target="_blank">here</a>.

Once you have these installed, complete the following steps:

1. Pull up your terminal on your computer and ensure that git and anaconda is installed (if you have a windows machine, you'll have a separate terminal called 'Anaconda Prompt'). You can verify installation by running the following commands:
    > git --version<br/>
    > conda --version

2. If this is your first time using git, change the username and email on your machine with the following commands (the email should be the one you used to create your github account):

    > git config --global user.name "Your name"<br/>
    > git config --global user.email yourname@email.com

3. Clone the repository by running the following command: 
    > git clone https://github.com/greendeilab/iScience_2024_Green.git

    - You may need to specify your username and password. In this instance, the username is your github account name and the password is a personal access token. If you're not familiar with access tokens, they're essentially secret values that you can use to authenticate yourself. They are highly confidential and should not be shared with anyone. To create this token, go to: 
        -  Settings > Developer Settings > Personal Access Tokens > Tokens (classic) > Generate New Token
    
4. Navigate to the folder you just downloaded and go into /src

5. For MacOS users: in the anaconda prompt, run the following command to create the necessary environment to run the program:
    > conda create -n df --file env.yml 
- For windows users: in the anaconda prompt, run the following command to create the necessary environment to run the program:
    > conda create --file environment.yml

6. Once the environment has been created, activate it by using the following command:
    > conda activate df 
  
7. Assuming you're still in the /src directory, now run the application by using the following command:
    > python main.py

You should now see an application with two tabs:

![Image Extraction Tab](./readme_images/image-extraction-frame.png?raw=true)


![Prediction Analysis Tab](./readme_images/prediction-analysis-frame.png?raw=true)

As you can probably infer, the first tab will be used to create our training set. We'll be able to point it to a set of videos, it'll then extract frames at random and save them in a folder. The lower portion of the tab is specific to retraining. If your initial model wrongly identifies objects or it if completely misses them in certain frames, you can utilize this portion to extract those specific ones.

<h1 id="p1">Part 1: Building a Training Set</h1>

<h2 id="training">Extracting images</h2>
In order to extract images you need to follow the first page of the application <strong>Image Extraction</strong>. Select the folder with your videos and extract the number of images that you will require for training your model (this will depend on the size and complexity of your dataset). 

<h2 id="training">Annotations</h2>

<p> After installing the console and extracting the frames you can begin the next stage of the pipeline. Write the following commands</p>

> pip install LabelImg </br>
> LabelImg

<p>You should select <strong>YOLO</strong> and change your save directory to the path where you're planning to store labels for the <strong>images.</strong></p>

You need to follow this procedure in order to select every label correctly, and perform the correct analysis:
<ul>
<li> Click 'Change Save Dir' and switch it to the folder where you intend to store labels. Preferably call it <strong>labels.</strong></li>
<li> Use 'CreateRectBox' and select an object you want.

<li>After you created rectangular boxes for everything you want to identify click <strong>Ctrl+S</strong> and go to the next picture.</li>
</li>
</ul>
Here's a useful table of shortcuts:
<table>
  <tr>
    <th>Shortcut</th>
    <th>Function</th>
  </tr>
  <tr>
    <td>Ctrl + s</td>
    <td>Save the current prediction</td>
  </tr>
  <tr>
    <td>Ctrl + Shift + d</td>
    <td>Delete current image from the dataset</td>
  </tr>
  <tr>
    <td>w</td>
    <td>Create a rectangular box</td>
  </tr>
  <tr>
    <td>d</td>
    <td>Next image</td>
  </tr>
  <tr>
    <td>a</td>
    <td>Previous image</td>
  </tr>
</table>

<h1 id="p2">Part 2: Training a Computer Vision Model</h1>

<h1 id="p3">Part 3: Processing Videos with the Trained Model</h1>
The input into AdaptedNeuralNet.ipynb, then, is three sets (folders) of files:
<br/><br/>

<ol>
    <li>images: images to be used for training</li>
    <li>labels: labeled images that are the output of LabelImg </li>
    <li>videos: videos to be analyzed by the model</li>
</ol>

Note that AdaptedNeuralNet.ipynb currently expects three folders with these exact names (images, labels, and videos). Additional details of AdaptedNeuralNet.ipynb function are included as comments within the notebook. The output of AdaptedNeuralNet.ipynb will be one .npy file per input video that contain predictions for specified objects of the model. These files will be input into the Part 4 application.
![Prediction Analysis Tab](./readme_images/prediction-analysis-frame.png?raw=true)
<li>Run the analysis.</li>
</ul>

<h1 id="p4">Part 4: Extracting Descriptive Information</h1>

<h3>Producing the Excel file</h3>
<p>In order to produce the Excel file with predictions you need to follow this procedure:</p>
<ul>
<li>Run the following commands if you have closed the window with the application (this is what happens 99% of the time):</li>

    conda activate df
    cd (Directory where application is stored)
    python main.py
<li>Choose the Prediction Analysis. <br> *If you <strong>DO</strong> have compass files, upload them in the same folder with other labels <strong>AND</strong> select <strong>Calibrate setup.</strong> If you <strong>DON'T</strong> have compass files deselect Calibrate setup. </li>
