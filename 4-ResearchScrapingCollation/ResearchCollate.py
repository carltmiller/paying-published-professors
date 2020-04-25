import sys
import scholarly
import time

#Default Input CSV Paths
inPath = "../3-DepartmentCollation/SalaryData-EDUCATOR-Department.csv"

#Default Output CSV Path
outPath = "SalaryData-EDUCATOR-Department+Research.csv"

def writeColl(wrtFile, salStr, rschArr):
	wrtFile.write(salStr.replace("\n", ","))
	sys.stdout.write(salStr.replace("\n", ","))
	wrtFile.write(str(rschArr[0]) + "," + str(rschArr[1]) + "\n")
	sys.stdout.write(str(rschArr[0]) + "," + str(rschArr[1]) + "\n")

#run
def runCollate():
	headLine = "Surname,Given_Name,Middle_Initial,Ext_Given_Name,Nickname,Job_Title,Ext_Job_Title,Salary,Travel,Organization,Fiscal_Year,Group,Subgroup,College,Department,Num_Papers,Num_Cites\n"
	#SALARY HEAD: Surname,Given Name(s),Middle Initial,Job Title,Salary,Travel,Organization,FiscalYear,Group,Subgroup
	#DEPT HEAD: Surname,Given Name(s),Nickname,Job Title,College,Department,Email,URL
	inFile = open(inPath, "r")
	inHeadLine = inFile.readline()
	outFile = open(outPath, "w+")
	outFile.write(headLine)
	currLine = inFile.readline()
	while(currLine != ""):
		currRsch = []
		currArr = currLine.replace("\n", "").split(",")
		print("Searching for " + currArr[1] + " " + currArr[0])
		loopWhile = True
		while(loopWhile):
			try:
				search_query = scholarly.search_author(currArr[1] + " " + currArr[0] + ", uga.edu")
				loopWhile = False
			except:
				print("Search Exception!")
				time.sleep(600) #wait 10 minutes
		try:
			author = next(search_query).fill()
			foundAuthor = True
		except:
			foundAuthor = False
		if(not foundAuthor):
			loopWhile = True
			while(loopWhile):
				try:
					time.sleep(10) #wait 10 seconds
					search_query = scholarly.search_author(currArr[3] + " " + currArr[0] + ", uga.edu")
					loopWhile = False
				except:
					print("Search Exception!")
					time.sleep(600) #wait 10 minutes
			try:
				author = next(search_query).fill()
				foundAuthor = True
			except:
				foundAuthor = False
		if(not foundAuthor):
			currRsch.append(0)
			currRsch.append(0)
			writeColl(outFile, currLine, currRsch)
			currLine = inFile.readline()
			continue
		pubs = author.publications
		currRsch.append(len(pubs))
		cites = 0
		for pub in pubs:
			print("Publication Found!")
			try:
				cites += pub.citedby
			except:
				cites += 0
		currRsch.append(cites)
		writeColl(outFile, currLine, currRsch)
		currLine = inFile.readline()

#main
if __name__ == "__main__":
	runCollate()
	sys.exit(0)
