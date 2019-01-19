# TWITTER SENTIMENT ANALYSER
Author: Max Xie, maxxie@kth.se

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
