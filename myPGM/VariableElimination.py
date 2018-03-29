class VariableElimination:
	def __init__(self, model):
		self.model = model

	def compute_joint_cpd(self, DAG, hidden_vars):
		node_list = DAG.get_nodes()
		cpd_list = {}
		for node_name in DAG.get_node_names():
			cpd_list[node_name] = node_list[node_name].get_cpd()

			if DAG.is_top_node(node_name) and node_name in hidden_vars.keys():
				hidden_vars[node_name] += 1

			in_edges = node_list[node_name].get_in_edges()
			for edge in in_edges:
				if edge in hidden_vars.keys():
					hidden_vars[edge] += 1
		
		joint_cpd = None			
		for i in range(len(hidden_vars.keys())):
			# choose var with least number of factors
			ith_min_var = min(hidden_vars, key=hidden_vars.get)

			product = None
			product_name = ''
			for cpd in list(cpd_list):
				if ith_min_var in cpd_list[cpd].get_evidence() or \
					ith_min_var in cpd_list[cpd].get_query_vars():
					if product:
						product = product.multiplyCPD(cpd_list[cpd], ith_min_var)
					else:
						product = cpd_list[cpd]
					product_name += cpd
					cpd_list.pop(cpd, None)

			marginal_var = product.marginalizeCPD(ith_min_var)
			if marginal_var:
				cpd_list[product_name] = marginal_var
			hidden_vars.pop(ith_min_var, None)

		return cpd_list
 		# 	for cpd in cpd_list.keys():
 		# 		if joint_cpd:
 		# 			joint_cpd = joint_cpd.multiplyCPD(cpd_list[cpd], )
 		# else:
 		# 	joint_cpd = cpd_list[cpd_list.keys()[0]]
 		# return marginal_var

	def query(self, variables, evidence = {}):
		node_list = self.model.graph.get_nodes()

		hidden_vars = {}
		for node_name in node_list.keys():
			if node_name not in evidence.keys() and node_name not in variables:
				hidden_vars[node_name] = 0

		joint_cpd_list = self.compute_joint_cpd(self.model.graph, hidden_vars)
		
		if len(joint_cpd_list.keys()) > 1:
			for cpd in list(joint_cpd_list): #joint_cpd_list.keys() raises error complaining dict change size during iter
				if cpd in evidence or cpd in variables:
					joint_cpd_list.pop(cpd)
		
		assert(len(joint_cpd_list.keys()) == 1)
		#joint_cpd_list
		print(joint_cpd_list[list(joint_cpd_list)[0]])