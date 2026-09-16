import pandas as pd
from pathlib import Path
import random

random.seed(42)

data = {
    "Water": [
        "There is no water supply in our area",
        "Water has not been coming for three days",
        "Our neighborhood is facing a water shortage",
        "The water pipeline is damaged",
        "Water supply is irregular in our locality",
        "There is no drinking water available",
        "The water connection is not working",
        "Our area has had no water since yesterday",
        "Water pressure is extremely low",
        "The municipal water supply has stopped",
        "There is a leakage in the water pipeline",
        "Residents are not receiving water",
        "Water tanker has not arrived",
        "Our water supply has been disrupted",
        "The public water tap is not working",
    ],

    "Roads": [
        "There is a large pothole on the main road",
        "The road near our school is badly damaged",
        "The street is full of potholes",
        "Road construction has been incomplete for months",
        "The road surface is broken",
        "There is a dangerous pothole near the bus stop",
        "The road needs urgent repair",
        "A damaged road is causing traffic problems",
        "The main road has cracks everywhere",
        "The road is unsafe for vehicles",
        "A large hole has appeared on the road",
        "Road maintenance has not been completed",
        "The footpath is broken",
        "The bridge road is damaged",
        "Vehicles are struggling because of the damaged road",
    ],

    "Electricity": [
        "There is no electricity in our area",
        "The street lights are not working",
        "Power has been out since yesterday",
        "Several street lamps are broken",
        "There is a power outage in our neighborhood",
        "The electricity supply is unstable",
        "Our street has no working lights",
        "The transformer is making unusual sounds",
        "Power cuts are happening frequently",
        "The electric pole is damaged",
        "Street lights have stopped working",
        "There is a problem with the electricity connection",
        "The area is completely dark at night",
        "The power supply has been interrupted",
        "Electricity wires are hanging dangerously",
    ],

    "Sanitation": [
        "Garbage has not been collected for several days",
        "There is garbage lying on the street",
        "The garbage bins are overflowing",
        "Our area has a serious waste problem",
        "Waste collection is irregular",
        "The garbage truck has not arrived",
        "There is a bad smell from accumulated garbage",
        "The public garbage bin is overflowing",
        "Waste is being dumped near houses",
        "The street has not been cleaned",
        "Garbage is scattered around the road",
        "Sanitation workers have not visited",
        "The area needs urgent cleaning",
        "There is a large pile of waste",
        "Uncollected garbage is attracting animals",
    ],

    "Healthcare": [
        "The government hospital does not have enough medicines",
        "The ambulance service is not responding",
        "There is a shortage of doctors at the health center",
        "The hospital is overcrowded",
        "Emergency medical services are unavailable",
        "The local clinic is closed during working hours",
        "Patients are waiting too long for treatment",
        "The health center lacks basic facilities",
        "There are no medicines available at the hospital",
        "The ambulance has not arrived",
        "The public hospital needs more staff",
        "Medical equipment is not working",
        "The health center is facing serious problems",
        "Emergency services are delayed",
        "Patients are unable to receive timely treatment",
    ],

    "Education": [
        "Our school does not have enough classrooms",
        "The classroom roof is damaged",
        "Students do not have proper drinking water",
        "The school toilets are not usable",
        "There are not enough teachers in our school",
        "The school building needs repair",
        "Students are missing classes because of infrastructure problems",
        "The school has no proper computer facilities",
        "The classroom fans are not working",
        "The school playground is damaged",
        "There is a shortage of books in the library",
        "The school needs better facilities",
        "Students are facing problems because of damaged classrooms",
        "The school electricity supply is unreliable",
        "The education facility needs maintenance",
    ],

    "Public Transport": [
        "Buses are not arriving on time",
        "Our area has very limited bus service",
        "The bus route has been cancelled",
        "Public buses are overcrowded",
        "There are no buses after 8 PM",
        "The bus stop is poorly maintained",
        "Bus services are frequently delayed",
        "The public transport service is unreliable",
        "The bus did not arrive today",
        "There are not enough buses on this route",
        "The bus schedule is not being followed",
        "Passengers are waiting for a long time",
        "The bus service has stopped in our area",
        "Public transport is causing problems for students",
        "The bus stop needs urgent repair",
    ],

    "Other": [
        "I want to report a public service problem",
        "There is an issue in our local area",
        "Please look into this community problem",
        "I want to report an unresolved civic issue",
        "The local authorities need to investigate this issue",
        "This public problem has not been addressed",
        "I need help regarding a civic service",
        "Please take action on this complaint",
        "The problem in our locality needs attention",
        "I want to report an issue affecting residents",
        "This issue needs government attention",
        "Please investigate this public complaint",
        "Residents are facing an unresolved problem",
        "I would like to report a local issue",
        "Please take appropriate action",
    ],
}

rows = []

for category, complaints in data.items():
    for complaint in complaints:
        rows.append({
            "complaint": complaint,
            "category": category
        })

# Shuffle dataset
random.shuffle(rows)

df = pd.DataFrame(rows)

output_path = Path("data/raw/complaints.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print(f"Dataset created successfully!")
print(f"Total complaints: {len(df)}")
print("\nCategory distribution:")
print(df["category"].value_counts())
print(f"\nSaved to: {output_path}")