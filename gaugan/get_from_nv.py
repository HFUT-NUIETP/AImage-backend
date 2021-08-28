import base64
import os
import urllib.parse
import re
import time
import random
from pathlib import Path
import subprocess

URLS=['54.190.129.191:443','54.244.111.218:443','54.191.253.241:443']

class run_request ():
    '''
    send request to server
    rely on bash and curl
    '''
    def __init__(self, request, name):
        self.request = request
        self.name = name

    def run(self):
        # print(self.request)
        print("进入：" + self.name)
        self.tempfile_name = 'temp_%s.sh' % self.name
        with open(self.tempfile_name, 'w+') as f:
            f.write(self.request)
        if self.name.startswith('request1'):
            self.p = subprocess.Popen('bash %s' % self.tempfile_name, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
            print("正在运行:" + self.name)
            # self.p = None
            # os.system('bash %s' % self.tempfile_name)
        else:
            self.p = None
            os.system('bash %s' % self.tempfile_name)
            print("退出：" + self.name)

    def stop(self):
        if self.p is not None:
            self.p.kill()
        if os.path.exists(self.tempfile_name):
            os.remove(self.tempfile_name)
        print("退出：" + self.name)

def get_urls():
    return URLS

def generate_result_from_nv(input_file, output_file, url):
    print('Trying to get from nv')
    # 54.244.111.218:443
    # http://54.190.129.191:443
    template1 = r'''
    echo "Using proxy at $http_proxy"
    curl 'http://__URL__/nvidia_gaugan_submit_map' \
  -x 127.0.0.1:8889 \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Accept: */*' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4558.0 Safari/537.36 Edg/93.0.946.1' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'Origin: http://nvidia-research-mingyuliu.com' \
  -H 'Referer: http://nvidia-research-mingyuliu.com/' \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  -H 'Accept-Encoding: gzip, deflate' \
  --data-raw '__DATA__' \
  --compressed \
  --insecure'''
    template2 = r"""
    echo "Using proxy at $http_proxy"
    curl 'http://54.190.129.191:443/nvidia_gaugan_receive_image' \
  -x 127.0.0.1:8889 \
  -H 'Connection: keep-alive' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4558.0 Safari/537.36 Edg/93.0.946.1' \
  -H 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryEls912uuOpbLfYzg' \
  -H 'Accept: */*' \
  -H 'Origin: http://nvidia-research-mingyuliu.com' \
  -H 'Referer: http://nvidia-research-mingyuliu.com/' \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  -H 'Accept-Encoding: gzip, deflate' \
  --data-raw $'------WebKitFormBoundaryEls912uuOpbLfYzg\r\nContent-Disposition: form-data; name="name"\r\n\r\n__NAME__\r\n------WebKitFormBoundaryEls912uuOpbLfYzg\r\nContent-Disposition: form-data; name="style_name"\r\n\r\nrandom\r\n------WebKitFormBoundaryEls912uuOpbLfYzg--\r\n' \
  --compressed \
  --insecure \
  --output '__OUTPUT_FILE__' """

    img_in_base64 = ''
    with open(input_file, 'rb') as f:
        img_in = f.read()
        img_in_base64 = base64.b64encode(img_in)

    # print(str(img_in_base64, encoding = 'utf-8'))
    match_obj = re.match(r"b'(.*)'", str(img_in_base64))

    name = time.strftime('%Y/%-m/%-d', time.localtime()) + \
        ',' + str(int(time.time()) * 10000) + '-' + str(random.randint(100000000,999999999))
    params = {
        'imageBase64': 'data:image/png;base64,' + match_obj.group(1),
        # 'imageBase64' : 'data:image/png;base64,' + img_in_base64,
        'name': name
    }
    params_encode = urllib.parse.urlencode(params)
    print(params)

    request1 = template1.replace('__DATA__', params_encode).replace('__URL__',url)
    request2 = template2.replace('__NAME__', name).replace(
        '__OUTPUT_FILE__', output_file).replace('__URL__',url)

    th_req1 = run_request(request1, 'request1-'+name.split(',')[1])
    th_req2 = run_request(request2, 'request2-'+name.split(',')[1])

    th_req1.run()
    time.sleep(7)
    th_req2.run()

    th_req1.stop()
    th_req2.stop()

    # check result
    result_path = Path(output_file)
    if result_path.exists():
        size = os.path.getsize(result_path)
        if(size < 1000):
            print('Failed(small files, url:%s)' % url)
            return 1
        else:
            print('Test Passed')
            return 0
    else:
        print('Failed')
        return 1


if __name__ == '__main__':
    status = generate_result_from_nv('gaugan/images/input/restored_color_label/1.png', 'test_result.jpg',URLS[1])
    print(status)
    # os.remove('test_result.jpg')
