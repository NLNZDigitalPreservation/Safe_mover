# Safe_mover
Python script to move files from A to B.
Creating file hash and grabbing file OS metadata along the way
Results in a log file for later consumption
Log file (csv) shape per file is:-

    original filepath, destination filepath, md5 hash of file, original modifed date, original accessed date 
    
    [f.source_f, f.destination_f, f.file_hash, f.modified_date, f.accessed_date]

To address issue with illegal chars in folders / file names, the following illegal chars (in WIN and *NIX current environments) get scrubbed, and replaced with an _.

List of illegal chars:- 

? < > : * | " ^

(See https://kb.acronis.com/content/39790 or https://msdn.microsoft.com/en-us/library/aa365247.aspx#basic_naming_conventions%22%20target=%22_new%22 for more)
