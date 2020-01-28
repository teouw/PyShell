#         ----------------------------------------------------------------------
#         |             * KALTRACHIAN Téo                                      |
#         |             * PROGRAMMATION SYSTÈME                                |
#         |             * Python Shell                                         | 
#         |             * HEPIA ITI sem. 3           * commands_handler.py     | 
#         ----------------------------------------------------------------------

import custom_commands as cc
import os
import sys
import hashlib

#============================================================#
#                 Store variables function                   #
#============================================================#

def std():
    #to store the std's
    std._out_ = []
    std._in_ = []
    std._err_ = []

def alias_dict():
    #to store the dict
    alias_dict.dict = {}

def cmd_n_params(user_input):
    '''*-----------------------------------------------*
        | This function will split the user's input and |
        * will extract and store the cmd and the params * 
        | into function variables. It'll also check for |
        * redirection and store the redirection file    *
        | into function variables then it'll remove the |
        * ">" and file params of the params variales.   *
        *-----------------------------------------------*'''
    #split the user's input into an array
    cmd_n_params_array = []
    cmd_n_params_array = user_input.split()
    cmd_n_params.redirect_file = "null"
    if cmd_n_params_array : #if user's input not empty
        
        # ----- Check for redirection -----
        if len(cmd_n_params_array) > 3 and ">" == cmd_n_params_array[-2]:
            if ".txt" in cmd_n_params_array[-1]:
                cmd_n_params.redirect_file = cmd_n_params_array[-1]
                cmd_n_params_array.pop() #remove redirection file
                cmd_n_params_array.pop() #remove ">" symbole
            else:
                std._err_.append("Tip: file redirection extension must be .txt ")
        # ---------------------------------

        #cmd will be the command -> string
        cmd_n_params.cmd = cmd_n_params_array[0]
        del cmd_n_params_array[0] #remove the cmd from array
        #params will be all the param -> [] of string (without cmd)
        #params can be a PATH, FLAG, PIPE, FILE, REGEX, SOURCE, DEST...
        cmd_n_params.params = cmd_n_params_array

#============================================================#
#                       commands lib                         #
#============================================================#

def check_if_separator(user_input):
    if ";" in user_input:
        all_command = user_input.split(";")
        return True, all_command
    elif "\n" in user_input:  #not working don't know why :(
        all_command = user_input.split()
        return True, all_command
    else:
        return False, "null"

def get_permission_stat(param_value, is_Directory=False):
    if is_Directory:
        permission = "d"
    else:
        permission = "-"

    for i in range(3):
        val = int(param_value[i])
        if val >= 4:
            permission += "r"
            val -= 4
        else: permission += "-"
        if val >= 2:
            permission += "w"
            val -= 2
        else: permission += "-"

        if val >= 1:
            permission += "x"
        else: permission += "-"

    return permission

def print_output():
    if std._err_:
        for err in std._err_:
            print("{} {}{}".format(cc.color.red, err, cc.color.end))
    elif std._out_: 
        # ----- Check for redirection -----
        if cmd_n_params.redirect_file != "null":
            copy_2_file(std._out_, cmd_n_params.redirect_file)
        # ---------------------------------
        else:
            for out in std._out_:
                print(out)

def get_hash_hex_from_file(file):
    BLOCK_SIZE = 65536 # The size of each read from the file

    file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
    with open(file, 'rb') as f: # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = f.read(BLOCK_SIZE) # Read the next block from the file
    f.close()
    return file_hash.hexdigest()

def copy_2_file(content, file):
    with open(file, 'w') as f:
        for c in content:
            f.write(c)
    f.close()

def check_for_alias():
    # ----- getting the params -----
    command = cmd_n_params.cmd    
    if command in alias_dict.dict: #if the cmd is an alias
        return True, alias_dict.dict.get(command)
    return False, "null"

def get_word_n_command_param():
    # ----- getting the params -----
    params = cmd_n_params.params
    param = params[0].split('=') #extract the word and command
    return param[0], param[1]         

def file_copy_2_file(source, destination):
    with open(source ,  encoding='utf-8') as f_to_r: #read the source file
        content = f_to_r.read()  
        with open(destination, "w",  encoding='utf-8') as f_to_w: #write the dest file
            f_to_w.write(content)    
    f_to_r.close()
    f_to_w.close()

def str_to_class(class_name):
    return getattr(sys.modules["custom_commands"], class_name)

#============================================================#
#                      parse commannd                        #
#============================================================#

def parse_command(user_input):
    try:
        is_sperator, all_command = check_if_separator(user_input)

        if is_sperator:
            for com in all_command:

                #extract the command and params from user_input
                cmd_n_params(com)

                #check if alias already exist, if yes return the cmd
                alias_found, cmd = check_for_alias()

                if alias_found:
                    #creating the command object from the cmd name of the alias
                    command = str_to_class(cmd)
                    command()
                else:
                    #creating the command object from the cmd name of user_input
                    command = str_to_class(cmd_n_params.cmd)
                    command()
        else:
            #extract the command and params from user_input
            cmd_n_params(user_input)

            #check if alias already exist, if yes return the cmd
            alias_found, cmd = check_for_alias()

            if alias_found:
                #creating the command object from the cmd name of the alias
                command = str_to_class(cmd)
                command()
            else:
                #creating the command object from the cmd name of user_input
                command = str_to_class(cmd_n_params.cmd)
                command()


    except AttributeError:
        std._err_.append("Error: Command not found.")
    except FileNotFoundError:
        std._err_.append("Error: File not found.")
    except PermissionError:
        std._err_.append("Error: Permission denied!") 
    except FileExistsError:
        std._err_.append("Error: File already exists.") 
    except NotADirectoryError:
        std._err_.append("Error: Is Not A Directory")
    except OSError:
        std._err_.append("Error: Can't delete. Directory not empty!") 

