from base import BEA, Meta, NIPA
from pprint import pprint

bea = BEA()
pprint(bea.ni_underlying_detail.show_dataset_tables())