import get_crawler
import caluGrade

# uid = '1318010120'
# pwd = '301821'

# uid = '1206010416'
# pwd = '941024'

uid = '1206010423'
pwd = '105512'

lists = get_crawler.getSource(uid,pwd)


subjects = []

for list in lists:
	subject = []
	if(list[5] == '\xe5\xbf\x85\xe4\xbf\xae'):
		# print '{} {} {} {}'.format(list[2],list[4],list[5],list[9])
		print '{:<}\t\t\t{:>3} {:<4} {:<5}'.format(list[2],list[4],list[5],list[6])
		subject.append(list[4])
		subject.append(list[6])
		subjects.append(subject)
caluGrade.get_credit(subjects)