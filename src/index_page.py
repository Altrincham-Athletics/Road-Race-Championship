from pathlib import Path
from typing import Collection

from src.athlete import Athlete
from src.race import Race

import src.html_pages as hp
from src.utils import date_to_str

class IndexPage:

    @staticmethod
    def print_index_page(
        page:Path, all_athletes:dict[str,Athlete], races:Collection[Race], combined_5k:Race, combined_marathon:Race):
        with page.open('wt') as file_id:
            hp.html_header('ADAC Road Race Championship', 'css/styles.css', file_id)
            IndexPage.print_overall_table(all_athletes, file_id)
            IndexPage.print_race_summary(races, combined_5k, combined_marathon, file_id)
            hp.html_footer(file_id, 'scripts/filters.js')
    
    @staticmethod
    def print_race_summary(races:Collection[Race], combined_5k:Race, combined_marathon:Race, file_id=None):
        
        club_races = [race for race in races if not (race.is_5k or race.is_marathon)]
        club_race_list = []
        for race in club_races:
             if race.in_past:
                  club_race_list.append(f'{race.name}, {date_to_str(race.race_date)} - {hp.html_link("results", race.summary_page)}')
             else:
                  club_race_list.append(f'{race.name}, {date_to_str(race.race_date)} - {hp.html_link("entries", race.race_path)}')
        
        hp.html_h('Club Races', 2, file=file_id)
        hp.html_list(club_race_list, file=file_id)

        combined_races = [
            hp.html_link('5K leaderboard', combined_5k.summary_page),
            hp.html_link('Marathon leaderboard', combined_marathon.summary_page)
        ]
        hp.html_h('Combined Races', 2, file=file_id)
        hp.html_list(combined_races, file=file_id)

    @staticmethod
    def print_overall_table(all_athletes:dict[str,Athlete], file_id=None):
        
        def print_table_headers():
            hp.html_start_table(
                ['Athlete', 'Gender  ', 'Category  ', 'Num. races', 'Time score', 'Age % score', 'Total score'], file=file_id)

        def print_table_row(athlete:Athlete):
            gender = 'M' if athlete.male else 'F'
            n_races = len(athlete.counting_races)
            if n_races:
                hp.html_table_row(
                    [
                        hp.html_link(athlete.name, athlete.summary_page),
                        gender,
                        athlete.age_category,
                        n_races,
                        athlete.time_score,
                        athlete.age_pct_score,
                        athlete.total_score],
                    file=file_id)
        
        hp.html_h('ADAC Road Race Championship', 1, file=file_id)
        hp.html_h('Overall leaderboard', 2, file=file_id)
        print_table_headers()
        for athlete in sorted(all_athletes.values(), key=lambda a:a.total_score, reverse=True):
            print_table_row(athlete)
        hp.html_end_table(file=file_id)
