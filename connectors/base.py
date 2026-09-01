from abc import ABC, abstractmethod


class Connector(ABC):
    @abstractmethod
    def insert(self, data):
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, record_id):
        pass

    @abstractmethod
    def update(self, data):
        pass

    @abstractmethod
    def delete(self, record_id):
        pass

    @abstractmethod
    def count(self):
        pass

    @abstractmethod
    def begin_transaction(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def close(self):
        pass