# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Account Tax Tags',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Control which taxes are triggered for products in different contexts',
    'description': """
        Account Tax Tags
        =================
        This module allows you to control which taxes will be triggered for products
        in different contexts (sales/purchases) based on tags.

        Features:
        - Define tax tags with country-specific contexts
        - Configure tag lines with partner, zip range, country, state, city and country group filters
        - Use in both sale and purchase contexts
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'base',
        'account',
        'contacts',
        'base_address_extended',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/actions_and_menus.xml',
        'views/account_tax_tag_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
