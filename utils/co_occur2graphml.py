import networkx as nx

def convert_co_occur_to_graphml(input_file, threshold=0):
    """ Transform co-occurence format to graphml format for visualization """

    with open(input_file, 'r', encoding='utf-8') as fr:
        G = nx.Graph()
        for line in fr:
            field_line = line.strip().split('\t')
            node1, node2 = field_line[0].strip(), field_line[1].strip()
            edge_weight = int(field_line[2])

            if edge_weight > threshold:
                G.add_edge(node1, node2, weight=edge_weight)

        nx.write_graphml(G, input_file.replace('.txt', '.graphml'), encoding='utf-8')

if __name__ == '__main__':

    input_file = 'test.txt'
    threshold = 0

    convert_co_occur_to_graphml(input_file, threshold)