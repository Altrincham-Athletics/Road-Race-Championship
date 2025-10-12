from dataclasses import dataclass
from datetime import date

from agegrader import AgeGrader # type: ignore
import numpy as np
from src.utils import years_since

age_grader = AgeGrader()
MARATHON_KM = 42.195

@dataclass
class RaceEntry:
    race_name:str
    athlete:str
    race_date:date
    time:int
    distance:float
    male:bool
    is_5k:bool
    is_marathon:bool
    time_score:int = 0
    age_pct:float = np.nan
    age_pct_score:int = 0

    def __post_init__(self):
        if self.is_marathon:
            self.distance = MARATHON_KM

    @property
    def total_score(self)->int:
        return self.time_score + self.age_pct_score
    
    @property
    def is_nominated(self)->bool:
        return not self.is_5k and not self.is_marathon

    def compute_age_pct(self, dob:date):
        mf = 'm' if self.male else 'f'
        yrs = years_since(dob, self.race_date)
        self.age_pct = 100*age_grader.age_graded_performance_factor(
            yrs, mf, self.distance, self.time)