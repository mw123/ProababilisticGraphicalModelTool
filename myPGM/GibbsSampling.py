import pandas as pd
import random
import math
from scipy.stats import rv_discrete
import numpy as np

class GibbsSampling:
	def __init__(self, model):
		self.model = model

	def compute_markov_blanket(self, node):
		graph = self.model.graph
		node_list = graph.get_nodes()
		blanket = None
		#print("fcn call "+node)
		for node_name in graph.get_node_names():
			#print("searching "+node_name)
			# child found
			if node_list[node_name].search_edge(node) or \
				(node_name == node and not graph.is_top_node(node_name)):
				if blanket:
					#print(blanket)
					#print(node_list[node_name].get_cpd())
					cpd = node_list[node_name].get_cpd()
					blanket = blanket.multiplyCPD(cpd, 
						list(
							set(blanket.get_query_vars()+blanket.get_evidence()).intersection(
								cpd.get_query_vars()+cpd.get_evidence())
							)[0])
				else:
					blanket = node_list[node_name].get_cpd()
				blanket.values = blanket.values.flatten()
		
		return blanket				

	def random_state(self):
		sample = {}
		for node in self.model.graph.get_node_names():
			sample[node] = [random.randint(0,1)]
		return sample

	def compute_cond_prob(self, node, blanket, samples):
		pos_index = 0
		neg_index = 0
		for var in blanket.get_query_vars():
			#print(var)
			if samples[var][-1] == 1 or var == node:
				var_index = len(blanket.queries + blanket.evidence) - (blanket.queries + blanket.evidence).index(var) - 1
				pos_index += int(math.pow(2,var_index))
		#print("cond")
		#print(blanket)
		return blanket.values[pos_index]

	def sample(self, start_state=None, size=1, query=[], evidence={}):
		graph = self.model.graph
		node_list = graph.get_nodes()

		if start_state:
			assert len(node_list)==len(start_state.keys()), "start state incomplete assignments"
			samples = {}
			for node in start_state.keys():
				samples[node] = [start_state[node]]
		else:
			samples = self.random_state()

		sample_i = 1
		burn_in = 200000
		for sample_i in range(size+burn_in):

			# init
			for node_name in graph.get_node_names():
				blanket = self.compute_markov_blanket(node_name)
				prob_pos = self.compute_cond_prob(node_name, blanket, samples)
				#print(prob_pos)
				if sample_i <= burn_in:
					samples[node_name][0] = np.random.choice([0,1], 1, p=[1-prob_pos,prob_pos])[0]#rv_discrete(([0,1],[prob_neg,prob_pos]))
				else:
					samples[node_name].append(np.random.choice([0,1],1,p=[1-prob_pos,prob_pos])[0])
					#print(samples[node_name])
				#print(samples[node_name][0])
				if evidence and node_name in evidence.keys():
					samples[node_name][-1] = evidence[node_name]

		if (query):
			df = pd.DataFrame(dict((k, v) for k, v in samples.items() if k in query))
		else:
			df = pd.DataFrame(samples)

		#for node_name in samples.keys():
		#	df[node_name] = samples[node_name]
		return df