# adac-club-championship
Code to automate the calculation and display of results in the Altrincham and District Athletics Club race championship

## Developer instructions

### Setting up an environment

The code so far is written in pure python and can be run in a simple python virtual environment.

1. Create and activate a virtual environment - the repository is set-up to ignore `venv` folders so I suggest doing this in the repository root

    ```
    python -m venv venv
    venv\Scripts\activate #for Windows, or as appropriate for nix systems
    ```

2. Install the external requirements

    > pip install -r requirements.txt

3. Clone the [age-grader repository](https://github.com/jbuckner/agegrader), then pip install it

    > pip install -e <path-to-local-clone-of-agegrader-repo>

Everything should now run.

### Package design

- `src` contains:

    - `race_processor.py` (class `RaceProcessor`): the top-level object that loads in all the data, processes the scores and write out the HTML pages
    - `athlete.py` (class `Athlete`): stores data for individual runners 
    - `race.py` (class `Race`): stores data for individual races
    - `race_entry.py` (class `RaceEntry`): stores the data for a single athlete in a given race
    - `index_page.py`(class `IndexPage`): generates the main output HMTL index
    - `athlete_page.py` (class `AthletePage`): generates the HTML output for each athlete's page
    - `race_page.py`(class `RacePage`): generates the HTML output for each race's page
    - `html_pages.py`: a module container helping functions for printing HTML to files
    - `utils.py`: other helper files for manipulating dates, race time strings *etc*

- `races` contains a set of CSV files, one per race, where each file lists the name and (chip where available) time of each Altrincham athlete that ran. These
are generally created in  descending time (ie finishing order) but this isn't actually a requirement. The format for each line should be:

    > first_name last_name,hh:mm:ss

    The `first_name last_name` must match an entry in the `athlete_list.csv` file (see below). Times must always finish `mm:ss` but can omit the hour or use a single digit hour.

    - `nifty` is there to store CSV files downloaded directly from nifty results pages (which at least half the club races use). A helper script `nifty_parser.py` can be used to
    filter these and output a race CSV file of just Altrincham athletes in the format above. The script has been cobbled together very quickly, but could be transformed into a more general
    scraper with time.

    - For non-nifty races, I have just been creating the CSV files manually (*eg* filtering results online by Altrincham, then copy-pasting and tidying the output into a CSV file)

- `race_list.csv` stores a list of all races to process. Each line should contain

    > name, distance, date, is_5k, is_marathon, filepath

    - name: the race name in human readable format (*eg* 'Mid-cheshire summer 5k')
    - distance: distance in either kms or miles, must be suffixed with `km` or `mi` (*eg* `10 km` or `10 mi`), The code works in kms, but will automatically convert miles
    - date: in format DD/MM/YYYY
    - is_5k/is_marathon: should be zero if the race is nominated club race, or 1 if the race is to be considered in the combined marathon or 5k leaderboards. Note I have deliberately set this not to be
    based on distance, as we may include some local 5k races as club races that won't be considered in the combined leaderboard
    - filepath: should either point to the race CSV file (for past races as described above) or a web-link to the race entry page for future races

- `athlete_list.csv`: this has been supplied by Jackie at the club. It is not checked into the repository and is in the `.gitignore` file as it contains a list of all
club members with the DOBs (which shouldn't shared publicly). Take a local copy of this (ask another dev for it) and store it in the repo root, but please do not share
without permission

- `process_race_list.py` is the main script to build all the output. This can run without arguments `python process_race_list.py` from the repo root. Because everything
runs so quickly, I have kept things simple and not tried to store any processed data. The script simply reloads and rebuilds all the HTML from scratch each time (in < 1 second)

- `docs` contains the output HTML. It must be in docs for the GitHub to automagic the pages onto the `github.io` server.

    - `index.html` the main page, displaying the overall leaderboard and list of races

    - `races` contains an output page for each race

    - `athletes` contains an output page for each runner

    - `css` contains a simple `styles.css` template the HTML pages have been hard-coded to use

### How the code works

- The `race_processor` loads `athlete_list.csv` to create an `Athlete` object for each runner

- The `race_processor` loads the `race_list.csv` to create a `Race` object for each race

- For races that have already been run, the processor loads the matching race CSV file. Each entry in the CSV file
creates a `RaceEntry` object, that stores the performance of a single `Athlete` in that race. A `Race` is thus a list
of `RaceEntry` objects for each athlete in the race, and likewise an `Athlete` stores a list of `RaceEntry` objects
for each race they've run. The `RaceEntry` objects are shared across the various container objects so updating the details
of a `RaceEntry` of a `Race` object will automatically update the `Athlete` object.

- Each `RaceEntry` computes the age-graded percentage for the performance, by using the athletes DOB, race time, race date and distance

- The `Race` objects then assign scores based on the time and age percentage score rankings. For club races, these are assigned as soon
as the race is loaded. For the 5k and marathons, the individual races are not scored. Instead, all the races need to be loaded, then each athlete returns their best 5k/marathon
to a combined `Race` object, before the scores can then be assigned in the same way as a standard club race.

- Once all races (including the combined 5k/marathon races) have scores assigned, the processor loops over each athlete to determine which their
counting races should be, based on the rules that your best 6 races count, but at least one of those needs to be a combined race. When the counting races
have been determined, the total score for each athlete can be determined

- Finally the processor can print out the output HTML pages

    - The index contains:
        - a table of all athletes, sorted by their total score, with each name being a link to the athlete page
        - the list of club races: for past races, a link to the race page, for future races, a link to the entry website

    - Each athlete page contains tables of their club, 5k and marathon races (with links to the race pages)

    - Each race page contains a table of athletes (with links to athletes pages). The combined 5k and marathon tables also show
    the race that counted for the athlete (with a link to it). Individual 5k or marathon race pages do not show the score columns
    as these look confusing for an individual race (because the score shown will either be 0, or based on the position in the
    combined table, not the race being viewed)

That's it. When you commit the updated HTML pages in `docs` and push to main on the GitHub origin, the new pages will automagically be deployed.

Things should just run. Things to watch out for:

- there's an annoying `numpy.loadtxt` warning I've not suppressed (add to the TODO)

- any athlete's in a race CSV that don't match an entry in the `athlete_list.csv` throw a warning. Often this is just a name mismatch (*eg* Andy vs Andrew) in the results
that can be manually corrected in the race CSV (TODO write a more robust check to guess a simple corrections). Others are where people have listed their club as us on entry forms, but not actually registered, so aren't on the official members list, so can be ignored as they're not technically eligible for the competition (unless the re-register).

### Contributing

Up to now, I've just committed directly to main while getting things set-up, but with multiple people potentially working on this now, I suggest we adopt a more formal
GitFlow approach where:

1. We create a new Issue on GitHub describing what we're working on

2. Create a branch off the issue page and work on this locally, making sure all the pages in `docs` work as intended locally

3. Create a PR from the issue branch to main on GitHub

4. Merge the PR, ideally with review from someone else

As we're not working on anything critical, it won't be the end of the world if we ever push to main and deploy non-functioning pages, but it would be nice to avoid this where possible
and having a code review always helps avoid this.

# More complex design plans

To be discussed...