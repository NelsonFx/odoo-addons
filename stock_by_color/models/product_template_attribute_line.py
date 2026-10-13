from odoo import api, models


class ProductTemplateAttributeLine(models.Model):
    _inherit = 'product.template.attribute.line'

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines._refresh_quant_color_value(lines.product_tmpl_id)
        return lines

    def write(self, vals):
        res = super().write(vals)
        if 'value_ids' in vals or 'attribute_id' in vals:
            self._refresh_quant_color_value(self.product_tmpl_id)
        return res

    def unlink(self):
        templates = self.product_tmpl_id
        res = super().unlink()
        self._refresh_quant_color_value(templates)
        return res

    @api.model
    def _refresh_quant_color_value(self, templates):
        """Recalcula el Color de los quants de los productos de estas plantillas."""
        if not templates:
            return
        quants = self.env['stock.quant'].sudo().search([
            ('product_tmpl_id', 'in', templates.ids),
        ])
        if quants:
            quants._compute_color_value()
