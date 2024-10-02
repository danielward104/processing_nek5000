module add ffmpeg

name=vertical_velocity
ext=.mov

ls -d */ > dirs.txt
rm my_list.txt                      2>/dev/null
cwd=$(pwd)

while read dirs;
do
    num=${#dirs}
    if test $num -eq 8 || test $num -eq 7; then
        echo file './'${dirs}'processing/'${name}${ext}'' >> my_list.txt
    fi
done < dirs.txt

ffmpeg -f concat -safe 0 -i my_list.txt -c copy ${name}${ext}

rm my_list.txt dirs.txt
