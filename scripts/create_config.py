#!/usr/bin/python3

import os
import argparse
import json
from glob import iglob


def main():

    print("\n" + "==== Config Creater ====" + "\n")

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bagfile-dir", type=str, default="/share/bagfiles/visual_indoor_nav")
    parser.add_argument("-o", "--output-dir", type=str, default="/home/amsl/hornet/datasets/dkan_dataset/base_data")
    parser.add_argument("-c", "--config-dir", type=str, default="/home/amsl/rosbag2dataset/myconfig")
    args = parser.parse_args()

    config = {}
    config["topics"] = ["camera/color/image_raw/compressed", "amcl_pose", "t_frog/odom"]
    config["dataset"] = ["obs", "global_pos", "odom"]
    config["hz"] = 10
    config["traj_steps"] = 1
    config["width"] = 224
    config["height"] = 224
    
    count = 1
    for section in iglob(os.path.join(args.bagfile_dir, "*")):
        section_name = os.path.basename(section)
        if section_name in ["test", "experiment"]:
            continue

        bagfile_names = []
        for bagfile_path in iglob(os.path.join(section, "*")):
            bagfile_names.append(os.path.basename(bagfile_path))

        if len(bagfile_names) == 0:
            continue

        config["bagfile_dir"] = os.path.join(args.bagfile_dir, section_name)
        config["bagfile_name"] = [f"{bagfile_name}" for bagfile_name in bagfile_names]
        config["output_dir"] = os.path.join(args.output_dir, section_name)

        os.makedirs(args.config_dir, exist_ok=True)
        with open(os.path.join(args.config_dir, f"config{count}.json"), "w") as f:
            json.dump(config, f, indent=4)

        count += 1

    print("\n" + "==== Created Config ====" + "\n")


if __name__ == "__main__":
    main()
