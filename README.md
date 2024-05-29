# time_logger.py
The app reads the latest CSV file and generates time log files for all dates.

The latest CSV file is read from the data directory where files are sorted by file names. The CSV file is exported by the [aTimeLogger Pro](https://atimelogger.pro/) App.

The log files are generated in the output directory, and each file is for
each date.

Usage 1: Generate all log files for all dates read from the latest CSV file. 

```
python time_logger.py
```

Usage 2: Follow Usage 1 and display contents as multiple lines. 
```
python time_logger.py -m
```

Usage 3: Follow Usage 2 and display time taken of each item. 
```
python time_logger.py -m -t
```

Usage 4: Follow Usage 3 and display non-first lines with indent.
```
python time_logger.py -m -t --indent
``` 

Usage 5: Generate one log file for the given date from the latest CSV file.
```
python time_logger.py -d 2023-09-15
```

# watch_dog.py
The app triggers time_logger when detecting a file CSV created in a specific directory. The application is run in Mac.

Usage 1:
```
python watch_dog.py
```