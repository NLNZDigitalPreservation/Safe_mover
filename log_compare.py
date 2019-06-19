import hashlib
import csv
import os
import sys


class Log(object):
	def __init__(self, f):
		self.log_name = f
		self.data = self.get_data(f)
		self.log_dict = self.log_parser(self.data)


	def get_data(self, f):
		"""pulls a csv reader from the file"""
		data = []
		csvfile = open(f, 'r')
		reader = csv.reader(csvfile)
		return reader

	def log_parser(self, log):
		"""parses the reader, and extracts the salient item data"""
		self.log_dict = {} 
		for row in log:
				key = os.path.join(row[4], row[5])
				self.log_dict[key] = [row[4], row[5], row[8]]
		return self.log_dict
				

class Tools(object):
	def __init__(self):
		pass

	def compare_hashes(self, a, b):
		"""returns the ans to does MD5 a == MD5 b"""
		m = hashlib.md5()
		m.update(a)
		a_hash = m.hexdigest()
		
		m = hashlib.md5()
		m.update(b)
		b_hash = m.hexdigest()
		
		return a_hash == b_hash

class Checks(object):
	def __init__(self, a, b):
		self.a = a.log_dict
		self.a_label = a.log_name
		self.b = b.log_dict
		self.b_label = b.log_name
		self.all_checks()


	def all_checks(self):
		"""performs the item check by iterating through both lists per item looking for the item in the other list, and item delta"""
		self.delta_check = None
		for item, value, in self.a.items():
			item_check = self.missing_check(item, self.b)

			if item_check:
				if value == self.b[item]:
					pass
				else:
					print("'{}' has a different hash".format(item))
			else:
				print("'{}' is missing from '{}'".format(item, self.b_label))

		print("Iteration 1 complete")
		
		for item, value, in self.b.items():
			item_check = self.missing_check(item, self.a)

			if item_check:
				if value == self.a[item]:
					pass
				else:
					print("'{}' has a different hash".format(item))
			else:
				print("'{}' is missing from '{}'".format(item, self.a_label))
		print("Iteration 2 complete")
			



	def missing_check(self, item, my_dict):
		"""returns the logic test if a is in list b"""
		if item in my_dict.keys():
			return True
		else:
			return False


def main(a, b):
	tools = Tools()
	log_a = Log(a)
	log_b = Log(b)

	checks = Checks(log_a, log_b)

if __name__ == '__main__':

	######## editable block ######### 

	"""Log file A location"""
	
	log_a = r"C:\source\Code\NDHA\SafeMover\destination\2019-05-13_logfile.csv"

	"""Log file B location""" 
	
	log_b = r"C:\source\Code\NDHA\SafeMover\destination\no_extension\2019-05-13_logfile_no_ext.csv"
	
	#################################


	if len(sys.argv) == 3:
		try:
			log_a = sys.argv[1]
			log_b = sys.argv[2]
		except:
			quit("Too many, or not enough arguments")
	
	main(log_a, log_b)

