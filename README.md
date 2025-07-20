# final-audition-matching
Final program for matching dancers to pieces during auditions

Because this code is run only after all auditions have concluded for the day, the csv files are the result of combining the makeup, 10am, and 1pm session data

## Relevant files:

    ** Names of .csv files subject to change based on vibes lol
        They're run as args to ./audition_program.py anyway, so their actual name doesn't matter, just use what makes sense to keep straight

    piece_assignments
        Folder containing outputted .txt files with dancers' piece assignments. WILL BE OVERWRITTEN each time audition_program.py is run, so be aware. 
        I always move the previous semester's results to "old" before running new stuff just in case.

    choreog_prefs.csv
        Result of manually entering choreographers' rankings at the very end of dancer auditions
        Column format: 
            ID,Name,Total,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32
            --> ID is the standardized piece name used across all spreadsheets (e.g. "A - Alex & Alisa (Beginner)")
            --> Name is abbreviated, readable shorthand for piece name (e.g. "Alex & Alisa")
            --> Total is the number of dancers they want to be in their piece, self included (e.g. 12 if they want 12 dancers total in the end)
            --> the rest of the columns are the ranked audition numbers of the dancers they want, including alternates
                Dancers [1] thru [Total] are ranked, with 1 being first choice definite, and Total being final choice definite. 
                Dancers [Total+1] thru [however many columns there are] are unranked alternates
                The number of these columns are arbitrary per semester, sized to fit the max number of definites+alternates that a choreographer gave
                Empty columns in the alternates don't make a difference


    prefs.csv 
        Each dancer's ranked piece choices
            Accumulated from makeup auditions, 10am auditions, and 1pm auditions
        Column format:
            Timestamp,Email,Audition Number,First Name,Last Name,Number of Pieces,,,,,,,,,,,,,,,,,,,
            --> Timestamp doesn't matter (auto-generated from Google Forms) but can be helpful in identifying duplicate entries
            --> Email is only useful when you have 2+ people with the same name (we had 3 grace tangs once lollll)
            --> Audition number should be a unique identifier; assume that categories of numbers are unique to audition times
                e.g. Numbers 1-7 are Directors, 10 < number < 50 = choreographers, 200-299 are 10am, 300-399 are 1pm, 400+ are makeup auditions or video submissions (subject to change each semester tho)
            --> First, Last Name self-explanatory
            --> Number of Pieces is the maximum number of pieces that individual wants to be placed into. 
                Must be < 4 if not choreographer
                Number of preffed pieces must be >= this number
            --> the rest of the columns are ranked piece choices (e.g. first col entry is their #1 choice piece, etc)
                See choreographer_printouts documentation for more info on data validation
        Each dancer in this table must have a corresponding entry in the sign in table.


    sign_in.csv
        Gathers dancers' info when they first get to auditions
        This info is used to generate the final printouts with their name, pronounds, and email
        Column format:
            Timestamp,Audition Number,First Name,Last Name,Student Status,CMU Email,How many semesters have you been in DS?,Phone Number
            --> because one of our requirements for auditionees is to have an active student ID within allegheny county, we check sign-ins to make sure everyone's student status is either undergrad something, grad something, or phd something (can't be a rando adult)


    audition_program.py
        To run in terminal: python audition_program.py <choreog_prefs.csv> <prefs.csv> <sign_in.csv>


Bonus!
    dancers.csv
        Used this in Spring 2025 to create rosters for each piece. Not necessary for now.

    validate_data.py
        Started before Spring 2025 auditions to make sure data doesn't have errors before running. Couldn't get fully tested in time, so didn't use. Could be helpful in the future!