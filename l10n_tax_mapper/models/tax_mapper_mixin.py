# -*- coding: utf-8 -*-
# Part of Odoo Brazil Hub. See LICENSE file for full copyright and licensing details.

from odoo import models


class TaxMapperMixin(models.AbstractModel):
    _name = 'tax.mapper.mixin'
    _description = 'Tax Mapper Mixin'
    _auto = False
    _abstract = True

    def get_tax_ids(self, partner, using_on='sale', tags=None, **filter):
        """
        Retrieve tax_ids for a given partner by applying a cascade filter
        on the mapper lines (partner > city > state > country > group).

        The **kwargs are applied as pre-filters (AND) on the domain,
        allowing other modules to add new fields to tax.mapper.line
        and pass their values directly as extra arguments.

        :param partner: res.partner record (single record)
        :param using_on: 'sale' or 'purchase' - context of usage
        :param tags: optional filter to restrict search among tax.mapper
                     records. Accepts a recordset of tax.mapper,
                     a list of IDs, or a list of tag names (strings).
        :param filter: extra pre-filter conditions mapped to field names
                       on tax.mapper.line (e.g. fiscal_regime='normal')
        :return: account.tax recordset
        """
        partner.ensure_one()
        TagLine = self.env['tax.mapper.line']
        domain = self._get_tag_line_domain(partner, using_on, tags=tags, **filter)
        lines = TagLine.search(domain)

        if not lines:
            return self.env['account.tax']

        matched_lines = self._apply_cascade_filter(lines, partner)
        return matched_lines.tax_ids if matched_lines else self.env['account.tax']

    def _get_tag_line_domain(self, partner, using_on, tags=None, **kwargs):
        """
        Build the base domain for searching tax.mapper.line records.

        The default domain filters by:
          - tag usage context (using_on)
          - company (self.env.company)
          - tags (optional) - restricts search to specific tax.mapper records
          - any extra kwargs as exact-match conditions

        Override this method to alter the base domain logic.

        :param partner: res.partner record
        :param using_on: 'sale' or 'purchase'
        :param tags: optional filter for tax.mapper.
                     Accepts a recordset of tax.mapper,
                     a list of IDs, or a list of tag names (strings).
        :param kwargs: extra pre-filter conditions
        :return: list of domain tuples
        """
        domain = [
            ('tag_id.using_on', '=', using_on),
            ('company_id', '=', self.env.company.id),
        ]

        if tags is not None:
            Tag = self.env['tax.mapper']
            if isinstance(tags, models.BaseModel):
                # Recordset - ensure it's of the correct model
                tag_ids = tags.ids
            elif isinstance(tags, (list, tuple)):
                if tags and isinstance(tags[0], str):
                    # List of tag names -> search by name
                    tag_records = Tag.search([('name', 'in', tags)])
                    tag_ids = tag_records.ids
                else:
                    # List of IDs
                    tag_ids = list(tags)
            else:
                tag_ids = [tags]

            if tag_ids:
                domain.append(('tag_id', 'in', tag_ids))
            else:
                # No matching tags found -> force empty result
                domain.append(('id', '=', False))

        for key, value in kwargs.items():
            if value or isinstance(value, bool):
                domain.append((key, '=', value))
        return domain

    def _apply_cascade_filter(self, lines, partner):
        """
        Apply the cascade priority filter on the given mapper lines.

        Priority order (most to least specific):
          1. partner_ids   - partner is directly listed
          2. city          - partner.city_id matches country_city_ids
          3. state         - partner.state_id matches country_state_ids
          4. country       - partner.country_id matches country_ids
          5. group         - partner.country_id belongs to country_group_id

        Returns the lines from the first priority level that matches,
        or an empty recordset if none match.

        Override this method to add, remove or reorder filter levels.

        :param lines: tax.mapper.line recordset to filter
        :param partner: res.partner record
        :return: tax.mapper.line recordset
        """
        # Level 1 – Most specific: direct partner match
        matched = self._filter_by_partner(lines, partner)
        if matched:
            return matched

        # Level 2 – City match
        matched = self._filter_by_city(lines, partner)
        if matched:
            return matched

        # Level 3 – State match
        matched = self._filter_by_state(lines, partner)
        if matched:
            return matched

        # Level 4 – Country match
        matched = self._filter_by_country(lines, partner)
        if matched:
            return matched

        # Level 5 – Least specific: country group match
        matched = self._filter_by_group(lines, partner)
        if matched:
            return matched

        return self.env['tax.mapper.line']

    def _filter_by_partner(self, lines, partner):
        """Return lines where partner is in partner_ids."""
        return lines.filtered(lambda l: partner in l.partner_ids)

    def _filter_by_city(self, lines, partner):
        """Return lines where partner.city_id is in country_city_ids."""
        if not partner.city_id:
            return self.env['tax.mapper.line']
        return lines.filtered(lambda l: partner.city_id in l.country_city_ids)

    def _filter_by_state(self, lines, partner):
        """Return lines where partner.state_id is in country_state_ids."""
        if not partner.state_id:
            return self.env['tax.mapper.line']
        return lines.filtered(lambda l: partner.state_id in l.country_state_ids)

    def _filter_by_country(self, lines, partner):
        """Return lines where partner.country_id is in country_ids."""
        if not partner.country_id:
            return self.env['tax.mapper.line']
        return lines.filtered(lambda l: partner.country_id in l.country_ids)

    def _filter_by_group(self, lines, partner):
        """Return lines where partner.country_id belongs to country_group_id."""
        if not partner.country_id:
            return self.env['tax.mapper.line']
        return lines.filtered(
            lambda l: l.country_group_id
            and partner.country_id in l.country_group_id.country_ids
        )
