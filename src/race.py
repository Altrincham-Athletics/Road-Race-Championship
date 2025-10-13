from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from warnings import warn

import numpy as np

from src.athlete import Athlete
from src.race_entry import RaceEntry
from src.utils import time_str_to_secs

MAX_PTS = 25

@dataclass
class Race:
    name:str
    race_path:Path
    race_date:date
    distance:float
    is_5k:bool
    is_marathon:bool
    athletes:list[RaceEntry] = field(default_factory=list)
    

    def __post_init__(self):
        pass

    def assign_scores(self):
        athletes_m_by_time = sorted([a for a in self.athletes if a.male], key=lambda r:r.time)
        athletes_f_by_time = sorted([a for a in self.athletes if not a.male], key=lambda r:r.time)
        athletes_by_age_pct = sorted(self.athletes, key=lambda r:r.age_pct, reverse=True)

        for athletes in [athletes_m_by_time, athletes_f_by_time]:
            for rank, athlete in enumerate(athletes):
                score = max(MAX_PTS - rank, 0)
                athlete.time_score = score

        for rank, athlete in enumerate(athletes_by_age_pct):
            score = max(MAX_PTS - rank, 0)
            athlete.age_pct_score = score


    def load_race(self, athletes:dict[str,Athlete]):
        race_athletes = np.loadtxt(self.race_path, delimiter=',', dtype=str).reshape((-1,2))
        self.athletes = []
        for name, race_time in race_athletes:
            try:
                athlete = athletes[name]
            except KeyError:
                warn_str = f'{name} not matched, check athlete list.'
                warn(warn_str)
                continue

            race_entry = RaceEntry(
                race_name=self.name,
                athlete=name,
                race_date=self.race_date, 
                time=time_str_to_secs(race_time), 
                distance=self.distance,
                male=athlete.male, 
                is_5k=self.is_5k, 
                is_marathon=self.is_marathon
            )
            
            athlete.add_race(race_entry)
            self.athletes.append(race_entry)

    @property
    def summary_page(self)->Path:
        races_dir = Path() / 'docs' / 'races'
        race_name = self.name.replace(' ', '-')
        return races_dir / f'{race_name.lower()}_summary.html'