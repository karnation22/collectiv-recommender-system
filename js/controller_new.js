var app = angular.module("myApp", ['ngMaterial']);
app.controller("myCtrl", function($scope) {

    $scope.data = {

        City: 'Boston',
        Sex: 'Male',
        Height: '6ft -> 6ft 5in',
        Weight: '150->199',
        Race: 'Asian',
        School: 'Public',
        Difficulty_Level: '400s',
        Course_Count: '30-39',
        GPA: '3.00->3.49',
        Major: 'Engineering',
        Grad_Year: '2020',
        Sports: 'Basketball',
        Cultural: 'Comics',
        Arts: 'Fine Arts',
        Travel: 'Business',
        Current_Industry: 'Aviation/Aeronautics',
        Number_Previous_Companies: '10->14'
    };


	//name of student, world cities, and attraction categories for students
    $scope.name = "Karn Dalmia";
    $scope.cities = ["Boston", "Seattle","Pittsburgh", "West-Lafayette"];
    $scope.attractions = ["University", "Retail", "Food/Drinks", "Professional Companies", 
    					  "Outdoor Activities", "Tourist Attractions", "Cultural"];

    //theme for student as well as valued sub-attributes
    $scope.student = {
                        Location:
                                [
                                    { City: ['Boston', 'Pittsburgh', 'Seattle', 'West-Lafayette'] } 
                                ],

                        Biography: [
                                    { Sex : ['Male', 'Female'] }, 
                                    { Height : ['< 4ft 6in', '4ft 6in -> 4ft 11in', '5ft -> 5ft 5in', '5ft 6in ->5ft 11in',
                                                             '6ft -> 6ft 5in', '6ft 6in -> 6ft 11in', '>= 7ft'] },
                                    { Weight : ['<100', '100->149', '150->199', '200->249', '250->299', '300->349',
                                                        '350->399', '400->449', '450->499', '>=500'] }, 
                                    { Race : ['Asian', 'Black/African American', 'Hispanic/Latino', 'Native American', 
                                                'Pacific Islander', 'White', 'Other'] }
                                 ],
                       
    				  Academics: [ 
								    { School : ['Public', 'Private', 'Co-Ed', 'Religious Affiliation', 'Other'] },
						            { Difficulty_Level : ['100s', '200s', '300s', '400s', 'Graduate', 'Post Grad'] } , 
						            { Course_Count : ['<10', '10->19', '20->29', '30-39', '40+'] }  
   					             ],

					  Academic_Profile: [
						  					{ GPA : ['<2.00', '2.00->2.49', '2.50->2.99', '3.00->3.49', '>=3.50'] } , 
						  					{ Major : ['Business', 'Engineering', 'Humanities', 'Sciences', 'Social Studies', 'Technology', 'Other'] }, 
						  					{ Grad_Year : ['Before', '2017', '2018', '2019', '2020', '2021', '2022', 'After'] }
					  					],

					  Interests: [
					  				{ Sports : ['Baseball', 'Basketball', 'Football', 'Racket Sports', 'Soccer', 'Water Sports', 'Other', 'None'] }, 
					  				{ Cultural : ['Arts', 'Cannabis', 'Comics', 'Exhibition', 'Fashion', 'Food and Drinks', 'Museum', 'Other', 'None'] }, 
					  				{ Arts : ['Architecture', 'Ceramics', 'Collage', 'Drawing', 'Fine Arts', 'Photography/Video', 'Sculpture/3D', 
                                                'Visual Arts', 'Other', 'None'] },
					  				{ Travel : ['Business', 'Exploration', 'Honeymoon', 'Missionary/Religious Travel', 'Study Abroad', 'Vacation', 'Other', 'None'] }
					  			 ],

					  Professional: [
					  					{ Current_Industry : ['Aviation/Aeronautics', 'Electricity and Power', 'Financial', 'Government', 
                                                'Media & Entertainment', 'Medical', 'Retail', 'Technology', 'Transporation', 'Travel', 'Other'] }, 
						 				{ Number_Previous_Companies : ['<5', '5->9', '10->14', '15+'] }
						 			]
					};

        $scope.saveAndContinue = function() {
            var main_data = [];
            //create a list of (key, value) pairs 
                //send that data via AJAX requst
            angular.forEach($scope.data, function(value, key){
                var map = {};
                map[key] = value;
                main_data.push(map);
            });
            debugger;
            //ensure that the length of the data is 16 (i.e user has selected all attributes)
            if(main_data.length != 17){
                alert("Please select an option for all of the subthemes");
            }
            else{
                //relocate back into world.html 
                //post attribute data to the respective python doc for eval
                $.ajax({
                  type: 'POST',
                  url: "/userdata",
                  contentType: "plain/text",
                  processData: false,
                  data: JSON.stringify(main_data),
                  success: function(main_data) {window.location = "world.html";},
                  dataType: "text"
                });
            }
        }
	// (key,value) pair in which key is city and value is dictionary of attraction categories and relevant items
	$scope.world = {
					Boston : 
							{  
								Universities: ["Harvard University", "Massachusetts Institute of Technology", "Boston College"],
    						    Retail_Stores: ["Macy's", "Nordstorm Rack", "TJ Maxx"],
    							Food_Drinks: ["Drink", "Townsman", "Sweet Cheeks Q"],
    							Professional_Companies: ['Boston Consulting Group', "Boston Interactive"],
    							Outdoor_Activities: ["Chareles River Esplanade"],
    							Tourist_Attractions : ["Freedom Trail", "New England Aquarium"],
    							Cultural: ["Museum of Science", "Harvard Museum of Natural History", "Boston Tea Party Ship"]
    						},

    				Seattle : 
    						{
    							Universities: ["University of Washington", "Seattle University", "Bellevue College"],
    							Retail_Stores: ["Nordstrom", "Target", "Costco", "Fred Meyer"],
    							Food_Drinks: ["Starbucks", "Dicks", "Pike's Place", "Whole Foods"],
    							Professional_Companies: ["Microsoft", "Amazon", "Boeing", "T-Mobile"],
    							Outdoor_Activities: ["Mt. Rainier", "Rattlesnake Ridge", "Lake Union"],
    							Tourist_Attractions : ["Museum of Flight", "Pacific Science Center", "Seattle Art Museum", "Chinatown"],
    							Cultural: ["LGBTQ Pride Day", "Seattle Cannabis Day"]
    						},

    				Pittsburgh : 
    						{
    							Universities : ["Carnegie Mellon University", "University of Pittsburgh", "Duquesne Univerity"],
    							Retail_Stores: ["Giant Eagle Supermarket", "American Eagle Outfitters", "Sheetz"],
    							Food_Drinks: ["Stacked", "Butcher and the Rye", "Vocelli Pizza"],
    							Professional_Companies: ["PNC Financial", "Heinz Company", "CMU Robotics Laboratory"],
    							Outdoor_Activities: ["National Aviary", "Venture Outdoors"],
    							Tourist_Attractions : ["Andy Warhol Museum", "Carnegie Museum of Art", "Carnegie Museum of Natural History"],
    							Cultural: ["Benedum Center of Fine Arts", "Heinz Hall", "Stage AE"]
    						},

    				West_Lafayette :
    						{
    							Universities: ["Purdue"], Retail_Stores: ["Tark Market", "CVS", "Walmart"], 
    							Food_Drinks: ["McDonalds","Yummy Time"], Professional_Companies: ["Hodson's Bay Company"],
  								Outdoor_Activities: ["Paintball Barn"], 
  								Cultural: ["African American Cultural Center","Grand Prix"]
    						} 

					}


	
});