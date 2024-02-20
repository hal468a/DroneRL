import os
import json
import argparse

def replace_json_content(new_content):

    if new_content == "PX4":
        file_name = "PX4.json"
    elif new_content == "Xbox":
        file_name = "Xbox.json"
    else:
        file_name = None
        print("File Path error!!!")

    print(f"Readding {new_content}.json...")
    with open(file_name, 'r') as file:
        data = json.load(file)
    print("******************************")

    local_path = f"C:\\Users\\{os.getlogin()}\\Documents\\AirSim\\settings.json"
        
    if not os.path.exists(local_path):
        local_path = f"C:\\Users\\{os.getlogin()}\\Onedrive\\Documents\\AirSim\\settings.json" # 如果有開啟onedrive設定檔會在這個路徑內
    
    print(f"Writting to {local_path}...")
    with open(local_path, 'w') as file:
        json.dump(data, file, indent=2)
    print("******************************")
    print("Finished!")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Choose PX4 or Xbox control drone')
    parser.add_argument('--contents', type=str, default="Xbox")

    args = parser.parse_args()
    replace_json_content(new_content=args.contents)