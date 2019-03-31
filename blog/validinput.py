def valdno(num):
	try:
		mobn = int(num[1:3]+num[4:])
		if num[0]=="+" and num[1]=="9" and num[2]=="1" and len(num)>=9 and len(num)<=16 and num[3]==" ":
			return True
		else:
			return False
	except:
		return False