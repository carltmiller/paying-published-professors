# Carl Thomas "Trey" Miller III, ID# 811082781

# Libraries
library(foreign)
library(gmodels)
library(broom)
library(lmtest)

# Working Directory and Housekeeping
setwd("/Users/carl/Documents/UGA/2020Spring/ECON5900/Code/5-EconAnalysisSingleYear")
rm(list = ls())

# Export Regression Function
ExpReg <- function(regr) {
  out <- tidy(regr)
  #out[,-1] <- round(out[,-1], digits = 3)
  regrName = deparse(substitute(regr))
  #write.table(out, file = paste(regrName, ".tbl", sep = ""), sep = ",", row.names = FALSE, quote = FALSE)
}

#Get Data
UGACiteSalFile <- read.csv("SalaryData-EDUCATOR-Department+Research.csv")

#Clean and Process Data
UGACiteSal <- UGACiteSalFile[UGACiteSalFile$Num_Papers != 0,]
UGACiteSal$LogSalary <- log(UGACiteSal$Salary)
UGACiteSal$Num_Cites_Sq <- UGACiteSal$Num_Cites ^ 2
UGACiteSal$Num_Papers_Sq <- UGACiteSal$Num_Papers ^ 2

#Regress Salary on Number of Citations
UGACiteSalReg <- lm(LogSalary ~ Num_Cites + Num_Cites_Sq + Department + Subgroup, data = UGACiteSal)
summary(UGACiteSalReg)
resettest(UGACiteSalReg, power = 2, type = "fitted", data = UGACiteSal)
ExpReg(UGACiteSalReg)

estimable(UGACiteSalReg, c(0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), conf.int = 0.95)

#Regress Salary on Number of Papers
UGAPubSalReg <- lm(LogSalary ~ Num_Papers + Num_Papers_Sq + Department + Subgroup, data = UGACiteSal)
summary(UGAPubSalReg)
resettest(UGAPubSalReg, power = 2, type = "fitted", data = UGACiteSal)
ExpReg(UGAPubSalReg)

estimable(UGAPubSalReg, c(0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), conf.int = 0.95)

