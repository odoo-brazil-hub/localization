# -*- coding: utf-8 -*-
# Part of Odoo Brazil Hub. See LICENSE file for full copyright and licensing details.
{
    'name': 'Taxes - Sale Integration',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Integrates tax mappers with sale orders for automatic tax determination',
    'description': """
        Taxes - Sale Integration
        ====================================
        This module extends the Brazil Tax Mapper functionality to integrate
        with sale orders, automatically determining taxes for sale order lines
        based on customizable mapper conditions.

        Features:
        - Automatic tax computation on sale order lines based on tax mappers
        - Extends the 'Used In' field to include the 'Sales' context
        - Seamlessly works with the base l10n_br_tax_mapper module
    """,
    'author': 'Mackilem Van der Laan - Odoo Brazil Hub',
    'website': 'https://github.com/odoo-brazil-hub',
    'depends': [
        'l10n_tax_mapper',
        'sale',
    ],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3',
}
