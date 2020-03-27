import pickle

import numpy as np
import pandas as pd
from treelib import Tree


class SuperTree(Tree):

	# tested
	def get_children_ids(self, nid):
		return self.is_branch(nid)

	def get_bfs_nodes(self, ):
		"""
		get BFS (breadth first search) node ids
		:return: ids
		"""
		# tested
		nodes = {}
		for i in range(self.depth() + 1):
			nodes[i] = []
			for node in self.expand_tree(mode=2):
				if self.level(node) == i:
					nodes[i].append(node)
		return nodes

	def get_bfs_data(self, ):
		"""
		get BFS (breadth first search) nodes data, in {layer_number: [values]} format
		:return: data: {layer_number: [values]}
		"""
		# tested
		nodes = self.get_bfs_nodes()
		return {i: list(map(lambda x: self[x].data, nodes[i])) for i in range(self.depth() + 1)}

	def get_dfs_nodes(self, ):
		"""
		get DFS (depth first search) node ids
		:return: ids
		"""
		# tested
		return self.paths_to_leaves()

	def get_dfs_data(self, ):
		"""
		get DFS (depth first search) nodes data, in [[val1, val2, ...], [val1, ...]] format
		the order of dfs node ids is preserved.
		:return: data: [[val1, val2, ...], [val1, ...]]
		"""
		# tested
		paths = self.get_dfs_nodes()  # list
		return [list(map(lambda x: self[x].data, path)) for path in paths]

	def init_nodes_data(self, value=0):
		"""
		initiate node values, you can specify the init_value of all nodes with :param value
		:return: None
		"""
		# tested
		for id in self.expand_tree(mode=1):
			self[id].data = value

	def from_paths(self, paths):
		"""
		construct a super_tree from node id paths
		:param paths: node id paths, eg [['country','china'],['country','usa','texas']]
		:return: None
		"""
		# tested
		# check duplicated son-fathur relationship
		for path in paths:
			current_node = self.root
			for nid in path:
				children_ids = self.get_children_ids(current_node)
				if nid not in children_ids: self.create_node(identifier=nid, parent=current_node)
				current_node = nid

	'''
	def from_child_father(self, ):
		return None
	'''

	def from_pickle(self, file: str):
		"""
		restore a super_tree from a pickle file
		:param file: path to pickle file
		:return: a super_tree obj.
		"""
		# tested
		with open(file, 'rb') as f:
			stree = pickle.load(f)
		return stree

	def path_to_node(self, node_id: str):
		"""
		get the path of any node in the tree
		:param node_id: node id
		:return: path
		"""
		# tested
		nid = node_id
		path_r = []
		while nid != 'root':
			path_r.append(nid)
			nid = self[nid].bpointer
		path_r.append('root')
		path_r.reverse()
		return path_r

	def fill_with(self, data: dict):
		"""
		update values for nodes on the tree
		fix multiple update issues. 2020/3/23
		:param data: data, eg.{id: value}
		:return: None
		"""
		# tested
		for nid, val in data.items():
			self[nid].data = val

	def update_value(self, ):
		"""
		starting from the leaf node to the root node, update the value of each node in the tree
		new_value = old_value + sum([child.data for child in children])
		:return: None
		"""
		# tested
		all_nodes = [nid for nid in self.expand_tree(mode=2)][::-1]
		for nid in all_nodes:
			d = sum([node.data for node in self.children(nid)])
			self[nid].data = self[nid].data + d

	def to_pickle(self, file: str):
		"""
		backup super_tree to a pickle file
		:param file: the path of pickle file
		:return: None
		"""
		# tested
		with open(file, 'wb') as f:
			pickle.dump(self, f)

	def get_matrix(self, dtype=np.float32):
		"""
		get matrix (like dfs data format but is a numpy n-dimensional array)
		:param dtype: data type
		:return: matrix
		"""
		# tested
		paths_to_leaves = self.paths_to_leaves()
		ncol = self.depth() + 1
		nrow = len(paths_to_leaves)
		Matrix = np.zeros(ncol * nrow, dtype=dtype).reshape(nrow, ncol)

		for row, path in enumerate(paths_to_leaves):
			for col, nid in enumerate(path):
				Matrix[row, col] = self[nid].data
		return Matrix

	def to_matrix_npy(self, file: str, dtype=np.float32):
		"""
		save matrix to npy file
		:param file: the path of npy file
		:param dtype: data type
		:return: None
		"""
		# tested
		matrix = self.get_matrix(dtype=dtype)
		np.save(file, matrix)

	def copy(self, ):
		"""
		get a deep copy of super_tree
		:return: new copy of super_tree
		"""
		# not working----test
		return pickle.loads(pickle.dumps(self, -1))

	# return super_tree(self.subtree(self.root), deep=True)

	def remove_levels(self, level: int):
		"""
		remove levels that are greater that :param level
		:param level: integer
		:return: None
		"""
		# tested
		nids = list(self.expand_tree(mode=1))[::-1]
		for nid in nids:
			if self.level(nid) >= level:
				self.remove_node(nid)  # check

	def save_paths_to_csv(self, file: str, fill_na=True):
		"""
		save id paths of super_tree to a csv file
		:param file: csv file path
		:param fill_na: if True, fill na with ''
		:return: None
		"""
		# tested
		paths = self.paths_to_leaves()
		df = pd.DataFrame(paths)
		if fill_na:
			df.fillna('')
		df.to_csv(file, sep=',')
