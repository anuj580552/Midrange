#!/bin/bash
hostname -a > /tmp/wasJAVAversion.txt
ps -ef | grep java | grep -i websphere | grep -i wasusr | awk '{print $NF, $8}' >> /tmp/wasJAVAversion.txt
sed -i 's/\/appl\/was\///g' /tmp/wasJAVAversion.txt
sed -i 's/\/appl\/was\///g' /tmp/wasJAVAversion.txt
sed -i 's/\/bin\/java//g' /tmp/wasJAVAversion.txt
sed -e :a -e ';$!N;s/\n/ /;ta' /tmp/wasJAVAversion.txt > /tmp/wasJAVAversion.res
