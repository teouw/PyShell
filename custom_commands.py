#         ----------------------------------------------------------------------
#         |             * KALTRACHIAN Téo                                      |
#         |             * PROGRAMMATION SYSTÈME                                |
#         |             * Python Shell                                         | 
#         |             * HEPIA ITI sem. 3           * custom_commands.py      | 
#         ----------------------------------------------------------------------

import sys
import os
import commands_handler as ch
import getpass
import re

#============================================================#
#                   Terminal Color Class                     #
#============================================================#
class color:
    red = "\033[91m"
    cyan = "\033[96m"
    bold = "\033[1m"
    end = "\033[00m"

#============================================================#
#                    All Commands class                      #
#============================================================#
class pwd:
    def __init__(self):
        params = ch.cmd_n_params.params #getting all params
        if not params: 
            ch.std._out_.append(os.getcwd()) 
        else:
            ch.std._err_.append("Tip: Try with only pwd command.")

class exit:
    def __init__(self):
        print("\nExit pyShel...")
        sys.exit()

class rm:
    def __init__(self):
        params = ch.cmd_n_params.params #getting all params
        if len(params) == 2:
            if params[0] == "-r": #if the -r flag is found
                path_name = params[1]
                self.recursive_rm(path_name)  #call recursive_rm
            else:
                ch.std._err_.append("Tip: Try -r flag.")
        else:
            path_name = params[0]
            if os.path.isdir(path_name):   #check if the path_name is a dir
                elements = os.listdir(path_name)  
                if elements:               #check if the dir is not empty -> error
                    ch.std._err_.append("Tip: Try -r flag for recursive remove.") 
                os.rmdir(path_name)
            else:                          #otherwise delete file
                os.remove(path_name)

    #empty the directory to delete it
    def recursive_rm(self, path_name):
        if os.path.isdir(path_name): #if element to delete is dir
            #get the actuel path name
            actuel_path = os.path.abspath(path_name)
            # get all elements of the dir
            elements = os.listdir(actuel_path)
            for elem in elements:
                # Attack the contents recursively
                next_path = actuel_path + "/" + elem
                self.recursive_rm(next_path)

            # Once done, remove the base path
            os.rmdir(actuel_path)

        else:
            # In case a recursive call is called on a file
            os.remove(path_name)

class ls:
    def __init__(self):
        params = ch.cmd_n_params.params #getting all params
        dir_string = []
        file_string = []
        elements = os.listdir()

        if(len(params) == 1 and params[0] == "-l"): #if the -l flag is found
            for elem in elements:
                elem_is_dir = os.path.isdir(elem)
                #add the permission, size, nbr of file and user_name before ls
                perm_val = str( oct( os.stat(elem).st_mode ) )[-3:]
                perm_stat = ch.get_permission_stat(perm_val, elem_is_dir)
                nbr_file_stat = str(os.stat(elem).st_nlink)
                size_stat = str(os.stat(elem).st_size)
                user_name = str(getpass.getuser())
                elem = perm_stat + " " + nbr_file_stat + " " + user_name + " " + size_stat + " " + elem

                if elem_is_dir:
                    dir_string.append(color.cyan + elem + "/" + color.end)
                else:
                    file_string.append(elem)
        elif len(params) == 0:                        #for regular ls
            for elem in elements:
                elem_is_dir = os.path.isdir(elem)
                if elem_is_dir:
                    dir_string.append(color.cyan + elem + "/" + color.end)
                else:
                    file_string.append(elem)
        else:
            ch.std._err_.append("Tip: Try with -l flag.")
            

        for d in dir_string:
            ch.std._out_.append(d)

        for f in file_string:
            ch.std._out_.append(f)

class cd:
    def __init__(self):
        # ----- getting the params -----
        params = ch.cmd_n_params.params
        path = params[0]

        if len(params) == 1: 
            os.chdir(path)
        else:
            ch.std._err_.append("Tip: Try with cd PATH.")

class touch:
    def __init__(self):
        # ----- getting the params -----
        params = ch.cmd_n_params.params
        path = params[0]

        if len(params) == 1: 
            open(path, 'a').close()
        else:
            ch.std._err_.append("Tip: Try with touch PATH.")

class mkdir:
    def __init__(self):
        # ----- getting the params -----
        params = ch.cmd_n_params.params
        path = params[0]
        
        if len(params) == 1: 
            os.mkdir(path)
        else:
            ch.std._err_.append("Tip: Try with mkdir PATH.")

class cat:
    def __init__(self):
        # ----- getting the params -----
        params = ch.cmd_n_params.params
        path = params[0]

        if len(params) == 1: 
            with open(path, 'r') as f:
                for line in f: #print each line of the file
                    ch.std._out_.append(line) 
            f.close()
        else:
            ch.std._err_.append("Tip: Try with cat PATH.")

class echo:
    def __init__(self):
        # ----- getting the params -----
        params = ch.cmd_n_params.params

        if params: 
            param = ""
            for p in params:
                param += p + " "
            ch.std._out_.append(param) 
        else:
            ch.std._err_.append("Tip: Try with echo PARAM.")

class mv:
    def __init__(self):
        # ----- getting the params -----
        params = ch.cmd_n_params.params

        if len(params) == 2: 
            source = params[0]
            destination = params[1]
            #copying source file content to destination file
            ch.file_copy_2_file(source, destination)

            #remove source file
            os.remove(source)
        else:
            ch.std._err_.append("Tip: Try with mv SOURCE DESTINATION.")

class alias:
    def __init__(self):
        # ----- getting the params -----
        alias_dict = ch.alias_dict.dict
        params = ch.cmd_n_params.params

        #check for WORD=COMMAND correct form, else tip.
        if len(params) == 1 and "=" in params[0]:
            #extract the word and command
            word, command = ch.get_word_n_command_param()

            if word in alias_dict: #check for no duplicate alias
                ch.std._err_.append("Error: Alias already exists.")
            else:
                alias_dict[word] = command
        else:
            ch.std._err_.append("Tip: try alias WORD=COMMAND.")

class cp: 
    def __init__(self):
        params = ch.cmd_n_params.params #getting all params
        if len(params) == 3:
            if params[0] == "-r": #if the -r flag is found
                source = params[1]
                destination = params[2]
                self.recursive_cp(source, destination)  #call recursive_cp
            else:
                ch.std._err_.append("Tip: Try -r flag.")
        else:
            source = params[0]
            destination = params[1]
            #copying source file content to destination file
            ch.file_copy_2_file(source, destination)

    def recursive_cp(self, source, destination):
        items = os.listdir(source)
        for item in items:
            s = source + "/" + item
            d = destination + "/" + item
            if os.path.isdir(s):
                os.mkdir(d)
                self.recursive_cp(s, d)
            else:
                if ".txt" in item:
                    ch.file_copy_2_file(s, d)

class wc:
    def __init__(self):
        # ----- getting the params -----
        params = ch.cmd_n_params.params
        if len(params) == 2: #if flag found
            l, w, c = self.wc_command(params[1])
            if params[0] == "-l":
                ch.std._out_.append(l)
            elif params[0] == "-w":
                ch.std._out_.append(w)
            elif params[0] == "-c":
                ch.std._out_.append(c)
            else:
               ch.std._err_.append("Tip: try with [-l -w -c] flag.") 
        else:
            l, w, c = self.wc_command(params[0])
            result = l + " " + w + " " + c
            ch.std._out_.append(result)

    def wc_command(self, path):
        line_cnt = 0
        word_cnt = 0
        char_cnt= 0
        with open(path, 'r') as file:
            for line in file:
                line_cnt += 1
                words = line.split()
                for char in line:
                    char_cnt += 1
                for word in words:
                    word_cnt += 1
        file.close()
        return str(line_cnt), str(word_cnt), str(char_cnt)

class tree:
    def __init__(self):
        params = ch.cmd_n_params.params #getting all params
        if len(params) == 1:
            path = params[0]
            if os.path.isdir(path):
                self.tree_command(path, 0)
            else:
                ch.std._err_.append("Tip: Invalid directory.")
        else:
            ch.std._err_.append("Tip: try tree PATH.")

    def tree_command(self, path, step_nbr):
        stp = step_nbr
        if os.path.isdir(path): #if element is dir
            # ----- DISPLAY TREE ------
            nbr_of_level = int(stp/2)
            level_by_leaf = "|  " * nbr_of_level
            root = level_by_leaf if stp>0 else ""
            ch.std._out_.append(root + "|-- " + color.cyan + os.path.basename(path) + color.end)

            #get the actuel path name
            actuel_path = os.path.abspath(path)
            # get all elements of the dir
            elements = os.listdir(actuel_path)
            for elem in elements:
                if(elem != ".DS_Store"): #for mac os
                    #Creating the next path
                    next_path = actuel_path + "/" + elem
                    self.tree_command(next_path, stp+2)
        else:
            # ----- DISPLAY TREE ------
            nbr_of_level = int(stp/2)
            level_by_leaf = "|  " * nbr_of_level
            root = level_by_leaf if stp>0 else ""
            ch.std._out_.append(root + "|-- " + os.path.basename(path))

class same:
    def __init__(self):
        # ----- getting the params -----
        params = ch.cmd_n_params.params
        if len(params) == 2:
            file1 = params[0]
            file2 = params[1]
            match = self.same_command(file1, file2)
            ch.std._out_.append(str(match))
        else:
            ch.std._err_.append("Tip: try same FILE FILE.")

    def same_command(self, file1, file2):
        hash_f1 = ch.get_hash_hex_from_file(file1)
        hash_f2 = ch.get_hash_hex_from_file(file2)
        if hash_f1 == hash_f2:
            return True
        return False

class duplicate:
    def __init__(self):
        params = ch.cmd_n_params.params #getting all params

        if len(params) == 1: 
            path  = params[0]
            hash_file_dict = {}
            all_files = []
            if os.path.isdir(path):
                self.duplicate_command(path, all_files, hash_file_dict, 0)

                temp_hash = hash_file_dict.get(all_files[0])
                dup_f = []
                #1- for every file in all_files[]
                for f in all_files: # 1
                    dup_files_str = " "
                    #2- check for same hash value with other file in dict
                    for k,v in hash_file_dict.items(): # 2
                        if v == hash_file_dict.get(f): # 3
                            #3- if match, add the key to dup_f and remove file from all_files
                            dup_f.append(k)
                            all_files.remove(k)

                    #4- print the current dup_f with his len and clear dup_f
                    for i in dup_f: #create a string of all the duplicate file name
                        dup_files_str += i + " "
                    if len(dup_f) > 1: 
                        ch.std._out_.append(color.cyan + str(len(dup_f)) + color.end + " " + dup_files_str)
                    dup_f.clear() 
            else:
                ch.std._err_.append("Tip: Try with a directory.")
        else:
            ch.std._err_.append("Tip: Try with duplicate PATH.")


    def duplicate_command(self, path, all_files, hash_file_dict, level):
        if os.path.isdir(path): #if element is dir

            #get the actuel path name
            actuel_path = os.path.abspath(path)
            # get all elements of the dir
            elements = os.listdir(actuel_path)
            for elem in elements:
                if elem != ".DS_Store" and ".txt" in elem: #for mac os
                    #Creating the next path
                    next_path = actuel_path + "/" + elem
                    self.duplicate_command(next_path, all_files, hash_file_dict, level+1)
        else:
            hash_f = ch.get_hash_hex_from_file(path)
            if level > 1: #if the match file is not in the root add the folder path
                hash_file_dict[os.path.basename(os.path.dirname(path)) + "/" + os.path.basename(path)] = hash_f
                all_files.append(os.path.basename(os.path.dirname(path)) + "/" + os.path.basename(path))
            else:
                hash_file_dict[ os.path.basename(path)] = hash_f
                all_files.append(os.path.basename(path))

class find:
    def __init__(self):
        params = ch.cmd_n_params.params #getting all params
        if len(params) == 2:
            regex  = params[0]
            path  = params[1]
            all_files = []
            if os.path.isdir(path):
                self.find_command(regex, path, all_files, 0)
                for f in all_files:
                    ch.std._out_.append(f)
            else:
                ch.std._err_.append("Tip: path should be a directory")
        elif len(params) == 1 and params[0] == "man":
            ch.std._err_.append("Tip: List of metacharacters you can use: ")
            ch.std._err_.append("[]  ->Square brackets specifies a set of characters you wish to match.")
            ch.std._err_.append(".   ->A period matches any single character (except newline '\\n').")
            ch.std._err_.append("^   ->The caret symbol ^ is used to check if a string starts with a certain character.")
            ch.std._err_.append("$   ->The dollar symbol $ is used to check if a string ends with a certain character.")
            ch.std._err_.append("*   ->The star symbol * matches zero or more occurrences of the pattern left to it.")
            ch.std._err_.append("+   ->The plus symbol + matches one or more occurrences of the pattern left to it.")
            ch.std._err_.append("?   ->The question mark symbol ? matches zero or one occurrence of the pattern left to it.")
            ch.std._err_.append("{ } ->Consider this code: {n,m}. This means at least n, and at most m repetitions of the pattern left to it.")
            ch.std._err_.append("()  ->Parentheses () is used to group sub-patterns. For example, (a|b|c)xz match any string that")
            ch.std._err_.append("      matches either a or b or c followed by xz")
            ch.std._err_.append("\   ->Backlash \ is used to escape various characters including all metacharacters.")
            ch.std._err_.append("|   ->Vertical bar | is used for alternation (or operator).")
        else:
            ch.std._err_.append("Tip: try -> find man")

    
    def find_command(self, regex, path, all_files, level):
        if os.path.isdir(path): #if element is dir
            match = re.search(regex, os.path.basename(path))
            if match:
                if level > 1: #if the match file is not in the root add the folder path
                    all_files.append(color.cyan + os.path.basename(os.path.dirname(path)) + color.end + "/" + color.cyan + os.path.basename(path) + color.end)
                else:
                    all_files.append(os.path.basename(path))
            #get the actuel path name
            actuel_path = os.path.abspath(path)
            # get all elements of the dir
            elements = os.listdir(actuel_path)
            for elem in elements:
                if(elem != ".DS_Store"): #for mac os
                    #Creating the next path
                    next_path = actuel_path + "/" + elem
                    self.find_command(regex, next_path, all_files, level+1)
        else:
            match = re.search(regex, os.path.basename(path))
            if match:
                if level > 1: #if the match file is not in the root add the folder path
                    all_files.append(color.cyan + os.path.basename(os.path.dirname(path)) + color.end + "/" + os.path.basename(path))
                else:
                    all_files.append(os.path.basename(path))

class grep:
    def __init__(self):
        params = ch.cmd_n_params.params #getting all params
        if len(params) == 2:
            regex  = params[0]
            path  = params[1]
            if ".txt" in path:
                match_pattern = self.grep_command(regex, path)
                for m in match_pattern:
                    ch.std._out_.append(m)
            else:
                ch.std._err_.append("Tip: try again with .txt file.")
        elif len(params) == 1 and params[0] == "man":
            ch.std._err_.append("Tip: List of metacharacters you can use: ")
            ch.std._err_.append("[]  ->Square brackets specifies a set of characters you wish to match.")
            ch.std._err_.append(".   ->A period matches any single character (except newline '\\n').")
            ch.std._err_.append("^   ->The caret symbol ^ is used to check if a string starts with a certain character.")
            ch.std._err_.append("$   ->The dollar symbol $ is used to check if a string ends with a certain character.")
            ch.std._err_.append("*   ->The star symbol * matches zero or more occurrences of the pattern left to it.")
            ch.std._err_.append("+   ->The plus symbol + matches one or more occurrences of the pattern left to it.")
            ch.std._err_.append("?   ->The question mark symbol ? matches zero or one occurrence of the pattern left to it.")
            ch.std._err_.append("{ } ->Consider this code: {n,m}. This means at least n, and at most m repetitions of the pattern left to it.")
            ch.std._err_.append("()  ->Parentheses () is used to group sub-patterns. For example, (a|b|c)xz match any string that")
            ch.std._err_.append("      matches either a or b or c followed by xz")
            ch.std._err_.append("\   ->Backlash \ is used to escape various characters including all metacharacters.")
            ch.std._err_.append("|   ->Vertical bar | is used for alternation (or operator).")
        else:
            ch.std._err_.append("Tip: try -> greb man")

    def grep_command(self, regex, path):
        with open(path, 'r') as f: 
            content = f.read() 
        result = re.findall(regex, content) 
        return result




