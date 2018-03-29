class Node:
	def __init__(self, name, in_edge=None):
		self.name = name
		self.in_edges = []
		self.cpd = None

		if in_edge:
			self.add_in_edge(in_edge)

	def get_name(self):
		return self.name

	def get_in_edges(self):
		return self.in_edges

	def search_edge(self, edge):
		return edge in self.in_edges

	def add_in_edge(self, in_edge):
		self.in_edges.append(in_edge) 

	def set_cpd(self, cpd):
		self.cpd = cpd

	def get_cpd(self):
		return self.cpd

	def __str__(self):
		return self.name + ' has in_nodes: ' + str(self.in_edges)

class DAG:
	def __init__(self):
		self.node_list = {}

	def add_node(self, name, edge=None):
		if name not in self.node_list.keys():
			self.node_list[name] = Node(name)

		if edge not in self.node_list.keys():
			self.node_list[edge] = Node(edge, name)
		elif edge in self.node_list.keys() and \
			not self.node_list[edge].search_edge(name):
			self.node_list[edge].add_in_edge(name)

	def is_top_node(self, name):
		return not len(self.node_list[name].get_in_edges()) # check if has parents

	def __contains__(self, name):
		return name in self.node_list.keys()

	def get_nodes(self):
		return self.node_list

	def get_node_names(self):
		return self.node_list.keys()

	def print_graph(self):
		for node in self.node_list.keys():
			print('Node ' + node + ' has parents ' 
				+ str(self.node_list[node].get_in_edges()))

		print('\nCPDs: ')
		for node in self.node_list.keys():
			print(self.node_list[node].get_cpd())

	def set_cpds(self, args):
		for cpd in args:
			#print(cpd)
			assert len(cpd.get_query_vars()) == 1
			for var in cpd.get_query_vars():
				assert var in self.node_list.keys()
			for evidence in cpd.get_evidence():
				assert evidence in self.node_list.keys()

			self.node_list[cpd.get_query_vars()[0]].set_cpd(cpd)

