# -*- encoding: utf-8 -*-
{
    'name': 'b2c_cheese_base app',
    'category': 'Sales',
    'Author':'VIM IT',
    'version': '1.0',
    'depends': ['product','sale','purchase','stock','stock_picking_invoice_link','barcode_picking_ean128', 'crm_claim', 'purchase_price_ht',
                'l10n_fr_siret','intrastat_product',
                'l10n_fr_intrastat_product'],
    'description': """
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_setting_views.xml',
        'views/partner.xml',
        'views/res_company_view.xml',
        'views/product_view.xml',
        'views/sale_view.xml',
        'views/purchase_view.xml',
        'views/stock_move_line_view.xml',
        'views/view_quant_package.xml',
        'views/stock_picking_view.xml',
        'views/product_tech_template.xml',
        'views/SupplierDiscount_view.xml',
        'views/invoice_view.xml',
        'views/stock_inventory_view.xml',
        'views/intrastat_product.xml',
        'views/stock_production_lot.xml',
        'report/fiche_prepa_template.xml',
        'report/sale_template.xml',
        'report/purchase_document.xml',
        'report/sale_invoice_template.xml',
        'report/invoice_template.xml',
        'report/external_layout_boxed.xml',
        'report/offre_report_template.xml',
        'report/fiche_palette.xml',

    ],

    'installable': True,

}
