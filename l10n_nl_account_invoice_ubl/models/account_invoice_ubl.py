# -*- coding: utf-8 -*-
# Copyright 2020 Sunflower IT (<https://sunflowerweb.nl>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, api, _
from lxml import etree
from openerp.tools import float_is_zero, float_round
from openerp.exceptions import Warning as UserError
import logging

logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = ['account.invoice']

    @api.multi
    def _ubl_add_header(self, parent_node, ns, version='2.1'):
        res = super(AccountInvoice, self)._ubl_add_header(
            parent_node, ns, version=version)

        # We add CustomizationID in the header just after UBLVersionID
        ubl_version_id = parent_node.find(ns["cbc"] + "UBLVersionID")
        customization_id = etree.Element(ns["cbc"] + "CustomizationID")
        customization_id.text = \
            "urn:cen.eu:en16931:2017#compliant#urn:fdc:nen.nl:nlcius:v1.0"
        ubl_version_id.addnext(customization_id)

        return res
