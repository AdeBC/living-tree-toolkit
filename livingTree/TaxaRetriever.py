from ete3 import NCBITaxa


class TaxaRetriever(object):

	# tested
	def __init__(self, category):
		self.ncbi = NCBITaxa()
		self.species = list(self.ncbi.get_descendant_taxa(category, collapse_subspecies=True))
		self.ranks = self.ncbi.get_rank(self.species)
		self.taxas = filter(lambda x: self.ranks[x] == 'species', self.species)
