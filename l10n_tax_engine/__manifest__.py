# -*- coding: utf-8 -*-
# Part of Odoo Brazil Hub. See LICENSE file for full copyright and licensing details.
{
    'name': 'Tax Engine (Base)',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Base tax engine framework for localization-specific tax calculation',
    'description': """
        Tax Engine (Base)
        ==================
        This module provides the base framework for hooking localization-specific
        tax calculation engines into Odoo's standard tax mechanism.

        It extends ``account.tax`` with a ``compute_taxes_with_localization()``
        method that localization modules (e.g. l10n_br_tax_engine) can override
        to provide custom tax computation logic.

        Features:
        - Hooks into ``_get_tax_details()`` to intercept tax computation
        - Provides the abstract ``compute_taxes_with_localization()`` method
        - Serves as a dependency for localization tax engine modules
    """,
    'author': 'Mackilem Van der Laan - Odoo Brazil Hub',
    'website': 'https://github.com/odoo-brazil-hub',
    'depends': [
        'base',
        'account',
        'product',
    ],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
