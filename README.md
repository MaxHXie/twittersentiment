# TWITTER SENTIMENT ANALYSER
AUTHOR: MAX XIE MAXXIE@KTH.SE

### BEFORE DEPLOYING
--------------------------

1. MAKE SURE YOUR ENVIRONMENT IS USING PYTHON 3.X

2. MAKE SURE YOU HAVE THE NLTK PYTHON PACKAGE INSTALLED 

3. DOWNLOAD ALL PACKAGES FROM NLTK VIA
  ```
  >>python
  >>import nltk
  >>nltk.download()
  ```
  
4. MAKE SURE THESE FILES EXIST IN THE FOLDER "data":
  1. **trainData.csv**
  2. **testData.csv**
  3. **test.csv**

### BUILDING THE MODEL
--------------------------
RUN THE FILE: **ModelBuilder.py**
MODEL IS STORED IN THE FILE: **data/modelFile.csv**

### RUNNING THE MODEL
--------------------------
RUN THE FILE: **Main.py**
**data/modelFile.csv** is required for the model to run.
if **data/modelFile.csv** does not exist, then run the file: **Modelbuilder.py**

### TESTING THE MODEL
--------------------------
1. CHOOSE ENTER FILE
2. ENTER "data/testData.csv"
