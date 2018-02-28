"""
Sample Similarity module.

This plot displays a dimensionality reduction of the data.

Samples are drawn near to similar samples in high dimensional space using a
machine learning algorithm: T-Stochastic Neighbours Embedding.

The plot can be colored by different sample metadata and the position of the
points can be adjust to reflect the analyses of different tools.
"""

# Re-export modules
from app.display_modules.sample_similarity.sample_similarity_module import (
    SampleSimilarityDisplayModule,
    SampleSimilarityResult,
    ToolDocument,
)
