import os


class Supports:
    def dicts(self):
        owner_file_dict = {
            '0': [],
            '1': [self.owner_exe_check],
            '2': [self.owner_write_check],
            '3': [self.owner_write_check, self.owner_exe_check],
            '4': [self.owner_read_check],
            '5': [self.owner_read_check, self.owner_exe_check],
            '6': [self.owner_read_check, self.owner_write_check],
            '7': [self.owner_read_check, self.owner_write_check, self.owner_exe_check]
        }
        
        owner_file_dict_2 = {
            '0': [],
            '1': [self.owner_exe_check_2],
            '2': [self.owner_write_check_2],
            '3': [self.owner_write_check_2, self.owner_exe_check_2],
            '4': [self.owner_read_check_2],
            '5': [self.owner_read_check_2, self.owner_exe_check_2],
            '6': [self.owner_read_check_2, self.owner_write_check_2],
            '7': [self.owner_read_check_2, self.owner_write_check_2, self.owner_exe_check_2]
        }

        group_file_dict = {
            '0': [],
            '1': [self.group_exe_check],
            '2': [self.group_write_check],
            '3': [self.group_write_check, self.group_exe_check],
            '4': [self.group_read_check],
            '5': [self.group_read_check, self.group_exe_check],
            '6': [self.group_read_check, self.group_write_check],
            '7': [self.group_read_check, self.group_write_check, self.group_exe_check]
        }

        group_file_dict_2 = {
            '0': [],
            '1': [self.group_exe_check_2],
            '2': [self.group_write_check_2],
            '3': [self.group_write_check_2, self.group_exe_check_2],
            '4': [self.group_read_check_2],
            '5': [self.group_read_check_2, self.group_exe_check_2],
            '6': [self.group_read_check_2, self.group_write_check_2],
            '7': [self.group_read_check_2, self.group_write_check_2, self.group_exe_check_2]
        }

        others_file_dict = {
            '0': [],
            '1': [self.others_exe_check],
            '2': [self.others_write_check],
            '3': [self.others_write_check, self.others_exe_check],
            '4': [self.others_read_check],
            '5': [self.others_read_check, self.others_exe_check],
            '6': [self.others_read_check, self.others_write_check],
            '7': [self.others_read_check, self.others_write_check, self.others_exe_check]
        }

        others_file_dict_2 = {
            '0': [],
            '1': [self.others_exe_check_2],
            '2': [self.others_write_check_2],
            '3': [self.others_write_check_2, self.others_exe_check_2],
            '4': [self.others_read_check_2],
            '5': [self.others_read_check_2, self.others_exe_check_2],
            '6': [self.others_read_check_2, self.others_write_check_2],
            '7': [self.others_read_check_2, self.others_write_check_2, self.others_exe_check_2]
        }
        
        return owner_file_dict, owner_file_dict_2, \
               group_file_dict, group_file_dict_2, \
               others_file_dict, others_file_dict_2
