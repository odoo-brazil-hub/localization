# -*- coding: utf-8 -*-
# Part of Odoo Brazil Hub. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    def _get_tax_details(
        self,
        price_unit,
        quantity,
        precision_rounding=0.01,
        rounding_method='round_per_line',
        product=None,
        product_uom=None,
        special_mode=False,
        manual_tax_amounts=None,
        filter_tax_function=None,
        ):

        mapped_taxes = self.compute_taxes_with_localization(
            price_unit,
            quantity,
            precision_rounding,
            rounding_method,
            product,
            product_uom,
            special_mode,
            manual_tax_amounts,
            filter_tax_function,
        )

        return mapped_taxes

    def compute_taxes_with_localization(
        self,
        price_unit,
        quantity,
        precision_rounding=0.01,
        rounding_method='round_per_line',
        product=None,
        product_uom=None,
        special_mode=False,
        manual_tax_amounts=None,
        filter_tax_function=None,
    ):
        """
            :return: A dict containing:
                'evaluation_context':       The evaluation_context parameter.
                'taxes_data':               A list of dictionaries, one per tax containing:
                    'tax':                      The tax record.
                    'base':                     The base amount of this tax.
                    'tax_amount':               The tax amount of this tax.
                'total_excluded':           The total without tax.
                'total_included':           The total with tax.
        """
        return {}