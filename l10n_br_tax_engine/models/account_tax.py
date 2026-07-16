# -*- coding: utf-8 -*-
# Part of Odoo Brazil Hub. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

try:
    from tributus_engine import TaxEngine
    _tributus_available = True
except ImportError:
    _logger.warning(
        "tributus-engine is not installed. "
        "Brazilian tax calculation will not be available."
    )
    TaxEngine = None  # noqa
    _tributus_available = False


class AccountTax(models.Model):
    _inherit = 'account.tax'

    l10n_br_tax_engine_type = fields.Selection(
        selection=[
            ('icms', 'ICMS'),
            ('ipi', 'IPI'),
            ('pis', 'PIS'),
            ('cofins', 'COFINS'),
            ('fcp', 'FCP'),
            ('ibs', 'IBS'),
            ('cbs', 'CBS'),
        ],
        string='Tax Engine Type',
        help="Identifies the Brazilian tax type for calculation via tributus-engine.",
    )

    l10n_br_cst = fields.Selection(
        selection=[
            ('00', '00 - Full taxation'),
            ('10', '10 - Taxation + ST'),
            ('20', '20 - Reduced base'),
            ('30', '30 - Exempt / not taxed + ST'),
            ('51', '51 - Deferral'),
            ('70', '70 - Reduction + ST'),
            ('90', '90 - Other'),
            ('101', '101 - Simples Nacional (credit)'),
            ('201', '201 - Simples Nacional (credit + ST)'),
            ('202', '202 - Simples Nacional (ST)'),
            ('203', '203 - Simples Nacional (ST)'),
            ('900', '900 - Other (Simples Nacional)'),
        ],
        string='ICMS CST',
        help="ICMS Tax Situation Code (CST). Required for ICMS tax type.",
    )

    # -------------------------------------------------------------------------
    # Helper methods
    # -------------------------------------------------------------------------

    def _build_tributus_payload(self, price_unit, quantity):
        """
        Builds the payload in the format expected by tributus-engine
        from the account.tax records in self.

        :param float price_unit: Product unit price.
        :param float quantity: Product quantity.
        :return dict: Payload for TaxEngine.calculate_from_dict().
        """
        gross_value = float(price_unit * quantity)

        payload = {
            'values': {
                'quantity': quantity,
                'unit_price': price_unit,
                'gross_value': gross_value,
                'discount_value': 0.0,
                'freight_value': 0.0,
                'insurance_value': 0.0,
                'other_expenses': 0.0,
            },
            'taxes': {},
        }

        for tax in self:
            tax_type = tax.l10n_br_tax_engine_type
            if not tax_type:
                continue

            if tax_type == 'icms':
                payload['taxes']['icms'] = {
                    'cst': tax.l10n_br_cst or '00',
                    'aliquota_icms_proprio': tax.amount,
                }
            elif tax_type == 'ipi':
                payload['taxes']['ipi'] = {
                    'aliquota_ipi': tax.amount,
                }
            elif tax_type == 'pis':
                payload['taxes']['pis'] = {
                    'aliquota_pis': tax.amount,
                }
            elif tax_type == 'cofins':
                payload['taxes']['cofins'] = {
                    'aliquota_cofins': tax.amount,
                }
            elif tax_type == 'fcp':
                payload['taxes']['fcp'] = {
                    'aliquota_fcp': tax.amount,
                }
            elif tax_type == 'ibs':
                payload['taxes']['ibs'] = {
                    'aliquota_efetiva_percentual': tax.amount,
                }
            elif tax_type == 'cbs':
                payload['taxes']['cbs'] = {
                    'aliquota_efetiva_percentual': tax.amount,
                }

        return payload

    def _map_engine_result_to_taxes(self, engine_result):
        """
        Maps the tributus-engine result (detailed=True) to the
        list format required by the docstring.

        :param dict engine_result: Return of TaxEngine.calculate_from_dict(detailed=True).
        :return list: List of dictionaries {'tax', 'base', 'tax_amount'}.
        """
        taxes_data = []
        taxes_by_type = {
            tax.l10n_br_tax_engine_type: tax
            for tax in self
            if tax.l10n_br_tax_engine_type
        }

        engine_taxes = engine_result.get('taxes', {})
        for tax_key, tax_values in engine_taxes.items():
            odoo_tax = taxes_by_type.get(tax_key)
            if odoo_tax:
                taxes_data.append({
                    'tax': odoo_tax,
                    'base_amount': float(tax_values['base']),
                    'tax_amount': float(tax_values['amount']),
                    'price_include': False,
                    'is_reverse_charge': False,
                })

        return taxes_data

    # -------------------------------------------------------------------------
    # Main integration method
    # -------------------------------------------------------------------------

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
        Compute Brazilian taxes using the tributus-engine library.

        Builds a payload from ``self`` (account.tax records),
        delegates the calculation to tributus-engine and adapts the
        response to the format expected by Odoo's tax mechanism.

        :return: A dict containing:
            'evaluation_context':       The evaluation context.
            'taxes_data':               A list of dictionaries, one per tax containing:
                'tax':                      The tax record.
                'base':                     The base amount of this tax.
                'tax_amount':               The tax amount of this tax.
            'total_excluded':           The total without tax.
            'total_included':           The total with tax.
        """
        gross_value = float(price_unit * quantity)

        evaluation_context = {
            'price_unit': price_unit,
            'quantity': quantity,
            'product': product,
            'product_uom': product_uom,
        }

        # If tributus-engine is not available, return empty data
        if not _tributus_available:
            _logger.warning(
                "tributus-engine not available. Returning without calculation for "
                "%d tax record(s).", len(self)
            )
            return {
                'evaluation_context': evaluation_context,
                'taxes_data': [],
                'total_excluded': gross_value,
                'total_included': gross_value,
            }

        # Build payload
        payload = self._build_tributus_payload(price_unit, quantity)

        # If no taxes were mapped, return without calculation
        if not payload['taxes']:
            _logger.debug(
                "No taxes with l10n_br_tax_engine_type found in "
                "%d record(s).", len(self)
            )
            return {
                'evaluation_context': evaluation_context,
                'taxes_data': [],
                'total_excluded': gross_value,
                'total_included': gross_value,
            }

        # Execute calculation via tributus-engine
        engine = TaxEngine()
        result = engine.calculate_from_dict(payload, detailed=True)

        # Log engine messages (warnings/errors)
        if result.get('messages'):
            for msg in result['messages']:
                _logger.warning("tributus-engine: %s", msg)

        # Map result to the expected format
        taxes_data = self._map_engine_result_to_taxes(result)
        total_tax = float(result.get('total', 0))

        return {
            'evaluation_context': evaluation_context,
            'taxes_data': taxes_data,
            'total_excluded': gross_value,
            'total_included': gross_value + total_tax,
        }

