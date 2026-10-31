# PHPOOMET
PHP Out of Memory Exploitation Test
How to use:

python .\phpVulnTest-v2.py --url=http://localhost --file-size=50

file-size is in MB
The script will create chunks of files of 1024 bytes from the total file size desired, then send the HTTP request to the Web Server URL.
