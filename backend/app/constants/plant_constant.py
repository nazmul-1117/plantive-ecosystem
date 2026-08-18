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

class SunlightRequirement(StrEnum):
    FULL_SUN = "FULL_SUN"
    PARTIAL_SUN = "PARTIAL_SUN"
    PARTIAL_SHADE = "PARTIAL_SHADE"
    FULL_SHADE = "FULL_SHADE"