# Greynoise.io Add on For Splunk

### Overview
This app was created to allow users of Splunk to programatically query Greynoise.io API.  This is performed by leveraging the Adaptive Response Framework.

### Installation Instructions

As Alert Action
 1. Install the Splunk Add on For CIM https://splunkbase.splunk.com/app/1621/
 2. Git clone this repo and install the Add on to the following server types:
	 Indexer, Search Head
 3. After installation restart the Indexer and Search Head
 4. If you have a proxy visit https://yoursplunkserver/en-GB/app/TA-greynoise/configuration#proxy and configure the proxy settings
 5. Configure the destination index that this data will be stored in by visiting https://yoursplunkserver/en-GB/app/TA-greynoise/configuration#add-on-settings
 6. Write a search that generates an IP address. Such as index=firewall | stats count by src_ip | head 10
 7. Click Save as Alert
 8. Under Triggers click Add Action and select Query IP.
 9. Enter field you want to search against greynoise with '$' preceding and following, for example $src_ip$
 10. Data is stored in  the index specified in Step 5.

### Issues, Bugs, Features ;)
Version 1.0.0 - No API Key functionality - Fixed

Hit me up on twitter (@)MickeyPerre for any issues, bugs and features.

### Release Notes
1.1.0 - Added API Key support, Validate that IP addresses and API Keys are valid.
1.0.0 - Initial Release, supports Alert Action / Adaptive Response to search an IP Address.  API Key option is present but not working.  Will add in next release once api key is received

