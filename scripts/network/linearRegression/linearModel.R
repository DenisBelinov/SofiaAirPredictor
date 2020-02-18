
Data <- read.csv("D:\\SofiaAirPredictor\\Dev\\mladostTrain2.csv")

testData <- read.csv("D:\\SofiaAirPredictor\\Dev\\mladostTest2.csv")
testData <- na.omit(testData)
regression = lm(p1~windSpeed + temperature + humidity + precipIntensity, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)

##############################################################
regression = lm(p1~windSpeed, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)

regression = lm(p1~temperature, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)

regression = lm(p1~humidity, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)

regression = lm(p1~precipIntensity, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)
##############################################################

regression = lm(p1~windSpeed+ temperature, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)

regression = lm(p1~humidity+ temperature, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)

regression = lm(p1~precipIntensity+ temperature, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)


regression = lm(p1~precipIntensity+ windSpeed, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)


regression = lm(p1~windSpeed+ humidity, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)

regression = lm(p1~precipIntensity+ humidity, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)

##############################################################

regression = lm(p1~windSpeed+ temperature + humidity, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)

regression = lm(p1~humidity+ temperature + precipIntensity, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)

regression = lm(p1~precipIntensity+ temperature + windSpeed, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)

regression = lm(p1~precipIntensity+ humidity + windSpeed, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)

##############################################################

regression = lm(p1~windSpeed + temperature + humidity + precipIntensity, data=Data)
mean((testData$p1 - predict.lm(regression, testData)) ^ 2)


mean((testData$p1 - predict.lm(regression, testData)) ^ 2)
mean((testData$p1 - mean(testData[["p1"]]))^2)

