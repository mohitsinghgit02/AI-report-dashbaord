from app.services.reports.base_report import BaseReport
from app.services.reports.damage_stock.pandas_analyzer import analyze_data
from app.services.reports.damage_stock.prompt_builder import build_prompt


class DamageStock(BaseReport):

    def analyze(self, df):
        return analyze_data(df)

    def build_prompt(self, analysis, lang):
        return build_prompt(analysis, lang)
