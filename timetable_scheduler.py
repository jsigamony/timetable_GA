# -*- coding: utf-8 -*-
"""i210814_Jeremy_AI_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1k62BdLtdXWF26FgFyQ3GX-x6Xj_oJWTd
"""




import pandas as pd

course_allocation_df = pd.read_excel('course_allocation.xlsx')

# Print the dataframe
# print(course_allocation_df)

course_allocation_df

course_allocation_df = course_allocation_df.iloc[3:]

course_allocation_df

course_allocation_df.rename(columns={'Unnamed: 1': 'Course-Code', 'Unnamed: 2': 'Course Name', 'Unnamed: 3': 'CHs', 'Unnamed: 4': 'Section', 'Unnamed: 5': 'Instructor', 'Unnamed: 6': 'Course Coordinator'}, inplace=True)

course_allocation_df

# course_allocation_df.drop(columns=['Course Coordinator', 'CHs'], inplace=True)

course_allocation_df.drop(columns=['CHs'], inplace=True)

course_allocation_df

course_allocation_df = course_allocation_df.dropna()

course_allocation_df

# course_allocation_df.set_index('FAST School of Computing, NUCES, Islamabad', inplace=True)

course_allocation_df.rename(columns={'FAST School of Computing, NUCES, Islamabad' : 'Index'})

import random
# import pandas as pd

df = pd.DataFrame(course_allocation_df)

# Monday till friday time slots
time_slots = [
    f"{day} {hour}" for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for hour in ['9-11', '11-1', '1-3']
]

# creating room numbers for 3rd floor and 4th floor c block
rooms = [f"C-{i}" for i in range(301, 312)] + [f"C-{i}" for i in range(401, 412)]

# Genetic algorithm parameters
POPULATION_SIZE = 50
NUM_GENERATIONS = 100
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.7

# Fitness function
def fitness(individual, df):
    score = 0
    #creating a dictionary that will map days to make implementation easier
    day_mapping = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4}

    #Implementing constraints
    #No professor should have overlapping classes
    for instructor in df['Instructor'].unique():
        instructor_slots = [ind['time'] for ind in individual if ind['instructor'] == instructor]
        if len(instructor_slots) != len(set(instructor_slots)):
            score -= 1  # deduct score if constraint violated

    #No professor can teach more than 3 courses
    for instructor in df['Instructor'].unique():
        if len([ind for ind in individual if ind['instructor'] == instructor]) > 3:
            score -= 1

    #No section can have more than 5 courses in a semester
    for section in df['Section'].unique():
        if len([ind for ind in individual if ind['section'] == section]) > 5:
            score -= 1

    #A room cannot be assigned for two different sections at the same time
    for room in rooms:
        room_slots = [(ind['time'], ind['section']) for ind in individual if ind['room'] == room]
        if len(room_slots) != len(set(room_slots)):
            score -= 1

    #Each course should have two lectures per week not on the same or adjacent days
    for course in df['Course-Code'].unique():
        course_times = [ind['time'] for ind in individual if ind['course'] == course]
        days = [day_mapping[time.split(' ')[0]] for time in course_times]
        if len(days) != 2 or abs(days[0] - days[1]) <= 1:
            score -= 1

    return score,

# creating individual chromoses timetables initially
def create_individual(df, time_slots, rooms):
    return [{'course': row['Course-Code'], 'instructor': row['Instructor'], 'section': row['Section'], 'time': random.choice(time_slots), 'room': random.choice(rooms)} for index, row in df.iterrows()]

# Crossover
def crossover(parent1, parent2):
    index = random.randint(1, len(parent1) - 1) #choosing a random point to do crossober

    child1 = parent1[:index] + parent2[index:]
    child2 = parent2[:index] + parent1[index:]
    return child1, child2

# Mutation
def mutate(individual, time_slots, rooms):

    index = random.randint(0, len(individual) - 1)
    individual[index]['time'] = random.choice(time_slots)
    individual[index]['room'] = random.choice(rooms)

    return individual

# Tournament Selection
def select(population, k, t_size=3):
    i = 0
    selected_pop = []
    for _ in range(k):
    # while i in range(k):
        tournament = random.sample(population, t_size)
        winner = max(tournament, key=lambda ind: fitness(ind, df)[0])
        selected_pop.append(winner)
    return selected_pop

#Creating an initial population of timetables
population = [create_individual(df, time_slots, rooms) for _ in range(POPULATION_SIZE)]

#running it upto 500 generations
for gen in range(NUM_GENERATIONS):
    new_population = []

    #creating a new population for every generation of algo
    for _ in range(int(len(population) / 2)):
        parent1, parent2 = select(population, 2)
        if random.random() < CROSSOVER_RATE:
            n1, n2 = crossover(parent1, parent2)
        else:
            n1, n2 = parent1, parent2
        new_population.append(n1)
        new_population.append(n2)
    population = new_population
    population = [mutate(ind, time_slots, rooms) if random.random() < MUTATION_RATE else ind for ind in population]

fitnesses = [fitness(ind, df) for ind in population]
index = max(range(len(fitnesses)), key=lambda i: fitnesses[i][0])
final_timetable = population[index]
#converting back to a dataframe
solution_df = pd.DataFrame(final_timetable)
solution_df







