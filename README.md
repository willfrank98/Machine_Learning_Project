# Machine_Learning_Project
Here I attempt to predict stock price movements via news 

## Instructions for Replication
Here are the necessary instructions to clone my github repository and run my code. My preferred environment was Anaconda 64-bit running on python 3.7.1, which ships with almost all the dependencies.  
1. Make sure all necessary dependencies are installed:  
    * numpy  
    * pandas  
    * scikit-learn  
    * lightgbm  
    * tensorflow  
    * and their dependencies
2. Clone my repo from https://github.com/willfrank98/Machine_Learning_Project.git  
3. First run 'python final_prep.py' to generate the final datasets which were too large for github.  
4. Here you can replicate my results by running 'python main_lgb.py' or 'python main_nn.py'.  
       
If you wish to replicate the full pipeline then do the following:  
1. Obtain a NYTimes API key from https://developer.nytimes.com/ (for free).  
2. In nyt_scraper.py, replace 'API_KEY_HERE' on line 28 with the API key, and set the appropriate year range on line 33 (add 1 to 2nd year). Run nyt_scraper.py.  
3. Set the appropriate year range (add 1 to 2nd year) on line 5 of nyt_combiner.py and run.    
4. Set the appropriate year range on line 5 of data_combiner.py and run.  
5. Set the appropriate year range on line 8 of final_prep.py and run.  
6. Finally point the test and train file paths to the correct files in main_lgp.py and main_nn.py and run those.  
7. To modify the train/test ratio do so on line  16 of final_prep.py.#  
