from abc import ABC, abstractmethod


class BaseReport(ABC):

    @abstractmethod
    def analyze(self, df):
        pass

    @abstractmethod
    def build_prompt(self, analysis, lang):
        pass
