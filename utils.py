import json
import os

CONFIG_FILE = "config.json"

# Load config data
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"password": "default_password", "verified_users": []}
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

# Save config data
def save_config(data):
    with open(CONFIG_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Check if user is verified
def is_verified(user_id):
    config = load_config()
    return user_id in config["verified_users"]

# Verify user after password check
def verify_user(user_id):
    config = load_config()
    if user_id not in config["verified_users"]:
        config["verified_users"].append(user_id)
        save_config(config)

# Validate user-entered password
def check_password(user_id, entered_password):
    config = load_config()
    return entered_password == config["password"]

# Change the bot password (only for the owner)
def change_password(new_password):
    config = load_config()
    config["password"] = new_password
    config["verified_users"] = []  # Reset all verified users
    save_config(config)

# Convert TXT to VCF
def txt_to_vcf(txt_file, vcf_file, default_name):
    contacts = []
    with open(txt_file, "r") as file:
        lines = file.readlines()
    
    count = 1
    for line in lines:
        data = line.strip().split(",")
        if len(data) == 2:
            name, phone = data
        elif len(data) == 1:
            phone = data[0]
            name = f"{default_name} {count}"  # Auto-generate name
            count += 1
        else:
            continue  # Skip invalid lines
        
        contact = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL:{phone}
END:VCARD
"""
        contacts.append(contact)

    with open(vcf_file, "w") as file:
        file.write("\n".join(contacts))

    return vcf_file