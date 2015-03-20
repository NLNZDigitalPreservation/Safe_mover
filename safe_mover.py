#!/usr/bin/python
# coding=utf-8

from __future__ import with_statement
import os
import hashlib
import time
import shutil
import sys
import csv

class File_Data(object):
	def __init__(self, f, folder, tools):
		"""holds all the data known about a file"""
		self.source_f = f
		self.source_head = folder.mount_point
		self.destination_head = folder.destination_folder
		self.destination_f = None
		self.source_f_path = None 
		self.source_f_name = None 
		self.destination_f_path = None 
		self.destination_f_name = None 
		self.new_file_hash = None
		self.new_modified_date = None
		self.new_created_date = None
		self.new_accessed_date = None
		self.hash_check = None
		self.modified_date_check = None
		self.relative_f_path_check = None
		self.fname_check = None
		self.modified_date, self.created_date, self.accessed_date = tools.get_file_dates(self.source_f)
		self.file_hash = tools.create_md5(self.source_f)
		self.set_source_names()
		self.set_destination_names()

	def set_source_names(self):
		"""captures all the source strings for the head, path and file items."""
		self.source_f_name = repr(os.path.basename(self.source_f))[1:-1]
		self.source_f_path = self.source_f.replace(self.source_head, "").replace(self.source_f_name, "")
		self.source_f_path = self.source_f_path[1:]

	def set_destination_names(self):
		"""makes all the destination strings for the head, path and file items."""
		self.temp_f = self.source_f.replace(self.source_head, self.destination_head)
		
		### this deals with netwrok paths (e.g. \\my_server vs mount points e.g. c:\)
		if self.temp_f.startswith("\\"):
			head_clipper_amount = 2
		else:
			head_clipper_amount = 3

		self.temp_f = self.fname_illegal_chars_handler(self.temp_f)[head_clipper_amount:]
		self.destination_f_name = self.clean_string(os.path.basename(self.temp_f))	
		self.destination_f_path = self.temp_f.replace(self.destination_head[head_clipper_amount:], "").replace(os.path.basename(self.temp_f), "")
		self.destination_f_path = self.destination_f_path.strip(os.sep)
		self.destination_f = os.path.join(self.destination_head, self.clean_extra_periods(self.destination_f_path), self.destination_f_name)

	def fname_illegal_chars_handler(self, filepath):
		"""replaces all illegal chars in the full file path with an underscore """ 
		list_of_bad_chars = ["?", "<", ">", ":", "\"", "*", "|", "^"]
		for bad_char in list_of_bad_chars:
			filepath = filepath.replace(bad_char, "_")
		return filepath

	def clean_extra_periods(self, folder):
		"""replaces periods in folders names with an underscore """ 
		folder = folder.replace(".", "_")
		if folder.startswith("_"):
			folder = folder.replace("_",".", 1)
		return folder

	def clean_string(self, string):
		"""stips all non UTF-8 chars"""
		return (string.decode("utf8","ignore"))

	def clean_os_metata(self):
		#todo.... 
		pass


class File_Tools(object):
	"""contains the various per file processes"""
	def __init__(self, logging_to_screen = False):
		self.logging_to_screen = logging_to_screen

	def get_file_dates(self, filepath):
		"""return the OS dates for a file object"""
		modified = time.ctime(os.path.getmtime(filepath))
		created = time.ctime(os.path.getctime(filepath))
		try:
			accessed = time.ctime(os.path.getatime(filepath))
		except:
			if self.logging_to_screen:
				print "Bad accessed date found: {}, {}".format(os.path.getatime(filepath), filepath)
			accessed = ""
		return (modified, created, accessed)

	def create_md5(self, filepath):
		"""return the MD5 hash of a file object"""
		hasher = hashlib.md5()
		BLOCKSIZE = 65536
		with open(filepath, 'rb') as afile:
			buf = afile.read(BLOCKSIZE)
			while len(buf) > 0:
				hasher.update(buf)
				buf = afile.read(BLOCKSIZE)
		return (hasher.hexdigest())


class Folder_Data(object):
	"""holds the metadata for the folder (file list and paths) """ 
	def __init__(self, mount_point, destination_folder, folder_tools):
		self.list_of_files = []
		self.mount_point = mount_point
		self.destination_folder = destination_folder

		
class Folder_Tools(object):
	"""methods for generating new folders, file lists and other folder level tools"""
	def __init__(self):
		self.delete_tests_data()

	def delete_tests_data(self):   
		"""this gets fired in case the basic test case has been run previously""" 
		dest = os.path.join(".", "tests", "destination") 
		
		try:
			shutil.rmtree(dest, ignore_errors=True)
		except:
			pass

		try:
			os.remove(os.path.join(".", "tests", "logfile.csv"))
		except:
			pass


	def create_folder(self, f):
		""" if not exists, created given folder"""
		if not os.path.exists(f):
			os.makedirs(f) 

	def list_folder_contents(self, location):
		"""returns recursed list of all file objects in location""" 
		list_of_files = []
		for root, subs, files in os.walk(location):
			for f in files:
				list_of_files.append(os.path.join(root, f))
		return list_of_files


def main(mount_point, destination_folder, log_file_location, on_screen_logging):

	log_file_name = "logfile.csv"
	
	log_file_location = os.path.join(log_file_location, log_file_name)
	
	if os.path.exists(os.path.join(log_file_location, log_file_name)):
		os.remove(log_file_location)

	###set to True if you want information dumps to screen
	file_tools = File_Tools(on_screen_logging)

	folder_tools = Folder_Tools()
	folder_data = Folder_Data(mount_point, destination_folder, folder_tools)
	folder_data.list_of_files = folder_tools.list_folder_contents(folder_data.mount_point)

	folder_tools.create_folder(folder_data.destination_folder)

	### Write log header row
	log_line = 			[
					"source_head", 
					"source_f_path",
					"source_f_name",
					"destination_head",
					"destination_f_path",
					"destination_f_name", 
					"relative_f_path_check",
					"filename_check",
					"source_file_hash", 
					"new_file_hash", 
					"hash_check",
					"source_modified_date", 
					"new_modified_date",
					"modified_date_check", 
					"source_accessed_date", 
					"new_accessed_date", 
					"source_created_date", 
					"new_created_date"
					]
	
	writer = csv.writer(open(log_file_location, "wb"), quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(log_line) 

	### process each item in the list of files, logging as we go

	for item in folder_data.list_of_files:
		f = File_Data(item, folder_data, file_tools)
		folder_tools.create_folder(os.path.dirname(f.destination_f))
		
		try:
			shutil.copy2(f.source_f, f.destination_f)
		except:
			if file_tools.on_screen_logging:	
				print "Copy might have failed: {}".format(f.destination_f)

		f.new_file_hash = file_tools.create_md5(f.destination_f)
		f.new_modified_date, f.new_created_date, f.new_accessed_date = file_tools.get_file_dates(f.destination_f)    

		### checking routines that look for delta between A and B values after move

		f.hash_check = f.new_file_hash == f.file_hash
		if f.new_file_hash != f.file_hash and file_tools.logging_to_screen:
			print "Hash check fail: {}".format(f.destination_f.replace(f.destination_head, ""))
		
		f.modified_date_check = f.new_modified_date == f.modified_date 
		if f.new_modified_date != f.modified_date and file_tools.logging_to_screen:
			print "Modified date check fail: {}".format(f.destination_f.replace(f.destination_head, ""))
			
		
		f.relative_f_path_check = f.source_f.replace(f.source_head, "") == str(f.destination_f.replace(f.destination_head, ""))
		if f.source_f.replace(f.source_head, "") != str(f.destination_f.replace(f.destination_head, "")) and file_tools.logging_to_screen:
			print "file path cleaning occured: {}".format(f.destination_f.replace(f.destination_head, ""))

			
		f.fname_check = f.source_f_name == f.destination_f_name
		if f.source_f_name != f.destination_f_name and file_tools.logging_to_screen:
			print "file name cleaning occured: {}".format(f.destination_f.replace(f.destination_head, ""))
			
		### logger - gives up if logging fails.  
		try:
			log_line = 	[
					f.source_head, 
					f.source_f_path,
					f.source_f_name,
					f.destination_head,
					f.destination_f_path,
					f.destination_f_name, 
					f.relative_f_path_check,
					f.fname_check,
					f.file_hash, 
					f.new_file_hash, 
					f.hash_check,
					f.modified_date, 
					f.new_modified_date,
					f.modified_date_check, 
					f.accessed_date, 
					f.new_accessed_date, 
					f.created_date,
					f.new_created_date 
					]

		except:
			print "logging failed - giving up. Please find an adult."
			quit()

		writer.writerow(log_line)


if __name__ == '__main__':
	
	######## editable block ######### 

	"""put your source location / mount point here. This must be the top level of the content you want to move
	Always start the string with a r... e.g. r"c:\my_locattion\..") """
	
	top_level_folder_of_files = os.path.join(".", "tests", "source")

	"""put the location you expect the files to be copied to here - network locations are supported
	if they are in full (e.g. r"\\pawai\..") """ 
	
	where_the_files_will_go = os.path.join(".", "tests", "destination")

	"""the log file defaults to the folder that houses the python script
	if you want a specific location, you can add is here (or to to the command line call) """
	
	where_the_log_file_will_go = where_the_files_will_go
	
	"""This variable is set True if you want on screen logging of interventions, or False if not. 
	Its worth noting that the log will hold a record of the intervention regardless"""
	
	on_screen_logging = False
	
	#################################

	if len(sys.argv) == 4:
		try:
			mount_point = sys.argv[1]
			estination_folder = sys.argv[2]
			log_file_location = sys.argv[3]
		except:
			mount_point = top_level_folder_of_files 
			destination_folder = where_the_files_will_go
			log_file_location = where_the_log_file_will_go

	elif len(sys.argv) == 3:
		try:
			mount_point = sys.argv[1]
			destination_folder = sys.argv[2]
		except:
			mount_point = top_level_folder_of_files 
			destination_folder = where_the_files_will_go
	else:
		mount_point = top_level_folder_of_files 
		destination_folder = where_the_files_will_go
		log_file_location = where_the_log_file_will_go

	main(mount_point, destination_folder, log_file_location, on_screen_logging)

