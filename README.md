# Online toiletpaper

This is the software I made to easily extract data for my research.

To use the program, because it does not yet have a command line interface,
change WORDS and TIMEFRAME in the main function to your liking (do not change if you want my exact results), and upload the program to karora with the following command:

scp /home/user/Documents/informatiekunde/intresmeth/final_project/program/analyzer.py s1234567@karora.let.rug.nl:~/

And ofcourse adjust the file paths and the student number to your needs and situation.

You can then log into karora, run the program with the following command, and wait (a long time). 

python3 analyzer.py

I have added a progress bar to see the progress.
At the end of the program, the encountered errors will be printed in the terminal. If this is a significant amount, please check for errors.

If you want to download the output files from karora, use the scp command the other way around:

(do not forget to use escape characters for the ':' in the time!)

scp s1234567@karora.let.rug.nl:~/path_to_output/output.txt /home/user/Documents/informatiekunde/intresmeth/final_project/program/

And again: ofcourse adjust the file paths and the student number to your needs and situation.

You can then use the jupyter notebook to see the graphs of your output. 
(don't forget to change te filepath to your file!)
