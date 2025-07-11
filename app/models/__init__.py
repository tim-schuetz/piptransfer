from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .machine_models import *
from .quality_models import *
from .leadtime_models import *
from .historicqualitymodels import *
