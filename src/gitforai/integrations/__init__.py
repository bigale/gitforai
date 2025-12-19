"""
GitForAI Integrations Package

Provides integration wrappers for external tools:
- beads: Distributed Git-backed issue tracker
- beads_viewer: Graph-theoretic task intelligence via Robot Protocol
- unified: Combined intelligence from all three layers (bd + bv + gitforai)
"""

from .beads import BeadsClient, BeadsViewerClient, BeadsConfig
from .unified import UnifiedTaskIntelligence, UnifiedConfig

__all__ = [
    'BeadsClient',
    'BeadsViewerClient',
    'BeadsConfig',
    'UnifiedTaskIntelligence',
    'UnifiedConfig'
]
