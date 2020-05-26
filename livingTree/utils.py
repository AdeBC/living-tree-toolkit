from .SuperTree import SuperTree
import pickle


def build_from_paths(paths):
	tree = SuperTree()
	tree.create_node(identifier='root')
	for path in paths:
		current_node = tree.root
		for nid in path:
			children_ids = tree.get_children_ids(current_node)
			if nid not in children_ids:
				tree.create_node(identifier=nid, parent=current_node)
			current_node = nid

	return tree


def restore_from_pkl(pkl_file):
	with open(pkl_file, 'rb') as f:
		tree = pickle.load(f)
	return tree
