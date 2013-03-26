'''Program to calculate possible positions of Mr. X in the game Scotland Yard.
'''

import networkx as nx
from collections import deque

# Prepare an empty graph with all stations
with open('nodes.txt') as nodefile:
    city = nx.Graph()
    for (node, line) in enumerate(nodefile):
        if line.rstrip('\r\n'):
            (x, y) = map(int, line.split())
            city.add_node(node+1, {'x':x, 'y':y})

# Provide the dictionary to use with networkx's draw methods
pos = dict()
for (node, position) in city.node.items():
    pos[node] = (position['x'], position['y'])

gs = {
    'taxi': 'taxi.txt',
    'bus': 'bus.txt',
    'subway': 'subway.txt'
    }

def graph_from_adj_file(graph_filename):
    '''Return the graph constructed from the edgelist in the given file.
    The file should contain lines with a startnode followed by a number of end
    nodes that are reachable from that start node.
    '''
    with open(graph_filename) as graphfile:
        graph = city.copy()
        for line in graphfile:
            splitted = line.split()
            if len(splitted) > 1:
                startnode = int(splitted[0])
                for end in splitted[1:]:
                    graph.add_edge(startnode, int(end))
    return graph

for (transport_method, graph_filename) in gs.items():
    gs[transport_method] = graph_from_adj_file(graph_filename)

# The police can travel by taxi, bus and subway.
gs['police'] = nx.compose_all(list(gs.values()))
# Mr. X has the ability to use the ferry.
gs['black'] = nx.compose(gs['police'], graph_from_adj_file('ferry.txt'))

def hop(nodes, ticket):
    '''Given a node considered to be a possible starting position (or a list
    of such) and a ticket, return the list of all stations at which the player
    could be after that move.

    ticket should be 'taxi', 'bus', 'subway' or 'black'.
    '''
    return sorted(set(map( lambda x: x[1], gs[ticket].edges(nodes))))

def trace(startnode, ticket_list):
    '''Given a node considered to be a possible starting position (or a list
    of such) and a list of tickets, return the list of all stations at which
    the player could be after all moves.

    ticket_list should consist of tickets 'taxi', 'bus', 'subway' or 'black'.
    '''
    nodes = startnode
    ticket_list = deque(ticket_list)
    while ticket_list:
        nodes = hop(nodes, ticket_list.popleft())
    return sorted(nodes)

if __name__ == '__main__':
    import sys
    startnode = int(sys.argv[1])
    ticket_list = sys.argv[2:]
    print('Possible positions for Mr. X:')
    print(', '.join(map(str, trace(startnode, ticket_list))))
