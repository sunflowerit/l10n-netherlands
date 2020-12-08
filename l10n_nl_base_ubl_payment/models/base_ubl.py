# -*- coding: utf-8 -*-
# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from openerp import api, models


class BaseUbl(models.AbstractModel):
    _inherit = "base.ubl"

    @api.model
    def _ubl_add_payment_means(
            self, partner_bank, payment_mode, date_due, parent_node, ns,
            version='2.1'):

        res = super(BaseUbl, self)._ubl_add_payment_means(
            partner_bank, payment_mode, date_due, parent_node, ns, version=version
        )

        if not self.env.context.get('l10n_nl_base_ubl_use_dutch_ubl'):
            return res

        # UBL-CR-412: A UBL invoice should not include the PaymentMeans PaymentDueDate
        invoice = parent_node
        payment_means = invoice.find(ns['cac'] + 'PaymentMeans')
        if payment_means is not None:
            payment_due_date = payment_means.find(ns['cbc'] + 'PaymentDueDate')
            if payment_due_date is not None:
                payment_means.remove(payment_due_date)

        return res
