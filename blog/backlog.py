from datetime import datetime

def backloghome(ip, data, loc, namef):
	filehandle = []
	temp =""
	if loc == "create":
		temp = str(ip)+"{title:"+str(data.title)+" content:"+str(data.content)+" date_posted:"+str(data.date_posted)+" author:"+str(data.author)+" img_url:"+str(data.image)+" booked:"+str(data.bookeditem)+" college:"+str(data.college)+" mob:"+str(data.mobileno)+" tokens:"+str(data.tokens)+" user_got:"+str(data.tokenbyuser)+" }\n"
		filehandle.append(temp)
		fname = "bkup/homepage/create/"+str(namef)+".txt"
	elif loc == "update":
		temp = str(ip)+"{title:"+str(data.title)+" content:"+str(data.content)+" date_posted:"+str(data.date_posted)+" author:"+str(data.author)+" img_url:"+str(data.image)+" booked:"+str(data.bookeditem)+" college:"+str(data.college)+" mob:"+str(data.mobileno)+" tokens:"+str(data.tokens)+" user_got:"+str(data.tokenbyuser)+" }\n"
		filehandle.append(temp)
		fname = "bkup/homepage/update/"+str(namef)+".txt"
	elif loc == "delete":
		temp = str(ip)+"{title:"+str(data.title)+" content:"+str(data.content)+" date_posted:"+str(data.date_posted)+" author:"+str(data.author)+" img_url:"+str(data.image)+" booked:"+str(data.bookeditem)+" college:"+str(data.college)+" mob:"+str(data.mobileno)+" tokens:"+str(data.tokens)+" user_got:"+str(data.tokenbyuser)+" }\n"
		filehandle.append(temp)
		fname = "bkup/homepage/delete/"+str(namef)+".txt"
	elif loc == "booked":
		temp = str(ip)+"{title:"+str(data.title)+" content:"+str(data.content)+" date_posted:"+str(data.date_posted)+" author:"+str(data.author)+" img_url:"+str(data.image)+" booked:"+str(data.bookeditem)+" college:"+str(data.college)+" mob:"+str(data.mobileno)+" tokens:"+str(data.tokens)+" user_got:"+str(data.tokenbyuser)+" }\n"
		filehandle.append(temp)
		fname = "bkup/homepage/booked/"+str(namef)+".txt"
	elif loc == "retbook":
		temp = str(ip)+"RET{title:"+str(data.title)+" content:"+str(data.content)+" date_posted:"+str(data.date_posted)+" author:"+str(data.author)+" img_url:"+str(data.image)+" booked:"+str(data.bookeditem)+" college:"+str(data.college)+" mob:"+str(data.mobileno)+" tokens:"+str(data.tokens)+" user_got:"+str(data.tokenbyuser)+" }\n"
		filehandle.append(temp)
		fname = "bkup/homepage/booked/"+str(namef)+".txt"
	filehandle.insert(0, str(datetime.now())+"\n")	
	try:
		f = open(fname, "a")
		f.write("\n")
		f.writelines(filehandle)
		f.close()
	except:
		f = open(fname, "w")
		f.write("\n")
		f.writelines(filehandle)
		f.close()
		

def backlog(ip, folder, data, namef):
	fname = "bkup/"+folder+"/"+str(namef)+".txt"
	data = str(ip)+" "+str(datetime.now()) + data
	try:
		f = open(fname, "a")
		f.write(data)
		f.close()
	except:
		f = open(fname, "w")
		f.write(data)
		f.close()

def backlogtoken(ip, folder, pk, data):
	fname = "bkup/"+folder+"/"+pk+".txt"
	data = str(ip) +" "+ str(datetime.now()) + data
	try:
		f = open(fname, "a")
		f.write(data)
		f.close()
	except:
		f = open(fname, "w")
		f.write(data)
		f.close()
