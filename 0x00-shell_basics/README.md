The first file current-working directory prints the current working directory of the shell.
The second file 1-listit lists all files and directory in the current working directory.
The third file 2-bringmehome takes the user to the home directory.
The fourth file 3-listfiles list all files in long format.
The fifth file 4-listmorefiles list all files(hidden inclusive) in long format.
The sixth file 5-listfilesdigitonly list all files in digits.
The seventh file make a folder in another directory
The eigth moves a file to another directory
The ninth deletes a file 
The tenth deletes a directory 
The eleventh changes directory to previous directory
12 Write a script that prints the type of the file named iamafile. The file iamafile will be in the /tmp directory when we will run your script.
13 Create a symbolic link to /bin/ls, named "__ls__" The symbolic link should be created in the current working directory.
14 Create a script that copies all the HTML files from the current working directory to the parent of the working directory, but only copy files that did not exist in the parent of the working directory or were newer than the versions in the parent of the working directory.
	You can consider that all HTML files have the extension .html
15 Create a script that moves all files beginning with an uppercase letter to the directory /tmp/u.
	You can assume that the directory /tmp/u will exist when we will run your script
16 Create a script that deletes all files in the current working directory that end with the character ~.
17 Create a script that creates the directories welcome/, welcome/to/ and welcome/to/school in the current directory.
	You are only allowed to use two spaces (and lines) in your script, not more.
18 Write a command that lists all the files and directories of the current directory, separated by commas (,).
	Directory names should end with a slash (/)
	Files and directories starting with a dot (.) should be listed
	The listing should be alpha ordered, except for the directories . and .. which should be listed at the very beginning
	Only digits and letters are used to sort; Digits should come first
	You can assume that all the files we will test with will have at least one letter or one digit
	The listing should end with a new line
19 Create a magic file school.mgc that can be used with the command file to detect School data files. School data files always contain the string SCHOOL at offset 0.
