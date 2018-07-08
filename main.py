import requests

class Requester:
    def __init__(self):
        #initializing requests
        self.get_res = requests.get('https://httpbin.org/get')
        self.head_res = requests.head('https://httpbin.org/get')
        self.post_res = requests.post('https://httpbin.org/get',
                                     data = {'foo':'bar', '228':1337})
        self.put_res = requests.put('https://httpbin.org/get',
                                   data = {'foo':'bar', '228':1337})

    def display(self):
        #display results of requests
        res = """
        Content of GET request: {0};
        Status of HEAD request: {1};
        Data of POST and PUT requests: {2}, {3};
        """
        return res.format(self.get_res.content, self.head_res.status_code,
                         self.post_res.request.body, self.put_res.request.body)

if __name__ == '__main__':
    r = Requester()
    print(r.display())
