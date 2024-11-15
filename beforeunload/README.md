Before Unload
=============

This module blocks reload on edited forms.


Changes protection
--------------------------

When a form is currently being edited and the user reloads the browser page (e.g. by pressing Ctrl-R),
Odoo automatically discard changes. This modules verifies if any fields were modified and warn the user 
before reloading page. Manually closing the browser and/or the tab page with unsaved changes also triggers 
a warning dialog.


Known limits
----------------

* A field is not considered modified as long as the user does not select another field (or 'Tab' out). In theses cases, reload will not be blocked.

* Back / Next browser buttons are not supported.


Version française
=================

Ce module bloque la navigation si un champ est modifié.


Protection des changements
--------------------------

Lorsqu'un formulaire est en édition, il reste possible de le quitter en oubliant de sauvegarder
les changements. Ce module vérifie si un champ a été modifié et avertit l'utilisateur lorsque celui-ci
rafraîchit la page. Fermer le naviguateur et/ou l'onglet lorsque des changements n'ont pas été sauvegardés
génère également un avertissement.


Problèmes connus
----------------

* Un champ n'est pas considéré modifié tant que l'utilisateur ne le quitte pas en cliquant sur un autre champ (ou en utilisant la touche 'Tab'). Dans ces cas, la naviguation n'est pas bloqué.

* La naviguation par les boutons 'Précédent' et 'Suivant' n'est pas bloqué.


Contributors
------------

* Stephane Le Cornec <slc@microcom.ca>


Maintainer
----------

This module is maintained by Microcom.

.. image:: http://microcom.ca/odoo/MICROCOM_500x146.png
   :alt: Microcom
   :target: https://microcom.ca/en/contacts/
