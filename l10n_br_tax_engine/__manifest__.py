# -*- coding: utf-8 -*-
# Part of Odoo Brazil Hub. See LICENSE file for full copyright and licensing details.
{
    'name': 'Brazilian Tax Engine',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Brazilian tax calculation using tributus-engine (ICMS, IPI, PIS, COFINS, etc.)',
    'description': """
        Brazilian Tax Engine (Tributus)
        ================================
        This module integrates the tributus-engine library with Odoo's tax mechanism
        to provide accurate Brazilian tax calculations.

        Supported tax types:
        - ICMS (with CST codes)
        - IPI
        - PIS
        - COFINS
        - FCP
        - IBS
        - CBS

        Features:
        - Configurable tax engine type per tax template
        - ICMS CST code selection with dynamic visibility
        - Payload-based communication with tributus-engine library
        - Fallback gracefully when tributus-engine is not installed
        - Seamlessly overrides the base tax engine's compute method
    """,
    'author': 'Mackilem Van der Laan - Odoo Brazil Hub',
    'website': 'https://github.com/odoo-brazil-hub',
    'depends': [
        'l10n_tax_engine',
    ],
    'data': [
        'views/account_tax_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'external_dependencies': {
        'python': ['tributus-engine'],
    },
}
