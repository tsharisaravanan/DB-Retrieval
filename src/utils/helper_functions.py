import os
import yaml
from typing import Union
from box import ConfigBox
from box.exceptions import BoxTypeError


def read_yaml_file(path: Union[str, os.PathLike]) -> Union[str, ConfigBox]:
    try:
        with open(path) as file:
            content = yaml.safe_load(file)
            return ConfigBox(content)
    except BoxTypeError:
        print("yaml file is empty")
    except Exception as e:
        print(e)


def printer(function: str, value: str, step_count: int = 0):
    print(f"======================================================")
    if function == "Query Generate":
        print(f"==> {step_count}. Generate the query for user given question <===")
    elif function == "Query Execution":
        print(f"==> {step_count}. Execute the query and return the response <====")
    elif function == "Query Error Fixing":
        print(f"=> {step_count}. Fix the issue in the SQL query and regenerate <=")
    elif function == "Natural Response":
        print(f"========> {step_count}. Generate the natural response <==========")
    elif function == "Decision Making":
        print(f"============> Decision making activity <==============")
    elif function == "Chart Type":
        print(f"=====> {step_count}. Identify the visualization chart type <=====")
    elif function == "Program Generate":
        print(f"========> {step_count}. Visualization program generate <=========")
    elif function == "Program Execution":
        print(f"=====> {step_count}. Execute program & save chart in local <=====")
    elif function == "Program Error Fixing":
        print(f"==> {step_count}. Fix the issue in the program and regenerate <==")
    print(f"======================================================")
    print(value)
