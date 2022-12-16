# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import collections


class File:
    # Creates a file. Only mandatory field is file_name; all others are option and default to empty/0
    def __init__(self, file_name, contents=[], size=0):
        # File name will be either:
        # "size file_name"
        # "dir dir_name" but this may never happen due to control logic below
        # "$ cd dir_name"
        self.file_name = file_name
        # Contents will be either:
        # []
        # ["size filename", File,...]
        self.contents = contents
        # size will be
        # int
        self.size = size

    # Function to add content to a directory ONLY; flat files are empty
    def add_directory_contents(self, content):
        self.contents.append(content)

    # Function to calculate the size of a directory ONLY. Recursively calculates nested directories
    def calculate_directory_size(self):
        size = 0
        for content in self.contents:
            if "cd" in content.file_name:
                content.calculate_directory_size()
                size += content.size
            else:
                size += content.size
        self.size = size


# Main control method. Parses input from user, line-by-line, building file structure
def process(u_input, file=None):
    # Main controller logic
    while len(u_input) > 0:
        head = u_input[0]
        if "cd" in head:
            # determine if it's a directory or going back into parent directory
            if ".." in head:
                # This is traversing the directory. Perhaps exit without continuing to next item? file finished?
                u_input.popleft()
                exit
            else:
                #print(u_input)
                # This is a directory, next command is an ls; need to grab everything to the next cd that is not ".."
                # Might want to recur here, instantiate a "cd dir_name"
                # Perhaps recursive?
                # f = File(line)
                # process(user_input[2:],f)
                # When recursive call completes, f.contents should contain all subdirectories, files contained in remai
                # ning input
                f = File(head)
                # do not recur on this cd command OR the following ls command; only get list
                # Possible to cd into a directory with no nested subdirectories, files. Should check before recurring.
                if len(u_input) >= 2:
                    u_input.popleft()
                    u_input.popleft()
                    process(u_input, f)
                # will want to append child file f to parent file <file> from parameter
                print(f)
                file.add_directory_contents(f)
        elif "dir" in head:
            # I might not care that there is a nested dir; nested dirs are captured in "cd <dir_name>" logic above
            # pop dir and continue gently into that good loop
            #print(u_input)
            u_input.popleft()
            continue
        else:
            # default case this is a file; make a file with "size file_name"
            u_input.popleft()
            file.add_directory_contents(head)


# Initial test input
user_input = "$ cd /\n$ ls\ndir a\n14848514 b.txt\n8504156 c.dat\ndir d\n$ cd a\n$ ls\n"
# Splits input on newline characters
parsed_input = collections.deque(user_input.splitlines())
#print(parsed_input)
# top level file
f = File(parsed_input[0])
#print(f)
# do not recur on this cd command OR the following ls command; only get list
parsed_input.popleft()
parsed_input.popleft()
#print(parsed_input)
process(parsed_input, f)
#print(f.contents)
#print(f.contents[2])
#print(f.contents[2].contents[2])
