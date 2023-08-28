import csv
import re

def getRegions(dir_config):
   return ["us-east-1", "us-east-2"]

def getEnvironments(dir_config):
   return ["dev", "int", "pre-prod","prod"]

file_error_logs = []
total_updated_files = 0

with open('build.csv', mode='r') as build_file:
   build_config= csv.DictReader(build_file)

   houseFolder = "dir"
   # validate csv file


   # make changes to files
   for dir_config in build_config:
      print("\nFile updates for:\t\t\t"+dir_config['dir_name']+"\n")
      standard_path = dir_config['org'].strip()+"/"+dir_config['app_id'].strip()+"/"+dir_config['dir_id'].strip()
      filename = dir_config['dir_id'].strip()+".yaml"

      files_to_update = []
      for region in getRegions(dir_config):
         for env in getEnvironments(dir_config):
            filepath = houseFolder+"/"+region+"/"+env+"/"+standard_path+"/"+filename
            files_to_update.append(filepath)
      
      file_update_count = 0
      for yaml_file in files_to_update:
         try:
            with open(yaml_file, "r+") as f:
               file = f.read()
               pattern = dir_config["dir_name"].strip()+":\d+.\d+.\d+"
               repl = dir_config["dir_name"].strip()+":"+dir_config["build_version"].strip()
               count = 1
               file = re.sub(pattern, repl, file)
               f.seek(0)
               f.write(file)
               f.truncate()
               file_update_count+=1
         except FileNotFoundError:
            msg = "WARNING, the file "+ yaml_file + " does not exist, make sure this update is not expected!"
            print(msg)
            file_error_logs.append(msg)

         print("Updated file: "+yaml_file)
      print("Updated :",file_update_count," files for ",dir_config["dir_name"])
      total_updated_files+=file_update_count
   print("*************************************")
   if(len(file_error_logs)==0):
      print("File update SUCCESSFULL :)")
      print(total_updated_files, " files were updated!")
   else:
      print("File update PARTIALLY SUCCESSFULL :(")
      print(total_updated_files, " files were updated!")
      print(len(file_error_logs)," issues were found while updating")
      print(*file_error_logs, sep="\n")
   print("*************************************")

      

