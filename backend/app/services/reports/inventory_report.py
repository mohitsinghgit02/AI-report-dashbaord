from app.services.reports.base_report import BaseReport


class InventoryReport(BaseReport):

    def analyze(self, df):

        overview = {"rows": len(df), "columns": list(df.columns)}

        kpis = [
            {"name": "Total Products", "value": len(df)},
        ]

        charts = []

        return {"overview": overview, "kpis": kpis, "charts": charts}

    def build_prompt(self, analysis, lang):

        return f"""
        Create an inventory dashboard in {lang}

        Data Summary:
        {analysis}
        """
