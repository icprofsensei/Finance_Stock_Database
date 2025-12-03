# Green Stock Data Management

<img width="240" height="185" alt="image" src="https://github.com/user-attachments/assets/761f54e6-7202-4aef-b7fd-a88f4ef17afb" />
<img width="280" height="140" alt="image" src="https://github.com/user-attachments/assets/c879e989-b7ab-4b6d-9acb-f9b7a16ef2b7" />

<img width="240" height="185" alt="image" src="https://github.com/user-attachments/assets/cc419505-20ed-4f7a-9108-7dd9d53a3e2d" />
<img width="280" height="140" alt="image" src="https://github.com/user-attachments/assets/a10d1f78-27e9-498b-8cc6-e4e27e1a0c56" />

:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|:----------------------

### This is an all-in-one python GUI and pipeline to enable green stock analysis, whilst managing free API rate limits automatically.

Pre-requisites: Python or Conda is installed on your machine. The following tutorial is for windows devices but can be adapted for MacOS. 

1) Download this repository as a zip folder and then extract all to your chosen directory. Alternatively, if you have git installed, you can clone via:

            git clone https://github.com/icprofsensei/Finance_Stock_Database.git

2) Open the command prompt and navigate to your repository:
   
            cd [YOUR PROJECT DIRECTORY]
3) Create a data folder within your directory:

            mkdir data

5) Create a virtual environment for your repository:
   
            python -m venv env

6) Activate your virtual environment:
   
            env\Scripts\activate.bat

8) Depending on your package manager:

      a) Install all the required packages using venv or conda:
            (env) pip install -r requirements.txt

     b) Install the full environment using poetry or uv:
  
            poetry install 
            
            uv sync

9) Visit the following sites and create a free account:
    
     a) *https://www.tiingo.com/documentation/general/connecting*
     Save the API token once created.

     b) *https://www.alphavantage.co/support/#api-key*
     Save the API token once created.

11) To make these keys accessible in your project, run the file initialiser.py, this will allow you to enter your saved API tokens/keys for each site. The script will automatically save the tokens into a JSON file in your data folder. This file will allow the main API caller to automatically manage API rate limits per hour / day.

                python -m initialiser

12) To begin creating green stock datasets, run stock_gui.py:

                python -m stock_gui






















