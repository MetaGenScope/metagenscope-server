"""Factory for generating Kraken result models for testing."""

from random import randint

from app.tool_results.vfdb import VFDBToolResult


def simulate_gene():
    """Return one row."""
    gene_name = 'sample_vfdb_gene_{}'.format(randint(1, 100))
    rpk = randint(1, 1000) / 0.33333
    rpkm = randint(1, 1000) / 0.33333
    rpkmg = randint(1, 1000) / 0.33333
    return gene_name, {'rpk': rpk, 'rpkm': rpkm, 'rpkmg': rpkmg}


def create_values():
    """Create methyl values."""
    genes = [simulate_gene() for _ in range(randint(3, 10))]
    result = {
        'genes': {gene_name: row for gene_name, row in genes}

    }
    return result


def create_vfdb():
    """Create VFDBlToolResult with randomized field data."""
    packed_data = create_values()
    return VFDBToolResult(**packed_data)
