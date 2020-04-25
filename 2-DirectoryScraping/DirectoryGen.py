import sys
import urllib.request as urllib2
import unidecode

#Default Output CSV Path
outPath = "UGADirectory.csv"

pagesFrank = []
pagesTerry = []

#setup
def initializeGen():
	#Franklin CAS
	#Art, Cmp. Lit, Music, Physics
	responseFrank = urllib2.urlopen(urllib2.Request('http://www.franklin.uga.edu/departmental-faculty-and-staff'))
	htmlBytesFrank = responseFrank.read()
	#print("HTML FETCHED")
	#print(type(htmlFrank))
	htmlFrank = htmlBytesFrank.decode("utf-8")
	begIndFrank = htmlFrank.find("<table><tbody><tr><td>")
	endIndFrank = htmlFrank.find("</tr></tbody></table><p> </p>")
	currInd = htmlFrank.find("\"", begIndFrank)
	while(currInd != -1):
		currURLEnd = htmlFrank.find("\"", currInd + 1)
		currURL = htmlFrank[(currInd + 1):currURLEnd]
		currURL = currURL.replace("front", "all")
		currURL = currURL.replace("full_directory", "all")
		currURL = currURL.replace("edu/all", "edu/directory/all")
		currURL = currURL.replace("cmlt.franklin.uga.edu/people", "cmlt.franklin.uga.edu/directory/all")
		currURL = currURL.replace("musi.franklin.uga.edu/people", "musi.franklin.uga.edu/directory")
		#print(currURL)
		currTitleBeg = currURLEnd + 2
		currTitleEnd = htmlFrank.find("<", currTitleBeg)
		currTitle = htmlFrank[currTitleBeg:currTitleEnd]
		currTitle = currTitle.replace("&amp;", "and")
		if(currTitle.find(",") != -1):
			commaClipInd = currTitle.find(",")
			currTitle = currTitle[:commaClipInd]
		currTitle = currTitle.strip()
		#print(currTitle)
		currPage = [currTitle,currURL]
		pagesFrank.append(currPage)
		currInd = htmlFrank.find("\"", currURLEnd + 1, endIndFrank)
	#Terry Business
	facArr = ["Faculty", "https://www.terry.uga.edu/directory/faculty/"]
	docArr = ["Doctoral Students", "https://www.terry.uga.edu/directory/phd-students/"]
	staArr = ["Staff", "https://www.terry.uga.edu/directory/staff/"]
	pagesTerry.append(facArr)
	pagesTerry.append(docArr)
	pagesTerry.append(staArr)
	#Engineering - Incomplete
	#http://engineering.uga.edu/people/all


def csvWrite(outFile, nameRaw, title, college, dept, email, persURL):
	nameLast = ""
	nameGiven = ""
	nameNick = ""
	title = title.replace("\n", "")
	if(nameRaw.find(",") == -1):
		#No Comma, Standard Name
		namePieces = nameRaw.split(" ")
		if(len(namePieces) < 2):
			print("TOO FEW NAMES!")
			print(dept + ": " + nameRaw)
		elif(len(namePieces) == 2):
			nameLast = namePieces[1]
			nameGiven = namePieces[0]
		elif(len(namePieces) == 3):
			if(namePieces[1].find("(") > -1):
				nameGiven = namePieces[0]
				nameNick = namePieces[1]
				nameLast = namePieces[2]
			else:
				nameLast = namePieces[2]
				nameGiven = namePieces[0] + " " + namePieces[1]
		else:
			if(len(namePieces[1]) == 0):
				#extra space in entry
				nameLast = namePieces[3]
				nameGiven = namePieces[0] + " " + namePieces[2]
			else:
				if(namePieces[1].find("(") > -1):
					#nickname
					nameGiven = namePieces[0] + " " + namePieces[2]
					nameNick = namePieces[1]
					nameLast = namePieces[3]
				else:
					#treat as hyphenated last name
					nameLast = namePieces[2] + "-" + namePieces[3]
					nameGiven = namePieces[0] + " " + namePieces[1]
	else:
		#Comma Format, Inverted Name
		nameHalves = nameRaw.split(",")
		if(len(nameHalves) > 2):
			#discard suffix
			nameLast = nameHalves[0].strip()
			nameFirsts = nameHalves[2].strip()
		else:
			nameLast = nameHalves[0].strip()
			nameFirsts = nameHalves[1].strip()
		if(nameFirsts.find("(") != -1):
			nameArr = nameFirsts.split(" ")
			i = 0
			for nm in nameArr:
				if(i == 0):
					nameGiven = nm
				else:
					nameNick = nameNick + nm
				i += 1
		else:
			nameGiven = nameFirsts
	nameNick = nameNick.replace("(", "").replace(")", "")
	#End Name Spec
	#print("WRITING: " + dept)
	outFile.write(unidecode.unidecode(nameLast + "," + nameGiven + "," + nameNick + ","))
	outFile.write(unidecode.unidecode(title.replace(",", "-") + "," + college + "," + dept + ","))
	outFile.write(unidecode.unidecode(email + "," + persURL + "\n"))

#run
def runGen():
	headLine = "Surname,Given Name(s),Nickname,Job Title,College,Department,Email,URL\n"
	outFile = open(outPath, "w+")
	outFile.write(headLine)
	for deptArr in pagesFrank:
		if(deptArr[0] == "Art"):
			#completely different directory format
			for i in range(0, 11):
				iURL = "https://art.uga.edu/directory?field_academic_area_target_id_entityreference_filter=All&page=" + str(i)
				responseDept = urllib2.urlopen(urllib2.Request(iURL))
				htmlBytesDept = responseDept.read()
				htmlDept = htmlBytesDept.decode("utf-8")
				begIndDept = htmlDept.find("last-name")
				endIndDept = htmlDept.find("pager")
				#print(deptArr[0] + "   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
				currInd = begIndDept
				while(currInd != -1):
					currURLBeg = currInd + 51
					currURLEnd = htmlDept.find("\"", currURLBeg + 1)
					currURL = htmlDept[currURLBeg:currURLEnd]
					#print(currURL)
					currNameBeg = currURLEnd + 2
					currNameEnd = htmlDept.find("<", currNameBeg)
					currName = htmlDept[currNameBeg:currNameEnd]
					currName = currName.replace("&#039;", "\'")
					if(currName.find("&quot") != -1):
						currNick = currName[currName.find("&quot"):]
						currNick = currNick.replace("&quot;", "").replace("&quot;", "")
						currName = currName[:currName.find("&quot")]
						currName = currName + "(" + currNick + ")"
					currName = currName.strip()
					currTitleBeg = htmlDept.find("field-position", currNameEnd) + 43
					currTitleEnd = htmlDept.find("<", currTitleBeg)
					currTitle = htmlDept[currTitleBeg:currTitleEnd]
					currTitle = currTitle.replace("&#039;", "\'")
					currTitle = currTitle.replace("&amp;", "&")
					currTitle = currTitle.replace("&quot;", "\"")
					currTitle = currTitle.strip()
					currMailEnd = currTitleEnd
					currMail = ""
					#sys.stdout.write(currName + "; " + currTitle + "; " + currURL + "; " + currMail + "\n")
					csvWrite(outFile, currName, currTitle, "Franklin", deptArr[0], currMail, currURL)
					currInd = htmlDept.find("last-name", currMailEnd, endIndDept)
			continue
		if(deptArr[0] == "Music"):
			#completely different directory format
			responseDept = urllib2.urlopen(urllib2.Request(deptArr[1]))
			htmlBytesDept = responseDept.read()
			htmlDept = htmlBytesDept.decode("utf-8")
			begIndDept = htmlDept.find("<tbody>")
			endIndDept = htmlDept.find("</tbody>")
			#print(deptArr[0] + "   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			currInd = htmlDept.find("<a href=", begIndDept)
			prevPrevName = "random"
			prevName = "random"
			while(currInd != -1):
				currURLBeg = currInd + 9
				currURLEnd = htmlDept.find("\"", currURLBeg + 1)
				currURL = htmlDept[currURLBeg:currURLEnd]
				currNameBeg = currURLEnd + 2
				currNameEnd = htmlDept.find("<", currNameBeg)
				currName = htmlDept[currNameBeg:currNameEnd]
				currName = currName.replace("&#039;", "\'")
				if(currName.find("&quot") != -1):
					currNick = currName[currName.find("&quot"):]
					currNick = currNick.replace("&quot;", "").replace("&quot;", "")
					currName = currName[:currName.find("&quot")]
					currName = currName + "(" + currNick + ")"
				currName = currName.strip()
				currMailBeg = htmlDept.find("mailto", currNameEnd) + 7
				currMailEnd = htmlDept.find("\"", currMailBeg)
				currMail = htmlDept[currMailBeg:currMailEnd]
				currTitleBeg = htmlDept.find("<td", currMailEnd) + 62
				currTitleEnd = htmlDept.find("<", currTitleBeg) - 7
				currTitle = htmlDept[currTitleBeg:currTitleEnd]
				currTitle = currTitle.replace("&#039;", "\'")
				currTitle = currTitle.replace("&amp;", "&")
				currTitle = currTitle.replace("&quot;", "\"")
				currTitle = currTitle.strip()
				if(prevName != currName and prevPrevName != currName):
					#sys.stdout.write(currName + "; " + currTitle + "; " + currURL + "; " + currMail + "\n")
					csvWrite(outFile, currName, currTitle, "Franklin", deptArr[0], currMail, currURL)
					int(0)
				prevPrevName = prevName
				prevName = currName
				currInd = htmlDept.find("<a href=", currTitleEnd, endIndDept)
			continue
		if(deptArr[0] == "Physics and Astronomy"):
			#completely different directory format
			responseDept = urllib2.urlopen(urllib2.Request(deptArr[1]))
			htmlBytesDept = responseDept.read()
			htmlDept = htmlBytesDept.decode("utf-8")
			begIndDept = htmlDept.find("<h4>")
			endIndDept = htmlDept.find("footer")
			#print(deptArr[0] + "   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			currInd = begIndDept
			while(currInd != -1):
				currURLBeg = currInd + 13
				currURLEnd = htmlDept.find("\"", currURLBeg + 1)
				currURL = htmlDept[currURLBeg:currURLEnd]
				#print(currURL)
				currNameBeg = currURLEnd + 2
				currNameEnd = htmlDept.find("<", currNameBeg)
				currName = htmlDept[currNameBeg:currNameEnd]
				currName = currName.replace("&#039;", "\'")
				if(currName.find("&quot") != -1):
					currNick = currName[currName.find("&quot"):]
					currNick = currNick.replace("&quot;", "").replace("&quot;", "")
					currName = currName[:currName.find("&quot")]
					currName = currName + "(" + currNick + ")"
				currName = currName.strip()
				currTitleBeg = currNameEnd + 4
				currTitleEnd = htmlDept.find("<", currTitleBeg)
				currTitle = htmlDept[currTitleBeg:currTitleEnd]
				currTitle = currTitle.replace(",", "")
				currTitle = currTitle.replace("&#039;", "\'")
				currTitle = currTitle.replace("&amp;", "&")
				currTitle = currTitle.replace("&quot;", "\"")
				currTitle = currTitle.strip()
				currMailEnd = currTitleEnd
				currMail = ""
				#sys.stdout.write(currName + "; " + currTitle + "; " + currURL + "; " + currMail + "\n")
				csvWrite(outFile, currName, currTitle, "Franklin", deptArr[0], currMail, currURL)
				currInd = htmlDept.find("<h4>", currMailEnd, endIndDept)
			continue
		if(deptArr[0] == "History"):
			#paginated directory
			for i in range(0, 4):
				iURL = "http://hist.franklin.uga.edu/directory/all?_ga=2.254430920.1527182522.1555568040-1834351857.1484694760&page=" + str(i)
				responseDept = urllib2.urlopen(urllib2.Request(iURL))
				htmlBytesDept = responseDept.read()
				htmlDept = htmlBytesDept.decode("utf-8")
				begIndDept = htmlDept.find("<div class=\"views-field views-field-field-last-name\"><strong class=\"field-content\">")
				endIndDept = htmlDept.find("nav class")
				#print(deptArr[0] + "   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
				#print(begIndDept)
				#print(endIndDept)
				currInd = htmlDept.find("<a href=", begIndDept)
				while(currInd != -1):
					currURLBeg = currInd + 9
					currURLEnd = htmlDept.find("\"", currURLBeg + 1)
					currURL = htmlDept[currURLBeg:currURLEnd]
					#print(currURL)
					currNameBeg = htmlDept.find("wrap2_personnel", currURLEnd) + 17
					currNameEnd = htmlDept.find("<", currNameBeg)
					currName = htmlDept[currNameBeg:currNameEnd]
					currName = currName.replace("&#039;", "\'")
					if(currName.find("&quot") != -1):
						currNick = currName[currName.find("&quot"):]
						currNick = currNick.replace("&quot;", "").replace("&quot;", "")
						currName = currName[:currName.find("&quot")]
						currName = currName + "(" + currNick + ")"
					currName = currName.strip()
					currTitleBeg = htmlDept.find("field-content", currNameEnd) + 15
					currTitleEnd = htmlDept.find("<", currTitleBeg)
					currTitle = htmlDept[currTitleBeg:currTitleEnd]
					currTitle = currTitle.replace("&#039;", "\'")
					currTitle = currTitle.replace("&amp;", "&")
					currTitle = currTitle.replace("&quot;", "\"")
					currTitle = currTitle.strip()
					currMailEnd = currTitleEnd
					currMail = ""
					#sys.stdout.write(currName + "; " + currTitle + "; " + currURL + "; " + currMail + "\n")
					csvWrite(outFile, currName, currTitle, "Franklin", deptArr[0], currMail, currURL)
					currInd = htmlDept.find("<a href=", currMailEnd, endIndDept)
			continue
		responseDept = urllib2.urlopen(urllib2.Request(deptArr[1]))
		htmlBytesDept = responseDept.read()
		htmlDept = htmlBytesDept.decode("utf-8")
		if(True):
			begIndDept = htmlDept.find("<div class=\"views-field views-field-field-last-name\"><strong class=\"field-content\">")
			endIndDept = htmlDept.find("</div></div>\n\n    </div>\n  \n          </div>\n</div>\n\n  ")
			currInd = htmlDept.find("<a href=", begIndDept)
			#print(deptArr[0] + "   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			#print(begIndDept)
			#print(endIndDept)
			while(currInd != -1):
				currURLBeg = currInd + 9
				currURLEnd = htmlDept.find("\"", currURLBeg + 1)
				currURL = htmlDept[currURLBeg:currURLEnd]
				#print(currURL)
				currNameBeg = htmlDept.find("wrap2_personnel", currURLEnd) + 17
				currNameEnd = htmlDept.find("<", currNameBeg)
				currName = htmlDept[currNameBeg:currNameEnd]
				currName = currName.replace("&#039;", "\'")
				if(currName.find("&quot") != -1):
					currNick = currName[currName.find("&quot"):]
					currNick = currNick.replace("&quot;", "").replace("&quot;", "")
					currName = currName[:currName.find("&quot")]
					currName = currName + "(" + currNick + ")"
				currName = currName.strip()
				currTitleBeg = htmlDept.find("field-content", currNameEnd) + 15
				currTitleEnd = htmlDept.find("<", currTitleBeg)
				currTitle = htmlDept[currTitleBeg:currTitleEnd]
				currTitle = currTitle.replace("&#039;", "\'")
				currTitle = currTitle.replace("&amp;", "&")
				currTitle = currTitle.replace("&quot;", "\"")
				currTitle = currTitle.strip()
				currMailEnd = currTitleEnd
				currMail = ""
				if(deptArr[0] == "Genetics"):
					currMailBeg = htmlDept.find("mailto", currTitleEnd) + 7
					currMailEnd = htmlDept.find("\"", currMailBeg)
					currMail = htmlDept[currMailBeg:currMailEnd]
				if(deptArr[0] == "Statistics"):
					#sys.stdout.write(currName + "; " + currTitle + "; " + currURL + "; " + currMail + "\n")
					int(0)
				csvWrite(outFile, currName, currTitle, "Franklin", deptArr[0], currMail, currURL)
				currInd = htmlDept.find("<a href=", currMailEnd, endIndDept)
	for deptArr in pagesTerry:
		responseDept = urllib2.urlopen(urllib2.Request(deptArr[1]))
		htmlBytesDept = responseDept.read()
		htmlDept = htmlBytesDept.decode("utf-8")
		begIndDept = htmlDept.find("<tbody>")
		endIndDept = htmlDept.find("</tbody>")
		#print(deptArr[0] + "   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		currInd = htmlDept.find("<a href=", begIndDept)
		while(currInd != -1):
			currURLBeg = currInd + 9
			currURLEnd = htmlDept.find("\"", currURLBeg + 1)
			currURL = htmlDept[currURLBeg:currURLEnd]
			currNameBeg = currURLEnd + 2
			currNameEnd = htmlDept.find("<", currNameBeg)
			currName = htmlDept[currNameBeg:currNameEnd]
			currName = currName.replace("&#039;", "\'")
			if(currName.find("&quot") != -1):
				currNick = currName[currName.find("&quot"):]
				currNick = currNick.replace("&quot;", "").replace("&quot;", "")
				currName = currName[:currName.find("&quot")]
				currName = currName + "(" + currNick + ")"
			currName = currName.strip()
			currTitleBeg = htmlDept.find("title", currNameEnd) + 7
			currTitleEnd = htmlDept.find("<", currTitleBeg)
			currTitle = htmlDept[currTitleBeg:currTitleEnd]
			currTitle = currTitle.replace("&#039;", "\'")
			currTitle = currTitle.replace("&amp;", "&")
			currTitle = currTitle.replace("&quot;", "\"")
			currTitle = currTitle.strip()
			currMailBeg = htmlDept.find("mailto", currTitleEnd) + 7
			currMailEnd = htmlDept.find("\"", currMailBeg)
			currMail = htmlDept[currMailBeg:currMailEnd]
			currMail = currMail.strip()
			#sys.stdout.write(currName + "; " + currTitle + "; " + currURL + "; " + currMail + "\n")
			currDeptBeg = 11
			currDeptEnd = currURL.find("/", currDeptBeg)
			currDept = currURL[currDeptBeg:currDeptEnd].replace("-", " ").title()
			currDept = currDept.strip()
			csvWrite(outFile, currName, currTitle, "Terry", currDept, currMail, currURL)
			currInd = htmlDept.find("<a href=", currMailEnd, endIndDept)


#main
if __name__ == "__main__":
	initializeGen()
	#print(pagesFrank)
	runGen()
	sys.exit(0)
