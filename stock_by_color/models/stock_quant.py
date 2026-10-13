from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    color_value = fields.Char(string="Color", compute="_compute_color_value", store=True)

    @api.depends('product_id.product_template_attribute_value_ids')
    def _compute_color_value(self):
        for quant in self:
            # LOG 1: Identificación
            _logger.info(f"--- INICIO DEBUG | Quant ID: {quant.id} | Producto: {quant.product_id.name} ---")
            
            # LOG 2: Listar todos los atributos encontrados en el producto
            todos = quant.product_id.product_template_attribute_value_ids
            _logger.info(f"DEBUG: Atributos hallados en producto: {[p.name for p in todos]}")
            
            # LOG 3: Filtrar color
            color_attr = todos.filtered(
                lambda p: p.attribute_id.name and p.attribute_id.name.lower() == 'color'
            )
            
            if color_attr:
                valor = color_attr[0].name.title()
                _logger.info(f"DEBUG: Color filtrado detectado: {valor}")
                quant.color_value = valor
            else:
                _logger.info(f"DEBUG: No se encontró ningún atributo 'Color'.")
                quant.color_value = "Sin Color"
            
            _logger.info(f"--- FIN DEBUG | Quant ID: {quant.id} ---")