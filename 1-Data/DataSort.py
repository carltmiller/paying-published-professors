import sys
#import getopt
#import time
#import calendar
#import numpy as np
#from collections import namedtuple
#from itertools import *
#from lib import *

#Default Input CSV Paths
inPath = "OPENGA-UGA-Salary19-Commaless.csv"

#Default Output CSV Path
outPathPre = "SalaryData-"
badOutPath = "SalaryData-TO_SORT.csv"

#Categorization Keywords
##Educator
headWords = ["DEPT_HEAD", "dept chair"]
profWords = ["PROFESSOR", "professor"]
asstWords = ["ASSOC_PROFESSOR", "assistant professor", "associate professor", "asst professor", "assoc professor"]
lectWords = ["LECTURER", "lecturer"]
pdocWords = ["POST_DOC", "post doc"]
instWords = ["INSTRUTOR", "instructor", "teacher"]
EDUWords = ["EDUCATOR", headWords, asstWords, profWords, lectWords, pdocWords, instWords]
##Research
rproWords = ["RESEARCH_PROFESSOR", "professor research"] #do before prof
rastWords = ["RESEARCH_WORKER", "laboratory", "research", "rsch"]
RESWords = ["RESEARCH", rproWords, rastWords]
##Athletics
athlWords = ["ATHLETICS", "athletic", "coach"]
ATHWords = ["ATHLETICS", athlWords]
##Admin. Support
execWords = ["EXECUTIVE", "dean", "pres", "provost", "registrar", "chief"]
admnWords = ["ADMINISTRATOR", "director", "asst dir", "administrator"]
mgmtWords = ["MANAGER", "coor", "mgr", "manager"]
aproWords = ["PROFESSIONAL", "pro", "para/pr", "librarian"] #do after prof
offiWords = ["OFFICE", "office/cleric"]
ADMWords = ["ADMIN_SUPPORT", execWords, admnWords, mgmtWords, aproWords, offiWords]
##Spec. Support
faclWords = ["FACILITIES", "maint", "craft", "architect", "engineer", "facilities"] #do before mgr, do before pro
polcWords = ["SECURITY", "police", "security guard"]
leglWords = ["LEGAL", "attorn", "paralegal"]
mediWords = ["MEDICAL", "counselor", "pharmacist", "therap", "physician"]
SPCWords = ["SPEC_SUPPORT", faclWords, polcWords, leglWords, mediWords]
##Student
ugrdWords = ["UNDERGRAD", "student", "trainee", "resident"]
gradWords = ["GRAD", "graduate"]
STUWords = ["STUDENT_WORKER", ugrdWords, gradWords]
##Excluded
tempWords = ["TEMPORARY", "temp", "acting", "visiting"]
postWords = ["FORMER", "former", "emeritus"]
EXCWords = ["EXCLUDED", tempWords, postWords]

MASTERWords = [EXCWords, RESWords, EDUWords, ATHWords, SPCWords, ADMWords, STUWords]

#run
def runSort():
	headLine = "Surname,Given Name(s),Middle Initial,Job Title,Salary,Travel,Organization,FiscalYear,Group,Subgroup\n"
	currLine = ""
	currLineLC = ""
	outFiles = []
	breaker = False
	inFile = open(inPath, "r")
	currLine = inFile.readline()
	badFile = open(badOutPath, "w+")
	badFile.write(headLine)
	for a in MASTERWords:
		outFiles.append(open(outPathPre + a[0] + ".csv", "w+"))
		outFiles[-1].write(headLine)
	currLine = inFile.readline()
	while(currLine != ""):
		currLine = currLine.strip()
		for i in range (0, 12):
			currLine = currLine.replace('\"', '')
		currLineLC = currLine.lower()
		currLineLCArr = currLineLC.split(',')
		i = 0
		for cat in MASTERWords:
			if(breaker):
				break
			for subcat in cat[1:]:
				if(breaker):
					break
				for str in subcat[1:]:
					if(breaker):
						break
					if(str in currLineLCArr[2]):
						#outFiles[i].write(currLine + "," + cat[0] + "," + subcat[0] + "\n")
						#Surname
						outFiles[i].write(currLineLCArr[0].upper())
						#Given Name and Middle Initial
						if(" " in currLineLCArr[1]):
							givName = currLineLCArr[1].split(' ')
							if(len(givName) == 2):
								outFiles[i].write("," + givName[0].upper())
								if(len(givName[1]) > 1):
									outFiles[i].write(" " + givName[1].upper() + ",")
								else:
									outFiles[i].write("," + givName[1].upper())
							elif(len(givName) == 3):
								outFiles[i].write("," + givName[0].upper())
								if(len(givName[1]) > 1):
									outFiles[i].write(" " + givName[1].upper())
									if(len(givName[2]) > 1):
										outFiles[i].write(" " + givName[2].upper())
									else:
										outFiles[i].write("," + givName[2].upper())
								else:
									outFiles[i].write("," + givName[1].upper() + " " + givName[2].upper())
							elif(len(givName) == 4):
								outFiles[i].write("," + givName[0].upper() + " " + givName[1].upper())
								outFiles[i].write("," + givName[2].upper() + " " + givName[3].upper())
							else:
								sys.stderr.write("ERROR: Too many / too few given names!\n")
								sys.stderr.write("ERROR: \"" + currLineLCArr[1] + "\"\n")
									#sys.exit(1)
						else:
							outFiles[i].write("," + currLineLCArr[1].upper() + ",")
						#Title
						outFiles[i].write("," + currLineLCArr[2].upper())
						#Salary
						outFiles[i].write("," + "{:.2f}".format(float(currLineLCArr[3])))
						#Travel
						outFiles[i].write("," + "{:.2f}".format(float(currLineLCArr[4])))
						#Organization
						outFiles[i].write("," + currLineLCArr[5].upper())
						#Fiscal Year
						outFiles[i].write("," + currLineLCArr[6])
						#Category
						outFiles[i].write("," + cat[0])
						#Subcategory
						outFiles[i].write("," + subcat[0])
						#College
						if(cat[0] == "EDUCATOR"):
							outFiles[i].write("," + "COLLEGE")
						#Department
						if(cat[0] == "EDUCATOR"):
							outFiles[i].write("," + "DEPT")
						#Endline
						outFiles[i].write("\n")
						breaker = True
			i += 1
		if(not breaker):
			badFile.write(currLine + ",UNKNOWN,UNKNOWN\n")
		currLine = inFile.readline()
		breaker = False


#main
if __name__ == "__main__":
	runSort()
	sys.exit(0)
