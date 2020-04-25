import sys
import scholarly
import time

def runCollate():
	try:
		search_query = scholarly.search_author("Ian Schmutte, uga.edu")
	except:
		print("Search Exception!")
		time.sleep(600) #wait 10 minutes
	try:
		author = next(search_query).fill()
		print("Author Found!")
		print(author)
		foundAuthor = True
	except:
		foundAuthor = False
	if foundAuthor:
		pubs = author.publications
		cites = 0
		for pub in pubs:
			print("Publication Found!")
			print(pub)
			try:
				cites += pub.citedby
			except:
				cites += 0
		print(str(cites) + " citations!")


#main
if __name__ == "__main__":
	runCollate()
	sys.exit(0)
