.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================
Payslip Input Policy
====================

This module adds feature to configure predefined values for
payslip inputs. Predefined value attach to each employee's contract.


Installation
============

To install this module, you need to:

1.  Clone the branch 8.0 of the repository https://github.com/open-synergy/opnsynid-hr
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list
4.  Go to menu *Setting -> Modules -> Local Modules*
5.  Search For *Payslip Input Policy*
6.  Install the module

Configuration
=============

Configure Input Type
--------------------

To configure input types, you need to:

1. Go to *Human Resources -> Configuration -> Payroll -> Input Type*
2. Create input type data

Note:

* Input type has to be unique

Usage
=====

Add Predefined Inputs Value On Employee's Contract
--------------------------------------------------------

You need to:

1. Go to *Human Resources -> Employee -> Contract*
2. Create/Open contract data
3. Open *Payslip Input Types* tab
4. Add predefined payslip input value

Use Predefined Payslip Input
----------------------------

No special action. Each time (1) payslip created, or (2) user compute
payslip, Odoo will search predefined payslip input value based on
(1) payslip's contract information, and (2) input type's code.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/opnsynid-hr/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id.com

This module is maintained by the PT. Simetri Sinergi Indonesia.
