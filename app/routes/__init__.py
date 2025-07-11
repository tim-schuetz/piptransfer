from .machineendpoints import machines_bp
from .qualitydataendpoints import quality_bp
from .leadtimeendpoints import leadtime_bp

all_blueprints = [
    machines_bp,
    quality_bp,
    leadtime_bp
]


