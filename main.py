import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
def cleanData(file):
  df=pd.read_csv(file)
  notinclude = 'timeOpen;timeClose;timeHigh;timeLow;timestamp;name'
  cols = df.columns

  s=cols[0].split(';')

  for i in range(0, len(s)):

    if s[i] not in notinclude:
      df[s[i]]=0
  df['timeOpen;timeClose;timeHigh;timeLow;name;open;high;low;close;volume;marketCap;timestamp']=df['timeOpen;timeClose;timeHigh;timeLow;name;open;high;low;close;volume;marketCap;timestamp'].str.split(';')
  for i in range(0,len(df)):
    li = df['timeOpen;timeClose;timeHigh;timeLow;name;open;high;low;close;volume;marketCap;timestamp'][i]
    ptr = 1
    for j in range(5, len(li)-1):
       df[df.columns[ptr]][i]=float(li[j])
       ptr+=1
  df.drop(columns=['timeOpen;timeClose;timeHigh;timeLow;name;open;high;low;close;volume;marketCap;timestamp'], inplace=True)
  return df
def getTrainingData(df,c,lbl):
  chosenColumns = c
  chosenLabel = lbl

  df=cleanData("dataset.csv")

  X,y=[],[]

  for i in range(len(df)):
    fet=[]
    for j in df.columns:
      if j in chosenColumns:
        fet.append(df[j][i])
    X.append(fet)
    y.append(df[chosenLabel][i])
  return [X,y]
#df=pd.read_csv("dataset.csv")
def plotWithModel(model,xtest,ytest):
  predictions=model.predict(xtest)
  l=[]
  for i in range(1, len(predictions)+1):
    l.append(i)
  plt.plot(l,predictions, color="red")
  plt.title("Model Predicted Prices vs. Real Prices")
  plt.xlabel("Feature #")
  plt.ylabel("Price")

  plt.plot(l,ytest, color="blue")
  plt.show()
def trainModel(train):
  print(train[1])
  x_train,x_test,y_train,y_test = train_test_split(train[0],train[1])
  model = LinearRegression().fit(x_train,y_train)
  return model
def forecastPrice(modelClose, modelOpen, modelVolume,modelLow, currentData, days):
  # Open - Low - Volume
  prevClose=modelClose.predict([[currentData[0], currentData[1], currentData[2]]])[0]
  prevLow=modelLow.predict([[currentData[0],prevClose,currentData[2]]])[0]
  prevOpen=modelOpen.predict([[currentData[1], prevClose, currentData[2]]])[0]
  prevVolume=modelVolume.predict([[currentData[0],currentData[1], prevClose]])[0]
  l = [prevClose]
  for i in range(days-1):
    predClose=modelClose.predict([[prevOpen,prevLow,prevVolume]])[0]
    l.append(predClose)
    predLow=modelLow.predict([[prevOpen,predClose,prevVolume]])[0]
    predOpen=modelLow.predict([[prevLow,predClose,prevVolume]])[0]
    predVolume=modelLow.predict([[prevOpen,prevLow,predClose]])[0]
    prevLow=predLow
    prevOpen=predOpen
    prevVolume=predVolume
  return l



