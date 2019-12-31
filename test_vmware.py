import pytest
import yaml
import requests

class TestVmWareClass:

    @pytest.fixture
    def workload_config(self):

        #loading workload_config file
        with open('workload_config.yaml') as f:
    
            data = yaml.load(f, Loader=yaml.FullLoader)
            print(data, self)
            print("here", self)

            return data

    def test_workload(self, workload_config):

        print(workload_config, self)
        print("here", self)

        #parsing dictionary created from workload_config file to get specific workload info
        print("name", workload_config.get("name"))
        
        print("input body", workload_config.get("input").get("body"))

        #create and send http request based on workload_config
        host = workload_config.get("entity").get("host")
        port = workload_config.get("entity").get("port")
        path = workload_config.get("input").get("path")
        
        url =  "http://" + host + ":" + str(port) + path
        print("URL" , url)
        
        contentType = workload_config.get("input").get("contentType")
        headers = {'content-type': contentType}
        print("Headers", headers)

        payload = workload_config.get("input").get("params")
        print("Params", payload)

        #skipping payload for the time being
        #response = requests.get(url, params=payload, headers=headers)
        response = requests.get(url, headers=headers)

        #compare actual and expected response code
        actualResponseCode = response.status_code
        expectedResponseCode = workload_config.get("output").get("http").get("status")
        print("Response Status Code (expected,actual)", expectedResponseCode, actualResponseCode)
        assert actualResponseCode == expectedResponseCode

        #compare actual and expected content type
        actualContentType = response.headers.get("content-type")
        expectedContentType = workload_config.get("output").get("http").get("contentType")
        print("Response content type(expected,actual)", expectedContentType, actualContentType)
        assert actualContentType == expectedContentType

        #compare actual and expected run time
        actualRuntime = 0
        if response.headers.get("x-runtime") != None :
            actualRuntime = int(response.headers.get("x-runtime"))
        expectedRunTime = int(workload_config.get("output").get("tcp").get("latency").get("threshold"))
        print("Run Time (expecetd,actual)", expectedRunTime, actualRuntime)
        assert actualRuntime <= expectedRunTime
