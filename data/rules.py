# List of "suspicious" generalizations that trigger an AI audit
GENERALIZATIONS = ["all", "always", "any", "each", "every"]

# Knowledge Base: Forbidden drug-condition pairs
SAFETY_DB = {
    "platinum": ["cisplatin", "carboplatin", "oxaliplatin"],
    "renal_failure": ["cisplatin", "nsaids", "methotrexate"],
    "penicillin": ["amoxicillin", "ampicillin", "benzylpenicillin"]
}

# White List: Drugs or substances that are generally considered safe in this context
SAFE_LIST = {"saline", "glucose", "vitamin", "water", "heparin"}