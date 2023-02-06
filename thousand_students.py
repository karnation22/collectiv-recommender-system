import cherrypy
import random
import requests
import json
import simplejson
import os
######################## GLOBAL DATA #####################################################################################################################

#these are the main themes for which a student is defined
theme_list = ["School", "Difficulty Level", "Course Count", "GPA", "Major", "Grad_Year", 
			"Sports", "Cultural", "Arts", "Travel", "Food","Shopping","Current Industry", "num_prev_comp",
			"Sex", "Height", "Weight", "Race"]

## Sex (Radio), Race (Radio), School (Radio), Major (Radio), Current Industry (Radio), 
	## Sports (Checkbox), Cultural (Checkbox), Arts (Checkbox), Travel (Checkbox), Food (Checkbox) , Shopping (Checkbox)

#this is a dump of all of the choices for each theme of same chronological order
choice_list = [['Public', 'Private', 'Co-Ed', 'Religious Affiliation', 'Other'],['<10', '10->19', '20->29', '30-39', '40+'],
				['<10', '10->19', '20->29', '30-39', '40+'], ['<2.00', '2.00->2.49', '2.50->2.99', '3.00->3.49', '>=3.50'], 
				['Engineering', 'Sciences', 'Humanities', 'Social Studies','Business', 'Technology', 'Other'],
				['Before', '2017', '2018', '2019', '2020', '2021', '2022', 'After'],
				['Football', 'Basketball', 'Water Sports', 'Racket Sports', 'Soccer','Baseball', 'Other', 'None'],
				['Arts', 'Cannabis', 'Comics', 'Exhibition', 'Fashion', 'Food and Drinks', 'Museum', 'Other', 'None'],
				['Photography/Video', 'Visual Arts', 'Sculpture/3D', 'Drawing', 'Ceramics', 'Collage', 
				 'Fine Arts', 'Architecture', 'Other', 'None'],['Study Abroad', 'Vacation', 'Business', 'Exploration', 
				 'Missionary/Religious Travel','Honeymoon', 'Other', 'None'], ['Chinese', 'Thai', 'Vietnamese', 'Mexican', 'Italian',
				  'Greek', 'Indian', 'American', 'Other', 'None'],['Toys','Electronics','Clothing','Furniture','Beauty', 'Other','None'],['Financial', 'Medical', 'Media & Entertainment', 
				 'Electricity and Power', 'Transporation', 'Retail', 'Travel', 'Technology', 'Aviation/Aeronautics','Government', 'Other'],
				 ['<5', '5->9', '10->14', '15+'], ['Male', 'Female'], ['< 4ft 6in', '4ft 6in -> 4ft 11in', '5ft -> 5ft 5in', 
				 '5ft 6in ->5ft 11in', '6ft -> 6ft 5in', '6ft 6in -> 6ft 11in', '>= 7ft'], ['<100', '100->149', '150->199', '200->249', 
				 '250->299', '300->349','350->399', '400->449', '450->499', '>=500'], ['Native American', 'Asian', 'Black/African American', 
				 'Hispanic/Latino', 'Pacific Islander', 'White', 'Other']]

#list of cities in our world
city_list = ["seattle", "boston", "pittsburgh", "west-lafayette"]

#list of locations that are indexed by city above...
loc_list = [["University of Washington", "Seattle University", "Bellevue College", "Nordstrom", "Target", "Costco", 
			 "Fred Meyer", "Starbucks", "Dicks Drive-In", "Pikes Place", "Whole Foods","Microsoft", "Amazon", "Boeing", "T-Mobile",
		     "Mt. Rainier", "Rattlesnake Ridge", "Lake Union","Museum of Flight", "Pacific Science Center", 
		     "Seattle Art Museum", "Chinatown","LGBTQ Pride", "Cannabis Day"], ["Harvard University", "Massachusetts Institute of Technology", 
			 "Boston College", "Macys", "Nordstrom Rack", "TJ Maxx","Drink", "Townsman", "Sweet Cheeks Q","Boston Consulting Group", "Boston Interactive",
			 "Charles River Esplanade","Freedom Trail", "New England Aquarium",
			"Museum of Science", "Harvard Museum of Natural History", "Boston Tea Party Ship"], ["Carnegie Mellon University", "University of Pittsburgh", "Duquesne University",
					"Giant Eagle Supermarket", "American Eagle Outfitters", "Sheetz",
					"Stacked", "Butcher and the Rye", "Vocelli Pizza",
					"PNC Financial", "Heinz Company", "CMU Robotics Laboratory",
					"National Aviary", "Venture Outdoors","Andy Warhol Museum", "Carnegie Museum of Art", "Carnegie Museum of Natural History",
					"Benedum Center of Fine Arts", "Heinz Hall", "Stage AE"],["Purdue University", "Tark Market", "CVS", "Walmart",
						"McDonalds","Yummy Time","Hodsons Bay Company","Paintball Barn", "African American Cultural Center","Grand Prix"]]

sample_data = [{'City': 'Seattle'}, {'School': 'Other'}, {'Difficulty_Level': 'Post Grad'}, 
				{'Course_Count': '40+'}, {'GPA': '>=3.50'}, {'Major': 'Other'}, {'Grad_Year': 'After'}, 
				{'Sports': 'None'}, {'Cultural': 'None'}, {'Arts': 'None'}, {'Travel': 'None'}, 
	       			{'Food': 'Chinese'}, {'Beauty': 'Hair'}
				{'Current_Industry': 'Other'}, {'Number_Previous_Companies': '15+'}, {'Sex': 'Female'}, 
				{'Height': '>= 7ft'}, {'Weight': '>=500'}, {'Race': 'Other'}]

############################################ GLOBAL DATA ############################################################################################################



#create num_stu random students, each of whom has one favorite location in a specified city
def create_random_students(num_stu, city):
	#error handling for invalid city input
	try: city_index = city_list.index(city.lower())
	except: return  "please input a city in the city list above"

	#create dictionary to store student themes and choices
	students = list()

	assert(len(theme_list) == len(choice_list))
	for student in range(num_stu):
		stud_prof = dict()
		for theme_num in range(len(theme_list)):
			stud_prof[theme_list[theme_num]] = random.choice(choice_list[theme_num])
		stud_prof[city_list[city_index]] = random.choice(loc_list[city_index])
		students.append(stud_prof)
	return students


#create random choice for the new incoming user (one one)
#return populated new user dict & the city of residence
def create_new_user(body):
	new_user = dict()
	#iterate through the entire body and populate new_user
	for attr_dict in body:
		if (attr_dict.keys()[0] == "City"):
			city = attr_dict["City"]
		else: new_user[attr_dict.keys()[0]] = attr_dict.values()[0]
	return (city, new_user)			


"""return a dictionary of (key, value) pairs, with the key showing
	the user number and value showing number of matches of a random
	user to new user"""
def create_user_match(random_students, new_user):
	match_dict = dict()
	#iterate through all of the random students to create match dictionary
	for (stu_id,student) in enumerate(random_students):	
		match_count = 0
		#iterate through each attribute of a student to find matches
		for attribute in student:
			try: 
				if(student[attribute] == new_user[attribute]): match_count += 1
			except: continue 
		match_dict[stu_id] = match_count
	return match_dict

#based on random users, new_user, and match numbers, give recommenatations
def give_recommendations(random_students, new_user, city, k_nearest):
	match_dict = create_user_match(random_students, new_user)
	closest = map(lambda (num, val): num, sorted(match_dict.items(), key=lambda tup: tup[1], reverse=True))
	(recs, index) = (list(), 0)
	while(len(recs) < k_nearest and index != len(closest)):
		if(random_students[closest[index]][city] not in recs):
			recs.append(random_students[closest[index]][city])
		index += 1
	return (recs, index)

#given an item, return a tuple of an image and text...
def create_file_path_tup(item):
	item_img = 'pictures/' + item.lower().replace(" ", "_") + '.jpg'
	item_txt = 'text/' + item.lower().replace(" ", "_") + '.txt'
	return (item_img, item_txt)


#given a city an a list of recommendations, format data to match a dict, with desp as key
# and respective image and txt values as files
def format_JSON_data(city, recs):
	city_img_txt = create_file_path_tup(city)
	new_recs = list()
	for rec in recs:
		new_recs.append(create_file_path_tup(rec))
	city = zip([city], [city_img_txt]) 
	recs = zip(recs, new_recs)
	ret_data = list()
	for (index,(name, (img,txt))) in enumerate(city + recs):
		temp_dict = dict()
		temp_dict["Name"] = name
		temp_dict["Image"] = img
		temp_dict["Text"] = txt
		ret_data.append(temp_dict)

	return str(ret_data).replace("'", "\"")


#inputs a list of (key, value) pairs from user.html webpage
#outputs k_nearest (6) recommendations in a given city...
def rec_items(body):
	(city, new_user) = create_new_user(body)
	rand_dict = create_random_students(100, city.lower())
	(recs, index) = give_recommendations(rand_dict, new_user, city.lower(), 6)
	return format_JSON_data(city, recs)

print rec_items(sample_data)
