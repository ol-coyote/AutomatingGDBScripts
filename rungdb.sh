#!/bin/bash
current_time=$(date "+%Y.%m.%d-%H.%M.%S");
echo "Current_time: $current_time";
dumppath="/media/sf_vm_share/dumptxt/";
btfile=$dumppath"btdump"$current_time".log";
stackfile=$dumppath"stackdump"$current_time".log";

echo "BTFILE: $btfile";
echo " STFILE: $stackfile";
gdb --core $1 -x btdump 2>&1 > btdump.log;
gdb --core $1 -x stackdump 2>&1 > stackdump.log;
cp btdump.log "$btfile";
cp stackdump.log $stackfile;

if [ -f $btfile ]; then
    echo "$btfile created successfully!"
else
    echo "$btfile not created successfully!"
fi

if [ -f $stackfile ]; then
    echo "$stackfile created successfully!"
else
    echo "$stackfile not created succesfully!"
fi

rm btdump.log && rm stackdump.log;
echo "Exiting!"
