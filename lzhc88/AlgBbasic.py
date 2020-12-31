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

input_file = "AISearchfile535.txt"

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

algorithm_code = "AC"

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

class Node:
    def __init__(self,ID,state,action,path_cost):
        self.ID=ID
        self.state=state
        self.action = action
        self.path_cost = path_cost

class State:
    def __init__(self,partial_tour):
        self.partial_tour=partial_tour
    
    def get(self):
        return self.partial_tour
    
        
def basic_greedy():
    node = Node(0,State([0]),0,0)
    path = [node.ID]
    while len(path)!=num_cities:
        successors = []
        for i in range(1,num_cities):#all successors
            if i==node.ID:
                continue
            if i in path:
                continue
            new_id = i
            new_partial_tour=node.state.get().copy()
            new_partial_tour.append(i)
            new_state = State(new_partial_tour)
            new_dist = dist_matrix[node.ID][i]
            new_pathcost = node.path_cost+new_dist
            new_node = Node(new_id,new_state,new_dist,new_pathcost)
            successors.append(new_node)
        node = min(successors,key=lambda node:node.action)
        path.append(node.ID)
    path_cost=node.path_cost+(dist_matrix[0][node.ID])
    return path,path_cost
        
    

starttime = time.time()      
#####determine the intial best-tour by an initial basic greedy search##########
tour_of_nearest_neighbour,tour_length_of_nearest_neighbour = basic_greedy()



####Parameters, user-defined####
max_it = 20 #maximum number of iterations
N= 20 #number of ants
tao_0 = N/tour_length_of_nearest_neighbour #initial pheromone deposit
row = 0.5 #pheromone decay rate
alpha = 1
beta = 3

added_note+=str(N)+' = number of ants, '+str(max_it)+' = maximum number of iterations, '+str(alpha)+' = alpha, '+str(beta)+' = beta, '+str(row)+' = row'

####helpful structures####
class Ant:
    def __init__(self,ID):
        self.ID = ID
        self.current=random.randint(0, num_cities-2)
        self.visited = [] #visited edges
        self.visited_vertices =[]
        self.path_cost=0

#########pheromone to deposit on each edge...recomputed every round##############
def build_pheromone_matrix():
    matrix = []
    for i in range(num_cities):
        matrix.append([])
        for j in range(num_cities):
            matrix[i].append(tao_0)
    return matrix
pheromone_matrix = build_pheromone_matrix()

######deposits pheromone on each dege that has been visited by this ant############
def pheromone_deposit_each_ant(ant,edge): #edge is a tuple
    if edge in ant.visited:
        return 1/(ant.path_cost)
    return 0

    
def probabilities_of_vertices(ant):
    heuristic_desirabilities=[]
    for i in range(num_cities):
        if i == ant.current:
            continue
        if i in ant.visited_vertices:
            continue
        else:
            if dist_matrix[ant.current][i]==0:#case that distance between two cities is 0
                heuristic_desirabilities.append(1)#this is very desired, so 1 is added
            else:#normal case, calculate desirability of going to an unvisited city
                heuristic_desirabilities.append(1/dist_matrix[ant.current][i])#1/length of edge
    if len(heuristic_desirabilities)==0:#all cities were visited
        return 1 ###finished
    #####Now calculate the overall probability of each edge being traversed next####
    probies = []
    index =0
    sum_of_all =0
    for i in range(num_cities):
        if i == ant.current:
            continue
        if i in ant.visited_vertices:
            continue
        else:
            ###prob=(current pheromone level at edge)^alpha*(1/length of edge)^beta
            prob=((pheromone_matrix[ant.current][i])**alpha)*((heuristic_desirabilities[index])**beta)
            sum_of_all+=prob
            probies.append(prob)
            index+=1
    probabilities =[]
    index =0
    for i in range(num_cities):
        if i == ant.current:
            continue
        if i in ant.visited_vertices:
            continue
        else:
            ####the overall probability of each edge finally computed######
            probabilities.append(probies[index]/sum_of_all)
            index+=1
    return probabilities



def ant_colony_opt():
    best_tour = tour_of_nearest_neighbour
    best_tour_length = tour_length_of_nearest_neighbour
    my_ants=[]
    for i in range(N):
        new_ant = Ant(i)
        my_ants.append(new_ant)
    for t in range(max_it): ###maybe change max_it later to time.time 
        #print(pheromone_matrix)
        for ant in my_ants:
            ant.current=random.randint(0, num_cities-2)
            ant.visited = [] #visited edges
            ant.visited_vertices =[ant.current]
            ant.path_cost=0
            for i in range(num_cities):##create a full length path for each ant, loop num_cities times
                probabilities = probabilities_of_vertices(ant)
                if probabilities ==1:
                    break
                else:
                    #print(ant.current)
                    #print(probabilities)
                    rand_float = random.random() # Random float:  0.0 <= x < 1.0
                    index = 1
                    past = probabilities[0]
                    next_vertex = 0
                    #print('**',rand_float,'**')
                    for e in range(num_cities): #for all neighbouring vertices of i, compute next vertex probability
                        if e == ant.current:
                            continue
                        elif e in ant.visited_vertices:
                            continue
                        else:
                            #print(past)
                            if rand_float<past:
                                next_vertex = e
                                break
                            past += probabilities[index]
                            index+=1
                    #print(next_vertex)
                    ant.visited.append([ant.current,next_vertex])
                    ant.path_cost+=dist_matrix[ant.current][next_vertex]
                    ant.visited_vertices.append(next_vertex)
                    ant.current = next_vertex
            ant.path_cost+=dist_matrix[ant.current][ant.visited_vertices[0]]
            ant.visited.append([ant.current,ant.visited_vertices[0]])
            #print(ant.visited_vertices,ant.path_cost)
        min_path_cost=min(my_ants,key=lambda ant:ant.path_cost)
        if min_path_cost.path_cost<best_tour_length:
            best_tour = min_path_cost.visited_vertices
            best_tour_length = min_path_cost.path_cost
        ##deposit,evaporate pheromone on edges
        #print('--------------')
        list_of_pheromone_deposit = {}
        for ant in my_ants:
            
            for edge in ant.visited:
                p = pheromone_deposit_each_ant(ant, edge)
                try:
                    list_of_pheromone_deposit[tuple(edge)]+=p
                except:
                    list_of_pheromone_deposit[tuple(edge)]=p
        for i in range(num_cities):
            for j in range(num_cities):
                evap = (1-row)*pheromone_matrix[i][j]
                try:
                    pheromone_matrix[i][j]= evap+list_of_pheromone_deposit[(i,j)]
                except:
                    pheromone_matrix[i][j]= evap
        
    return best_tour,best_tour_length

#print(dist_matrix)
tour,tour_length=ant_colony_opt()
print(tour_of_nearest_neighbour,tour_length_of_nearest_neighbour)
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
    











    


