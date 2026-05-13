# Imports mínimos - evitar circular imports
try:
    from aether_os.agents.training_agent import TrainingAgent
except ImportError:
    pass

__all__ = ["TrainingAgent"]
