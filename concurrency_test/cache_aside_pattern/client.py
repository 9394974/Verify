import requests
import threading

from server import Session, Table, key, redis_client


class Client(object):

    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.base_url = "http://" + host + ":" + str(port)
        self.session = Session()
        self.origin_database_value = self.session.query(Table).\
            filter(Table.id == 1).\
            first().value

    def query(self):
        print "Query thread begin..."
        res = requests.get(self.base_url + "/query")
        print "Query get value : {}".format(res.content)

    def update(self):
        print "Update thread begin..."
        print "Update value {}".format(self.origin_database_value + 1)
        requests.get(self.base_url + "/update/" + str(self.origin_database_value + 1))
        print "Update over"

    def test_init(self):
        print "Concurrency test init..."
        print "Origin database value: {}".format(self.origin_database_value)

        query_thread = threading.Thread(target=self.query)
        update_thread = threading.Thread(target=self.update)
        query_thread.start()
        update_thread.start()

        update_thread.join()
        query_thread.join()

        print "Now Cache value : {}".format(redis_client.get(key))
        print "Now Database value: {}".format(Session().query(Table).
                                              filter(Table.id == 1).
                                              first().value)

if __name__ == '__main__':
    client = Client()
    client.test_init()