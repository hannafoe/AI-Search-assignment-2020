# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 17:27:57 2020

@author: ich
"""

############
############ ALTHOUGH I GIVE YOU THE 'BARE BONES' OF THIS PROGRAM WITH THE NAME
############ 'skeleton.py', YOU CAN RENAME IT TO ANYTHING YOU LIKE. HOWEVER, FOR
############ THE PURPOSES OF THE EXPLANATION IN THESE COMMENTS, I ASSUME THAT
############ THIS PROGRAM IS STILL CALLED 'skeleton.py'.
############
############ IF YOU WISH TO IMPORT STANDARD MODULES, YOU CAN ADD THEM AFTER THOSE BELOW.
############ NOTE THAT YOU ARE NOT ALLOWED TO IMPORT ANY NON-STANDARD MODULES!
############

import os
import sys
import time
import random
import math

############
############ NOW PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

def read_file_into_string(input_file, ord_range):
    the_file = open(input_file, 'r') 
    current_char = the_file.read(1) 
    file_string = ""
    length = len(ord_range)
    while current_char != "":
        i = 0
        while i < length:
            if ord(current_char) >= ord_range[i][0] and ord(current_char) <= ord_range[i][1]:
                file_string = file_string + current_char
                i = length
            else:
                i = i + 1
        current_char = the_file.read(1)
    the_file.close()
    return file_string

def remove_all_spaces(the_string):
    length = len(the_string)
    new_string = ""
    for i in range(length):
        if the_string[i] != " ":
            new_string = new_string + the_string[i]
    return new_string

def integerize(the_string):
    length = len(the_string)
    stripped_string = "0"
    for i in range(0, length):
        if ord(the_string[i]) >= 48 and ord(the_string[i]) <= 57:
            stripped_string = stripped_string + the_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def convert_to_list_of_int(the_string):
    list_of_integers = []
    location = 0
    finished = False
    while finished == False:
        found_comma = the_string.find(',', location)
        if found_comma == -1:
            finished = True
        else:
            list_of_integers.append(integerize(the_string[location:found_comma]))
            location = found_comma + 1
            if the_string[location:location + 5] == "NOTE=":
                finished = True
    return list_of_integers

def build_distance_matrix(num_cities, distances, city_format):
    dist_matrix = []
    i = 0
    if city_format == "full":
        for j in range(num_cities):
            row = []
            for k in range(0, num_cities):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    elif city_format == "upper_tri":
        for j in range(0, num_cities):
            row = []
            for k in range(j):
                row.append(0)
            for k in range(num_cities - j):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    else:
        for j in range(0, num_cities):
            row = []
            for k in range(j + 1):
                row.append(0)
            for k in range(0, num_cities - (j + 1)):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    if city_format == "upper_tri" or city_format == "strict_upper_tri":
        for i in range(0, num_cities):
            for j in range(0, num_cities):
                if i > j:
                    dist_matrix[i][j] = dist_matrix[j][i]
    return dist_matrix

def read_in_algorithm_codes_and_tariffs(alg_codes_file):
    flag = "good"
    code_dictionary = {}   
    tariff_dictionary = {}  
    if not os.path.exists(alg_codes_file):
        flag = "not_exist"  
        return code_dictionary, tariff_dictionary, flag
    ord_range = [[32, 126]]
    file_string = read_file_into_string(alg_codes_file, ord_range)  
    location = 0
    EOF = False
    list_of_items = []  
    while EOF == False: 
        found_comma = file_string.find(",", location)
        if found_comma == -1:
            EOF = True
            sandwich = file_string[location:]
        else:
            sandwich = file_string[location:found_comma]
            location = found_comma + 1
        list_of_items.append(sandwich)
    third_length = int(len(list_of_items)/3)
    for i in range(third_length):
        code_dictionary[list_of_items[3 * i]] = list_of_items[3 * i + 1]
        tariff_dictionary[list_of_items[3 * i]] = int(list_of_items[3 * i + 2])
    return code_dictionary, tariff_dictionary, flag

############
############ THE RESERVED VARIABLE 'input_file' IS THE CITY FILE UNDER CONSIDERATION.
############
############ IT CAN BE SUPPLIED BY SETTING THE VARIABLE BELOW OR VIA A COMMAND-LINE
############ EXECUTION OF THE FORM 'python skeleton.py city_file.txt'. WHEN SUPPLYING
############ THE CITY FILE VIA A COMMAND-LINE EXECUTION, ANY ASSIGNMENT OF THE VARIABLE
############ 'input_file' IN THE LINE BELOW iS SUPPRESSED.
############
############ IT IS ASSUMED THAT THIS PROGRAM 'skeleton.py' SITS IN A FOLDER THE NAME OF
############ WHICH IS YOUR USER-NAME, E.G., 'abcd12', WHICH IN TURN SITS IN ANOTHER
############ FOLDER. IN THIS OTHER FOLDER IS THE FOLDER 'city-files' AND NO MATTER HOW
############ THE NAME OF THE CITY FILE IS SUPPLIED TO THIS PROGRAM, IT IS ASSUMED THAT 
############ THE CITY FILE IS IN THE FOLDER 'city-files'.
############

input_file = "AISearchfile012.txt"

############
############ PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

if len(sys.argv) > 1:
    input_file = sys.argv[1]

the_particular_city_file_folder = "city-files"
    
if os.path.isfile("../" + the_particular_city_file_folder + "/" + input_file):
    ord_range = [[32, 126]]
    file_string = read_file_into_string("../" + the_particular_city_file_folder + "/" + input_file, ord_range)
    file_string = remove_all_spaces(file_string)
    print("I have found and read the input file " + input_file + ":")
else:
    print("*** error: The city file " + input_file + " does not exist in the folder '" + the_particular_city_file_folder + "'.")
    sys.exit()

location = file_string.find("SIZE=")
if location == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()
    
comma = file_string.find(",", location)
if comma == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()
    
num_cities_as_string = file_string[location + 5:comma]
num_cities = integerize(num_cities_as_string)
print("   the number of cities is stored in 'num_cities' and is " + str(num_cities))

comma = comma + 1
stripped_file_string = file_string[comma:]
distances = convert_to_list_of_int(stripped_file_string)

counted_distances = len(distances)
if counted_distances == num_cities * num_cities:
    city_format = "full"
elif counted_distances == (num_cities * (num_cities + 1))/2:
    city_format = "upper_tri"
elif counted_distances == (num_cities * (num_cities - 1))/2:
    city_format = "strict_upper_tri"
else:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

dist_matrix = build_distance_matrix(num_cities, distances, city_format)
print("   the distance matrix 'dist_matrix' has been built.")

############
############ YOU NOW HAVE THE NUMBER OF CITIES STORED IN THE INTEGER VARIABLE 'num_cities'
############ AND THE TWO_DIMENSIONAL MATRIX 'dist_matrix' HOLDS THE INTEGER CITY-TO-CITY 
############ DISTANCES SO THAT 'dist_matrix[i][j]' IS THE DISTANCE FROM CITY 'i' TO CITY 'j'.
############ BOTH 'num_cities' AND 'dist_matrix' ARE RESERVED VARIABLES AND SHOULD FEED
############ INTO YOUR IMPLEMENTATIONS.
############

############
############ THERE NOW FOLLOWS CODE THAT READS THE ALGORITHM CODES AND TARIFFS FROM
############ THE TEXT-FILE 'alg_codes_and_tariffs.txt' INTO THE RESERVED DICTIONARIES
############ 'code_dictionary' AND 'tariff_dictionary'. DO NOT AMEND THIS CODE!
############ THE TEXT FILE 'alg_codes_and_tariffs.txt' SHOULD BE IN THE SAME FOLDER AS
############ THE FOLDER 'city-files' AND THE FOLDER WHOSE NAME IS YOUR USER-NAME, E.G., 'abcd12'.
############

code_dictionary, tariff_dictionary, flag = read_in_algorithm_codes_and_tariffs("../alg_codes_and_tariffs.txt")

if flag != "good":
    print("*** error: The text file 'alg_codes_and_tariffs.txt' does not exist.")
    sys.exit()

print("The codes and tariffs have been read from 'alg_codes_and_tariffs.txt':")

############
############ YOU NOW NEED TO SUPPLY SOME PARAMETERS.
############
############ THE RESERVED STRING VARIABLE 'my_user_name' SHOULD BE SET AT YOUR USER-NAME, E.G., "abcd12"
############

my_user_name = "lzhc88"

############
############ YOU CAN SUPPLY, IF YOU WANT, YOUR FULL NAME. THIS IS NOT USED AT ALL BUT SERVES AS
############ AN EXTRA CHECK THAT THIS FILE BELONGS TO YOU. IF YOU DO NOT WANT TO SUPPLY YOUR
############ NAME THEN EITHER SET THE STRING VARIABLES 'my_first_name' AND 'my_last_name' AT 
############ SOMETHING LIKE "Mickey" AND "Mouse" OR AS THE EMPTY STRING (AS THEY ARE NOW;
############ BUT PLEASE ENSURE THAT THE RESERVED VARIABLES 'my_first_name' AND 'my_last_name'
############ ARE SET AT SOMETHING).
############

my_first_name = "Hanna"
my_last_name = "Foerster"

############
############ YOU NEED TO SUPPLY THE ALGORITHM CODE IN THE RESERVED STRING VARIABLE 'algorithm_code'
############ FOR THE ALGORITHM YOU ARE IMPLEMENTING. IT NEEDS TO BE A LEGAL CODE FROM THE TEXT-FILE
############ 'alg_codes_and_tariffs.txt' (READ THIS FILE TO SEE THE CODES).
############

algorithm_code = "PS"

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW! YOU HAVE BEEN WARNED!
############

if not algorithm_code in code_dictionary:
    print("*** error: the agorithm code " + algorithm_code + " is illegal")
    sys.exit()
print("   your algorithm code is legal and is " + algorithm_code + " -" + code_dictionary[algorithm_code] + ".")

############
############ YOU CAN ADD A NOTE THAT WILL BE ADDED AT THE END OF THE RESULTING TOUR FILE IF YOU LIKE,
############ E.G., "in my basic greedy search, I broke ties by always visiting the first 
############ city found" BY USING THE RESERVED STRING VARIABLE 'added_note' OR LEAVE IT EMPTY
############ IF YOU WISH. THIS HAS NO EFFECT ON MARKS BUT HELPS YOU TO REMEMBER THINGS ABOUT
############ YOUR TOUR THAT YOU MIGHT BE INTERESTED IN LATER.
############

added_note = ""

############
############ NOW YOUR CODE SHOULD BEGIN.
############
starttime = time.time()  

def generate_random_tour():
    #make a list to cross off the cities that have been added
    to_visit = []
    for i in range(num_cities):
        to_visit.append(i)
    tour = []
    for i in range(num_cities):
        next_vertex = random.randint(0,num_cities-i-1)
        tour.append(to_visit[next_vertex])
        to_visit.pop(next_vertex)#delete city that has been added to tour
    return tour

def all_possible_swaps():
    #in bubble_sort
    #there are n-1 times swaps of (0,1) ... and 1 swap of (n-1,n)
    #it is necessary to add the right amount of swaps for each of (i,i+1) to get the right probability of each swap
    swaps = []
    for i in range(num_cities):
        for j in range(num_cities-i-1,0,-1):
            new_swap = (i,i+1)
            swaps.append(new_swap)
    return swaps

all_swaps = all_possible_swaps()

def generate_random_velocity():
    max_number_of_swaps = (num_cities*(num_cities-1))/2 #maximum number of swaps according to bubble_sort
    num_of_swaps = random.randint(0,max_number_of_swaps)#random amount of swaps for each velocity
    swap_possibilities = all_swaps.copy()
    swaps = []#choose however many swaps from swap_possibilities as num_of_swaps
    for i in range(num_of_swaps):
        choose_swap = random.randint(0, len(swap_possibilities)-1)
        swaps.append(swap_possibilities[choose_swap])
        swap_possibilities.pop(choose_swap)
    return swaps


class Particle:
    def __init__(self,ID,velocity,tour):
        self.ID = ID
        self.velocity = velocity
        self.tour = tour
        self.tour_length = -1
        self.best_tour = []
        self.best_tour_length = -1
    
    def add_velocity(self):
        for swap in self.velocity:
            i,j = swap
            self.tour[i],self.tour[j]=self.tour[j],self.tour[i]
        calculate_tour_length(self)
        
            
    def multiply(self,num): #num can be a float
        if num<1 and num>0:
           k = math.floor(len(self.velocity)*num)
           new_velocity = self.velocity.copy()
           new_velocity = new_velocity[:k]
           return new_velocity
        if num==1:
            return self.velocity
        if num>1:
            new_velocity=int(num)*self.velocity.copy()
            k = math.floor(len(self.velocity)*(num-int(num)))
            lst = self.velocity.copy()
            new_velocity.extend(lst[:k])
            return new_velocity

def calculate_tour_length(particle):
    length = 0
    for i in range(len(particle.tour)-1):
        length+=dist_matrix[particle.tour[i]][particle.tour[i+1]]
    length+=dist_matrix[(particle.tour[len(particle.tour)-1])][(particle.tour[0])]
    particle.tour_length = length
    if particle.best_tour_length==-1:
        particle.best_tour_length = length
        particle.best_tour = particle.tour.copy()
    else:
        if length<particle.best_tour_length:
            particle.best_tour_length = length
            particle.best_tour = particle.tour.copy()
        
def min_tour (particles):
    for particle in particles:
        calculate_tour_length(particle)
    return min(particles,key=lambda particle:particle.best_tour_length)
'''
def bubble_sort(tour):
    for i in range(num_cities):
        swapped = False
        for j in range(0,num_cities-i-1):
            if tour[j]>tour[j+1]:
                tour[j],tour[j+1]=tour[j+1],tour[j]
                swapped = True
        if swapped==False:
            break
'''
def distance(p1,p2): #distance of two tours from each other
    swaps = []
    for i in range(num_cities):
        swapped = False
        for j in range(0,num_cities-i-1):
            if p2.index(p1[j])>p2.index(p1[j+1]):
                p1[j],p1[j+1]=p1[j+1],p1[j]
                swaps.append((j,j+1))
                swapped = True
        if swapped == False:
            break
    return swaps

def multiply(velocity, num): #num can be a float
        if num<1 and num>0:
           k = math.floor(len(velocity)*num)
           new_velocity = velocity.copy()
           new_velocity = new_velocity[:k]
           return new_velocity
        if num==1:
            return velocity
        if num>1:
            new_velocity=int(num)*velocity.copy()
            k = math.floor(len(velocity)*(num-int(num)))
            lst = velocity.copy()
            new_velocity.extend(lst[:k])
            return new_velocity
    


###Parameters, user-defined####
max_it = 20 #maximum number of iterations
N= 5 #number of particles
delta = math.inf #neighbourhood
theta = 0.4 #inertia function: weight to be give to particle's current velocity
alpha = 0.9 #cognitive learning factor: weight to be given to particle's own best position
beta = 3 #social leraning factor: weight to be given to the particle's neighbourhood's best position

def best_in_neighbourhood(particles,a):#including a
    neighbourhood = [a]
    for p in particles:
        if p.ID == a.ID:
            continue
        if len(distance(a.tour.copy(),p.tour.copy()))<=delta:
            neighbourhood.append(p)
    return min(neighbourhood,key=lambda particle:particle.best_tour_length)
'''
def add_velocity(tour,velocity):
    for swap in velocity:
        i,j = swap
        tour[i],tour[j]=tour[j],tour[i]
    length = 0
    for i in range(len(tour)-1):
        length+=dist_matrix[tour[i]][tour[i+1]]
    length+=dist_matrix[(tour[len(tour)-1])][(tour[0])]
    return tour,length
'''##just a check help function

def particle_swarm_opt():
    my_particles = []
    for i in range(N):
        my_particles.append(Particle(i,generate_random_velocity(),generate_random_tour()))
    bestTour = min_tour(my_particles)
    print(bestTour.best_tour,bestTour.best_tour_length,bestTour.tour,bestTour.tour_length,'\n')
    t = 0
    for a in my_particles:
        print(a.best_tour,a.best_tour_length,a.tour,a.tour_length)
    while t<max_it:
        for a in my_particles:
            best_in_nhood = best_in_neighbourhood(my_particles, a)
            current_tour = a.tour.copy()
            a.add_velocity() #adding the velocity to the current tour to get new tour
            ####NORMALISE VELOCITY###
            a.velocity = distance(current_tour.copy(), a.tour.copy())
            #########################
            new_velocity = []
            new_velocity.extend(a.multiply(theta))#adding the former velocity with weight theta
            #calculate weight of particle's own position in new_velocity
            dif_aBestTour_aCurTour = distance(a.best_tour.copy(),current_tour.copy()) #difference of a's best tour-a' current tour
            #component-wise multiplication of epsilon*dif_aBestTour_aCurTour, 
            #each component of epsilon is a random number between 0 and 1
            #multiply random float in range (0,1) (-> epsilon) with dif_aBestTour_aCurTour
            epsilon = random.random()
            new_velocity.extend(multiply(dif_aBestTour_aCurTour,(epsilon*alpha)))
            dif_nhoodBest_aCurTour = distance(best_in_nhood.best_tour.copy(),current_tour.copy())
            epsilon_p = random.random()
            new_velocity.extend(multiply(dif_nhoodBest_aCurTour, (epsilon_p*beta)))
            a.velocity = new_velocity
            if a.best_tour_length>a.tour_length:
                a.best_tour_length=a.tour_length
                a.best_tour=a.tour.copy()
                print('x')
        print()
        for a in my_particles:
            print(a.best_tour,a.best_tour_length,a.tour,a.tour_length)
        print()
        bestTour=min_tour(my_particles)
        print(bestTour.best_tour,bestTour.best_tour_length,bestTour.tour,bestTour.tour_length)
        t+=1
        print('----------------')
    return bestTour.best_tour,bestTour.best_tour_length


tour,tour_length=particle_swarm_opt()
print(tour,tour_length)

endtime=time.time()
print('Time: ',endtime-starttime)

############
############ YOUR CODE SHOULD NOW BE COMPLETE AND WHEN EXECUTION OF THIS PROGRAM 'skeleton.py'
############ REACHES THIS POINT, YOU SHOULD HAVE COMPUTED A TOUR IN THE RESERVED LIST VARIABLE 'tour', 
############ WHICH HOLDS A LIST OF THE INTEGERS FROM {0, 1, ..., 'num_cities' - 1}, AND YOU SHOULD ALSO
############ HOLD THE LENGTH OF THIS TOUR IN THE RESERVED INTEGER VARIABLE 'tour_length'.
############

############
############ YOUR TOUR WILL BE PACKAGED IN A TOUR FILE OF THE APPROPRIATE FORMAT AND THIS TOUR FILE,
############ WHOSE NAME WILL BE A MIX OF THE NAME OF THE CITY FILE, THE NAME OF THIS PROGRAM AND THE
############ CURRENT DATA AND TIME. SO, EVERY SUCCESSFUL EXECUTION GIVES A TOUR FILE WITH A UNIQUE
############ NAME AND YOU CAN RENAME THE ONES YOU WANT TO KEEP LATER.
############

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW THIS POINT! YOU HAVE BEEN WARNED!
############
'''
flag = "good"
length = len(tour)
for i in range(0, length):
    if isinstance(tour[i], int) == False:
        flag = "bad"
    else:
        tour[i] = int(tour[i])
if flag == "bad":
    print("*** error: Your tour contains non-integer values.")
    sys.exit()
if isinstance(tour_length, int) == False:
    print("*** error: The tour-length is a non-integer value.")
    sys.exit()
tour_length = int(tour_length)
if len(tour) != num_cities:
    print("*** error: The tour does not consist of " + str(num_cities) + " cities as there are, in fact, " + str(len(tour)) + ".")
    sys.exit()
flag = "good"
for i in range(0, num_cities):
    if not i in tour:
        flag = "bad"
if flag == "bad":
    print("*** error: Your tour has illegal or repeated city names.")
    sys.exit()
check_tour_length = 0
for i in range(0, num_cities - 1):
    check_tour_length = check_tour_length + dist_matrix[tour[i]][tour[i + 1]]
check_tour_length = check_tour_length + dist_matrix[tour[num_cities - 1]][tour[0]]
if tour_length != check_tour_length:
    flag = print("*** error: The length of your tour is not " + str(tour_length) + "; it is actually " + str(check_tour_length) + ".")
    sys.exit()
print("You, user " + my_user_name + ", have successfully built a tour of length " + str(tour_length) + "!")

local_time = time.asctime(time.localtime(time.time()))
output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
output_file_time = output_file_time.replace(" ", "0")
script_name = os.path.basename(sys.argv[0])
if len(sys.argv) > 2:
    output_file_time = sys.argv[2]
output_file_name = script_name[0:len(script_name) - 3] + "_" + input_file[0:len(input_file) - 4] + "_" + output_file_time + ".txt"

f = open(output_file_name,'w')
f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + "),\n")
f.write("ALGORITHM CODE = " + algorithm_code + ", NAME OF CITY-FILE = " + input_file + ",\n")
f.write("SIZE = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + ",\n")
f.write(str(tour[0]))
for i in range(1,num_cities):
    f.write("," + str(tour[i]))
f.write(",\nNOTE = " + added_note)
f.close()
print("I have successfully written your tour to the tour file:\n   " + output_file_name + ".")
    



'''







    


