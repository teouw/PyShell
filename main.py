
#         ----------------------------------------------------------------------
#         |             * KALTRACHIAN Téo                                      |
#         |             * PROGRAMMATION SYSTÈME                                |
#         |             * Python Shell                                         | 
#         |             * HEPIA ITI sem. 3            * main.py                | 
#         ----------------------------------------------------------------------

from commands_handler import *
from custom_commands import *
import getpass

#============================================================#
#                         main loop                          #
#============================================================#

if __name__ == '__main__':

    ch.alias_dict()

    while True:
        
        std() #init std

        #commannd line
        user_input = input(color.bold + "######## ~" + getpass.getuser() + color.end + ": ")

        parse_command(user_input)

        print_output()