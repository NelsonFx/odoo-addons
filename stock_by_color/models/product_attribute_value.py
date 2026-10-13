from odoo import models


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    def write(self, vals):
        res = super().write(vals)
        if 'name' in vals or 'attribute_id' in vals:
            self._refresh_quant_color_value()
        return res

    def _refresh_quant_color_value(self):
        """Recalcula el Color de los quants cuyos productos usan estos valores."""
        quants = self.env['stock.quant'].sudo().search([
            (
                'product_id.product_template_attribute_value_ids.product_attribute_value_id',
                'in',
                self.ids,
            ),
        ])
        if quants:
            quants._compute_color_value()
