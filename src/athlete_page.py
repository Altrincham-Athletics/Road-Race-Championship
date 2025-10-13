from pathlib import Path
from typing import Collection

from src.athlete import Athlete
from src.race import Race
from src.race_entry import RaceEntry

import src.html_pages as hp
from src.utils import date_to_str, secs_to_time_str

class AthletePage:

    @staticmethod
    def print_athlete_page(athlete:Athlete, all_athletes:dict[str,Athlete], all_races:dict[str,Race]):
        def scored_more(other_athlete:Athlete):
            return other_athlete.total_score > athlete.total_score
        
        def same_gender(other_athlete:Athlete):
            return athlete.male == other_athlete.male
        
        def same_category(other_athlete:Athlete):
            return athlete.age_category == other_athlete.age_category
        
        def rank_str(other_athletes:Collection[Athlete]):
            total = len(other_athletes)
            rank = sum(scored_more(a) for a in other_athletes)+1
            return f'{rank} out of {total}'
        
        def print_race_headers(file_id):
            hp.html_start_table(['Race', 'Date', 'Time', 'Age %', 'Time score', 'Age % score', 'Total score'], file_id)

        def print_race_summary(race_entry:RaceEntry, file_id):
            race = all_races[race_entry.race_name]
            col_values = [
                hp.html_link(race_entry.race_name, Path('..')/race.summary_page),
                date_to_str(race_entry.race_date),
                secs_to_time_str(race_entry.time),
                f'{race_entry.age_pct:3.2f}',
                race_entry.time_score,
                race_entry.age_pct_score,
                race_entry.total_score
            ]
            hp.html_table_row(col_values, file_id)
            
        
        def print_race_list(races:list[RaceEntry], file_id):
            if races:
                print_race_headers(file_id)
                for race in races:
                    print_race_summary(race, file_id)
                hp.html_end_table(file=file_id)
            else:
                print('None', file=file_id)

        gender = 'male' if athlete.male else 'female'
        matched_gender_athletes = [a for a in all_athletes.values() if same_gender(a)]
        matched_category_athletes = [a for a in matched_gender_athletes if same_category(a)]

        with athlete.summary_page.open('wt') as file_id:
            hp.html_header(athlete.name, '../css/styles.css', file_id)
            hp.html_h(f'{athlete.name}', 1, file=file_id)
            hp.html_list(
            [
            f'Category: {athlete.age_category} {gender}',
            f'Total score: {athlete.total_score}',
            f'Overall position: {rank_str(all_athletes.values())}',
            f'Gender position: {rank_str(matched_gender_athletes)}',
            f'Category position: {rank_str(matched_category_athletes)}'], file=file_id)

            hp.html_h('Club races', 2, file=file_id)
            print_race_list(athlete.club_races, file_id)

            hp.html_h('5k races', 2, file=file_id)
            print_race_list(athlete._5k_races, file_id)

            hp.html_h('Marathons', 2, file=file_id)
            print_race_list(athlete.marathons, file_id)
            hp.html_list([hp.html_link('Home', Path('../index.html'))], file=file_id)
            hp.html_footer(file_id)
