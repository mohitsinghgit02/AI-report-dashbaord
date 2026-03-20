from app.services.reports.damage_stock.damage_stock_report import DamageStock
from app.services.reports.inventory_report import InventoryReport


REPORT_REGISTRY = {
    "damage_stock": DamageStock(),
    "inventory": InventoryReport(),
}
