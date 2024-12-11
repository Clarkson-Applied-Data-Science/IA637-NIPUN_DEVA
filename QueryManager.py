import configparser

class QueryManager:
    def __init__(self, file_path='static/queries.properties'):
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(file_path)

    def get_query(self, query_name):
        return self.config['queries'].get(query_name)

