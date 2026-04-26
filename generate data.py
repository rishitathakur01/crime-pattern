import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_crime_data(num_records=100):
    states = [
        "Himachal Pradesh", "Haryana", "Punjab", 
        "Jammu and Kashmir", "Uttarakhand", "Uttar Pradesh"
    ]
    
    crime_types = [
        "Theft", "Burglary", "Assault", "Cybercrime", 
        "Drug Trafficking", "Vehicle Theft", "Vandalism", "Fraud"
    ]
    
    cities_by_state = {
        "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Solan"],
        "Haryana": ["Gurugram", "Faridabad", "Panipat", "Ambala"],
        "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala"],
        "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Baramulla"],
        "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Nainital"],
        "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Noida"]
    }
    
    descriptions_templates = {
        "Theft": ["Stolen wallet from {location}", "Pickpocketing incident reported at {location} market", "Bag snatched near {location} bus stand"],
        "Burglary": ["Break-in at a residential house in {location}", "Shop burgled late night in {location}", "Valuables stolen from an apartment in {location}"],
        "Assault": ["Physical altercation reported outside a bar in {location}", "Street fight resulting in minor injuries at {location}", "Assault incident in {location} park"],
        "Cybercrime": ["Phishing scam targeting residents of {location}", "Online bank fraud reported from {location}", "Identity theft incident logged from {location}"],
        "Drug Trafficking": ["Suspicious individuals caught with narcotics near {location} border", "Drug bust operation successful in {location}", "Illegal substance distribution stopped in {location}"],
        "Vehicle Theft": ["Car stolen from residential parking in {location}", "Motorcycle lifted from {location} market area", "Vehicle hijacked on the highway near {location}"],
        "Vandalism": ["Public property damaged in {location}", "Graffiti and window smashing at {location} shop", "Vandalism reported at {location} community center"],
        "Fraud": ["Fake investment scheme exposed in {location}", "Real estate fraud reported in {location}", "Counterfeit currency circulated in {location} market"]
    }

    data = []
    
    # Generate dates over the past year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    for i in range(num_records):
        state = random.choice(states)
        city = random.choice(cities_by_state[state])
        location = f"{city}, {state}"
        
        crime_type = random.choice(crime_types)
        
        # Pick a random date
        random_days = random.randint(0, 365)
        random_date = start_date + timedelta(days=random_days)
        time_str = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
        date_time = f"{random_date.strftime('%Y-%m-%d')} {time_str}"
        
        # Generate description
        desc_template = random.choice(descriptions_templates[crime_type])
        description = desc_template.format(location=location)
        
        data.append({
            "Incident_ID": f"CR-{1000 + i}",
            "Date_Time": date_time,
            "State": state,
            "City": city,
            "Location": location,
            "Crime_Type": crime_type,
            "Description": description
        })
        
    df = pd.DataFrame(data)
    df.to_csv("crime_data.csv", index=False)
    print(f"Generated {num_records} synthetic crime records in 'crime_data.csv'.")

if __name__ == "__main__":
    generate_crime_data(150)
