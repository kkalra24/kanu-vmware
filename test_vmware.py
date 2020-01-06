import pytest
import yaml
import requests
import logging

class TestVmWareClass:
    
    @pytest.fixture(scope="module", autouse=True)
    def setup_logger(self):
        self.mylogger = logging.getLogger()
        

    @pytest.fixture(scope="module")
    def workload_config(self):

        #loading workload_config file
        f = open('workload_config.yaml')
    
        data = yaml.load(f, Loader=yaml.FullLoader)
        self.mylogger.debug(data)

        yield data
        f.close()
    
    @pytest.fixture(scope="module")    
    def make_http_request(self, workload_config):
    
      response = None
      
      try:
        self.mylogger.debug(workload_config)

        #parsing dictionary created from workload_config file to get specific workload info
        
        #create and send http request based on workload_config
        host = workload_config.get("entity").get("host")
        port = workload_config.get("entity").get("port")
        path = workload_config.get("input").get("path")
        
        url =  "http://" + host + ":" + str(port) + path
        self.mylogger.debug("URL: " + url)

        #overload with google for the time being
        #url = "http://www.google.com:80/"
        
        contentType = workload_config.get("input").get("contentType")
        headers = {'content-type': contentType}
        self.mylogger.debug(headers)

        payload = workload_config.get("input").get("params")
        self.mylogger.debug(payload)
        
        tcpLatencyThreshold = int(workload_config.get("output").get("tcp").get("latency").get("threshold"))

        #skipping payload for the time being
        #response = requests.get(url, params=payload, headers=headers)
        response = requests.get(url, headers=headers, timeout=tcpLatencyThreshold/1000)
        return response
        
      except Timeout as timex:
        logging.getLogger().debug("Timeout Error in getting http response ")
        logging.getLogger().debug(timex)
        print("Timeout error", self)
      except Exception as anex:
        logging.getLogger().debug("Another Error in getting http response ")
        logging.getLogger().debug(anex)
        print("Other error", self)
      finally:
        return response
        

    def test_workload(self, workload_config, make_http_request):
    
    
        response = make_http_request
        
        assert response != None

        actualResponseCode = response.status_code
        expectedResponseCode = workload_config.get("output").get("http").get("status")
        logging.getLogger().debug(expectedResponseCode)
        logging.getLogger().debug(actualResponseCode)
        assert actualResponseCode == expectedResponseCode

        actualContentType = response.headers.get("content-type")
        expectedContentType = workload_config.get("output").get("http").get("contentType")
        logging.getLogger().debug(expectedContentType)
        logging.getLogger().debug(actualContentType)
        assert expectedContentType in actualContentType

        #actualRuntime = 0
        #if response.headers.get("x-runtime") != None :
        #    actualRuntime = int(response.headers.get("x-runtime"))
        #expectedRunTime = int(workload_config.get("output").get("tcp").get("latency").get("threshold"))
        #self.mylogger.debug("Run Time (expecetd,actual)", expectedRunTime, actualRuntime)
        #assert actualRuntime <= expectedRunTime

