import pickle
import dbconnector as db

def openMv():
	with open('mvs.pickle', 'rb') as handle:
		mvs = pickle.load(handle)
	print('opened')
	return mvs


def saveMv(mvs):
	with open('mvs.pickle', 'wb') as handle:
		pickle.dump(mvs, handle, protocol=pickle.HIGHEST_PROTOCOL)
	print('saved....')

mvs = openMv()
cntr = 1
for i in mvs:
	sql = "INSERT INTO movies(title, genre, release_year, rating, description, trailer_url, thumbnail) VALUES(%s, %s, %s, %s, %s, %s, %s)"
	data = (mvs[i]['title'], mvs[i]['genre'], '', mvs[i]['rating'], '', '', '')
	# Save into db
	db.save(sql, data)
	print(cntr)
	cntr += 1
