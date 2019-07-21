import pandas as pd
import math
import re
import argparse
pd.options.display.max_colwidth = 10000

class TL():
    def __init__(self, name, readlines):
        self.name = name
        self.readlines = readlines
        self.tl_lines = {}
        self.common_lines = {}
        self.df = None
        
        self.num_lines_replaced = 0
        self.unmatched = 0
        self.unmatched_line_number = []
        self.replaced_line_number = []

    def create_df(self, corresponding_dialogue_file):
        self.df = corresponding_dialogue_file.loc[corresponding_dialogue_file['Filename'] == 'game/' + self.name + '.rpy']
        return
        
def jupyter_main(game_dir, dialogue, tl_files, language):

    game_df = pd.read_csv(game_dir + "/" + dialogue, sep='\t',skiprows=(0),header=(0))

    tl_files_holder = {}
    for tl_file in tl_files:
        file_path = game_dir + "/game/tl/" + language + "/" + tl_file + ".rpy"
        print(file_path)
        with open(file_path, 'r') as f:
            tl_files_holder[tl_file] = TL(tl_file, f.readlines())

        count = 0
        tl_files_holder[tl_file].tl_lines[0] = []
        for line in tl_files_holder[tl_file].readlines:
            if line.startswith("# game/"+tl_file+".rpy"):
                count = int(re.findall(re.compile("[0-9]+"),line.split(":")[-1])[0]) 
                tl_files_holder[tl_file].tl_lines[count] = [line]

            if not line.startswith("# game/"+tl_file+".rpy"):
                if line.startswith('translate ' + language + ' strings:\n'):
                    break
                tl_files_holder[tl_file].tl_lines[count].append(line)
                
        print("Popping the header row: ", tl_files_holder[tl_file].tl_lines.pop(0, None))
        tl_files_holder[tl_file].create_df(game_df)

    for item in tl_files_holder.items():
        print(item)
        num_lines_replaced = 0
        unmatched = 0
        unmatched_line_number = []
        replaced_line_number = []
        
        for key in item[1].tl_lines.keys():
            line_id_compare(key, item[1].df, item[1].tl_lines, "chinese_simp", item[1])
            
        print("num lines replaced: {}".format(num_lines_replaced))
        print("num lines dialogue doesnt match: {}".format(unmatched))
        print()
        print("unmatched line numbers: {}".format(unmatched_line_number))
        print("replaced line numbers: {}".format(replaced_line_number))
        
    return tl_files_holder
    
def line_id_compare(line_number, char_df, char_tl_dict, language, char_obj):
    
    tab_row = char_df.loc[char_df["Line Number"] == line_number]

    try:
        tab_dl = tab_row["Dialogue"].to_string().split("    ")[1].strip('\\"')
    except IndexError:
        print("Index Error at line: {}".format(line_number))
        print(tab_row["Dialogue"].to_string())
        return
    tab_id = tab_row["Identifier"].to_string().split("    ")[1]
    
    tl_dl = char_tl_dict[line_number]
    tl_id = tl_dl[1].split()[2].split(":")[0]
    tl_orig_text = tl_dl[3]
    tl_orig_text = re.findall(re.compile("\".+\""), tl_orig_text)[0].strip('\\"')
    
#     print("Dialogue.tab: || {}\nTL.rpy:       || {}".format(tab_dl, tl_orig_text)) #sanity check 
    if tab_dl == tl_orig_text:
#         print("DIALOGUE MATCH: Line {}".format(line_number))
#         print("TAB ID: {}\nTL  ID: {}".format(tab_id, tl_id))
        if tab_id == tl_id:
#             print("GOOD")
            pass
        
        else:
            print("INCORRECT: Line{}".format(line_number))
            print("TAB ID: {}\nTL  ID: {}".format(tab_id, tl_id))
            
            print("REPLACING ID NOW...")
            char_obj.num_lines_replaced += 1
            
            char_obj.replaced_line_number.append(line_number)
        
        
            tl_dl[1] = "translate " + language + " {}:\n".format(tab_id)
    else:
        print("DIALOGUE DOESN'T MATCH")
        char_obj.unmatched += 1
        char_obj.unmatched_line_number.append(line_number)
        
    return 
        
if __name__ == '__main__':
    tfh = jupyter_main("RenpyGames/YourDryDelight", "dialogue.tab", ["common", "eastman", "leslie", "script"], "chinese_simp")
    for item in tfh.items():
        print(item[0])
        print("num lines replaced: {}".format(item[1].num_lines_replaced))
        print("num lines dialogue doesnt match: {}".format(item[1].unmatched))
        print("unmatched line numbers: {}".format(item[1].unmatched_line_number))
        print("replaced line numbers: {}".format(item[1].replaced_line_number))
        print()
