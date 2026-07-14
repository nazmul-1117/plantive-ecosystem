from enum import StrEnum

class ReminderType(StrEnum):
    WATER: str = "water"
    FERTILIZER: str = "fertilizer"
    PRUNE: str = "prune"
    REPOT: str = "repot"


class PlantHealth(StrEnum):
    HEALTHY: str = "healthy"
    WARNING: str = "warning"
    CRITICAL: str = "critical"
    DEAD: str = "dead"