import pandas as pd


def checkChoreoRankings(file):
    pass

def checkDancerRankings(file):
    pieces = [chr(ord("A")+i) for i in range(16)if i!=8]
    headers = ["timestamp", "email","first_name","last_name","audition_id","pronouns","num_dances"] + pieces
    df = pd.read_csv(file)
    df.columns = headers
    if len(list(df.audition_id)) != len(set(df.audition_id)):
        print("erorr: multiple sign-ins for same number")
    for a_id in df.audition_id:
        if not isinstance(a_id,int):
            print(f"error: audition ID {a_id} is not an integer")
        if a_id<1:
            print(f"error: audition ID {a_id} is negative somehow")
    for lname in df.last_name:
        if not isinstance(lname,str) or lname.isspace():
            print(f"error: someone didn't enter a valid last name: {lname}")
    for fname in df.first_name:
        if not isinstance(fname,str) or fname.isspace():
            print(f"error: someone didn't enter a valid first name: {fname}")
    for email in df.email:
        if not isinstance(email,str) or email.isspace():
            print(f"error: invalid email: {email}")
    for pronouns in df.pronouns:
        if not isinstance(pronouns,str) or pronouns.isspace():
            print(f"error: pronouns invalid: {pronouns}")
    #TODO: check if dancer is choreographer to see if num_dances is valid
            #check if dancer is in tap piece to check if num_dances valid

    print("Dancer rankings look good!")


def checkSignIn(file):
    headers = ["timestamp", "audition_id", "last_name", "first_name", "class_year", "email", "num_semesters", "phone_number"]
    df = pd.read_csv(file)
    df.columns = headers
    if len(list(df.audition_id)) != len(set(df.audition_id)):
        print("erorr: multiple sign-ins for same number")
    for a_id in df.audition_id:
        if not isinstance(a_id,int):
            print(f"error: audition ID {a_id} is not an integer")
        if a_id<1:
            print(f"error: audition ID {a_id} is negative somehow")
    for lname in df.last_name:
        if not isinstance(lname,str) or lname.isspace():
            print(f"error: someone didn't enter a valid last name: {lname}")
    for fname in df.first_name:
        if not isinstance(fname,str) or fname.isspace():
            print(f"error: someone didn't enter a valid first name: {fname}")
    for email in df.email:
        if not isinstance(email,str) or email.isspace():
            print(f"error: invalid email: {email}")
    for phone in df.phone_number:
        if phone.isspace():
            print(f"error: phone number is empty")


    print("Sign In sheet looks good!")

def check_consistent_ids(sign_in, rankings):
    sign_in_headers = ["timestamp", "audition_id", "last_name", "first_name", "class_year", "email", "num_semesters", "phone_number"]
    sign_in_df = pd.read_csv(sign_in)
    sign_in_df.columns = sign_in_headers
    
    rankings_headers = ['time', 'email', 'first_name', 'last_name', 
							'audition_number', 'pronouns','num_pieces',"A","B","C","D","E","F","G","H","J","K","L","M","N","O","P"]
    rankings_df = pd.read_csv(rankings)
    rankings_df.columns = rankings_headers
    
    rank_numbers = rankings_df["audition_number"]
    sign_in_numbers = sign_in_df["audition_id"]
    print(rank_numbers,sign_in_numbers)


checkDancerRankings("dancer_prefs.csv")