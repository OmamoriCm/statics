#!/usr/bin/env python

"""
If you change your base currency you have to ensure it has the
exchange rate of 1.00. Otherwise the currency_rate_update module
will not run.

Author: Bringsvor Consulting AS (www.bringsvor.com)
"""
import sys
import odoorpc
import arrow

odoo = odoorpc.ODOO.load('server')

rc = odoo.env['res.currency']
base = rc.search([('base','=',True)])
if len(base)!=1:
	print 'You must have one and only one currency set as base currency.'
	sys.exit(0)

print 'Base currency is', rc.browse(base).name


# Check if it has the correct rate already
current_rate = rc.read(base, ['rate'])
if current_rate[0]['rate'] == 1.0:
	print 'Your base currency rate is already correct.'
	sys.exit(0)

rcr = odoo.env['res.currency.rate']

# currency_id name rate
new_name = arrow.now().floor('day').format('YYYY-MM-DD HH:mm:ss')
print new_name

new_id = rcr.create({'currency_id': base[0],
	'name': new_name,
	'rate': 1.0})

assert type(new_id) == int
print 'Created new currency date with id %d' % new_id

