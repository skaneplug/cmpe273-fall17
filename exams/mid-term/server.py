'''
################################## server.py #############################
# Encoder Server encodes string and decodes integer back to the original
# string. It can be used to generate unique id for a given URL.
################################## server.py #############################
'''
import time
import grpc
import encoder_pb2
import encoder_pb2_grpc

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class EncoderServer(encoder_pb2.EncoderServicer):
    '''
    EncoderServer is the main class that handles encoding and decoding.
    '''

    def encode_helper(self, url):
        id = 0
        for i in range(0, len(url)):
            if ('a' <= url[i]) and (url[i] <= 'z'):
                id = id*62 + url[i] - 'a'
            if ('A' <= url[i]) and (url[i] <= 'Z'):
                id = id*62 + url[i] - 'A' + 26
            if ('0' <= url[i]) and (url[i] <= '9'):
                id = id*62 + url[i] - '0' + 52
        return id

    def decode_helper(self, id):
        id = int(id)
        url = ""
        map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        while id > 0:
            url = url + str(map[id % 62])
            id = id / 62
        return url[::-1]

    def __init__(self):
        print("init")


    def encode(self, request, context):
        '''
        :return: encoder_pb2.EncodeResponse
        '''
        # TODO
        print("Encode:\n", request)
        _id = self.encode_helper(str(request.url))
        return encoder_pb2.EncodeResponse(id=_id)

    def decode(self, request, context):
        '''
        :return: encoder_pb2.DecodeResponse
        '''
        # TODO
        print("Decode:\n", request)
        _url = self.decode_helper(str(request.id))
        return encoder_pb2.DecodeResponse(url=_url)

def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    encoder_pb2_grpc.add_EncoderServicer_to_server(EncoderServer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)
