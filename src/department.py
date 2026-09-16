# CivicResolve AI
# Department Recommendation Engine


DEPARTMENT_MAP = {
    "Water": {
        "department": "Water Supply Department",
        "officer": "Water Supply Officer",
        "action": "Inspect water supply network and restore service"
    },

    "Electricity": {
        "department": "Electricity Department",
        "officer": "Electrical Maintenance Officer",
        "action": "Inspect electrical infrastructure and restore service"
    },

    "Healthcare": {
        "department": "Public Health Department",
        "officer": "Health Department Officer",
        "action": "Verify healthcare issue and coordinate required medical resources"
    },

    "Education": {
        "department": "Education Department",
        "officer": "Education Officer",
        "action": "Verify educational facility issue and coordinate corrective action"
    },

    "Public Transport": {
        "department": "Public Transport Department",
        "officer": "Transport Officer",
        "action": "Investigate transport service issue and coordinate resolution"
    },

    "Roads": {
        "department": "Roads and Infrastructure Department",
        "officer": "Road Maintenance Officer",
        "action": "Inspect road condition and schedule maintenance"
    },

    "Sanitation": {
        "department": "Municipal Sanitation Department",
        "officer": "Sanitation Officer",
        "action": "Inspect sanitation issue and arrange cleaning or waste collection"
    },

    "Other": {
        "department": "General Civic Administration",
        "officer": "Civic Grievance Officer",
        "action": "Review complaint and forward it to the appropriate department"
    }
}


def recommend_department(category):

    return DEPARTMENT_MAP.get(
        category,
        DEPARTMENT_MAP["Other"]
    )


if __name__ == "__main__":

    test_categories = [
        "Water",
        "Electricity",
        "Healthcare",
        "Education",
        "Public Transport",
        "Roads",
        "Sanitation",
        "Other"
    ]

    for category in test_categories:

        result = recommend_department(category)

        print("\n" + "=" * 60)

        print("Category:", category)
        print("Department:", result["department"])
        print("Responsible Officer:", result["officer"])
        print("Recommended Action:", result["action"])