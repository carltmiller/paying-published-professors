import sys

#Default Input CSV Paths
salaryPath = "../1-Data/SalaryData-EDUCATOR.csv"
deptPath = "../2-DirectoryScraping/UGADirectory.csv"

#Default Output CSV Path
outPath = "SalaryData-EDUCATOR-Department.csv"
rejectPath = "SalaryData-EDUCATOR-NotFound.csv"

deptData = []
deptHeadline = ""

def loadDepartments():
	deptFile = open(deptPath, "r")
	deptHeadline = deptFile.readline()
	currLine = deptFile.readline()
	while(currLine != ""):
		currArr = currLine.replace("\n", "").split(",")
		deptData.append(currArr)
		currLine = deptFile.readline()
	print("DEPARTMENT INFO LOADED!")

def writeColl(wrtFile, salArr, deptArr):
	wrtFile.write(salArr[0] + "," + salArr[1] + "," + salArr[2] + ",")
	wrtFile.write(deptArr[1] + "," + deptArr[2] + "," + salArr[3] + ",")
	wrtFile.write(deptArr[3] + "," + salArr[4] + "," + salArr[5] + ",")
	wrtFile.write(salArr[6] + "," + salArr[7] + "," + salArr[8] + ",")
	wrtFile.write(salArr[9] + "," + deptArr[4] + "," + deptArr[5] + "\n")


#run
def runCollate():
	headLine = "Surname,Given Name(s),Middle Initial,Extended Given Name(s),Nickname,Job Title,Extended Job Title,Salary,Travel,Organization,FiscalYear,Group,Subgroup,College,Department\n"
	#SALARY HEAD: Surname,Given Name(s),Middle Initial,Job Title,Salary,Travel,Organization,FiscalYear,Group,Subgroup
	#DEPT HEAD: Surname,Given Name(s),Nickname,Job Title,College,Department,Email,URL
	salaryFile = open(salaryPath, "r")
	salaryHeadLine = salaryFile.readline()
	outFile = open(outPath, "w+")
	outFile.write(headLine)
	rejFile = open(rejectPath, "w+")
	rejFile.write(salaryHeadLine)
	currLine = salaryFile.readline()
	while(currLine != ""):
		currArr = currLine.replace("\n", "").split(",")
		print("Searching for " + currArr[1] + " " + currArr[0])
		currResults = []
		currResultBool = False
		for elem in deptData:
			if(elem[0].lower() == currArr[0].lower()):
				currResultBool = True
				currResults.append(elem)
		if(not currResultBool):
			for elem in deptData:
				if(elem[0].lower().find(currArr[0].lower()) != -1):
					currResultBool = True
					currResults.append(elem)
		if(not currResultBool):
			for elem in deptData:
				if(currArr[0].lower().find(elem[0].lower()) != -1):
					currResultBool = True
					currResults.append(elem)
		if(not currResultBool):
			rejFile.write(currLine)
			currLine = salaryFile.readline()
			continue
		if(len(currResults) > 0):
			for elem in currResults:
				if((currArr[1].lower().find(elem[1].lower()) != -1 and len(elem[1]) > 1) or (elem[1].lower().find(currArr[1].lower()) != -1 and len(currArr[1]) > 1)):
					print(currArr[1] + " " + currArr[0] + " matched with " + elem[1] + " " + elem[0])
					writeColl(outFile, currArr, elem)
					break #optional: can output dupes if not inserted here
		currLine = salaryFile.readline()

#main
if __name__ == "__main__":
	loadDepartments()
	runCollate()
	sys.exit(0)
