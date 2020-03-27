# from [[name, name......]] to [[name, name;name, ....]]


class IDConverter(object):

	def __init__(self, paths_sp):
		self.paths_sp = paths_sp
		self.ids_paths_with_path_info = self.convert_paths_from_paths_sp(self.paths_sp)

	def convert_path_from_path_sp(self, path_sp, sep=';'):
		# tested, use path
		"""
		convert ids path (string) to ids path (list) for building and updating the tree
		:param path_sp: string type eg. 'Root;K_Bacteria;...'
		:param sep: character(s) that separates the ids in path
		:return: converted ids
		"""
		ids = path_sp.split(sep)
		tail = ids[-1].split('__')[-1]
		ids = list(map(lambda x: x + tail if x[-2:] == '__' else x, ids))
		ids = [sep.join(ids[0:i]) for i in range(1, len(ids) + 1)]
		self.nid = ids
		return ids

	def convert_paths_from_paths_sp(self, paths_sp, sep=';'):
		return [self.convert_path_from_path_sp(i, sep=sep) for i in paths_sp]






