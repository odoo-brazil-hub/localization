# -*- coding: utf-8 -*-
# Part of Odoo Brazil Hub. See LICENSE file for full copyright and licensing details.
{
    'name': 'Tax Mapper',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Map tax tags to products based on configurable conditions (country, state, city, partner)',
    'description': """
        Tax Mapper
        ==================
        This module allows you to control which taxes will be triggered for products
        in different contexts based on configurable tax mapper rules.

        Features:
        - Define tax mapper rules with country-specific contexts
        - Configure mapper lines with partner, country, state, city and country group filters
        - Use in sale and purchase contexts
    """,
    'author': 'Mackilem Van der Laan - Odoo Brazil Hub',
    'website': 'https://github.com/odoo-brazil-hub',
    'depends': [
        'base',
        'account',
        'product',
        'contacts',
        'base_address_extended',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/tax_mapper_views.xml',
        'views/product_template_views.xml',
        'views/actions_and_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
