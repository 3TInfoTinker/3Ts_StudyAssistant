"""
3Ta Tutor - AI Study Assistant Agent
Helps students learn from their textbooks
"""

from .agent import Tutor, root_agent

# For ADK compatibility
ROOT_AGENT = root_agent

__all__ = ['Tutor', 'root_agent', 'ROOT_AGENT']
__version__ = '1.0.0'