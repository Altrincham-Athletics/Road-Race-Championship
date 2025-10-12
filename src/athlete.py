from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from src.race_entry import RaceEntry
from src.utils import years_since

TOTAL_RACES = 6

@dataclass
class Athlete:
    name:str
    dob:date
    male:bool
    races:list[RaceEntry] = field(default_factory=list)
    best_5k:RaceEntry = None # type: ignore
    best_marathon:RaceEntry = None # type: ignore
    counting_races:list[RaceEntry] = field(default_factory=list)

    def __post_init__(self):
        if self.best_5k is None:
            self.best_5k = RaceEntry(
                athlete=self.name,
                race_name='',
                race_date=date.today(),
                time=int(1e6),
                distance=5,
                male=self.male,
                is_5k=True,
                is_marathon=False,
                time_score=0,
                age_pct=0,
                age_pct_score=0)
            
        if self.best_marathon is None:
            self.best_marathon = RaceEntry(
                athlete=self.name,
                race_name='',
                race_date=date.today(),
                time=int(1e6),
                distance=0,
                male=self.male,
                is_5k=False,
                is_marathon=True,
                time_score=0,
                age_pct=0,
                age_pct_score=0)
        
    @property
    def summary_page(self)->Path:
        athletes_dir = Path() / 'docs' / 'athletes'
        athlete_name = self.name.replace(' ', '-')
        return athletes_dir / f'{athlete_name.lower()}_summary.html'

    @property
    def age_category(self):
        age = years_since(self.dob)
        if age < 17:
            return 'U17'
        elif age < 20:
            return 'U20'
        elif age < 35:
            return 'Senior'
        else:
            return f'V{5 * (age // 5)}'
            

    @property
    def nominated_races(self)->list[RaceEntry]:
        return [race for race in self.races if race.is_nominated]
    
    @property
    def _5k_races(self)->list[RaceEntry]:
        return [race for race in self.races if race.is_5k]
    
    @property
    def marathons(self)->list[RaceEntry]:
        return [race for race in self.races if race.is_marathon]
    
    @property
    def required_races(self):
        if self.best_5k.total_score > self.best_marathon.total_score:
            return self.best_5k, self.best_marathon
        else:
            return self.best_marathon, self.best_5k 

    def add_race(self, race:RaceEntry):

        if race.athlete != self.name:
            raise ValueError(f'Race name ({race.athlete}) does not match athlete name ({self.name})')
        
        race.compute_age_pct(self.dob)

        self.races.append(race)

        if race.is_5k and (self.best_5k is None or (race.time < self.best_5k.time)):
            self.best_5k = race

        if race.is_marathon and (self.best_marathon is None or (race.time < self.best_marathon.time)):
            self.best_marathon = race

    @property
    def time_score(self):
        return sum(race.time_score for race in self.counting_races)
    
    @property
    def age_pct_score(self):
        return sum(race.age_pct_score for race in self.counting_races)
    
    @property
    def total_score(self):
        return sum(race.total_score for race in self.counting_races)
    
    def update_scores_lists(self):
        races_by_score = sorted(self.nominated_races, key=lambda race:race.total_score, reverse=True)
        
        self.counting_races = [self.required_races[0]]
        for race in races_by_score[:TOTAL_RACES-1]:
            if race.total_score > self.required_races[1].total_score:
                self.counting_races.append(race)

        if len(self.counting_races) < TOTAL_RACES:
            self.counting_races.append(self.required_races[1])

        self.counting_races = [race for race in self.counting_races if race.race_name]