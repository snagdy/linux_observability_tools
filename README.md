### LSOF Scraper

Used with `sudo lsof -F`

usage: lsof_scrape_f_flag.py [-h] [-full_cfg_file_path [FULL_CFG_FILE_PATH]]
                             [-display_option [DISPLAY_OPTION]]
                             [cfg_file_name] [infile]

positional arguments:
  cfg_file_name         REQUIRED: Pass file name of the field lookup config
                        JSON file in script directory, else use full file path
                        and set "full_cfg_file_path" optional argument to 1
                        instead.
  infile                REQUIRED: This is by default the data passed in using
                        STDIN for which a file object is created.

optional arguments:
  -h, --help            show this help message and exit
  -full_cfg_file_path [FULL_CFG_FILE_PATH]
                        Set to 1 when field lookup config JSON file is not in
                        the script directory, supply the full file path to
                        "cfg_file_name". Default is 0.
  -display_option [DISPLAY_OPTION]
                        Pass either "json" or "df" to get output to STDOUT as
                        JSON or a pandas.DataFrame object. Default is "json".

### SS Scraper

Used with `sudo ss -apne`
                        
usage: ss_scrape.py [-h] [-display_option [DISPLAY_OPTION]] [infile]

positional arguments:
  infile                Provide the data via a STDIN pipe.

optional arguments:
  -h, --help            show this help message and exit
  -display_option [DISPLAY_OPTION]
                        Specify JSON "json" or pandas.DataFrame "df" as
                        output. Default is "json".

### TCP Dump Scraper

Used with `sudo tcpdump -i <interface>`

usage: tcpdump_scrape.py [-h] [--display-option [DISPLAY_OPTION]] [infile]

positional arguments:
  infile                Pass this file in via a STDIN pipe.

optional arguments:
  -h, --help            show this help message and exit
  --display-option [DISPLAY_OPTION]
                        Specify "json" or "df" for JSON and DataFrame
                        respectively. Default is "json".
