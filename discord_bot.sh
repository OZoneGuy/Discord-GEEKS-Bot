while :
do
	python3 discord_bot.py
	echo -e "\e[31mDiscod Bot Died.\e[0m"
	date >> discord_bot.log
	echo -e "\e[32mRestarting...\e[0m"
	sleep 1
done
