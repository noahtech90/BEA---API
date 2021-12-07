from base import BEA, Meta, NIPA
from pprint import pprint

bea = BEA()
pprint(bea.meta.get_available_data_sets())