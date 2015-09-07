import string

def get_grade(gra):
	if(gra == '\xe4\xbc\x98\xe7\xa7\x80'):
		return 5
	if(gra == '\xe8\x89\xaf\xe5\xa5\xbd'):
		return 4.5
	if(gra == '\xe4\xb8\xad\xe7\xad\x89'):
		return 3.5
	if(gra == '\xe5\x8f\x8a\xe6\xa0\xbc'):
		return 2.5
	return min(5,((int(string.atof(gra))-60)//5)*5/10.0 + 2)

def get_credit(lines):
	credits = 0
	grades = 0
	for line in lines:
		if(line[1] == ''):
			continue
		credit = string.atof(line[0])
		grade = get_grade(line[1])
		# print credit,grade
		credits += credit
		grades += grade * credit
	return grades/credits