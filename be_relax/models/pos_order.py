from odoo import api, models, fields, _
from odoo.exceptions import UserError

class Salesreport(models.Model):
    _inherit = 'pos.order'

    total_qty = fields.Float("Qty")
    df_amount = fields.Float("DF")
    dp_amount = fields.Float("DP")
    discount_amount = fields.Float("Discount")
    total_excl_tax = fields.Float("Total(excl tax)")
    compute_sales_report = fields.Boolean(compute='compute_sales_data')

    def compute_sales_data(self):
        for rec in self:
            total_qty = df_amount = dp_amount = discount_amount = tip_amount =0.0
            for line in rec.lines:
                if line.product_id.detailed_type == 'service':
                    df_amount += line.price_subtotal
                    total_qty += line.qty
                if line.product_id.detailed_type == 'product':
                    dp_amount += line.price_subtotal
                    total_qty += line.qty

                discount_amount += ((line.price_unit * line.qty) * line.discount/100)
            rec.discount_amount = discount_amount
            rec.total_qty = total_qty
            rec.total_excl_tax = rec.amount_total - rec.amount_tax
            rec.df_amount = df_amount
            rec.dp_amount = dp_amount
            rec.compute_sales_report = True
