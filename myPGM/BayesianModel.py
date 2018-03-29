from myPGM.DAG import DAG

class BayesianModel:
	
	def __init__(self, edge_list=None):
		self.graph = DAG()
		
		if edge_list:
			self.add_nodes(edge_list)

	def add_nodes(self, edge_list):
		for node_pair in edge_list:
			start_node = node_pair[0]
			end_node = node_pair[1]

			self.graph.add_node(start_node, end_node)

	def print_graph(self):
		self.graph.print_graph()

	def add_cpds(self, *args):
		self.graph.set_cpds(args)




				



            

