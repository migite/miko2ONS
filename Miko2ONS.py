import sys
import os
import glob
import chardet
import re

Game_path = (os.path.dirname(sys.argv[0]))

Senario_dir = os.path.join(Game_path,"scx")

with open(os.path.join(Game_path,"default.txt")) as f:
    txt = f.read()

Pathlist = glob.glob(os.path.join(Senario_dir,"*.scx"))

for Snr_path in Pathlist:

    with open(Snr_path,"rb") as f:
        char_code = chardet.detect(f.read())["encoding"]

    with open(Snr_path, encoding=char_code, errors="ignore") as f:

        txt += ';--------------- '+ os.path.splitext(os.path.basename(Snr_path))[0] +' ---------------\nend\n'

        Name_variable= ""
        Voicenum_variable = ""

        
        for line in f:

            #Messeage_line= re.match(r"")
            Message_line = re.match(r"\/Mes",line)
            TextMain_line= re.match(r"([^\x01-\x7E\xA1-\xDF]+)",line)
            BGMPlay_line = re.match(r"\/BgmPlay\s\[(\d+)\]",line)
            SEPlay_line = re.match(r"\/SePlay\s\[(\d+)\]",line)
            Character_in_line = re.match(r"\/ChrIn\s<CHR_\d{1}>",line)
            Wait_line = re.match(r"\/Wait\s\[(\d+)\]",line)

            if Message_line:
                #テキストが出る際に/Mes命令が使われているみたいです。
                #発言者、参照するボイス、コメントアウトはこの行に入ることが多いです。
                #とりあえずコメントアウトは含んでいませんが、可能なら残す方針で
                Name_and_Voice_line= re.match(r"\/Mes	\[(\d+)\]	\'(\S+)\'	\"voice\\(\d+)\.ogg\"",line)
                Name_Only_line=re.match(r"\/Mes	\[(\d+)\]	\'(\S+)\'",line)
                Noname_line=re.match(r"\/Mes	\[(\d+)\]",line)

                if re.match(r"\/MesWait",line):
                    #テキスト表示終了の命令みたいです
                    #ここでウインドウのクリアしようかなと
                    #もしかしたら文字を全部変数で取って、変数リセットを繰り返して
                    #改ページの代わりにしてもいいかなと
                    line = "\\\n"
                    Name_variable=""
                    Voicenum_variable=""


                elif Name_and_Voice_line:
                    Name_variable=Name_and_Voice_line[2]
                    Voicenum_variable=Name_and_Voice_line[3]
                    #print(r"["+Name_variable+"|"+Voicenum_variable+"]\n")
                    line ="dwave 0 \"voice\\" +Name_and_Voice_line[3] + ".ogg\"\n"
                    #print(line)

                elif Name_Only_line:
                    Name_variable=Name_Only_line[2]
                    Voicenum_variable=""
                    #print(r"["+Name_variable+"|"+Voicenum_variable+"]\n")
                    line ="\n"

                elif Noname_line:
                    Name_variable=""
                    Voicenum_variable=""
                    #print(r"["+Name_variable+"|"+Voicenum_variable+"]\n")
                    line ="\n"

                else:
                    line = ";;;" + line + "\n"
            
            elif TextMain_line:

                TEXT_and_Commentout = re.fullmatch(r"[^\x01-\x7E\xA1-\xDF]\s;(\S+)",line)
                
                line = "[" + Name_variable + "]" + line
                #print(line)
            
            elif BGMPlay_line:

                BGMPlay_Outline = re.match(r"\/BgmPlay\s\[(\d+)\]\s; ([^\x01-\x7E\xA1-\xDF]+)",line)

                if BGMPlay_Outline:
                    line = "bgm \"BGM\\M" + BGMPlay_Outline[1] + ".WAV\"\n;;;" + BGMPlay_Outline[2] + "\n"
                    #print(line)
                else:
                    line = "bgm \"BGM\\M" + BGMPlay_line[1] + ".WAV\"\n"
                    #print(line)

            elif SEPlay_line:
                SEPlay_Outline = re.match(r"\/SePlay\s\[(\d+)\]\s; ([^\x01-\x7E\xA1-\xDF]+)",line)

                if SEPlay_Outline:
                    line = "dwave 1 \"SE\\SE_" + SEPlay_Outline[1] + ".WAV\"\n;;;" + SEPlay_Outline[2] + "\n"
                    print(line)
                else:
                    line = "dwave 1 \"SE\\SE_" + SEPlay_line[1] + ".WAV\"\n"

            elif Wait_line:
                line = "delay " + Wait_line[1] + "\n"

                
            txt += line

open(os.path.join(Game_path,'0.txt'), 'w', errors='ignore').write(txt)