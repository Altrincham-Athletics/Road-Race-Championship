'''
0. Load list of athletes

1. Load list of races

2. For each race:
    - Load athletes and finishing times
    - Compute age-graded scores
    - Print race table

    3. For each athlete in race:
        - Add race entry
        
    
    
4. Update 5k or marathon table:
    - For each athlete in master list 


5. For each athlete in master list:
    - Update athlete score
    - Print athlete table
    - Add to overall table

6. Sort overall table

7. Print overall table
    

'''
from pathlib import Path
from src.race_processor import RaceProcessor

if __name__ == "__main__":
    rp = RaceProcessor(
        athlete_list_path = Path('athletes_list.csv'),
        race_list_path = Path('race_list.csv')
    )
    
    rp.process_races()
