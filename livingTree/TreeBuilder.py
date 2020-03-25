from .LineageTracker import LineageTracker
from .SuperTree import SuperTree
from .TaxaRetriever import TaxaRetriever


class TreeBuilder(object):

	def __init__(self, taxa_name):
		"""
		generate taxonomy tree using NCBI taxonomy database
		:param taxa_name: the root of subtree
		"""
		self.taxa_name = taxa_name
		self.retriever = TaxaRetriever(taxa_name)
		self.taxa_ids = list(self.retriever.taxas)
		tracker = LineageTracker(['Homo', 'Mammalia'])
		self.taxa_names = tracker.get_names_from_taxids(self.taxa_ids)
		self.tracker = LineageTracker(self.taxa_names)
		self.paths = self.tracker.lineages
		self.tree = SuperTree()
		self.tree.create_node(identifier='root')

	def build(self):
		self.tree.from_paths(self.paths)
