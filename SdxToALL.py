#!/usr/bin/python

########################################################################################################
# ex: python SdxToAll.py XXX_Germany_OOO.sdx
###### python SdxToAll.py XXX_Austria_OOO.sdx XXX_Germany_OOO.sdx  #####
# python SdxToAll.py XXX_Germany_OOO.sdx
# python SdxToAll.py GermanChannels.sdx                                                           #
#  or python SdxToXml.py GermanChannels.sdx AAA_Austria_BBB.sdx                                       #
#     output will be sat_germany.txt sat_austria.txt dvbt_scan_maps_cfg.xml and dvbc_scan_maps_cfg.xml #
########################################################################################################

import sys

if len(sys.argv) > 3:
    print("Argc wrong! len(sys.argv) = %d") % (len(sys.argv))
    exit(0)

if len(sys.argv) == 2:
    infile1 = sys.argv[1]
    fpIn1 = open(infile1, "r")
elif len(sys.argv) == 3:
    infile1, infile2 = sys.argv[1], sys.argv[2]
    fpIn1 = open(infile1, "r")
    fpIn2 = open(infile2, "r")

outfileXmlDVBT = "dvbt_scan_maps_cfg.xml"
outfileXmlDVBC = "dvbc_scan_maps_cfg.xml"
fpOutXmlDVBT = open(outfileXmlDVBT, "w")
fpOutXmlDVBC = open(outfileXmlDVBC, "w")

outline = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<configuration version=\"1\">\n    <F_sorting_rank>\n"
print(outline)
fpOutXmlDVBT.write(outline)
fpOutXmlDVBC.write(outline)

for i in range(2):
    if (sys.argv[i+1].find("Germany")) >= 0:
        country = "DEU"
        outfileTxt = "sat_germany.txt"
        fpOutTxt = open(outfileTxt, "w")
    elif (sys.argv[i+1].find("Austria")) >= 0:
        country = "AUT"
        outfileTxt = "sat_austria.txt"
        fpOutTxt = open(outfileTxt, "w")

    outline = "        <country name=\"%s\">\n" % (country)
    print(outline)
    fpOutXmlDVBT.write(outline)
    fpOutXmlDVBC.write(outline)


    number = 1

    if i == 0:
        line = fpIn1.readline()
    elif i == 1:
        line = fpIn2.readline()

    while line:
        prefix = line[0:7]
        if prefix != "SATCODX":
            print("no SATCODX prefix, return!")
            break
        sat_name = line[10:28]
        temp1 = sat_name.split('(',1)
        #print(temp1[1])
        temp2 = temp1[1].split(')',1)
        #print(temp2[0])
        temp3 = temp2[0].split('.',1)
        orbit = temp3[0]+temp3[1][0]
        position = temp3[1][1]
        #print(orbit)
        #print(position)

        valid_symbols = "+-.()/&!',"
        svc_name1 = ''
        svc_name2 = ''
        svc_name1 = line[43:51]
        if svc_name1:
#            svc_name1 = svc_name1.strip()
            svc_name2 = line[115:132]
#            if svc_name2:
#                svc_name2 = svc_name2.strip()
        svc_name = svc_name1 + svc_name2
        new_svc_name = ''
        for c in svc_name:
            if c.isalpha():
                #print c
                new_svc_name += c
            elif c.isdigit():
                    #print c
                new_svc_name += c
            elif c.isspace():
                    #print c
                new_svc_name += c
            elif c in valid_symbols:
                new_svc_name += c

        sid = (int(line[87:92]))
        nid = (int(line[92:97]))
        tsid = (int(line[97:102]))

        hex_sid = hex(int(line[87:92]))
        hex_nid = hex(int(line[92:97]))
        hex_tsid = hex(int(line[97:102]))

        TXToutline = "%d,%s,%s,%s,%s,%s,%s\n" % (number, orbit, position, hex_nid, hex_tsid, hex_sid, new_svc_name)
        #print(TXToutline)
        fpOutTxt.write(TXToutline)
        number += 1

        outline = "            <rank name=\"%27s\" on_id=\"%8d\"  ts_id=\"%8d\"   svc_id=\"%8d\" />\n" % (new_svc_name, nid, tsid, sid)
        print(outline)
        fpOutXmlDVBT.write(outline)
        fpOutXmlDVBC.write(outline)

        if i == 0:
            line = fpIn1.readline()
        elif i == 1:
            line = fpIn2.readline()
    outline = "        </country>\n"
    print(outline)
    fpOutXmlDVBT.write(outline)
    fpOutXmlDVBC.write(outline)
    if len(sys.argv) == 2:
        break

outline = "    </F_sorting_rank>\n</configuration>"
print(outline)
fpOutXmlDVBT.write(outline)
fpOutXmlDVBC.write(outline)

fpIn1.close()
if len(sys.argv) == 4:
    fpIn2.close()
fpOutXmlDVBT.close()
fpOutXmlDVBC.close()
fpOutTxt.close()