# Safe_mover.py

Python script to move files from A to B.
Creating file hash and grabbing file OS metadata along the way
Results in a log file for later consumption
Log file (csv) shape per file is:-

    "source_head","source_f_path","source_f_name","destination_head","destination_f_path","destination_f_name","relative_f_path_check","filename_check","source_file_hash","new_file_hash","hash_check","source_modified_date","new_modified_date","modified_date_check","source_accessed_date","new_accessed_date","source_created_date","new_created_date"
    
To address issue with illegal chars in folders / file names, the following illegal chars (in WIN and *NIX current environments) get scrubbed, and replaced with an _.

List of illegal chars:- 

? < > : * | " ^

(See https://kb.acronis.com/content/39790 or https://msdn.microsoft.com/en-us/library/aa365247.aspx#basic_naming_conventions%22%20target=%22_new%22 for more)

To address issue of non ascii chars in filenames (e.g. soft hyphens from MAC OS) there is a sanitiser that replaces these items with a "". This is achieved by scrubbing the filename through a `string.decode("utf8","ignore")` step. The pre and post cleaning filename is logged, as is a boolean product of a string.compare() to help mark changed filenames for provenance note writing steps downstream. 

### (Commandline) deployment


Can be deployed from command line, or from the script directly. 

There are two cmd line modes, one that expects the source and destination location as arguments:- 
 
    cmd> python safe_mover.py "my_source_folder" "my_destination_folder"
    
in this mode, the log file (logfile,csv) is written to the location of the python script
    
the 2nd mode expects the source, destination and log file destination:- 

    cmd> python safe_mover.py "my_source_folder" "my_destination_folder" "my_log_file_destinatation" 
    
if no arguments are given, the script will expect the locations in the script body to be valid and correct. 

### TODO 

The naming of the logfile needs to be better, to allow them to be written to one location (e.g. ".\my_log_files" - currently they are always called logfile.csv, so if the location of the logfiles is not changed between new mount points the new file data will just get appended to the existing file. This may or may not be desirable.


# log_compare.py

This is an automated method of comparing two of the logs file generate by the script. The use case is for where 1+n moves are needed to get content from donor into safe harbour on protected storage. 

It extracts the per item relative / constant details from a log file (relative destination path, destination filename,  and file hash) and checks if (1) the item is both logs, and (2) that the names and hashes are the same.. If not, it dumps a log entry to screen. 

Its deployable via cmdline per above:- 

   cmd> python log_comparer.py "log_file_A.csv" "log_file_B.csv"
   
Or the log locations can be changed in script.  
