'''
Switch Multiple Fronts Plugin
- Allows switching multiple members/custom fronts to fronting status.

- Version 1.1
- Created on 2/2/2026
- Updated on 2/9/2026

- For Ampersand Remote
'''

from api_client import ApiClient
import json, binascii, os

# get api from json file.
with open("api_and_id.json", 'r') as f:
    api_and_id = json.load(f)

api_client = ApiClient(api_and_id['api'], api_and_id['id'])

def getDocID():
    random_bytes = os.urandom(12)
    docId = binascii.hexlify(random_bytes).decode('utf-8')

    return docId

def run():
    # Open files and run them as variables.

    with open("member_names.json", 'r') as f:
        members_names = json.load(f)

    with open("member_ids.json", 'r') as f:
        members_list = json.load(f)

    with open("cfront_members.json", 'r') as f:
        custom_fronts = json.load(f)
    
    with open("cfront_ids.json", 'r') as f:
        custom_fronts_ids = json.load(f)

    try:
        with open("fronting_members.json", 'r') as f:
            data = json.load(f)
    except:
        data = {}

    # Load members and custom fronts
    # # Load Members
    for n, member in enumerate(members_names):
        print(f"{n+1}. {members_names[str(n)]}\n")
    
    print("=" * 50)

    # # Load custom fronts
    for n, front in enumerate(custom_fronts):
        print(f"{len(members_names)+n+1}. {custom_fronts[str(n)]}\n")

    print("=" * 50)

    # Input prompt for adding multiple members.
    total_options = len(members_list) + len(custom_fronts)

    print(f"Select member/front to do multiple fronts. (1-{total_options})\nSeparate list by comma.")
    inputs = input(f">>> ")
    values = [int(value.strip()) for value in inputs.split(",")]
    docId = getDocID()

    if values[0] == 0:
        print("Request aborted.")
    elif values[0] > total_options:
        print("Please try again.")
    else:
        api_client.remove_all_fronters()
        
        if values[0] <= len(members_list):
            selected_front_str = str(values[0]-1)
            fronter_to_add = {}
            fronter_to_add[docId] = members_list[selected_front_str]
            front_value = members_list[selected_front_str]
        else:
            custom_front_idx = str(values[0] - len(members_list) - 1)
            fronter_to_add = {}
            fronter_to_add[docId] = custom_fronts_ids[custom_front_idx]
            front_value = custom_fronts_ids[custom_front_idx]

        if front_value in data.values():
            print(f"{front_value} already in front, will pass.")
        else:
            data.update(fronter_to_add)

            with open("fronting_members.json", "w") as f:
                json.dump(data, f, indent=2)

            set_url = api_client.url_switch[2] + docId
            payload = api_client.build_payload(True, True, api_client.get_current_epoch(), "start", front_value)
            api_client.load_request(set_url, payload, True, api_and_id['api'], "POST")

            values.pop(0)

            # Continue adding rest of the members/fronts.
            for value in values:
                docId = getDocID()
                if value <= len(members_list):
                    selected_front_str = str(value-1)
                    fronter_to_add = {}
                    fronter_to_add[docId] = members_list[selected_front_str]
                    front_value = members_list[selected_front_str]
                else:
                    custom_front_idx = str(value - len(members_list) - 1)
                    fronter_to_add = {}
                    fronter_to_add[docId] = custom_fronts_ids[custom_front_idx]
                    front_value = custom_fronts_ids[custom_front_idx]

                if front_value in data.values():
                    print(f"{front_value} already in front, will pass.")
                else:
                    data.update(fronter_to_add)

                    with open("fronting_members.json", "w") as f:
                        json.dump(data, f, indent=2)

                    set_url = api_client.url_switch[2] + docId
                    payload = api_client.build_payload(True, True, api_client.get_current_epoch(), "start", front_value)
                    api_client.load_request(set_url, payload, True, api_and_id['api'], "POST")
                
            print("Request successful.")
    return