from base import BEA, Meta, NIPA
from pprint import pprint

bea = BEA()
pprint(bea.api_dataset_meta_data.show_dataset_tables())