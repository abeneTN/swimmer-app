from datetime import datetime
from bs4 import BeautifulSoup
from common import event_names, event_minimas, categorize_swimmer, compare_times, check_ranking


# Initialize the classement dictionary
classement = {
    "Championnat d'Hiver 2024 MCJS18+": {
        "Poussin": {
            # "Club A": 120,
            # "Club B": 110,
            # "Club C": 95
        },
        "Benjamin": {
            # "Club A": 130,
            # "Club B": 125,
            # "Club C": 100
        },
        "Minime": {
            # "Club A": 140,
            # "Club B": 135,
            # "Club C": 120
        },
        "Cadet": {
            # "Club A": 150,
            # "Club B": 145,
            # "Club C": 130
        },
        "18+": {
            # "Club A": 160,
            # "Club B": 155,
            # "Club C": 140
        }
    },
    "Championnat d'Été 2024 MCJS18+": {
        "Poussin": {
            # "Club A": 120,
            # "Club B": 110,
            # "Club C": 95
        },
        "Benjamin": {
            # "Club A": 130,
            # "Club B": 125,
            # "Club C": 100
        },
        "Minime": {
            # "Club A": 140,
            # "Club B": 135,
            # "Club C": 120
        },
        "Cadet": {
            # "Club A": 150,
            # "Club B": 145,
            # "Club C": 130
        },
        "18+": {
            # "Club A": 160,
            # "Club B": 155,
            # "Club C": 140
        },
        "TC": {
            # "Club A": 160,
            # "Club B": 155,
            # "Club C": 140
        }
    },
    "Championnat d'Été 2023 MCJS18+": {
        "Poussin": {
            # "Club A": 120,
            # "Club B": 110,
            # "Club C": 95
        },
        "Benjamin": {
            # "Club A": 130,
            # "Club B": 125,
            # "Club C": 100
        },
        "Minime": {
            # "Club A": 140,
            # "Club B": 135,
            # "Club C": 120
        },
        "Cadet": {
            # "Club A": 150,
            # "Club B": 145,
            # "Club C": 130
        },
        "18+": {
            # "Club A": 160,
            # "Club B": 155,
            # "Club C": 140
        }
    },
    "Championnat d'Hiver 2024 Benjamins": {
        "Benjamin": {
            # "Club A": 130,
            # "Club B": 125,
            # "Club C": 100
        }
    },
    "Championnat d'Été 2024 Benjamins": {
        "Benjamin": {
            # "Club A": 130,
            # "Club B": 125,
            # "Club C": 100
        }
    },
    "Championnat d'Hiver 2023 Benjamins": {
        "Poussin": {
            # "Club A": 130,
            # "Club B": 125,
            # "Club C": 100
        },
        "Benjamin": {
            # "Club A": 130,
            # "Club B": 125,
            # "Club C": 100
        }
    },
}

def process_html(files):
    current_event = None

    content = list(files)[0].read()
    soup = BeautifulSoup(content, 'html.parser')

    championnat = soup.title.string    

    classement[championnat] = {
        "Poussin": {},
        "Benjamin": {},
        "Minime": {},
        "Cadet": {},
        "18+": {}
    }

    # Initialize the events data dictionary
    events_data = {
        championnat: {
            event_code: {
                category: [] for category in classement[championnat].keys()
            } for event_code in event_names.keys()
        } for championnat in classement.keys()
    }
    pointsFound = 1
    for element in soup.find_all():
        # Get all the links with a name attribute and not the top link
        if element.name == 'a' and element.get('name') and element.get('name') != "top": 
            # Get the event code
            current_event = element.get('name')
            # Initialize the events_data dictionary for the current championship and event with empty lists for each category
            events_data[championnat][current_event] = {category: [] for category in classement.keys()} 
            notCounted = 0
            lastCategory = ""
        elif current_event and element.name == 'tr':  # Assuming the data is within table rows of the previously found a tag with an attribute name of theevent code
            columns = element.find_all('td')
            if columns[0].text.strip() == "Place":
                continue
            if len(columns) > 5:  # Adjust based on actual number of columns
                # print(current_event)
                if "x" not in event_names[current_event]:
                    name = columns[1].text.strip()
                    club = columns[4].text.strip()  
                    year_of_birth = columns[3].text.strip()  
                    time = columns[5].text.strip()  
                    nat = columns[2].text.strip()
                    category = categorize_swimmer(year_of_birth, championnat)
                    try:
                        place = int(columns[0].text.strip().rstrip('.'))
                    except ValueError:
                        place = 0
                    try:
                        points = int(columns[6].text.strip())
                    except ValueError:
                        points = 0 
                else:  # Relay events
                    if pointsFound == 1:
                        year_of_birth = columns[3].text.strip()
                        category = categorize_swimmer(year_of_birth,championnat)
                        try:
                            place = int(columns[0].text.strip().rstrip('.'))
                        except ValueError:
                            place = 0
                        name = columns[1].text.strip()
                        pointsFound += 1
                        continue
                    elif pointsFound <= 4:
                        name += "," + columns[1].text.strip()  
                        if pointsFound == 4:
                            club = columns[4].text.strip()
                            time = columns[5].text.strip()
                            try:
                                points = int(columns[6].text.strip())
                            except ValueError:
                                points = 0
                            pointsFound = 1
                        else :
                            pointsFound += 1
                            continue
                        
                pointsFound = 1
                
                swimmer_data = {
                    'Event': event_names.get(current_event, f"Event {current_event}"),
                    'Championnat' : championnat,
                    'Name': name.replace('\xa0', ' '),
                    'Place': place,
                    'Year of Birth': year_of_birth,
                    'Club': club,
                    'Time': time,
                    'Category': category,
                    'Points' : points,
                    'Nationality' : nat
                }

                events_data[championnat][current_event].setdefault(category, []).append(swimmer_data) 
                    
                minima = event_minimas.get(current_event, {}).get(category, "N/A")

                # Number of swimmers that does NOT count
                if (nat != 'TUN' and place in range(1, 9 + notCounted)) or (club == 'LP'):
                    lastCategory = category
                    notCounted += 1 
                    continue
                if lastCategory != category: 
                    notCounted = 0
                    
                if compare_times(time,minima) :
                    if check_ranking(category,place,notCounted,current_event):
                        if club in classement[championnat][category]:
                            if current_event in ["37","87","43","93","44","94","46","96","47","97","48","98"]:
                                points *= 2
                            classement[championnat][category][club] += points
                        else:
                            classement[championnat][category][club] = points

    sorted_classement = {
        championship: {
            category: dict(sorted(clubs.items(), key=lambda x: x[1], reverse=True)) for category, clubs in categories.items()}
            for championship, categories in classement.items()}
    
    for category, clubs in classement.items():
            if not clubs:
                continue
            print(f"Catégorie: {category}")
            for club, points in clubs.items():
                print(f"{club}: {points} points")
            print()
    return sorted_classement[championnat]
