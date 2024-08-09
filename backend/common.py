from datetime import datetime

# Initialize the event names dictionary
# Initialize the event names dictionary
event_names = {
    "01": "50 m NAGE LIBRE DAMES",
    "51": "50 m NAGE LIBRE MESSIEURS",
    "02": "100 m NAGE LIBRE DAMES",
    "52": "100 m NAGE LIBRE MESSIEURS",
    "03": "200 m NAGE LIBRE DAMES",
    "53": "200 m NAGE LIBRE MESSIEURS",
    "04": "400 m NAGE LIBRE DAMES",
    "54": "400 m NAGE LIBRE MESSIEURS",
    "05": "800 m NAGE LIBRE DAMES",
    "55": "800 m NAGE LIBRE MESSIEURS",
    "06": "1500 m NAGE LIBRE DAMES",
    "56": "1500 m NAGE LIBRE MESSIEURS",
    "43": "4 x 100 m NAGE LIBRE DAMES",
    "93": "4 x 100 m NAGE LIBRE MESSIEURS", 
    "44": "4 x 200 m NAGE LIBRE DAMES",
    "94": "4 x 200 m NAGE LIBRE MESSIEURS",
    "11": "50 m DOS DAMES",
    "61": "50 m DOS MESSIEURS",
    "12": "100 m DOS DAMES",
    "62": "100 m DOS MESSIEURS",
    "13": "200 m DOS DAMES",
    "63": "200 m DOS MESSIEURS",
    "21": "50 m BRASSE DAMES",
    "71": "50 m BRASSE MESSIEURS",
    "22": "100 m BRASSE DAMES",
    "72": "100 m BRASSE MESSIEURS",
    "23": "200 m BRASSE DAMES",
    "73": "200 m BRASSE MESSIEURS",
    "31": "50 m PAPILLON DAMES",
    "81": "50 m PAPILLON MESSIEURS",
    "32": "100 m PAPILLON DAMES",
    "82": "100 m PAPILLON MESSIEURS",
    "33": "200 m PAPILLON DAMES",
    "83": "200 m PAPILLON MESSIEURS",
    "41": "200 m 4 NAGES DAMES",
    "91": "200 m 4 NAGES MESSIEURS",
    "42": "400 m 4 NAGES DAMES",
    "92": "400 m 4 NAGES MESSIEURS",
    "46": "4 x 100 m 4 NAGES DAMES", 
    "96": "4 x 100 m 4 NAGES MESSIEURS",
    "47": "4 x 50 m NAGE LIBRES DAMES",
    "97": "4 x 50 m NAGE LIBRES MESSIEURS",
    "48": "4 x 50 m 4 NAGES DAMES",
    "98": "4 x 50 m 4 NAGES MESSIEURS",
    "37": "4 x 50 m 4 NAGES Mixte",
    "87": "4 x 50 NAGE LIBRES Mixte"
}

# Initialize the event minimas dictionary
event_minimas = {
    "01": {  # 50 NL
        "Poussin": "0:45.08",
        "Benjamin": "0:43.49",
        "Minime": "0:34.89",
        "Cadet": "0:33.25",
        "18+": "0:30.71"
    },
    "51": {  # 50 NL
        "Poussin": "0:42.32",
        "Benjamin": "0:38.23",
        "Minime": "0:30.82",
        "Cadet": "0:29.01",
        "18+": "0:26.34"
    },
    "02": {  # 100 NL
        "Poussin": "1:37.40",
        "Benjamin": "1:30.89",
        "Minime": "1:13.42",
        "Cadet": "1:11.01",
        "18+": "1:06.45"
    },
    "52": {  # 100 NL
        "Poussin": "1:29.56",
        "Benjamin": "1:22.11",
        "Minime": "1:07.03",
        "Cadet": "1:02.56",
        "18+": "0:58.06"
    },
    "03": {  # 200 NL
        
        "Benjamin": "2:50.00",
        "Minime": "2:39.84",
        "Cadet": "2:34.46",
        "18+": "2:23.26"
    },
    "53": {  # 200 NL
        "Benjamin": "3:01.87",
        "Minime": "2:21.02",
        "Cadet": "2:14.46",
        "18+": "2:07.34"
    },
    "04": {  # 400 NL
        "Poussin": "7:05.23",
        "Benjamin": "6:43.43",
        
        "Minime": "5:39.94",
        "Cadet": "5:22.98",
        "18+": "5:00.18"
    },
    "54": {  # 400 NL
        "Poussin": "6:31.50",
        "Benjamin": "6:14.53",
        "Minime": "5:01.29",
        "Cadet": "4:46.20",
        "18+": "4:30.50"
    },
    "05": {  # 800 NL
        "Benjamin": "13:40.33",
        "Minime": "11:25.38",
        "Cadet": "10:54.71",
        "18+": "10:15.64"
    },
    "55": {  # 800 NL
        "Benjamin": "12:46.93",
        "Minime": "10:30.86",
        "Cadet": "9:58.40",
        "18+": "9:21.00"
    },
    "06": {  # 1500 NL
        "Minime": "21:54.58",
        "Cadet": "21:00.30",
        "18+": "19:50.30"
    },
    "56": {  # 1500 NL
        "Minime": "20:45.85",
        "Cadet": "18:47.64",
        "18+": "17:45.61"
    },
    "11": {  # 50 Dos
        "Poussin": "0:52.09",
        "Benjamin": "0:50.07",
        "Minime": "0:42.78",
        "Cadet": "0:38.13",
        "18+": "0:35.95"
    },
    "61": {  # 50 Dos
        "Poussin": "0:48.87",
        "Benjamin": "0:46.01",
        "Minime": "0:37.38",
        "Cadet": "0:33.06",
        "18+": "0:30.61"
        
    },
    "12": {  # 100 Dos
        "Poussin": "1:50.23",
        "Benjamin": "1:44.61",
        "Minime": "1:27.72",
        "Cadet": "1:21.73",
        "18+": "1:16.30"
    },
    "62": {  # 100 Dos
        "Poussin": "1:45.52",
        "Benjamin": "1:36.97",
        "Minime": "1:19.60",
        "Cadet": "1:13.11",
        "18+": "1:06.38"
    },
    "13": {  # 200 Dos
        "Benjamin": "3:37.58",
        "Minime": "3:02.55",
        "Cadet": "2:50.30",
        "18+": "2:42.40"
    },
    "63": {  # 200 Dos
        "Benjamin": "3:23.81",
        "Minime": "2:46.02",
        "Cadet": "2:35.84",
        "18+": "2:24.53"
    },
    "21": {  # 50 Brasse
        "Poussin": "0:59.10",
        "Benjamin": "0:56.09",
        "Minime": "0:44.49",
        "Cadet": "0:41.20",
        "18+": "0:38.68"
    },
    "71": {  # 50 Brasse
        "Poussin": "0:54.43",
        "Benjamin": "0:50.20",
        "Minime": "0:40.43",
        "Cadet": "0:36.96",
        "18+": "0:33.73"
        
    },
    "22": {  # 100 Brasse
        "Poussin": "2:01.07",
        "Benjamin": "1:57.76",
        "Minime": "1:36.23",
        "Cadet": "1:34.19",
        "18+": "1:25.04"
        
    },
    "72": {  # 100 Brasse
        "Poussin": "1:57.41",
        "Benjamin": "1:46.31",
        "Minime": "1:27.39",
        "Cadet": "1:19.90",
        "18+": "1:14.47"
    },
    "23": {  # 200 Brasse
        "Benjamin": "4:05.35",
        "Minime": "3:25.55",
        "Cadet": "3:20.58",
        "18+": "3:02.57"
    },
    "73": {  # 200 Brasse
        "Benjamin": "3:42.42",
        "Minime": "3:06.04",
        "Cadet": "2:50.45",
        "18+": "2:40.01"
        
    },
    "31": {  # 50 Papillon
        "Poussin": "0:52.28",
        "Benjamin": "0:50.08",
        "Minime": "0:38.14",
        "Cadet": "0:36.94",
        "18+": "0:34.17"
    },
    "81": {  # 50 Papillon
        "Poussin": "0:47.25",
        "Benjamin": "0:46.10",
        "Minime": "0:32.88",
        "Cadet": "0:30.45",
        "18+": "0:28.25"
        
    },
    "32": {  # 100 Papillon
        "Poussin": "1:59.33",
        "Benjamin": "1:45.93",
        "Minime": "1:25.74",
        "Cadet": "1:20.22",
        "18+": "1:14.11"
    },
    "82": {  # 100 Papillon
        "Poussin": "1:44.49",
        "Benjamin": "1:38.21",
        "Minime": "1:15.37",
        "Cadet": "1:07.40",
        "18+": "1:04.75"
    },
    "33": {  # 200 Papillon
        "Benjamin": "3:45.00",
        "Minime": "3:10.76",
        "Cadet": "2:52.54",
        "18+": "2:42.65"
    },
    "83": {  # 200 Papillon
        "Benjamin": "3:26.00",
        "Minime": "2:48.25",
        "Cadet": "2:28.70",
        "18+": "2:22.18"
    },
    "41": {  # 200 4 Nages
        "Poussin": "3:54.03",
        "Benjamin": "3:30.45",
        "Minime": "3:00.71",
        "Cadet": "2:53.09",
        "18+": "2:42.50"
    },
    "91": {  # 200 4 Nages
        "Poussin": "3:39.95",
        "Benjamin": "3:17.86",
        "Minime": "2:43.44",
        "Cadet": "2:33.34",
        "18+": "2:25.57"
        
    },
    "42": {  # 400 4 Nages
        
        "Minime": "6:29.77",
        "Cadet": "5:59.18",
        "18+": "5:42.86"
    },
    "92": {  # 400 4 Nages
        "Minime": "5:37.25",
        "Cadet": "5:27.13",
        "18+": "5:10.61"
    },
    "47": {  # 4 x 50 m NAGE LIBRES DAMES
        "Poussin": "3:12.32",
        "Benjamin": "2:54.08"
    },
    "97": {  # 4 x 50 m NAGE LIBRES DAMES
        "Benjamin": "2:54.08"
    },
    "48": {  # 4 x 50 m 4 NAGES DAMES
        "Poussin": "3:36.61",
    },
    "98": {  # 4 x 50 m 4 NAGES DAMES
        "Benjamin": "3:18.88"
    },
    "43": {  # 4 x 100 m NAGE LIBRE DAMES
        
        "Minime": "4:53.68",
        "Cadet": "4:44.04",
        "18+": "4:25.80"
    },
    "46": {  # 4 x 100 m 4 NAGES DAMES
        
        "Minime": "5:43.11",
        "Cadet": "5:27.15",
        "18+": "5:01.90"
    },
    "93": {  # 4 x 100 m NAGE LIBRE MESSIEURS
        "Minime": "4:28.12",
        "Cadet": "4:10.24",
        "18+": "3:52.24"
    },
    "96": {  # 4 x 100 m 4 NAGES MESSIEURS
        "Minime": "5:09.39",
        "Cadet": "4:42.97",
        "18+": "4:21.94"
    },
    "44": {  # 4 x 200 m NAGE LIBRE DAMES
        
        "Minime": "10:29.36",
        "Cadet": "10:17.84",
        "18+": "9:33.04"
    },
    "94": {  # 4 x 200 m NAGE LIBRE MESSIEURS
        "Minime": "9:24.08",
        "Cadet": "8:57.84",
        "18+": "8:29.36"
    }
}


# Function to categorize swimmers by year of birth
def categorize_swimmer(year_of_birth, championnat):
    year_to_date = datetime.now().year
    if year_of_birth != 'Naissance' :
        year_of_birth = int(year_of_birth)
        if "TC" in championnat:
            return "18+"
        if "2023" in championnat:
            year_to_date -= 1
        if year_to_date - year_of_birth in [10, 11]:
            return "Poussin"
        elif year_to_date - year_of_birth in [12, 13]:
            return "Benjamin"
        elif year_to_date - year_of_birth in [14, 15]:
            return "Minime"
        elif year_to_date - year_of_birth in [16, 17]:
            return "Cadet"
        else:
            return "18+"

def check_ranking(category, rank, notCounted,event):
    if "x" in event_names[event] and category == "Poussin":
        return rank <= 8
    if category == "Poussin":
        return rank <= 32 + notCounted
    elif category == "Benjamin":
        return rank <=24 + notCounted
    elif category == "Minime":
        return rank <= 16 + notCounted
    elif category == "Cadet" or category == "18+":
        return rank <= 8 + notCounted
    else:
        return False


# Function to compare swimmer times to minimas
def time_to_seconds(time_str):
    try:
        if ':' in time_str:
            minutes, rest = time_str.split(':')
            seconds, milliseconds = rest.split('.')
            total_seconds = int(minutes) * 60 + int(seconds) + int(milliseconds) / 100
        else:
            seconds, milliseconds = time_str.split('.')
            total_seconds = int(seconds) + int(milliseconds) / 100
        return total_seconds
    except ValueError:
        # print(f"Invalid time format: {time_str}",)
        return 999999

def compare_times(swimmer_time, minima_time):
    swimmer_seconds = time_to_seconds(swimmer_time)
    minima_seconds = time_to_seconds(minima_time)
    
    if swimmer_seconds is None or minima_seconds is None:
        return False
    
    return swimmer_seconds <= minima_seconds
