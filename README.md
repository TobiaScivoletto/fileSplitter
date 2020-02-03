# fileSplitter
Python library that can split a file

# EXAMPLE:
 my_splitter = fileSplitter() 
 
 new_files = my_splitter.split("file_name.ext", 51200)
 
 print(new_files)
 
 file_name_list = my_splitter.foundSplittedFile(os.getcwd(), "file_name.ext")
 
 my_splitter.reverseSplit(file_name_list)
