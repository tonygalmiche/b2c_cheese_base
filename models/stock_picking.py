##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    user_id = fields.Many2one(
        'res.users',
        string="Responsable", related="sale_id.user_id"
    )
    team_id = fields.Many2one('crm.team', 'Equipe Commerciale', related="sale_id.team_id")

    @api.multi
    def do_print_pickingorder(self):
        self.write({'printed': True})
        return self.env.ref('stock.action_report_delivery').report_action(self)

