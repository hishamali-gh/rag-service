import re


# We transition from static naming to keyword index tokens

OPERATOR_MANUALS = [
    {
        "error_code": "OVN-404",
        "component": "Oven Core Assembly",
        "keywords": {"OVEN", "OVN", "OVERHEAT", "HEAT", "TEMPERATURE", "SPIKE", "COOLING"},
        "instructions": "CRITICAL SPIKE: Error OVN-404 means the cooling loop has failed. Immediately confirm the fluid pump status, check for physical pipe obstructions, and manually toggle the secondary radiator switch on the console panel."
    },
    {
        "error_code": "CNV-BELT",
        "component": "Conveyor Alignment Tracker",
        "keywords": {"CONVEYOR", "BELT", "SLIP", "SLIPPING", "ALIGNMENT", "TRACKER", "TRACKING"},
        "instructions": "SLIPPAGE DETECTED: If the conveyor belt slips or drifts off-center, locate the manual tension bolts under the lower intake manifold. Turn them clockwise exactly 2 full rotations to tighten and realign tracking values."
    },
    {
        "error_code": "PMP-SAUCE",
        "component": "Pneumatic Fluid Discharger",
        "keywords": {"PUMP", "SAUCE", "PRESSURE", "LOW", "FAULT", "CLOG", "VISCOSITY"},
        "instructions": "LOW PRESSURE: A low-pressure fault on the tomato sauce pump indicates a viscosity block. Operator must flush the central hopper line with warm water before resetting the manifold back to auto-run mode."
    }
]

def search_manuals(user_message: str) -> str:


    """
    Smarter tokenized search routine.
    Breaks down the incoming message into distinct word elements 
    and determines the best documentation match based on keyword overlap weight.
    """


    # Convert query to uppercase and extract individual word tokens using regex boundaries

    query_words = set(re.findall(r'\b\w+\b', user_message.upper()))
    
    best_match = None
    max_overlap = 0
    
    for manual in OPERATOR_MANUALS:


        # Determine the shared set matching intersection between input words and manual target tags

        shared_keywords = query_words.intersection(manual["keywords"])
        overlap_count = len(shared_keywords)
        

        # Track the database entry with the highest keyword correlation score

        if overlap_count > max_overlap:
            max_overlap = overlap_count
            best_match = manual
            

    # Return document match sequence if structural correlation exists

    if best_match and max_overlap > 0:
        return f"FOUND METADATA [{best_match['component']} - {best_match['error_code']}]:\n{best_match['instructions']}"
        
    return "SYSTEM ALARM: Query did not match core machinery manuals. Please contact the Plant Systems Engineer on duty."