. ~/.profile
xrdb merge ~/.Xresources

xbindkeys &

sleep 1

~jude/bin/touchscreen.sh disable

syndaemon -d -t -i 1
exec openbox-session 

