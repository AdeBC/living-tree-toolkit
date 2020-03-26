from ete3 import NCBITaxa


class LineageTracker(object):

	# tested
	def __init__(self, ids):
		# self.names = names
		self.ncbi = NCBITaxa()
		self.main_ranks = ['superkingdom', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
		self.taxa_ids = ids                                # how to get valid ids
		self.lineages_ids = self.get_multi_lineage_ids()
		self.lineages = [self.get_names_from_taxids(i) for i in self.lineages_ids]
		self.paths_sp = self.lineages_ids_to_paths_sp(self.lineages_ids)

	def get_single_lineage_ids(self, id_):
		"""
		get lineage ids of a species id
		:param id_: species id
		:return: lineage ids
		"""
		lineages = self.ncbi.get_lineage(id_)
		ranks = self.ncbi.get_rank(lineages)
		lineages = list(filter(lambda x: ranks[x] in self.main_ranks, lineages))
		return lineages

	def get_multi_lineage_ids(self):
		"""
		get lineage ids of species ids
		:param ids: species ids
		:return: lineage ids
		"""
		lineage_ids = list(map(self.get_single_lineage_ids, self.taxa_ids))
		return lineage_ids

	def get_ranks_from_ids(self, id_list):
		"""
		get ranks
		:param name_list: name list
		:return: ranks
		"""
		name2rank = self.ncbi.get_rank(id_list)
		return [name2rank[name] for name in id_list]

	def get_names_from_taxids(self, id_list):
		"""
		get names
		:param id_list:
		:return:
		"""
		names = self.ncbi.get_taxid_translator(id_list)
		return [names[id] for id in id_list]

	def get_ids_from_names(self, names):
		"""
		get valid NCBI taxonomy ids
		:param names: names
		:return: ids
		"""
		ids = self.ncbi.get_name_translator(names)
		return [ids[name][-1] for name in names]

	def lineage_ids_to_path_sp(self, lineage_ids):
		"""

		:param lineage_ids:
		:return:
		"""
		ranks = self.get_ranks_from_ids(lineage_ids)
		names = self.get_names_from_taxids(lineage_ids)
		heads = {rank: 'sk' if rank == 'superkingdom' else rank[0:1] for rank in self.main_ranks}
		tails = {rank: names[ranks.index(rank)] if rank in ranks else '' for rank in self.main_ranks}
		path_sp = ['{}__{}'.format(heads[rank], tails[rank]) for rank in self.main_ranks]
		while path_sp[-1].endswith('__'):
			path_sp.remove(path_sp[-1])
		return path_sp

	def lineages_ids_to_paths_sp(self, lineages_ids):
		paths_sp = [self.lineage_ids_to_path_sp(ids) for ids in lineages_ids]
		return paths_sp


'''
def get_lineages(taxa_id: int):
	main_ranks = ['superkingdom', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
	l = ncbi.get_lineage(taxa_id)
	rank = ncbi.get_rank(l)
	lineages = [id for id in l if rank[id] in main_ranks]
	print([ncbi.get_rank([i]) for i in lineages])
	return lineages
'''
