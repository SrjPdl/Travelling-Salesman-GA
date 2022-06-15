import pickle
import os
import csv
from urllib.request import urlopen
import codecs
import numpy as np
import matplotlib.pyplot as plt

class TSP:
    '''
    Encapsulation of Traveling Salesman(TSP) Problem.
    '''
    def __init__(self, tsp_name: str):
        '''
        Initialize TSP problem according to the name.
        param:
            tsp_name: str, name of the TSP problem defined in http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/
        '''
        self.name = tsp_name
        self.coordinates = []
        self.distance_matrix = []
        self.size = 0
        self.__load_data()
        
    def __load_data(self):
        try:
            with open(os.path.join('data', self.name + '-coord.pkl'), 'rb') as f1, open(os.path.join('data', self.name + '-dist.pkl'), 'rb') as f2:
                self.coordinates = pickle.load(f1)
                self.distance_matrix = pickle.load(f2)
                self.size = len(self.coordinates)
        except:
            pass
    
        if not len(self.coordinates) or not len(self.distance_matrix):
            self.__init_data()
            
    def __init_data(self):
        '''
        Reads TSP data from http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/ according to the name, initilizes distance matrix and serializes coordinates and distances into files.
        '''
        self.coordinates = []
        url = 'http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/' + self.name + '.tsp'

        with urlopen(url) as response:
            body = codecs.iterdecode(response, 'utf-8')
            reader = csv.reader(body, delimiter=' ', skipinitialspace=True)

            for line in reader:
                if line[0] in ('DISPLAY_DATA_SECTION', 'NODE_COORD_SECTION'):
                    break

            for line in reader:
                if line[0] == 'EOF':
                    break
                self.coordinates.append(np.array(line[1:], dtype = "float32"))

            self.size = len(self.coordinates)

            self.distance_matrix = np.zeros((self.size, self.size))

            for i in range(self.size):
                for j in range(self.size):
                    dist = np.sqrt((self.coordinates[i][0] - self.coordinates[j][0]) ** 2 + (self.coordinates[i][1] - self.coordinates[j][1]) ** 2)

                    dist = np.linalg.norm(self.coordinates[i]- self.coordinates[j])
                    self.distance_matrix[i][j] = dist
                    self.distance_matrix[j][i] = dist
            
            if not os.path.exists('data'):
                os.makedirs('data')
            with open(os.path.join('data', self.name + '-coord.pkl'), 'wb') as f1, open(os.path.join('data', self.name + '-dist.pkl'), 'wb') as f2:
                pickle.dump(self.coordinates, f1)
                pickle.dump(self.distance_matrix, f2)
        

    def plot_tsp(self, path: list):
        '''
        Plot TSP problem.
        '''
        plt.scatter(*zip(*self.coordinates), marker='o', c='b')

        coords = [self.coordinates[i] for i in path]
        coords.append(coords[0])
        plt.plot(*zip(*coords), 'g')
        return plt
    
    def get_distance(self, path: list):
        '''
        Calculates distance of the path.
        '''
        distance = 0
        for i in range(len(path) - 1):
            distance += self.distance_matrix[path[i]][path[i + 1]]

        distance += self.distance_matrix[path[-1]][path[0]]
        return distance

    def __len__(self):
        return self.size