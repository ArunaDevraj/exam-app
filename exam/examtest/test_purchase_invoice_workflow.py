import frappe
import unittest
from frappe.utils import nowdate, add_days

class TestPurchaseInvoiceWorkflow(unittest.TestCase):
	def create_purchase_invoice(self, grand_total):
		return frappe.get_doc({
			"doctype": "Purchase Invoice",
			"supplier": "India Post",
			"posting_date": nowdate(),
			"due_date": add_days(nowdate(), 30),
			"company": "exam",
			"currency": "INR",
			"items": [
				{
					"item_code": "STO-ITEM-2025-00005",
					"qty": 1,
					"rate": grand_total,
					"amount": grand_total
				}
			],
			"grand_total": grand_total,
			"workflow_state": "Draft"
		})

	def test_approval_workflow(self):

		# Test for invoice amount < 5000

		invoice = self.create_purchase_invoice(4000)
		invoice.insert()

		# Finance manager approves

		invoice.submit()
		print(f"Workflow state after finance manager approves (4000): {invoice.workflow_state}")
		self.assertEqual(invoice.workflow_state, "Approved")
		self.assertEqual(invoice.docstatus, 1)

		# Finace Manager rejects

		invoice = self.create_purchase_invoice(4000)
		invoice.insert()
		invoice.workflow_state = "Rejected"
		invoice.save()
		print(f"Workflow state after finance manager rejects (4000): {invoice.workflow_state}")
		self.assertEqual(invoice.workflow_state, "Rejected")
		self.assertEqual(invoice.docstatus, 0)


		# amount between 5000 and 20000

		invoice = self.create_purchase_invoice(15000)
		invoice.insert()

		# Finance Manager Approves

		invoice.workflow_state = "Approved by Finance Manager"
		invoice.save()
		print(f"Workflow state after finance manager Approves (15000): {invoice.workflow_state}")
		self.assertEqual(invoice.workflow_state, "Approved by Finance Manager")
		self.assertEqual(invoice.docstatus, 0)


		# CEO Approves

		invoice.reload()
		invoice.submit()
		print(f"Workflow state after CEO Approves (15000): {invoice.workflow_state}")
		self.assertEqual(invoice.workflow_state, "Approved")
		self.assertEqual(invoice.docstatus, 1)


		# Finance Manager Rejects

		invoice = self.create_purchase_invoice(15000)
		invoice.insert()
		invoice.workflow_state = "Rejected"
		invoice.save()
		print(f"Workflow state after finance manager rejects (15000): {invoice.workflow_state}")
		self.assertEqual(invoice.workflow_state, "Rejected")
		self.assertEqual(invoice.docstatus, 0)


		# CEO Rejects

		invoice = self.create_purchase_invoice(15000)
		invoice.insert()
		invoice.workflow_state = "Approved by Finance Manager"
		invoice.save()
		invoice.workflow_state = "Rejected"
		invoice.save()
		print(f"Workflow state after ceo rejects (15000): {invoice.workflow_state}")
		self.assertEqual(invoice.workflow_state, "Rejected")
		self.assertEqual(invoice.docstatus, 0)


		# test for amount > 20000

		# Approves Finance Manager
		invoice = self.create_purchase_invoice(25000)
		invoice.insert()
		invoice.workflow_state = "Approved by Finance Manager"
		invoice.save()
		print(f"Workflow state after Finance Manager Approves (25000): {invoice.workflow_state}")
		self.assertEqual(invoice.workflow_state, "Approved by Finance Manager")
		self.assertEqual(invoice.docstatus, 0)

		# CEO Approves

		invoice.workflow_state = "Approved by CEO"
		invoice.save()
		print(f"Workflow state after CEO Approves (25000): {invoice.workflow_state}")
		self.assertEqual(invoice.workflow_state, "Approved by CEO")
		self.assertEqual(invoice.docstatus, 0)


		# Approves by Board of Directors

		invoice.reload()
		invoice.submit()
		print(f"Workflow state after  Board of Directors Approves (25000): {invoice.workflow_state}")
		self.assertEqual(invoice.workflow_state, "Approved")
		self.assertEqual(invoice.docstatus, 1)

		# Finance Maanger rejects

		invoice = self.create_purchase_invoice(25000)
		invoice.insert()
		invoice.workflow_state = "Rejected"
		invoice.save()
		print(f"Workflow state after Finance Manager rejects (25000): {invoice.workflow_state}")
		self.assertEqual(invoice.workflow_state, "Rejected")
		self.assertEqual(invoice.docstatus, 0)


		# CEO rejects


		invoice = self.create_purchase_invoice(25000)
		invoice.insert()
		invoice.workflow_state = "Approved by Finance Manager"
		invoice.save()
		invoice.workflow_state = "Rejected"
		invoice.save()
		print(f"Workflow state after CEO rejects (25000): {invoice.workflow_state}")
		self.assertEqual(invoice.workflow_state, "Rejected")
		self.assertEqual(invoice.docstatus, 0)

		# Board of Directors Rejects

		invoice = self.create_purchase_invoice(25000)
		invoice.insert()
		invoice.workflow_state = "Approved by Finance Manager"
		invoice.save()
		invoice.workflow_state = "Approved by CEO"
		invoice.save()
		invoice.workflow_state = "Rejected"
		invoice.save()
		print(f"Workflow state after Board of Directora rejects (25000): {invoice.workflow_state}")
		self.assertEqual(invoice.workflow_state, "Rejected")
		self.assertEqual(invoice.docstatus, 0)

if __name__ == "__main__":
	unittest.main()

