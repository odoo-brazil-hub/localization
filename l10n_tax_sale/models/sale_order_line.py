# -*- coding: utf-8 -*-
# Part of Odoo Brazil Hub. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = ['sale.order.line', 'analytic.mixin', 'tax.mapper.mixin']

    @api.depends('product_id', 'company_id')
    def _compute_tax_ids(self):
        for line in self:
            if line.product_id and (taxes := line._get_sale_taxes()):
                line.tax_ids = taxes
            else:
                super()._compute_tax_ids()

    def _get_sale_taxes(self):
        self.ensure_one()
        filters = self._get_taxes_filter()
        return self.get_tax_ids(
            partner=self.order_id.partner_id.commercial_partner_id,
            using_on='sale',
            tags=self.product_id.sale_tax_tag_ids or None,
            **filters
        )

    def _get_tag_line_domain(self, partner, using_on, tags=None, **kwargs):
        """
        Override to handle 'product_type' filter: allow tags with matching
        product_type OR empty product_type (meaning the tag applies to all).
        """
        product_type = kwargs.pop('product_type', None)
        domain = super()._get_tag_line_domain(partner, using_on, tags=tags, **kwargs)
        if product_type:
            domain.append('|')
            domain.append(('product_type', '=', product_type))
            domain.append(('product_type', '=', False))
        return domain

    def _get_taxes_filter(self):
        """
        Build a dictionary of pre-filters to be applied as **kwargs
        to _get_tax_ids().

        Keys must correspond to field names on tax.mapper.line.
        Override this method in submodules to add new filter conditions.

        :return: dict with field_name -> value mappings
        """
        self.ensure_one()
        return {
            'product_type': self.product_id.product_tmpl_id.type,
        }
    
    
