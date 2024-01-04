<h1>Installation</h1>

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
