# basic setup script: @plasmarad (github) 

import os
import argparse
import sys
import zipfile
import requests

class Project:
    # inputted variables
    name        = ""
    author      = ""
    description = ""
    version     = ""
    path        = ""
    # non-inputted variables
    ProjectDir  = ""

class Generate_Project(Project):
    def __init__(self, **kwargs):
        Project.name        = kwargs["_name"]
        Project.author      = kwargs["_author"]
        Project.description = kwargs["_description"]
        Project.path        = kwargs["_path"]
        Project.version     = kwargs["_version"]
        
        Project.ProjectDir              = os.path.join(Project.path, Project.name)
        Generate_Project.TemplateDir    = kwargs["_template"]
        
        Generate_Project.create_project()

    def create_project(self):
        _temp_name = "tmp.zip"
        zip_dir = os.path.join(Project.ProjectDir, _temp_name)
        try:
            os.makedirs(Project.ProjectDir, exist_ok=True)
            
            if  (Generate_Project.TemplateDir == None) or (Generate_Project.TemplateDir == ""):
                if input("No template given. Download template from Polaris repo instead? (y/n) ") == ("y" or "Y"):
                    Generate_Project.fetch_polaris()
                else:
                    sys.exit("Exiting...")
            else:
                zip_dir = Generate_Project.TemplateDir
            

            with zipfile.ZipFile(zip_dir, 'r') as zip_ref:
                zip_ref.extractall(Project.ProjectDir)

            os.remove(os.path.join(Project.ProjectDir, _temp_name))

        except OSError as error:
            os.remove(os.path.join(Project.ProjectDir, _temp_name))
            print("Error: " + error.strerror)



    def fetch_polaris(self):
        _temp_name = "tmp.zip"
        
        fetch  = requests.get("https://api.github.com/repos/PolarisEngine/Polaris/releases/latest")
        
        #todo: add interactive prompt for version
        if fetch.status_code == 200:
            open (os.path.join(Project.ProjectDir, _temp_name), 'wb').write(requests.get( fetch.json()['assets'][0]['browser_download_url'] ).content)
        else:
            print("Error: " + str(fetch.status_code))
            sys.exit("Exiting...")     


# TODO
class Generate_Module(Project):
    def __init__(self, **kwargs):
        Project.name        = kwargs["_name"]
        Project.author      = kwargs["_author"]
        Project.description = kwargs["_description"]
        Project.path        = kwargs["_path"]
        Project.version     = kwargs["_version"]
        Project.ProjectDir  = os.path.join(Project.path, Project.name)
        
        Generate_Module.TemplateDir    = kwargs["_template"]
        
        Generate_Module.create_module()

    #! TODO
    def create_module(self):
        pass

if __name__ == "__main__":
    
    _parser = argparse.ArgumentParser(description="Polaris Project Generator")
    _parser.add_argument("-m", "--mode", help="Mode of operation [Project, Module]", default="project")


    
    _parser.add_argument("-n", "--name",        help="Project Name"         , required=True                         )
    _parser.add_argument("-a", "--author",      help="Project Author"       , default=""                            )
    _parser.add_argument("-d", "--description", help="Project Description"  , default=""                            )
    _parser.add_argument("-p", "--path",        help="Project Path"         , required=True                         )
    _parser.add_argument("-v", "--version",     help="Project Version"      , default="1.0.0"                       )       
    _parser.add_argument("-t", "--template",    help="path to the offline project template file", required=False    )  


    print(  "\n"
            "██████╗░░█████╗░██╗░░░░░░█████╗░██████╗░██╗░██████╗\n"
            "██╔══██╗██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║██╔════╝\n"
            "██████╔╝██║░░██║██║░░░░░███████║██████╔╝██║╚█████╗░\n"
            "██╔═══╝░██║░░██║██║░░░░░██╔══██║██╔══██╗██║░╚═══██╗\n"
            "██║░░░░░╚█████╔╝███████╗██║░░██║██║░░██║██║██████╔╝\n"
            "╚═╝░░░░░░╚════╝░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝╚═════╝░\n")

    args = _parser.parse_args()
    if args.mode == "project":
        Generate_Project(   _name         = args.name,                    _author     = args.author, 
                            _description  = args.description,             _path       = args.path, 
                            _version      = args.version,                 _template   = args.template)
    elif args.mode == "module":
        Generate_Module(    _name         = args.name,                    _author     = args.author, 
                            _description  = args.description,             _path       = args.path, 
                            _version      = args.version,                 _template   = args.template)
#! remember to work on Generate_Module