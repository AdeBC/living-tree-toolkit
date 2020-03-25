from ete3 import NCBITaxa


class TaxaRetriever(object):

	def __init__(self, category):
		self.ncbi = NCBITaxa()
		sps = self.ncbi.get_descendant_taxa(category, collapse_subspecies=True)
		ranks = self.ncbi.get_rank(sps)
		self.taxas = filter(lambda x: ranks[x] == 'species', sps)
