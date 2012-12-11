screen -X -S mcserver -p 0 -X stuff "say going down! $(printf '\r')"
sleep 5
screen -X -S mcserver -p 0 -X stuff "stop $(printf '\r')"
