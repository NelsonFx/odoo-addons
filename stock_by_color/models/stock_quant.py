from odoo import models, fields, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    color_value = fields.Char(string="Color", compute="_compute_color_value", store=True)
    tipo_value = fields.Char(string="Tipo", compute="_compute_tipo_value", store=True)
    marca_value = fields.Char(string="Marca", compute="_compute_marca_value", store=True)

    @staticmethod
    def _active_attr_value(product, attr_name):
        """Primer valor activo del atributo `attr_name` (sin distinguir mayúsculas)."""
        values = product.product_template_attribute_value_ids.filtered(
            lambda p: p.ptav_active
            and p.attribute_id.name
            and p.attribute_id.name.strip().lower() == attr_name
        )
        return values[0].name if values else False

    @api.depends(
        'product_id.product_template_attribute_value_ids',
        'product_id.product_template_attribute_value_ids.ptav_active',
        'product_id.product_template_attribute_value_ids.product_attribute_value_id.name',
    )
    def _compute_color_value(self):
        for quant in self:
            value = self._active_attr_value(quant.product_id, 'color')
            quant.color_value = value.title() if value else "Sin Color"

    @api.depends(
        'product_id.product_template_attribute_value_ids',
        'product_id.product_template_attribute_value_ids.ptav_active',
        'product_id.product_template_attribute_value_ids.product_attribute_value_id.name',
    )
    def _compute_tipo_value(self):
        for quant in self:
            quant.tipo_value = self._active_attr_value(quant.product_id, 'tipo de filamento') or "Sin Tipo"

    @api.depends(
        'product_id.product_template_attribute_value_ids',
        'product_id.product_template_attribute_value_ids.ptav_active',
        'product_id.product_template_attribute_value_ids.product_attribute_value_id.name',
    )
    def _compute_marca_value(self):
        for quant in self:
            quant.marca_value = self._active_attr_value(quant.product_id, 'brand') or "Sin Marca"

    def _recompute_filament_fields(self):
        """Fuerza el recálculo de Color, Tipo y Marca."""
        self._compute_color_value()
        self._compute_tipo_value()
        self._compute_marca_value()
