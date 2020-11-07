while :
do
    docker start geeks-bot
    echo -e "\e[31mDiscod Bot Died.\e[0m"
    echo "`date` - Bot died." >> data/GEEK.log
    echo -e "\e[32mRestarting...\e[0m"
    sleep 1
done
