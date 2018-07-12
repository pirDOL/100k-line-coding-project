import pickle

if __name__ == '__main__':
    s_send = {'id': 1, 'name': 'liduo04'}
    byte_stream = pickle.dumps(s_send)

    s_recv = pickle.loads(byte_stream)
    print s_send, s_recv
