# TWITTER SENTIMENT ANALYSER
Author: Max Xie, maxxie@kth.se

### ABOUT THE DATA
--------------------------
Training data (trainData.csv): 65000 datapoints.   
Test data (testData.csv): 20000 datapoints.  

Datapoint has 4 attributes:
  1. Datapoint index number
  2. True sentiment (1=positive, 0=negative)
  3. Name of data source
  4. Tweet message

Example datapoint:  
532606,1,Sentiment140,Almost done unpacking!!!!! Beautiful day in my new city

### BEFORE DEPLOYING
--------------------------

1. Make sure your environment is using python 3.x  

2. Make sure you have the NLTK python package installed using:  
```
pip install nltk
```

3. Download all packages from NLTK via  
  ```
  >>python
  >>import nltk
  >>nltk.download()
  #install the package all_nltk
  ```
  
4. Make sure these files exist in the folder "data":
  1. **trainData.csv**
  2. **testData.csv**
  3. **test.csv**

### BUILDING THE MODEL
--------------------------
RUN THE FILE: **ModelBuilder.py**  
Model is stored in the file: **data/modelFile.csv**  

### RUNNING THE MODEL
--------------------------
RUN THE FILE: **Main.py**  
**data/modelFile.csv** is required for the model to run.  
if **data/modelFile.csv** does not exist, then run the file: **Modelbuilder.py**  

### TESTING THE MODEL
--------------------------
1. Choose "ENTER FILE"  

2. Input "data/testData.csv"  
