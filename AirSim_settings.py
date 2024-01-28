import json
import argparse

def replace_json_content(new_content):
    if new_content == "PX4":
        file_path = "C:\\Users\\Louis\\Documents\\AirSim\\airsim-setting\\PX4.json"
    elif new_content == "Xbox":
        file_path = "C:\\Users\\Louis\\Documents\\AirSim\\airsim-setting\\Xbox.json"
    else:
        file_path = None
        print("File Path error!!!")

    print(f"Readding {new_content}.json...")
    with open(file_path, 'r') as file:
        data = json.load(file)
    print("******************************")

    print(f"Writting to C:\\Users\\Louis\\Documents\\AirSim\\settings.json...")
    with open('C:\\Users\\Louis\\Documents\\AirSim\\settings.json', 'w') as file:
        json.dump(data, file, indent=2)
    print("******************************")
    print("Finished!")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Choose PX4 or Xbox control drone')
    parser.add_argument('--contents', type=str, default="Xbox")

    args = parser.parse_args()
    replace_json_content(new_content=args.contents)