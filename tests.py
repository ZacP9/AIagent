import sys
from functions.get_files_info import *

# if len(sys.argv) < 2:
#     print("Error: Content argument is required")
#     sys.exit(1)

# # get test info or content
# if sys.argv[1] == "info":
#     print(get_files_info("calculator", "."))
#     print(get_files_info("calculator", "pkg"))
#     print(get_files_info("calculator", "/bin"))
#     print(get_files_info("calculator", "../"))
# elif sys.argv[1] == "content":
#     # print(get_file_content("calculator", "lorem.txt"))
#     print(get_file_content("calculator", "main.py"))
#     print(get_file_content("calculator", "pkg/calculator.py"))
#     print(get_file_content("calculator", "/bin/cat"))  # (this should return an error string)
#     print(get_file_content("calculator", "pkg/does_not_exist.py"))  # (this should return an error string)
# elif sys.argv[1] == "write":
#     write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
#     write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
#     write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))