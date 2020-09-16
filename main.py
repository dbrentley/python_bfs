import json
import sys


class Node:
    label = None
    neighbors = []
    parent = None
    visited = False
    is_actor = False

    def __init__(self, label):
        self.label = label
        self.neighbors = []
        self.parent = None
        self.visited = False
        self.is_actor = False

    def add_neighbor(self, n):
        self.neighbors.append(n)
        # both directions
        n.neighbors.append(self)


class Graph:
    graph = {}

    def add_node(self, n):
        self.graph[n.label] = n

    def get_node(self, label):
        return self.graph[label] if label in self.graph.keys() else None

    def search(self, start, end):
        queue = []
        print(f'Searching for {end} beginning with {start}')

        # add the 'start' node to the queue
        starting_node = self.graph.get(start)

        if starting_node is None:
            print(f'Could not find start node {start}')
            sys.exit(-1)

        starting_node.visited = True
        queue.append(starting_node)

        # begin BFS search
        while queue:
            current_node = queue.pop(0)
            if current_node.label == end:
                break

            for neighbor in current_node.neighbors:
                if not neighbor.visited:
                    neighbor.visited = True
                    neighbor.parent = current_node
                    queue.append(neighbor)
        # end BFS search

        # print the path leading to 'end' node
        end_node = self.graph.get(end)
        path = [end_node]
        next_node = end_node.parent
        while next_node:
            if next_node.parent:
                path.append(next_node)
            next_node = next_node.parent

        count = 0
        total_nodes = len(path)
        for node in reversed(path):
            print(f'{node.label}', end='')
            if count < total_nodes - 1:
                print(' > ', end='')
            count += 1


def main():
    graph = Graph()

    # load the data
    with open('kevin_bacon.json') as f:
        data = json.load(f)

    # create nodes for the movies
    for movie in data['movies']:
        movie_node = Node(movie['title'])
        # add movie node to graph
        graph.add_node(movie_node)

        # create nodes for the actors
        for actor in movie['cast']:
            # get existing actor node
            actor_node = graph.get_node(actor)
            if actor_node is None:
                # create new actor node if it doesn't exist
                actor_node = Node(actor)
                actor_node.is_actor = True
            # add actor node to graph
            graph.add_node(actor_node)
            # set the actor node as a neighbor (edge) of the movie node
            movie_node.add_neighbor(actor_node)

    graph.search('Tim Progosh', 'Kevin Bacon')


if __name__ == '__main__':
    main()
