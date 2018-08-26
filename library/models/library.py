import datetime
import uuid

from odoo import api, fields, models
from odoo import tools


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'title'

    title = fields.Char(required=True)
    summary = fields.Html()
    author_id = fields.Many2one('library.author', string="Author", required=True)
    isbn = fields.Char(string='ISBN')
    borrower_id = fields.Many2one('res.partner', string='Borrowed by', groups='base.group_user')
    available = fields.Boolean(compute='_compute_available', compute_sudo=True)
    date_borrow = fields.Date(string='Borrow Start', groups='base.group_user')
    date_return = fields.Date(string='Return Date', groups='base.group_user')
    reference = fields.Char(default=lambda s: uuid.uuid4(), groups='base.group_user')
    image = fields.Binary("Image", attachment=True)
    image_medium = fields.Binary("Medium-sized image", attachment=True)
    image_small = fields.Binary("Small-sized image", attachment=True)

    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(LibraryBook, self).create(vals)

    def write(self, vals):
        tools.image_resize_images(vals)
        return super(LibraryBook, self).write(vals)

    def _compute_available(self):
       for book in self:
           book.available = not bool(book.borrower_id)
    
    def action_return(self):
        self.write({'borrower_id': False, 'date_borrow': False, 'date_return': False})


class LibraryBookWizard(models.TransientModel):
    _name = 'library.book.wizard'
    _description = 'Book Borrowing Wizard'

    book_id = fields.Many2one('library.book', string='Book', default=lambda s: s._context.get('active_id'))
    borrower_id = fields.Many2one('res.partner', string='Borrowed by')
    duration = fields.Integer(string='Duration (days)', default=7)

    def action_confirm(self):
        date_return = fields.Date.to_string(datetime.date.today() + datetime.timedelta(days=self.duration))
        self.book_id.write({'borrower_id': self.borrower_id.id, 'date_borrow': fields.Date.today(), 'date_return': date_return})

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Author'

    name = fields.Char(required=True)
    book_ids = fields.One2many('library.book', 'author_id', string='Books')