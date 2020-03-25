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
		self.taxa_names = self.retriever.taxas
		self.tracker = LineageTracker(self.taxa_names)
		self.tree = SuperTree()
		self.paths = self.tracker.lineages

	def build(self):
		self.tree.from_paths(self.paths)
