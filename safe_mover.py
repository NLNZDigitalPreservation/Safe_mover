from __future__ import with_statement
import os
import hashlib
import time
import shutil
import sys

class File_Data(object):
	def __init__(self, f, folder, tools):
		"""holds all the data known about a file"""
		self.source_f = f
		self.destination_f = self.source_f.replace(folder.mount_point, folder.destination_folder)
		self.file_hash = tools.create_md5(self.source_f)
		self.new_file_hash = None
		self.modified_date, self.created_date, self.accessed_date = tools.get_file_dates(self.source_f)
		self.new_modified_date = None
		self.new_created_date = None
		self.new_accessed_date = None

class File_Tools(object):
	"""contains the various per file processes"""
	def __init__(self):
		pass


	def fname_sanitiser(self, filepath):
		"""replaces all illegal chars in the full file path with an underscore """ 
		list_of_bad_chars = ["?", "<", ">", ":", "\"", "*", "|", "^"]
		for bad_char in list_of_bad_chars:
			filepath = filepath.replace(bad_char, "_")
		return filepath
		

	def get_file_dates(self, filepath):
		"""return the OS dates for a file object"""
		modified = time.ctime(os.path.getmtime(filepath))
		created = time.ctime(os.path.getctime(filepath))
		accessed = time.ctime(os.path.getatime(filepath))
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


def main(mount_point, destination_folder, log_file_location):
	
	log_file_location = os.path.join(log_file_location, "logfile.csv")

	try: 
		os.remove(log_file_location)
	except:
		pass

	file_tools = File_Tools()
	folder_tools = Folder_Tools()
	folder_data = Folder_Data(mount_point, destination_folder, folder_tools)
	folder_data.list_of_files = folder_tools.list_folder_contents(folder_data.mount_point)
	folder_tools.create_folder(folder_data.destination_folder)


	for item in folder_data.list_of_files:
		f = File_Data(item, folder_data, file_tools)
		f.destination_f = file_tools.fname_sanitiser(f.destination_f)
		folder_tools.create_folder(os.path.dirname(f.destination_f))
		shutil.copy2(f.source_f, f.destination_f)
		f.new_file_hash = file_tools.create_md5(f.destination_f)
	
	if f.new_file_hash != f.file_hash:
		print "Hash check fail: {}".format(f.source_f)
		quit()
	
	f.new_modified_date, f.new_created_date, f.new_accessed_date = file_tools.get_file_dates(f.destination_f)    
	
	if f.new_modified_date != f.modified_date:
		print "Modified date check fail: {}".format(f.source_f)
		quit()


	### logger - comment out if no logging wanted
	try:
		log_line = "{}, {}, {}, {}, {}\n".format(f.source_f, f.destination_f, f.file_hash, f.modified_date, f.accessed_date)
	except:
		log_line = "%s, %s, %s, %s,  %s" % (f.source_f, f.destination_f, f.file_hash, f.modified_date, f.accessed_date)
		
	log = open(log_file_location,'a')
	log.write(log_line)
	log.close()


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
	
	where_the_log_file_will_go = os.path.join(".", "tests")
	
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
			estination_folder = sys.argv[2]
		except:
			mount_point = top_level_folder_of_files 
			destination_folder = where_the_files_will_go

	else:
		mount_point = top_level_folder_of_files 
		destination_folder = where_the_files_will_go
		log_file_location = where_the_log_file_will_go

	
	main(mount_point, destination_folder, log_file_location)

