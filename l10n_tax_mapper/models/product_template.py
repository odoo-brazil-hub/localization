# -*- coding: utf-8 -*-
# Part of Odoo Brazil Hub. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_tax_tag_ids = fields.Many2many(
        comodel_name='tax.mapper',
        relation='product_template_sale_tax_mapper_rel',
        string='Sale Tax Tags',
        domain="[('using_on', '=', 'sale'), '|', ('product_type', '=', type), ('product_type', '=', False)]",
        help='Optional Tax tags to apply in sale contexts',
    )
    purchase_tax_tag_ids = fields.Many2many(
        comodel_name='tax.mapper',
        relation='product_template_purchase_tax_mapper_rel',
        string='Purchase Tax Tags',
        domain="[('using_on', '=', 'purchase'), '|', ('product_type', '=', type), ('product_type', '=', False)]",
        help='Optional Tax tags to apply in purchase contexts',
    )
