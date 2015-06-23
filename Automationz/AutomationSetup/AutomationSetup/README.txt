First run Setup.py from console using the command:
	python Setup.py

If you want to do android automation then please do follow the following steps:
	1. Set the ADT_HOME and ANDROID_HOME in environment variable.
	2. ADT_HOME and ANDROID_HOME both should be the default android sdk root directory
	3. Set ANT_HOME in enviroment variables.(default ANT_HOME would be C:\Python27\Lib\site-packages\{apache-ant folder name}
	4. Set MAVEN_HOME in enviroment variables.(default MAVEN_HOME would be C:\Python27\Lib\site-packages\{apache-maven folder name}

	5. Now add this following line to path variable.
	%ADT_HOME%\tools;%ADT_HOME%\platform-tools;%ANT_HOME%\bin;%MAVEN_HOME%\bin;
	6. Add a USER Variable name MAVEN_OPTS = -Xms256m -Xmx512m