import time 
import matplotlib.pyplot as plt

class Node:
    def __init__(self, node_number, x, y):
        self.node_number = str(node_number)
        self.x = float(x)
        self.y = float(y)
        
    def __str__(self):
        return "Node " + self.node_number


class Graph:
    global city_name
    def __init__(self, node_list, algo_name : str = None, tour = []):
        self.node_list = node_list
        self.city_name = city_name
        self.algo_name = algo_name
        self.tour = tour 
        
    def draw(self):
        plt.figure(figsize = (14,7))
        plt.scatter([item.x for item in node_list], [item.y for item in self.node_list], color = 'blue')

        for n in range(dim):
            plt.annotate(str(n), xy=(self.node_list[n].x, self.node_list[n].y), xytext = (self.node_list[n].x-0.1, self.node_list[n].y+0.1), color = 'black')

        if len(self.tour) != 0:
            for n in range(len(self.tour)-1):
                point1 = [self.node_list[self.tour[n]].x,self.node_list[self.tour[n+1]].x]
                point2 = [self.node_list[self.tour[n]].y,self.node_list[self.tour[n+1]].y]
                plt.plot(point1, point2, color= 'red')

        plt.xlabel("X")
        plt.ylabel("Y")
        if self.algo_name is None: 
            plt.title("Graph for nodes in {0} data set".format(self.city_name))
        else:
            plt.title("Graph for nodes in {0} data set using the {1} algorithm".format(self.city_name, self.algo_name))
        return plt.show()


def total_distance(tour, distances):
    distance = 0
    for n in range(len(tour)-1):
        distance += distances[(tour[n],tour[n+1])]
    return distance 

def nearest_neighbor(node_list, distances, dim, starting_node=0):
    res = [starting_node]
    
    while len(res) < dim:
        i = res[-1]
        nn = {(i,j): distances[(i,j)] for j in range(dim) if j != i and j not in res}
        new_edge = min(nn.items(), key = lambda x: x[1])
        res.append(new_edge[0][1])
        
    res.append(starting_node)
    return res, total_distance(res, distances)

def algo_2opt(avail_tour, distances):
    
    
    for i in range(len(avail_tour) - 2):
        optimal_change = 0
        for j in range(i+2, len(avail_tour)-1):
            old_cost = distances[(avail_tour[i], avail_tour[i+1])] + distances[(avail_tour[j], avail_tour[j+1])]
            new_cost = distances[(avail_tour[i], avail_tour[j])] + distances[(avail_tour[i+1], avail_tour[j+1])]
            change = new_cost - old_cost
            
            if change < optimal_change: 
                optimal_change = change
                optimal_i, optimal_j = i, j
        
        #if we found an optimal swapped edges (just one optimal pair for each node i), then update the tour
        if optimal_change < 0:
            avail_tour[optimal_i+1:optimal_j+1] = avail_tour[optimal_i+1:optimal_j+1][::-1]
        
    return avail_tour, total_distance(avail_tour, distances)

if __name__ == "__main__":
    file_name = input("Enter the name of the data set you want to use: ")
    if file_name[-4:] != ".tsp":
        file_name += ".tsp"
        
    with open("data_set/" + file_name, 'r') as file:
        for line in file:
            if line.startswith("NAME"):
                city_name = line.strip().split()[-1]
            elif line.startswith("DIMENSION"):
                dim = int(line.strip().split()[-1])
            elif line.startswith("NODE_COORD"):
                # A list of node objects 
                node_list = []
                # A list contains tuples of edge 
                node_edges = [(i,j) for i in range(dim) for j in range(dim) if i!=j]
                for i in range(int(dim)):
                    node, x, y = next(file).strip().split()
                    node_list.append(Node(int(node)-1,x,y))

    basic_graph = Graph(node_list)
    basic_graph.draw()

    distances = {(i,j):((node_list[i].x-node_list[j].x)**2 + (node_list[i].y-node_list[j].y)**2)**0.5 for i,j in node_edges}

    #timer on, nearest_neighbor, timer off
    start_time = time.time() 
    tour_nn, tour_nn_distance = nearest_neighbor(node_list, distances, dim)
    finish_time = time.time()

    time_taken = finish_time - start_time

    #Make a graph of connected nodes
    tour_nn_graph = Graph(node_list, "Nearest-Neighbor", tour_nn)
    print("Nearest-Neighbor tour: {0}\nTotal tour distance: {1}\nTime complexity: O(n^2)\nActual time taken: {2}".format(tour_nn, tour_nn_distance, time_taken))
    tour_nn_graph.draw()

    tour_nn_clone = tour_nn[:]

    #timer on, 2-opt, timer off
    start_time = time.time() 
    tour_2opt, tour_2opt_distance = algo_2opt(tour_nn_clone, distances)
    finish_time = time.time()

    time_taken = finish_time - start_time

    #Make a graph of connected nodes
    tour_2opt_graph = Graph(node_list, "2-opt", tour_2opt)

    print("2-opt tour: {0}\nTotal tour distance: {1}\nTime complexity: O(n^2)\nActual time taken: {2}".format(tour_2opt, tour_2opt_distance, time_taken))
    tour_2opt_graph.draw()

