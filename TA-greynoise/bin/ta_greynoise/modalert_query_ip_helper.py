# encoding = utf-8

def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example sends rest requests to some endpoint
    # response is a response object in python requests library
    response = helper.send_http_request("http://www.splunk.com", "GET", parameters=None,
                                        payload=None, headers=None, cookies=None, verify=True, cert=None, timeout=None, use_proxy=True)
    # get the response headers
    r_headers = response.headers
    # get the response body as text
    r_text = response.text
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = response.json()
    # get response cookies
    r_cookies = response.cookies
    # get redirect history
    historical_responses = response.history
    # get response status code
    r_status = response.status_code
    # check the response status, if the status is not sucessful, raise requests.HTTPError
    response.raise_for_status()


    # The following example gets the setup parameters and prints them to the log
    api_key = helper.get_global_setting("api_key")
    helper.log_info("api_key={}".format(api_key))
    index = helper.get_global_setting("index")
    helper.log_info("index={}".format(index))

    # The following example gets the alert action parameters and prints them to the log
    ip_address = helper.get_param("ip_address")
    helper.log_info("ip_address={}".format(ip_address))

    search_description = helper.get_param("search_description")
    helper.log_info("search_description={}".format(search_description))


    # The following example adds two sample events ("hello", "world")
    # and writes them to Splunk
    # NOTE: Call helper.writeevents() only once after all events
    # have been added
    helper.addevent("hello", sourcetype="sample_sourcetype")
    helper.addevent("world", sourcetype="sample_sourcetype")
    helper.writeevents(index="summary", host="localhost", source="localhost")

    # The following example gets the events that trigger the alert
    events = helper.get_events()
    for event in events:
        helper.log_info("event={}".format(event))

    # helper.settings is a dict that includes environment configuration
    # Example usage: helper.settings["server_uri"]
    helper.log_info("server_uri={}".format(helper.settings["server_uri"]))
    [sample_code_macro:end]
    """
    import json, re, sys
    
    helper.log_info("Alert action query_ip for Greynoise.io started.")
    
    proxy = helper.get_proxy()
    
    if proxy:
        use_proxy = True
    else:
        use_proxy = False
    
    
    
    #Get Global Parameters
    api_key = helper.get_global_setting("api_key")
    index_name = helper.get_global_setting("index")
    
    #Get Local Parameters
    ip_address = helper.get_param("ip_address")
    search_description = helper.get_param("search_description")
    
    #Create the URI String that looks for the domain
    url = 'https://api.greynoise.io/v1/query/ip'
    
    #Set the method
    method = "POST"
    
    #Create a heaer variable
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
        }
    
    #Check if is valid IPv4 Address
    regex_ip = re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", str(ip_address))
    
    #Check to see if API key is valid
    regex_apikey = re.match("^\w{32}$",str(api_key))
    
    if not regex_ip:
        helper.log_error("Invalid IPv4 Address passed, exiting")
        sys.exit()
    
    #Check API Key has been inserted
    if api_key:
        #Validate that the regex is valid for api_key
        if regex_apikey:
        payload_ip = 'ip=' + str(ip_address) + 'key='+str(api_key)
        #If the regex is not valid for api_key log an error an exit
        else:
            helper.log_error("Invalid api key passed, exiting")
        sys.exit()
    else:
        #If there is no api_key then just send the ip address
        payload_ip = 'ip=' + str(ip_address)
        
    
    #Make HTTP Request
    response = helper.send_http_request(url, method, parameters=None, payload=payload_ip, headers=header, cookies=None, verify=True, cert=None, timeout=30, use_proxy=use_proxy)

    #If 200 response
    if response.status_code == 200:
        #Log successfull request
        helper.log_info("Received 200 OK from greynoise.io for IP {}.".format(ip_address))
        
        #Add note information to JSON output
        json_load = response.json()
        json_load['requested_ip'] = ip_address
        json_load['search_description'] = search_description
        json_load['search_type'] = "Greynoise.io IP Search"
        
        #Convert output to JSON String
        json_data = json.dumps(json_load)
        
        #Add Event to Adaptive Response Framework
        helper.addevent(json_data, sourcetype="greynoiseio:json")
        try:
            #Try writing to the specified index in global settings
            helper.writeevents(source="greynoiseio", index=index_name, host="adaptive_response")
        except Exception as e:
            #If that fails write this as an exception
            helper.log_error("Error with writing event. Error Message:{}".format(e))

    else:        
        #If all fails then output an error message to the logging framework for passing onto greynoise.io
        helper.log_error("Error with request of {}, response code of {} and content of {}.  Please pass this information onto greynoise.io if you believe this is incorrect.".format(domain,response.status_code,response.json()))

    # TODO: Implement your alert action logic here
    return 0
