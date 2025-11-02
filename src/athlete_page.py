from copy import copy
from pathlib import Path
from typing import Collection

from src.athlete import Athlete
from src.race import Race
from src.race_entry import RaceEntry

import src.html_pages as hp
from src.utils import date_to_str, secs_to_time_str

class AthletePage:

    @staticmethod
    def print_athlete_page(
        athlete:Athlete,
        all_athletes:dict[str,Athlete],
        all_races:dict[str,Race],
        combined_5k_page:Path,
        combined_marathon_page:Path):
        
        
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
        
        def print_race_headers(is_club:bool, file_id):
            caption = "* denotes race contributes to athlete's total score"
            headers = ['Race', 'Date', 'Time', 'Age %']
            if is_club:
                headers += ['Time score', 'Age % score', 'Race score']
            hp.html_start_table(headers, file_id, caption=caption)

        def print_race_summary(race_entry:RaceEntry, file_id):
            race = all_races[race_entry.race_name]
            counter = '*' if race_entry in athlete.counting_races else ''
            col_values = [
                hp.html_link(race_entry.race_name+counter, Path('..')/race.summary_page),
                date_to_str(race_entry.race_date),
                secs_to_time_str(race_entry.time),
                f'{race_entry.age_pct:3.2f}',         
            ]
            if race_entry.is_club:
                col_values += [
                    race_entry.time_score,
                race_entry.age_pct_score,
                race_entry.total_score
                ]
            hp.html_table_row(col_values, file_id)

        def print_combined_race_summary(race_entry:RaceEntry, title:str, link:Path, file_id):
            
            counter = '*' if race_entry in athlete.counting_races else ''
            col_values = [
                hp.html_link(title+counter, Path('..')/link),
                date_to_str(race_entry.race_date),
                secs_to_time_str(race_entry.time),
                f'{race_entry.age_pct:3.2f}',
                race_entry.time_score,
                race_entry.age_pct_score,
                race_entry.total_score
            ]
            hp.html_table_row(col_values, file_id)
            
        
        def print_race_list(is_club_table:bool, races:list[RaceEntry], file_id):
            n_races = len(races)
            if is_club_table:
                n_races += bool(athlete.best_5k.race_name) + bool(athlete.best_marathon.race_name)

            if n_races:    
                print_race_headers(is_club_table, file_id)
                for race in races:
                    print_race_summary(race, file_id)

                if is_club_table:
                    if athlete.best_5k.race_name:
                        print_combined_race_summary(athlete.best_5k, 'Best 5k', combined_5k_page, file_id)
                    if athlete.best_marathon.race_name:
                        print_combined_race_summary(athlete.best_marathon, 'Marathon', combined_marathon_page, file_id)

                    totals_cols = [
                        '<b>Totals</>',
                    '',
                    '',
                    '',
                    athlete.time_score,
                    athlete.age_pct_score,
                    athlete.total_score
                    ]
                    hp.html_table_row(totals_cols, file_id)

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
            print_race_list(True, athlete.club_races, file_id)

            hp.html_h('5k races', 2, file=file_id)
            if athlete._5k_races:
                hp.html_p(
                    '5k races are not scored individually. '
                    'Instead, your fastest time contributes to the ' +
                    hp.html_link('best 5k leaderboard', Path('..')/combined_5k_page) +
                    ', which is then scored as if it were '
                    'a single race.', file_id
                    )
            print_race_list(False, athlete._5k_races, file_id)

            hp.html_h('Marathons', 2, file=file_id)
            if athlete.marathons:
                hp.html_p(
                    'Marathons are not scored individually. '
                    'Instead, your fastest time contributes to the ' +
                    hp.html_link('best marathon leaderboard', Path('..')/combined_marathon_page) +
                    ', which is then scored as if it were '
                    'a single race.', file_id
                    )
            print_race_list(False, athlete.marathons, file_id)
            hp.html_p(hp.html_link('<br><br>Home', Path('../index.html')), file=file_id)
            hp.html_footer(file_id, '')
