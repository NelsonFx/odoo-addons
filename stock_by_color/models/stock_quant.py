from odoo import models, fields, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    color_value = fields.Char(
        string="Color",
        compute="_compute_color_value",
        store=True,
    )

    @api.depends(
        'product_id.product_template_attribute_value_ids',
        'product_id.product_template_attribute_value_ids.ptav_active',
        'product_id.product_template_attribute_value_ids.product_attribute_value_id.name',
    )
    def _compute_color_value(self):
        for quant in self:
            color_attr = quant.product_id.product_template_attribute_value_ids.filtered(
                lambda p: p.ptav_active
                and p.attribute_id.name
                and p.attribute_id.name.lower() == 'color'
            )
            quant.color_value = color_attr[0].name.title() if color_attr else "Sin Color"
