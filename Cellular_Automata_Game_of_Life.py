
# Cellular Automata Game of Life

# Haig Douzdjian

IPython = (__doc__ is not None) and ('IPython' in __doc__)
Main    = __name__ == '__main__'

import numpy as np
import random

logging = False

def log(message):
    if logging:
        print(message)

class World:
    '''
    This class sets the grid for the for the fish and bear simulation
    '''
    def __init__(self, rows, columns):
        '''
        Creates the rows, columns, table and biome list instances.
        '''
        self._rows = rows
        self._columns = columns
        self._table = np.array([None] * (rows * columns)).reshape(rows, columns)
        self._biome_list = []

    def array(self):
        '''
        Accessor function.
        '''
        return self._table

    def rows(self):
        '''
        Accessor function.
        '''
        return self._rows

    def columns(self):
        '''
        Accessor function.
        '''
        return self._columns

    def add(self, obj, location):
        '''
        Sets a location in the table equal to the object and then appends the biome list
        so that the user can tell what objects are in the world.
        '''
        self._table[location] = obj
        self._biome_list.append(obj)

    def fetch(self, location):
        '''
        Returns the location of an object inside of the world.
        '''
        return self._table[location]

    def remove(self, obj, location):
        '''
        Removes an object from the world and if there is nothing in the world
        it removes any object that was in the biome list.
        '''
        self._table[location] = None
        self._biome_list.remove(obj)

    def empty_location(self, location):
        '''
        Tests to see if a location is occupied if it is not occupied it returns True.
        If the location is occupied returns false.
        '''
        if self._table[location] == None:
            return True
        else:
            return False

    def biota(self):
        '''
        Returns the biome list.
        '''
        return self._biome_list

w0 = World(5,5)

assert len(w0.biota()) == 0

w1 = World(5,5)

w1.add('hello', (0,0))
w1.add('world', (1,1))

assert w1.fetch((0,0)) == 'hello'
assert w1.fetch((1,1)) == 'world'

w2 = World(5,5)

w2.add('hello', (0,0))
w2.add('world', (1,1))

assert sorted(w2.biota()) == ['hello','world']

w2.remove('hello', (0,0))
w2.remove('world', (1,1))

assert w2.biota() == []


# Fish Class:
# (1) Fish are susceptible to overcrowding:  if there are fish in 2 or more neighboring cells the fish dies (it's removed from the simulation)
# (2) A fish can reproduce if it has been alive for a certain number of time steps: a random neighboring cell is chosen, and if that cell is empty, a new fish is placed in that cell
# (3) A fish can move to another cell:  it picks a random direction, and if the neighboring cell in that direction is unoccupied the fish moves there

class Animal:
    def __init__(self, world, location):
        '''
        Creates the instances for the location, world, world.add, life, and counter.
        '''
        self._location = location
        self._world = world
        self._world.add(self, self._location)
        self._life = True
        self._counter = 0

    def location(self):
        '''
        Accessor function for location.
        '''
        return self._location

    def move(self):
        '''
        Picks a neighbor of a location at random and returns the new location for an object.
        '''
        live_list = [(-1, 1), (0, 1), (1, 1), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]
        z = random.choice(live_list)
        new_location = ((self._location[0] + z[0]) % self._world.rows(), (self._location[1] + z[1]) % self._world.rows())
        self._location = new_location
        return self._location

class Fish(Animal):
    breed_interval = 12

    def __init__(self, world, location):
        '''
        Uses the animal class's instances.
        '''
        Animal.__init__(self, world, location)

    def __repr__(self):
        '''
        Returns the fish symbol.
        '''
        return "\U0001F41F"

    def live(self):
        '''
        Creates a list of all of the neighnoring cells and sees if their are fish near by.  If there are greater than
        2 fish it removes one due starvation if not then it creates a new fish in a new location.
        '''
        live_list = [(-1, 1), (0, 1), (1, 1), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]
        adjacent_fish = 0
        for z in live_list:
            newx = self._location[0] + z[0]
            newy = self._location[1] + z[1]
            if (newx >= 0 and newx < self._world._rows and newy >= 0 and newy < self._world._columns):
                if (0 <= self._location[0] < self._world._rows) and (0 <= self._location[1] < self._world._columns):
                    if (not self._world.empty_location((newx, newy))) and isinstance(self._world.fetch((newx, newy)), Fish):
                        adjacent_fish += 1
        if adjacent_fish >= 2:
            self._world.remove(self, self._location)
        else:
            self._counter += 1
            if self._counter >= Fish.breed_interval:
                z = random.choice(live_list)
                nx = self._location[0] + z[0]
                ny = self._location[1] + z[1]
                new_location = (nx, ny)
                if self._world._table[new_location] == None:
                    self._world.add(self, new_location)


fw2 = World(5,5)
Fish.breed_interval = 1
f2 = Fish(fw2, (2,2))
f2.live()

fw2.biota()

fw1 = World(5,5)
assert len(fw1.biota()) == 0

f1 = Fish(fw1, (2,2))
assert len(fw1.biota()) == 1

assert f1.location() == (2,2)

fw2 = World(5,5)
Fish.breed_interval = 1
f2 = Fish(fw2, (2,2))
f2.live()
assert len(fw2.biota()) == 2

Fish.breed_interval = 12

fw3 = World(5,5)
f3 = Fish(fw3, (2,2))
Fish(fw3, (1,1))
Fish(fw3, (3,3))
f3.live()
assert len(fw3.biota()) == 2

fw4 = World(5,5)
f4 = Fish(fw4, (2,2))
f4.move()
r, c = f4.location()
assert (r,c) != (2,2)
assert abs(r-2) <= 1 and abs(c-2) <= 1

# Bear Class:
# (1) A bear looks for fish in each adjacent cell; if it finds one or more fish it eats one at random
# (2) If a bear has not eaten for certain number of time steps it dies (it's removed from the simulation)
# (3) A bear can reproduce if it has been alive for a certain number of time steps: a random neighboring cell is chosen, and if that cell is empty, a new bear is placed in that cell
# (4) A bear can move to another cell:  it picks a random direction, and if the neighboring cell in that direction is unoccupied the bear moves there

class Bear(Animal):
    breed_interval = 12
    survive_without_food = 10

    def __init__(self, world, location):
        '''
        Uses instances from Animal and also adds a counter and days without fish instance.
        '''
        Animal.__init__(self, world, location)
        self.days_without_food = 0
        self._counter = 0

    def __repr__(self):
        '''
        Returns the bear symbol.
        '''
        return "\U0001F43B"

    def live(self):
        '''
        Checks to see if there is any fish in its neighboring cells and will move around.  If the bear goes
        without food for 10 time steps without food it will be removed.  After 8 time steps the bear will
        breed and another bear will be placed at random in the simulation.
        '''
        live_list = [(-1, 1), (0, 1), (1, 1), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]
        adjacent_fish = 0
        food_list = []
        for z in live_list:
            newx = self._location[0] + z[0]
            newy = self._location[1] + z[1]
            if (newx >= 0 and newx < self._world._rows and newy >= 0 and newy < self._world._columns):
                if (0 <= self._location[0] < self._world._rows) and (0 <= self._location[1] < self._world._columns):
                    if (not self._world.empty_location((newx, newy))) and isinstance(self._world.fetch((newx, newy)), Fish):
                        adjacent_fish += 1
                        food_list.append(self._world.fetch((newx, newy)))
        if len(food_list) == 0:
            self.days_without_food += 1
        if len(food_list) >= 1:
            f = random.choice(food_list)
            self._world.remove(f, f._location)
        else:
            self._counter += 1
            if self._counter >= Bear.breed_interval:
                z = random.choice(live_list)
                nx = self._location[0] + z[0]
                ny = self._location[1] + z[1]
                new_location = (nx, ny)
                if self._world._table[new_location] == None:
                    self._world.add(self, new_location)
        if self.days_without_food == self.survive_without_food:
            self._world.remove(self, self._location)

bw3 = World(5,5)
b3 = Bear(bw3, (2,2))
Fish(bw3, (1,1))
Fish(bw3, (3,3))
b3.live()

print(len(bw3.biota()))
print(bw3.biota())

bw1 = World(5,5)
b1 = Bear(bw1, (1,1))
assert len(bw1.biota()) == 1
assert b1.location() == (1,1)

bw2 = World(5,5)
Bear.breed_interval = 1
b2 = Bear(bw2, (2,2))
b2.live()
assert len(bw2.biota()) == 2
Bear.breed_interval = 8

bw3 = World(5,5)
b3 = Bear(bw3, (2,2))
Fish(bw3, (1,1))
Fish(bw3, (3,3))
b3.live()
assert len(bw3.biota()) == 2

bw4 = World(5,5)
Bear.survive_without_food = 1
b4 = Bear(bw4, (2,2))
b4.live()
assert len(bw4.biota()) == 0
Bear.survive_without_food = 10

bw5 = World(5,5)
b5 = Bear(bw5, (2,2))
b5.move()
r, c = b5.location()
assert (r,c) != (2,2)
assert abs(r-2) <= 1 and abs(c-2) <= 1

def wbf(nrows, ncols, nbears, nfish):
    '''
    Checks to see if the amount of fish location is less than the number of fish and bears together.  returns a world
    object with a certain amount of rows and columns with the number of Bears and Fish at random locations.
    '''
    w = World(nrows, ncols)
    animal_loc_list = set()
    bear_loc_list = []
    fish_loc_list = []

    while len(animal_loc_list) < (nbears + nfish):
        animal_loc_list.add((random.randint(0, nrows - 1), random.randint(0, ncols - 1)))

    for x in range(nbears):
        bear_loc_list.append(animal_loc_list.pop())

    fish_loc_list = list(animal_loc_list)

    for c in bear_loc_list:
        Bear(w, (c[0], c[1]))

    for d in fish_loc_list:
        Fish(w, (d[0], d[1]))

    return w

w = wbf(10,10,3,12)
for i in range(3):
    print(w)

w = wbf(10,10,3,12)

dct = { Bear: 0, Fish: 0 }
for x in w.biota():
    dct[x.__class__] += 1

assert dct[Bear] == 3
assert dct[Fish] == 12

def step_system(world):
    for x in world.biota():
        x.live()
    for x in world.biota():
        x.move()

#if IPython:
 #   logging = True
  #  w = wbf(10,10,3,12)
   # for i in range(3):
    #    print(w)
     #   step_system(w)
