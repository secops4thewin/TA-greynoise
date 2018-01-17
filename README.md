# Greynoise.io Add on For Splunk

### Overview
This app was created to allow users of Splunk to programatically query Greynoise.io API.  This is performed by leveraging the Adaptive Response Framework.

### Installation Instructions

 1. Install the Splunk Add on For CIM https://splunkbase.splunk.com/app/1621/
 2. Git clone this repo and install the Add on to the following server types:
	 Indexer, Search Head
 3. After installation restart the Indexer and Search Head
 4. If you have a proxy visit https://yoursplunkserver/en-GB/app/TA-greynoise/configuration#proxy and configure the proxy settings
 5. Configure the destination index that this data will be stored in by visiting https://yoursplunkserver/en-GB/app/TA-greynoise/configuration#add-on-settings

### Issues, Bugs, Features ;)
Version 0.0.1 - No API Key functionality

Hit me up on twitter (@)MickeyPerre for any issues, bugs and features.

### Release Notes
0.0.1 - Initial Release, supports Alert Action / Adaptive Response to search an IP Address.  API Key option is present but not working.  Will add in next release once api key is received
