# CivicResolve AI
# Resolution Recommendation Engine


RESOLUTION_MAP = {

    "Water": {
        "immediate_action": [
            "Verify the affected area",
            "Inspect water supply pipeline/network",
            "Identify the cause of service disruption"
        ],
        "resolution": "Repair the affected water infrastructure and restore water supply",
        "follow_up": "Confirm restoration with affected citizens"
    },

    "Electricity": {
        "immediate_action": [
            "Verify the affected location",
            "Inspect electrical infrastructure",
            "Check for outages or damaged equipment"
        ],
        "resolution": "Repair the electrical fault and restore power service",
        "follow_up": "Confirm that electricity service has been restored"
    },

    "Healthcare": {
        "immediate_action": [
            "Verify the healthcare facility",
            "Check availability of required medical resources",
            "Notify the responsible health authority"
        ],
        "resolution": "Provide the required medical resources or corrective action",
        "follow_up": "Confirm that the healthcare issue has been addressed"
    },

    "Education": {
        "immediate_action": [
            "Verify the educational institution",
            "Identify the reported infrastructure or service issue",
            "Notify the responsible education authority"
        ],
        "resolution": "Resolve the reported educational facility or service issue",
        "follow_up": "Confirm completion with the institution"
    },

    "Public Transport": {
        "immediate_action": [
            "Verify the route or transport service",
            "Identify the operational issue",
            "Notify the transport authority"
        ],
        "resolution": "Restore or improve the affected transport service",
        "follow_up": "Monitor the route/service after resolution"
    },

    "Roads": {
        "immediate_action": [
            "Verify the reported road location",
            "Inspect the road condition",
            "Assess public safety risk"
        ],
        "resolution": "Repair the damaged road infrastructure",
        "follow_up": "Verify that the road has been repaired and is safe"
    },

    "Sanitation": {
        "immediate_action": [
            "Verify the reported location",
            "Inspect sanitation conditions",
            "Arrange required cleaning or waste collection"
        ],
        "resolution": "Complete sanitation or waste-management work at the affected location",
        "follow_up": "Confirm that the area has been cleaned"
    },

    "Other": {
        "immediate_action": [
            "Verify the complaint details",
            "Identify the responsible authority",
            "Forward the complaint to the appropriate department"
        ],
        "resolution": "Resolve the complaint through the responsible civic authority",
        "follow_up": "Confirm resolution with the complainant"
    }
}


def recommend_resolution(category):

    return RESOLUTION_MAP.get(
        category,
        RESOLUTION_MAP["Other"]
    )


if __name__ == "__main__":

    test_categories = [
        "Water",
        "Electricity",
        "Roads",
        "Sanitation"
    ]

    for category in test_categories:

        result = recommend_resolution(category)

        print("\n" + "=" * 60)

        print("CATEGORY:", category)

        print("\nIMMEDIATE ACTIONS:")

        for action in result["immediate_action"]:
            print("-", action)

        print("\nRECOMMENDED RESOLUTION:")
        print(result["resolution"])

        print("\nFOLLOW-UP:")
        print(result["follow_up"])