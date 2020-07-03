while :
do
	python3 src/discord_bot.py
	echo -e "\e[31mDiscod Bot Died.\e[0m"
	echo "`date` - Bot died." >> GEEK.log
	echo -e "\e[32mRestarting...\e[0m"
	sleep 1
done
