import os
import glob
import pickle
import re
from collections import Counter
'''
Parse out metablock at top of email, begin with Jeff Skilling
Generate list of senders of received emails and recipients for sent emails
'''
email_list = ['jeffrey.sherrick@enron.com', 'jeffrey.mcmahon@enron.com', 'dick.westfahl@enron.com', 
'bill.cordes@enron.com', 'dan.leff@enron.com', 'mark.haedicke@enron.com', 'jeffrey.shankman@enron.com', 
'mark.koenig@enron.com', 'rick.buy@enron.com', 'steven.kean@enron.com', 'frank.stabler@enron.com', 
'mark.frevert@enron.com', 'john.sherriff@enron.com', 'paula.rieker@enron.com', 'jim.piro@enron.com', 
's..muller@enron.com', 'george.wasaff@enron.com', 'frank.bay@enron.com', 'ken.rice@enron.com', 
'james.hughes@enron.com', 'chip.cox@enron.com', 'george.mcclellan@enron.com', 'thomas.white@enron.com', 
'vicki.sharp@enron.com', 'mike.mcconnell@enron.com', 'w.duran@enron.com', 'rick.bergsieker@enron.com', 
'rockford.meyer@enron.com', 'rebecca.mcdonald@enron.com', 'larry.izzo@enron.com', 
'matthew.scrimshaw@enron.com', 'michael.moran@enron.com', 'kenneth.lay@enron.com', 
'richard.shapiro@enron.com', 'jim.fallon@enron.com', 'robert.hayes@enron.com', 'philippe.bibi@enron.com', 
'james.prentice@enron.com', 'joe.kishkill@enron.com', 'rebecca.carter@enron.com', 'james.bannantine@enron.com',
'tod.lindholm@enron.com', 'gene.humphrey@enron.com', 'tim.belden@enron.com', 'david.delainey@enron.com', 
'richard.dimichele@enron.com', 'julia.murray@enron.com', 'christopher.calger@enron.com', 
'greg.whalley@enron.com', 'diomedes.christodoulou@enron.com', 'bob.butts@enron.com', 
'sanjay.bhatnagar@enron.com', 'a..martin@enron.com', 'joseph.deffner@enron.com', 'danny.mccarty@enron.com', 
'joe.gold@enron.com', 'janet.dietrich@enron.com', 'rex.shelby@enron.com', 'elizabeth.tilney@enron.com', 
'mark.pickering@enron.com', 'mitchell.taylor@enron.com', 'lou.pai@enron.com', 'rob.walls@enron.com', 
'marty.sunde@enron.com', 'michael.kopper@enron.com', 'mark.metts@enron.com', 'richard.lewis@enron.com', 
'jeff.skilling@enron.com', 'david.berberian@enron.com', 'brian.redmond@enron.com', 'rod.hayslett@enron.com', 
'robert.hermann@enron.com', 'dana.gibbs@enron.com', 'john.echols@enron.com', 'david.haug@enron.com', 
'stanley.horton@enron.com', 'vince.kaminski@enron.com', 'tracy.foy@enron.com', 'keith.dodson@enron.com', 
'john.buchanan@enron.com', 'kulvinder.fowler@enron.com', 'greg.piper@enron.com', 'ken.powers@enron.com', 
'jere.overdyke@enron.com', 'cindy.olson@enron.com', 'ben.glisan@enron.com', 'joe.hirko@enron.com', 
'richard.causey@enron.com', 'raymond.bowen@enron.com', 'timothy.detmering@enron.com', 
'charlene.jackson@enron.com', 'kevin.hannon@enron.com', 'steven.elliott@enron.com', 'john.wodraska@enron.com', 
'james.derrick@enron.com', 'scott.yeager@enron.com', 'phillip.allen@enron.com', 'adam.umanoff@enron.com', 
'kevin.garland@enron.com', 'jay.fitzgerald@enron.com', 'michael.brown@enron.com', 'jeff.donahue@enron.com', 
'sally.beck@enron.com', 'wes.colwell@enron.com', 'gary.hickerson@enron.com', 'jeremy.blachman@enron.com', 
'andrew.fastow@enron.com', 'louise.kitchen@enron.com', 'john.lavorato@enron.com', 
'kristina.mordaunt@enron.com', 'terence.thorn@enron.com']

def parseOutMeta(f):
	f.seek(0)  ### go back to beginning of file (annoying)
	#returns a string of file's contents
	all_text = f.read()

	### split off metadata
	meta = all_text.partition("X-From:")[0]
	no_space_meta = re.sub('[\s<>()]', '', meta)
	split_meta = re.split(':|[A-Z]', no_space_meta)
	fields = ["From", "To", "Cc", "Bcc"]
	indices = []
	for field in fields:
		for i in range(0, len(split_meta)):
			if split_meta[i] == field[1:]:
				indices.append(i+1)
	emails = [split_meta[i].strip().split(',') for i in indices]
	email_dict = dict(zip(fields, emails))
	return email_dict

#sender_file  = open("C:/Users/Jenny/Documents/Data Analyst/P5/ud120-projects/final_project/emails_by_address/from_jeff.skilling@enron.com.txt", "r")

email_folder_path = '../final_project/emails_by_address'

final_dict = {}
missing_files = 0 

#for filename in glob.glob(os.path.join(email_folder_path, 'from_*.txt')):
for address in email_list:
	filename = 'from_' + address + '.txt'
	filepath = os.path.join(email_folder_path, filename)
	try: 
		sender_file = open(filepath, 'r')
		print(filepath)
	except FileNotFoundError:
		print(address, "'s file doesn't exist")
		missing_files += 1
		continue


	from_list = []
	to_list = []
	cc_list = []
	bcc_list = []

	#for each file object (i.e. from_jeff.txt)
	for file in sender_file:
		#change pathname to "../pathinfile minus the last character which is a period"
		path = "C:/Users/Jenny/Documents/Data Analyst/P5/ud120-projects/" + file[:-2] + "_"
		#read the file at the above path
		try:
			email = open(path, "r")
		except FileNotFoundError:
			print(path)
			print("Single email file doesn't exist")
			continue

		#use parseOutMeta to extract the text from the opened email
		email_dict = parseOutMeta(email)

		for key in email_dict.keys():
			if key == "From":
				from_list.extend(email_dict[key])
			if key == "To":
				to_list.extend(email_dict[key])
			if key == "Bcc":
				bcc_list.extend(email_dict[key])
			if key == "Cc":
				cc_list.extend(email_dict[key])
		
		email.close()

	print("emails processed")
	sender_file.close()

	tocnt = Counter()
	cccnt = Counter()
	bcccnt = Counter()

	for word in to_list:
		if word.find("enron") == -1:
			tocnt[word] += 1

	for word in cc_list:
		if word.find("enron") == -1:
			cccnt[word] += 1

	for word in bcc_list:
		if word.find("enron") == -1:
			bcccnt[word] += 1

	final_dict[from_list[1]] = sum(tocnt.values()) + sum(cccnt.values()) + sum(bcccnt.values())

print(missing_files, " missing files")

pickle.dump(final_dict, open("my_data.pkl", "wb"))