# Carl Thomas "Trey" Miller III, ID# 811082781

# Libraries
#library(foreign)
#library(sandwich)
#library(gmodels)
#library(broom)
library(lmtest)
library(robustbase)

# Working Directory and Housekeeping
setwd("/Users/carl/Documents/UGA/2020Spring/ECON5900/Code/5-EconAnalysisSingleYear")
rm(list = ls())

# Export Regression Function - DEPRECATED
ExpReg <- function(regr) {
  out <- tidy(regr)
  out[,-1] <- round(out[,-1], digits = 3)
  regrName = deparse(substitute(regr))
  write.table(out, file = paste(regrName, ".tbl", sep = ""), sep = ",", row.names = FALSE, quote = FALSE)
}

# Custom Summary Function
PrintRevelant <- function(regr) {
  regrName = deparse(substitute(regr))
  regrSumma <- summary(regr)
  constCoeff <- regrSumma$coefficients[1,1]
  constStdE <- regrSumma$coefficients[1,2]
  constPVal <- regrSumma$coefficients[1,4]
  linearCoeff <- regrSumma$coefficients[2,1]
  linearStdE <- regrSumma$coefficients[2,2]
  linearPVal <- regrSumma$coefficients[2,4]
  sqCoeff <- regrSumma$coefficients[3,1]
  sqStdE <- regrSumma$coefficients[3,2]
  sqPVal <- regrSumma$coefficients[3,4]
  linearConfLo <- linearCoeff - (1.96 * linearStdE)
  linearConfHi <- linearCoeff + (1.96 * linearStdE)
  adjRSq <- regrSumma$adj.r.squared
  cat("\nREGRESSION SUMMARY FOR", regrName, 
      "\n\nConstant Coefficient Estimate:\t\t", constCoeff, "\nConstant Coefficient Standard Error:\t", constStdE, "\nConstant Coefficient P-Value:\t\t", constPVal,
      "\n\nLinear Coefficient Estimate:\t\t", linearCoeff, "\nLinear Coefficient Standard Error:\t", linearStdE, "\nLinear Coefficient P-Value:\t\t", linearPVal,
      "\n\nQuadratic Coefficient Estimate:\t\t", sqCoeff, "\nQuadratic Coefficient Standard Error:\t", sqStdE, "\nQuadratic Coefficient P-Value:\t\t", sqPVal,
      "\n\nLinear Coefficient Confidence Interval:\t (", linearConfLo, ",", linearConfHi, ")\n\nAdjusted R-Squared:\t", adjRSq)
}

#Get Data
UGACiteSalFile <- read.csv("SalaryData-EDUCATOR-Department+Research.csv")

#Clean and Process Data
UGACiteSal <- UGACiteSalFile[UGACiteSalFile$Num_Papers != 0,]
UGACiteSal$LogSalary <- log(UGACiteSal$Salary)
UGACiteSal$Num_Cites_Sq <- UGACiteSal$Num_Cites ^ 2
UGACiteSal$Num_Papers_Sq <- UGACiteSal$Num_Papers ^ 2

#REGRESS SALARY ON NUMBER OF PAPERS
#With No Controls
UGAPubSalRegNo <- lm(LogSalary ~ Num_Papers + Num_Papers_Sq, data = UGACiteSal)
PrintRevelant(UGAPubSalRegNo)

#With Controls for Department
UGAPubSalRegDept <- lm(LogSalary ~ Num_Papers + Num_Papers_Sq + Department, data = UGACiteSal)
PrintRevelant(UGAPubSalRegDept)

#With Controls for Position
UGAPubSalRegPos <- lm(LogSalary ~ Num_Papers + Num_Papers_Sq + Subgroup, data = UGACiteSal)
PrintRevelant(UGAPubSalRegPos)

#With Controls for Department and Position (Primary)
UGAPubSalReg <- lm(LogSalary ~ Num_Papers + Num_Papers_Sq + Department + Subgroup, data = UGACiteSal)
PrintRevelant(UGAPubSalReg)

resettest(UGAPubSalReg, power = 2, type = "fitted", data = UGACiteSal)

#With Control for Department and Position Interaction
UGAPubSalRegInter <- lm(LogSalary ~ Num_Papers + Num_Papers_Sq + Department * Subgroup, data = UGACiteSal)
PrintRevelant(UGAPubSalRegInter)

#REGRESS SALARY ON NUMBER OF CITATIONS
#With No Controls
UGACiteSalRegNo <- lmrob(LogSalary ~ Num_Cites + Num_Cites_Sq, data = UGACiteSal, k.max = 1000)
PrintRevelant(UGACiteSalRegNo)

#With Controls for Department
UGACiteSalRegDept <- lmrob(LogSalary ~ Num_Cites + Num_Cites_Sq + Department, data = UGACiteSal, k.max = 1000)
PrintRevelant(UGACiteSalRegDept)

#With Controls for Position
UGACiteSalRegPos <- lmrob(LogSalary ~ Num_Cites + Num_Cites_Sq + Subgroup, data = UGACiteSal, k.max = 1000)
PrintRevelant(UGACiteSalRegPos)

#With Controls for Department and Position (Primary)
UGACiteSalReg <- lmrob(LogSalary ~ Num_Cites + Num_Cites_Sq + Department + Subgroup, data = UGACiteSal, k.max = 1000)
PrintRevelant(UGACiteSalReg)

resettest(UGACiteSalReg, power = 2, type = "fitted", data = UGACiteSal)

#With Control for Department and Position Interaction
UGACiteSalRegInter <- lmrob(LogSalary ~ Num_Cites + Num_Cites_Sq + Department * Subgroup, data = UGACiteSal, k.max = 1000)
PrintRevelant(UGACiteSalRegInter)

