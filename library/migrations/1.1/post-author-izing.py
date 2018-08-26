from odoo.tools import migration

def migrate(cr,version):
    """Convert author char column to m2o field on book."""
    # create all missing authors
    cr.execute('SELECT DISTINCT author FROM library_book')
    author_vals = [{'name': author['author']} for author in cr.dictfetchall()]
    env = migration.env(cr)
    authors = env['library.author'].create(author_vals)
    # update existing books for correct m2o
    for author in authors:
        cr.execute('UPDATE library_book SET author_id=%s WHERE author=%s', (author.id, author.name))
    # not null constraint could not be applied at ini, re-apply it
    cr.execute('ALTER TABLE library_book ALTER COLUMN author_id SET NOT NULL')
    # drop old column
    migration.remove_column(cr, 'library_book', 'author')
