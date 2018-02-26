Jarbas web API endpoints
========================

Chamber of Deputies API endpoints
---------------------------------

Reimbursement
~~~~~~~~~~~~~

Each ``Reimbursement`` object is a reimbursement claimed by a congressperson and identified publicly by its ``document_id``.

Retrieving a specific reimbursement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``GET /api/chamber_of_deputies/reimbursement/<document_id>/``
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Details from a specific reimbursement. If ``receipt_url`` wasn't fetched yet, the server **won't** try to fetch it automatically.

``GET /api/chamber_of_deputies/reimbursement/<document_id>/receipt/``
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

URL of the digitalized version of the receipt of this specific reimbursement.

If ``receipt_url`` wasn't fetched yet, the server **will** try to fetch it automatically.

If you append the parameter ``force`` (i.e. ``GET /api/chamber_of_deputies/reimbursement/<document_id>/receipt/?force=1``) the server will re-fetch the receipt URL.

Not all receipts are available, so this URL can be ``null``.

Listing reimbursements
^^^^^^^^^^^^^^^^^^^^^^

``GET /api/chamber_of_deputies/reimbursement/``
'''''''''''''''''''''''''''''''''''''''''''''''

Lists all reimbursements.

Filtering
'''''''''

All these endpoints accepts any combination of the following parameters:

-  ``applicant_id``
-  ``cnpj_cpf``
-  ``document_id``
-  ``issue_date_start`` (inclusive)
-  ``issue_date_end`` (exclusive)
-  ``month``
-  ``subquota_id``
-  ``suspicions`` (*boolean*, ``1`` parses to ``True``, ``0`` to ``False``)
-  ``has_receipt`` (*boolean*, ``1`` parses to ``True``, ``0`` to ``False``)
-  ``year``
-  ``order_by``: ``issue_date`` (default) or ``probability`` (both descending)
-  ``in_latest_dataset`` (*boolean*, ``1`` parses to ``True``, ``0`` to ``False``)

For example:

::

    GET /api/chamber_of_deputies/reimbursement/?year=2016&cnpj_cpf=11111111111111&subquota_id=42&order_by=probability

This request will list:

-  all 2016 reimbursements
-  made in the supplier with the CNPJ 11.111.111/1111-11
-  made according to the subquota with the ID 42
-  sorted by the highest probability

Also you can pass more than one value per field (e.g. ``document_id=111111,222222``).

``GET /api/chamber_of_deputies/reimbursement/<document_id>/same_day/``
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Lists all reimbursements of expenses from the same day as ``document_id``.

Subquota
~~~~~~~~

Subqoutas are categories of expenses that can be reimbursed by congresspeople.

Listing subquotas
^^^^^^^^^^^^^^^^^

``GET /api/chamber_of_deputies/subquota/``
''''''''''''''''''''''''''''''''''''''''''

Lists all subquotas names and IDs.

Filtering
'''''''''

Accepts a case-insensitve ``LIKE`` filter in as the ``q`` URL parameter (e.g. ``GET /api/chamber_of_deputies/subquota/?q=meal`` list all applicant that have ``meal`` in their names.

Applicant
~~~~~~~~~

An applicant is the person (congressperson or theleadership of aparty or government) who claimed the reimbursemement.

List applicants
^^^^^^^^^^^^^^^

``GET /api/chamber_of_deputies/applicant/``
'''''''''''''''''''''''''''''''''''''''''''

Lists all names of applicants together with their IDs.

Filtering
'''''''''

Accepts a case-insensitve ``LIKE`` filter in as the ``q`` URL parameter (e.g. ``GET /api/chamber_of_deputies/applicant/?q=lideranca`` list all applicant that have ``lideranca`` in their names.

Genegral API endpoints
----------------------

Company
~~~~~~~

A company is a Brazilian company in which congressperson have made expenses and claimed for reimbursement.

Retrieving a specific company
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``GET /api/company/<cnpj>/``
''''''''''''''''''''''''''''

This endpoit gets the info we have for a specific company. The endpoint expects a ``cnpj`` (i.e. the CNPJ of a ``Company`` object, digits only). It returns ``404`` if the company is not found.
