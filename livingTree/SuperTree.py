import pickle
import warnings
import numpy as np
import pandas as pd
from copy import copy
from treelib import Tree
from functools import reduce


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
		return self.get_paths_to_leaves()

	def get_paths_to_leaves(self, ):
		"""

		:return:
		"""
		res = []
		for leaf in self.leaves():
			res.append([nid for nid in self.rsearch(leaf.identifier)][::-1])
		return res

	def get_dfs_data(self, dfs_nodes=None):
		"""
		get DFS (depth first search) nodes data, in [[val1, val2, ...], [val1, ...]] format
		the order of dfs node ids is preserved.
		:return: data: [[val1, val2, ...], [val1, ...]]
		"""
		# tested
		if not dfs_nodes:
			dfs_nodes = self.get_dfs_nodes()  # list
		return [list(map(lambda x: self[x].data, path)) for path in dfs_nodes]

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
				if nid not in children_ids:
					self.create_node(identifier=nid, parent=current_node)
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

	def get_path_to_node(self, node_id: str):
		"""
		get the path of any node in the tree
		:param node_id: node id
		:return: path
		"""
		# tested
		path = [nid for nid in self.rsearch(node_id)]
		path.reverse()
		return path

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

	def to_pickle(self, file: str):
		"""
		backup super_tree to a pickle file
		:param file: the path of pickle file
		:return: None
		"""
		# tested
		with open(file, 'wb') as f:
			pickle.dump(self, f)

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
		return copy(self)

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
		paths = self.get_paths_to_leaves()
		df = pd.DataFrame(paths)
		if fill_na:
			df.fillna('')
		df.to_csv(file, sep=',')

	def get_top_down_ids(self, max_level=-1):
		"""
		get node ids in top-down order, tested.
		:return: [id1, id2, ...]
		"""
		if max_level == -1:
			return [nid for nid in self.expand_tree(mode=self.WIDTH)]
		else:
			return [nid for nid in self.expand_tree(mode=self.WIDTH) if self.level(nid) <= max_level]

	def get_bottom_up_ids(self, ):
		"""
		get node ids in bottom-up order, tested.
		:return: [id1, id2, ...]
		"""
		top_down_ids = self.get_top_down_ids()
		ids = copy(top_down_ids)
		ids.reverse()
		return ids

	def get_ids_by_level(self, ):
		"""
		get node ids grouped by level, tested.
		:return: {1: [id1, ...], 2: [idn, ...], ...}
		"""
		levels = range(self.depth() + 1)
		ids = {level: [] for level in levels}
		for nid in self.expand_tree(mode=self.WIDTH):
			ids[self.level(nid)].append(nid)
		return ids

	def get_paths_to_level(self, level=-1, ids_by_level=None, include_inner_leaves=True):
		"""
		get paths to specific level of the tree, you can specify the ids_by_level :param to \
		speed up this calculation, tested
		:param include_inner_leaves: paths to inner leaves are included with this set to be True
		:param ids_by_level: ids_by_level dict calculated by `get_ids_by_level` method
		:param level: level
		:return: [path1, path2, path3, ...], each path: [id1, id2, id3, ...]
		"""
		if not ids_by_level:
			msg = '''Calculating ids_by_level could be time-consuming, \
			you can specify the `ids_by_level` parameter to speed up. 
			e.g. `ids=tree.get_ids_by_level(); tree.get_paths_to_level(level=1; ids_by_level=ids)`.'''.replace('\t', '')
			warnings.warn(msg, SyntaxWarning)
			ids_by_level = self.get_ids_by_level()
		if level == -1:
			return self.get_paths_to_leaves()
		elif include_inner_leaves:
			print('include_inner_leaves: yes')
			inner_leaves = [node.identifier for node in self.leaves() if self.level(node.identifier) < level]
			ids_use = ids_by_level[level] + inner_leaves
		else:
			print('include_inner_leaves: no')
			ids_use = ids_by_level[level]
		return [[nid_ for nid_ in self.rsearch(nid)][::-1] for nid in ids_use]

	def get_matrix(self, paths=None, ncol=None, dtype=np.float32):
		"""
		get matrix (like dfs data format but is a numpy n-dimensional array), tested
		:param ncol: number of columns of matrix
		:param paths: paths you want to generate matrix, will calculate itself (time-consuming) if absent \
		:param dtype: data type
		:return: matrix
		"""
		# tested
		if not paths:
			paths = self.get_paths_to_leaves()
		if not ncol:
			ncol = max([len(i) for i in paths])
		nrow = len(paths)
		Matrix = np.zeros(ncol * nrow, dtype=dtype).reshape(nrow, ncol)

		for row, path in enumerate(paths):
			for col, nid in enumerate(path):
				Matrix[row, col] = self[nid].data
		return Matrix

	def update_values(self, bottom_up_ids=None):
		"""
		starting from the leaf node to the root node, update the value of each node in the tree
		new_value = old_value + sum([child.data for child in children])
		:return: None
		"""
		# tested
		if not bottom_up_ids:
			msg = '''Calculating the bottom up ids could be very time-consuming, \
			you can specify the `bottom_up_ids` parameter to speed up. 
			e.g. `ids=tree.get_bottom_up_ids; tree.update_value(bottom_up_ids=ids)`.'''.replace('\t', '')
			warnings.warn(msg, SyntaxWarning)
			bottom_up_ids = self.get_bottom_up_ids()

		for nid in bottom_up_ids:
			d = sum([node.data for node in self.children(nid)])
			self[nid].data = self[nid].data + d

	"""
	get_bottom_up_ids()   tested
	get_top_down_ids()    tested
	update_values()       tested
	get_matrix()          tested
	get_ids_by_level()    tested
	get_paths_to_level()  tested
	"""

	# paths_to_leaves replacement
