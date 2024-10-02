ls -d */ > dirs.txt
cwd=$(pwd)

while read dirs;
do
    num=${#dirs}
    if test $num -eq 8; then

        cp ./processing_scripts/postProcess.py $dirs

    fi
done < dirs.txt

rm dirs.txt
