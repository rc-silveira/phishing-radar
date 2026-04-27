from abc import ABC, abstractmethod


class LlmClient(ABC):
    @abstractmethod
    def client_communication(self,message:list [str], model: str) -> str:
        ...