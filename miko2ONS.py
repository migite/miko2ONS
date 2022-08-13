import glob
import sys
import os
import re
import chardet

same_hierarchy = (os.path.dirname(sys.argv[0]))

scenario_dir = os.path.join(same_hierarchy,'scx')

with open(os.path.join(same_hierarchy, 'default.txt')) as f:
	txt = f.read()

pathlist = glob.glob(os.path.join(scenario_dir, '*.scx'))

for snr_path in pathlist:

    with open(snr_path, 'rb') as f:
        char_code =chardet.detect(f.read())['encoding']

    with open(snr_path, encoding=char_code, errors='ignore') as f:
        
        txt += ';--------------- '+ os.path.splitext(os.path.basename(snr_path))[0] +' ---------------\nend\n'
        txt = txt.replace('//', ';;;')

        for line in f:

            Message_line = re.match(r'/Mes\s(\[[0-9]+\])\s(\S*)\s(\S*)',line)
            bgmplay_line = re.match(r'/BgmPlay\s\[(\d+)\]',line)
            seplay_line = re.match(r'/SePlay\s\[(\S+)\]',line)
            wait_line = re.match(r'/Wait\s\[(\d+)\]',line)

            if Message_line:

                Chara_name = re.sub(r'\'','',Message_line[2],2)
                Voice_non = Message_line[3]


                line = 'dwave 0,' + Voice_non + '\n' + '[' + Chara_name + ']'

            elif bgmplay_line:

                line = 'bgm "BGM\\M' + bgmplay_line[1] + '.wav\n'
                print(line)

            elif seplay_line:

                line = 'dwave 1,"SE\\SE_' + seplay_line[1] + '.wav\n'
                

            elif wait_line:

                line = 'wait ' + wait_line[1]


            elif re.match(r'/MesWait',line):

                line = '\\\n'
        


            txt += line

open(os.path.join(same_hierarchy,'0.txt'), 'w', errors='ignore').write(txt)