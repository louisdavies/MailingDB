from fpdf import FPDF
import sys,pyperclip

class Supporter():

	numSupporters = 0 
	Supporters = list()
	receiveLetter = [1,2,3,4,6,7,8,9]
	receiveEmail = [5,6,7,8,9]

	def __init__(self, first="", last="", email=None, address=None, letters = [1,1,1], preference = 5):
		self.first = first
		self.last = last
		if email == "":
			self.email = None
		else:
			self.email = email
		self.address = address
		self.letters = letters
		if preference == "":
			self.preference = 5
		else:
			self.preference = int(preference)
		self.id = Supporter.numSupporters
		Supporter.numSupporters += 1

	@property
	def fullname(self):
		return "{} {}".format(self.first,self.last)

	@fullname.setter
	def fullname(self,value):
		# try:
		names = value.split(' ')
		self.last = names[-1]
		self.first = ""
		if len(names) > 1:
			self.first = " ".join(names[:-1])
	def __str__(self):
		#Whole info in a string for searching
		result = self.fullname
		if self.address != None:
			result += " " + " ".join(self.address.split("\n"))
		if self.email != None:
			result += " " + self.email
		return result.lower()

	@classmethod
	def makePDF(cls,PDFName):
		pdf = FPDF('P','mm',(220,110))
		for supporter in cls.Supporters:
			print(supporter.preference)
			envelope = [1,2,3,4,6,7,8,9]
			if supporter.preference	in envelope:
				pdf.add_page()
				font_size = 20
				line_spacing = 8
				pdf.set_font('Arial', 'B', font_size)
				pdf.set_xy(20, 20)
				x_orig = pdf.get_x()
				y_orig = pdf.get_y()
				print(x_orig)
				print(y_orig)
				pdf.cell(40, 0, supporter.fullname)
				addrLines = supporter.address.split("\n")
				for i in range(0,len(addrLines)):
					print(addrLines[i])
					pdf.set_xy(x_orig, y_orig + line_spacing*(i+1))
					pdf.set_font('Arial', 'B', font_size)
					pdf.cell(40, 0, addrLines[i])
				pdf.image('logo.jpg',120,35, 60,60)
				pdf.set_font('Arial', '', 6)
				stamptext = ""
				if supporter.preference in [3,4,8,9]:
					stamptext = "Hand"
				elif supporter.preference in [1,6]:
					stamptext = "UK"
				elif supporter.preference in [2,7]:
					stamptext = "Int"
				pdf.set_xy(180, 12)
				pdf.cell(15,20,stamptext,border = 1,align = 'C')
				pdf.set_xy(180, 14)
				pdf.cell(15,20,"{}T {}P {}F".format(supporter.letters[0],supporter.letters[1],supporter.letters[2]),border = 0,align = 'C')

		pdf.output(PDFName, 'F')

	@classmethod
	def loadCSV(cls,file_name):
		print(file_name)
		with open(file_name, "r") as f_obj:
			fileContent = f_obj.read()
			info = list()
			string = ""
			result = list()
			for char in fileContent:
				if char == ';':
					result.append(Supporter(info[2],info[1],info[6],info[4],[int(info[8]),int(info[9]),int(info[10])],int(info[3])))
					info = list()
				if char == ',':
					info.append(string)
					string = ""
				else:
					string += char
			cls.Supporters = result

	@classmethod
	def saveCSV(cls,file_name):
		with open(file_name, "w") as f_obj:
			count = 0
			for supporter in Supporter.Supporters:
				count += 1
				csvstring = "{},{},{},{},{},".format(count,supporter.last,supporter.first,supporter.preference,supporter.address)
				csvstring += ",{},,{},{},{},;\n".format(supporter.email,supporter.letters[0],supporter.letters[1],supporter.letters[2])
				f_obj.write(csvstring)
		print("{} Saved succesfully".format(file_name))

	@classmethod
	def emailList(cls):
		emails = ""
		for supporter in cls.Supporters:
			if supporter.preference in [5,6,7,8,9]:
				emails += "{} <{}>,".format(supporter.fullname,supporter.email)
		emails = emails[:-1]
		print(emails)
		pyperclip.copy(emails)# r.update()
		return emails


if __name__ == '__main__':
	test = Supporter("hugh","davith","eemail")
	print(test.fullname)
	test.fullname = "Hugh go Grant"
	print(test.fullname)
	print(test.first)
	print(test.last)