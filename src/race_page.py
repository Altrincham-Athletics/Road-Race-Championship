from pathlib import Path

from src.athlete import Athlete
from src.race import Race
from src.race_entry import RaceEntry

import src.html_pages as hp
from src.utils import date_to_str, secs_to_time_str

class RacePage:

    @staticmethod
    def print_race_page(race:Race, all_athletes:dict[str,Athlete]):
        
        def print_race_headers(file_id):
            headers = ['Athlete', 'Gender', 'Category', 'Time', 'Age %']
            if not (race.is_5k or race.is_marathon):
                headers += ['Time score', 'Age % score', 'Total score']
            caption = "* denotes race contributes to athlete's total score"
            hp.html_start_table(
                headers, file=file_id, caption=caption)

        def print_race_summary(race:RaceEntry, file_id):
            gender = 'M' if race.male else 'F'
            athlete = all_athletes[race.athlete]
            counter = '*' if race in athlete.counting_races else ''
            cols = [
                    hp.html_link(race.athlete+counter, Path('..')/athlete.summary_page),
                    gender,
                    athlete.age_category,
                    secs_to_time_str(race.time),
                    f'{race.age_pct:3.2f}'
                ]
            
            if not (race.is_5k or race.is_marathon):
                cols += [
                    race.time_score, 
                    race.age_pct_score,
                    race.total_score
                ]

            hp.html_table_row(
                cols,
                file=file_id)
        
        def print_athlete_list(athletes:list[RaceEntry], file_id):            
            print_race_headers(file_id)
            for race in sorted(athletes, key=lambda r:r.time):
                print_race_summary(race, file_id)
            hp.html_end_table(file=file_id)

        with race.summary_page.open('wt') as file_id:
            hp.html_header(race.name, '../css/styles.css', file_id)
            hp.html_h(f'{race.name}, {date_to_str(race.race_date)}', 1, file=file_id)
            hp.html_list([f'Number of Altrincham runners: {len(race.athletes)}'], file=file_id)
            print_athlete_list(race.athletes, file_id)
            hp.html_list([hp.html_link('Home', Path('../index.html'))], file=file_id)
            hp.html_footer(file_id)

    @staticmethod
    def print_combined_race_page(race:Race, all_athletes:dict[str,Athlete]):
        
        def print_race_headers(file_id):
            hp.html_start_table(
                ['Athlete', 'Gender', 'Category', 'Race', 'Date', 'Time', 'Age %', 'Time score', 'Age % score', 'Total score'],
                file=file_id)

        def print_race_summary(race:RaceEntry, file_id):
            gender = 'M' if race.male else 'F'
            athlete = all_athletes[race.athlete]
            hp.html_table_row(
                [
                    hp.html_link(race.athlete, Path('..')/athlete.summary_page),
                    gender,
                    athlete.age_category,
                    race.race_name,
                    date_to_str(race.race_date),
                    secs_to_time_str(race.time), 
                    f'{race.age_pct:3.2f}',
                    race.time_score,
                    race.age_pct_score,
                    race.total_score
                ],
                file=file_id)
        
        def print_athlete_list(athletes:list[RaceEntry], file_id):
            
            print_race_headers(file_id)
            for race in sorted(athletes, key=lambda r:r.time):
                if race.race_name:
                    print_race_summary(race, file_id)
            hp.html_end_table(file=file_id)

        race_str = '5K' if race.is_5k else 'marathon'

        with race.summary_page.open('wt') as file_id:
            hp.html_header(f'Combined best {race_str}', '../css/styles.css', file_id)
            hp.html_h(f'Combined best {race_str}, June 2025 - May 2026', 1, file=file_id)
            print_athlete_list(race.athletes, file_id)
            hp.html_list([hp.html_link('Home', Path('../index.html'))], file=file_id)
            hp.html_footer(file_id)