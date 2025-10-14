from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np

from src.athlete import Athlete
from src.athlete_page import AthletePage
from src.index_page import IndexPage
from src.race import Race
from src.race_page import RacePage
from src.race_entry import MARATHON_KM
from src.utils import date_from_str, distance_in_kms

@dataclass
class RaceProcessor:
    athlete_list_path:Path
    race_list_path:Path
    athletes:dict[str,Athlete] = None #type: ignore
    races:dict[str,Race] = None #type: ignore
    combined_5k:Race = None #type: ignore
    combined_marathon:Race = None #type: ignore

    def __post_init__(self):
        pass

    def load_athletes(self):
        athlete_data = np.loadtxt(self.athlete_list_path, delimiter=',', dtype=str)
        self.athletes = {}
        for first_name, last_name, gender, dob in athlete_data:
            name= f'{first_name} {last_name}'
            self.athletes[name] = Athlete(
                name=name,
                dob=date_from_str(dob),
                male=gender.lower()=='male'
            )

    def load_races(self):

        race_details = np.loadtxt(self.race_list_path, delimiter=',', dtype=str, skiprows=1)

        self.races = {}
        for name, distance, race_date_str, is_5k_str, is_marathon_str, filepath in race_details:
            
            is_5k = bool(int(is_5k_str))
            is_marathon = bool(int(is_marathon_str))
            race_date = date_from_str(race_date_str)
            race = Race(
                name=name,
                race_date=race_date, 
                race_path=Path(filepath), 
                distance=distance_in_kms(distance), 
                is_5k=is_5k, 
                is_marathon=is_marathon)
            if race.in_past:
                race.load_race(self.athletes)
                if not is_5k and not is_marathon:
                    race.assign_scores()

            self.races[name] = race
            
        
    def make_combined_5k(self):
        athletes = [athlete.best_5k for athlete in self.athletes.values() if athlete.best_5k is not None]
        self.combined_5k = Race(
            name='Combined 5k leaderboard', 
            race_date=date.today(), 
            race_path=None, #type: ignore
            distance=5.0,
            is_5k=True, 
            is_marathon=False, 
            athletes=athletes)
        self.combined_5k.assign_scores()

    def make_combined_marathon(self):
        athletes = [athlete.best_marathon for athlete in self.athletes.values() if athlete.best_marathon is not None]
        self.combined_marathon = Race(
            name='Combined marathon leaderboard', 
            race_date=date.today(), 
            race_path=None, #type: ignore
            distance=MARATHON_KM,
            is_5k=False, 
            is_marathon=True, 
            athletes=athletes)
        self.combined_marathon.assign_scores()

    def update_athlete_scores(self):
        for athlete in self.athletes.values():
            athlete.update_scores_lists()

    def print_tables(self):
        for athlete in self.athletes.values():
            if athlete.total_score:                
                AthletePage.print_athlete_page(
                    athlete, self.athletes, self.races,
                    self.combined_5k.summary_page, self.combined_marathon.summary_page)

        for race in self.races.values():
            RacePage.print_race_page(race, self.athletes)

        RacePage.print_combined_race_page(self.combined_5k, self.athletes, self.races)

        RacePage.print_combined_race_page(self.combined_marathon, self.athletes, self.races)

        IndexPage.print_index_page(
            Path() / 'docs' / 'index.html', self.athletes, self.races.values(), self.combined_5k, self.combined_marathon
        )
        

    def process_races(self):

        self.load_athletes()
        self.load_races()
        self.make_combined_5k()
        self.make_combined_marathon()
        self.update_athlete_scores()
        self.print_tables()