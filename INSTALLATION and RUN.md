<h1>Installation and Running Parts 1, 4</h1>

1. Pull up your terminal on your local computer and ensure that git and anaconda is installed (if you have a windows machine, you'll have a separate terminal called 'Anaconda Prompt'). You can do this by running the following commands:
    > git --version<br/>
    > conda --version

2. If this is your first time using git, change the username and email on your machine with the following commands (the email should be the one you used to create your github account):

    > git config --global user.name "Your name"<br/>
    git config --global user.email yourname@email.com

3. Clone the repository by running the following command: 
    > git clone https://github.com/greendeilab/iScience_2024_Green.git

    - You may need to specify your username and password. In this instance, the username is your github account name and the password is a personal access token. To create this token, go to: 
        -  Settings > Developer Settings > Personal Access Tokens > Tokens (classic) > Generate New Token
    
4. Navigate to the folder you just downloaded and go into /src

5. For MacOS users: in the anaconda prompt, run the following command to create the necessary environment to run the program:
    > conda create -n df --file env.yml 
- For windows users: in the anaconda prompt, run the following command to create the necessary environment to run the program:
  > conda create --file environment.yml

6. Once the environment has been installed, activate it by using the following command:
    > conda activate df 
  
7. Assuming you're still in the /application directory, now run the application by using the following command:
    > python main.py

The installed program contains the code for performing both Part 1 (image labeling) and Part 4 (video analysis).

<h2>Running Part 1</h2>

<h3 id="training">Extracting images</h3>
In order to extract images you need to follow the first page of the application <strong>Image Extraction</strong>. Select the folder with your videos and extract the number of images that you will require for training your model (this will depend on the size and complexity of your dataset). 

<h3 id="training">Creating the dataset</h3>

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

<h2>Running Part 4</h2>

<h3>Producing the Excel file</h3>
<p>In order to produce the Excel file with predictions you need to follow this procedure:</p>
<ul>
<li>Run the following commands if you have closed the window with the application (this is what happens 99% of the time):</li>

    conda activate df
    cd (Directory where application is stored)
    python main.py
<li>Choose the Prediction Analysis. <br> *If you <strong>DO</strong> have compass files, upload them in the same folder with other labels <strong>AND</strong> select <strong>Calibrate setup.</strong> If you <strong>DON'T</strong> have compass files deselect Calibrate setup. </li>

![Prediction Analysis Tab](./readme_images/prediction-analysis-frame.png?raw=true)
<li>Run the analysis.</li>
</ul>
