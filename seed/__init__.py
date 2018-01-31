"""MetaGenScope seed data."""

from seed.abrf_2017 import (
    load_sample_similarity,
    load_taxon_abundance,
    load_reads_classified
)


sample_similarity = load_sample_similarity()
taxon_abundance = load_taxon_abundance()
reads_classified = load_reads_classified()
