import numpy as np
import math
from collections import OrderedDict

class TabularCPD:
	def __init__(self, queries, values, evidence=[]):
		self.queries = queries
		self.evidence = evidence
		self.values = np.asarray(values)
		self.num_vars = len(queries) + len(evidence)
	
	def __str__(self):
		return 'Query variables: ' + ', '.join(self.queries) + '\n' \
			+ 'Evidences: ' + ', '.join(self.evidence) + '\n' \
			+ 'CPD: \n' + np.array2string(self.values)

	def get_query_vars(self):
		return self.queries

	def get_evidence(self):
		return self.evidence

	def multiply_helper(self, var, switch, product_values, joint_cpd_ind, joint_list, joint_index):
		cond_list = list(self.values.flatten())
		cond_var_index = len(self.queries + self.evidence) - (self.queries + self.evidence).index(var) - 1

		cond_index = 0				
		while cond_index < len(cond_list):
			if cond_index and cond_var_index == 0: #corner case; anything mod 1 is 0
				switch = not switch
			elif cond_index and cond_index%int(math.pow(2,cond_var_index)) == 0:
				switch = not switch

			if switch:
				product_values[joint_cpd_ind*len(cond_list)+cond_index] += cond_list[cond_index]*joint_list[joint_index] # sum of product

			cond_index += 1

	# def multiplyCPD(self, rhs, var):
	# 	new_vars = list(OrderedDict.fromkeys(self.queries + self.evidence + rhs.queries + rhs.evidence))
	# 	repeated_vars = list(set(self.queries+self.evidence).intersection(rhs.queries+rhs.evidence))

	# 	new_num_vars = len(new_vars)
	# 	new_num_rows = int(math.pow(2,new_num_vars))
	# 	product_values = np.zeros((new_num_rows,1))

	# 	for row in range(new_num_rows):

	def multiplyCPD(self, joint, var):
		#assert(len(joint.evidence) == 0)
		joint_var_index = len(joint.queries +joint.evidence) - (joint.queries + joint.evidence).index(var) - 1

		joint_list = list(joint.values.flatten())
		
		new_joint_vars = joint.queries + joint.evidence + self.queries + self.evidence
		new_joint_vars.remove(var)

		new_num_vars = len(new_joint_vars)
		num_joint_rows = int(math.pow(2,new_num_vars))
		product_values = np.zeros((num_joint_rows,1))		
		
		joint_index = 0
		joint_cpd_ind = 0
		incr_cnt = 0
		interval_cnt = 0
		while joint_index < len(joint_list):
			self.multiply_helper(var, 1, product_values, joint_cpd_ind, joint_list, joint_index)
			self.multiply_helper(var, 0, product_values, joint_cpd_ind, joint_list, 
							joint_index+int(math.pow(2,joint_var_index)))
			joint_cpd_ind += 1

			joint_index += 1
			incr_cnt += 1
			if incr_cnt == int(math.pow(2,joint_var_index)):
				interval_cnt += 1
				joint_index = int(math.pow(2,joint_var_index+1))*interval_cnt
				incr_cnt = 0

		product = TabularCPD(new_joint_vars, np.asarray(product_values))		
		return product
		
	def marginalizeCPD(self, var):
		if len(self.queries) == 1 and var in self.queries:
			return None
		
		assert(self.values.shape[1] == 1)
		joint_list = list(self.values.flatten())
		var_index = len(self.queries) - self.queries.index(var) - 1
		#var_index = self.queries.index(var)

		new_joint_vars = self.queries + self.evidence
		new_joint_vars.remove(var)
		new_num_vars = len(new_joint_vars)

		num_joint_rows = int(math.pow(2,new_num_vars))
		product_values = np.zeros((num_joint_rows,1))

		new_joint_index = 0
		joint_index = 0
		incr_cnt = 0
		interval_cnt = 0
		while joint_index < len(joint_list):		
			marginal_sum = joint_list[joint_index] + joint_list[joint_index+int(math.pow(2,var_index))]
			product_values[new_joint_index] = marginal_sum
			new_joint_index+=1
		
			joint_index += 1
			incr_cnt += 1
			if incr_cnt == int(math.pow(2,var_index)):
				interval_cnt += 1
				joint_index = int(math.pow(2,var_index+1))*interval_cnt
				incr_cnt = 0

		return TabularCPD(new_joint_vars, np.asarray(product_values))
