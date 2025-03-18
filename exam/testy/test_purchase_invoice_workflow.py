import frappe
import unittest
from frappe.utils import nowdate, add_days

class TestPurchaseInvoiceWorkflow(unittest.TestCase):
    def create_purchase_invoice(self, grand_total):
        """
        Helper function to create a Purchase Invoice with the given grand_total.
        """
        return frappe.get_doc({
            "doctype": "Purchase Invoice",
            "supplier": "India Post",
            "posting_date": nowdate(),
            "due_date": add_days(nowdate(), 30),
            "company": "exam",  # Updated company name
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
            "workflow_state": "Draft"  # Use workflow_state instead of status
        })

    def test_approval_workflow(self):
        """
        Test the workflow transitions for different invoice amounts.
        """
        # Test for invoice amount < 5000
        invoice = self.create_purchase_invoice(4000)
        invoice.insert()

        # Finance Manager Approves
        invoice.submit()
        print(f"Workflow State after Finance Manager Approves (4000): {invoice.workflow_state}")  # Debug
        self.assertEqual(invoice.workflow_state, "Approved")
        self.assertEqual(invoice.docstatus, 1)  # Ensure the document is submitted
#        invoice.cancel()
#        invoice.delete()

        # Finance Manager Rejects
        invoice = self.create_purchase_invoice(4000)
        invoice.insert()
        invoice.workflow_state = "Rejected"
        invoice.save()
        print(f"Workflow State after Finance Manager Rejects (4000): {invoice.workflow_state}")  # Debug
        self.assertEqual(invoice.workflow_state, "Rejected")
        self.assertEqual(invoice.docstatus, 0)  # Ensure the document is saved
#        invoice.delete()

        # Test for invoice amount between 5000 and 20000
        invoice = self.create_purchase_invoice(15000)
        invoice.insert()

        # Finance Manager Approves
        invoice.workflow_state = "Approved by Finance Manager"
        invoice.save()
        print(f"Workflow State after Finance Manager Approves (15000): {invoice.workflow_state}")  # Debug
        self.assertEqual(invoice.workflow_state, "Approved by Finance Manager")
        self.assertEqual(invoice.docstatus, 0)  # Ensure the document is saved

        # CEO Approves
        invoice.reload()  # Reload the document before submitting
        invoice.submit()
        print(f"Workflow State after CEO Approves (15000): {invoice.workflow_state}")  # Debug
        self.assertEqual(invoice.workflow_state, "Approved")
        self.assertEqual(invoice.docstatus, 1)  # Ensure the document is submitted
#        invoice.cancel()
#        invoice.delete()

        # Finance Manager Rejects (Additional Condition)
        invoice = self.create_purchase_invoice(15000)
        invoice.insert()
        invoice.workflow_state = "Rejected"
        invoice.save()
        print(f"Workflow State after Finance Manager Rejects (15000): {invoice.workflow_state}")  # Debug
        self.assertEqual(invoice.workflow_state, "Rejected")
        self.assertEqual(invoice.docstatus, 0)  # Ensure the document is saved
#        invoice.delete()

        # CEO Rejects
        invoice = self.create_purchase_invoice(15000)
        invoice.insert()
        invoice.workflow_state = "Approved by Finance Manager"
        invoice.save()
        invoice.workflow_state = "Rejected"
        invoice.save()
        print(f"Workflow State after CEO Rejects (15000): {invoice.workflow_state}")  # Debug
        self.assertEqual(invoice.workflow_state, "Rejected")
        self.assertEqual(invoice.docstatus, 0)  # Ensure the document is saved
#        invoice.delete()

        # Test for invoice amount > 20000
        invoice = self.create_purchase_invoice(25000)
        invoice.insert()

        # Finance Manager Approves
        invoice.workflow_state = "Approved by Finance Manager"
        invoice.save()
        print(f"Workflow State after Finance Manager Approves (25000): {invoice.workflow_state}")  # Debug
        self.assertEqual(invoice.workflow_state, "Approved by Finance Manager")
        self.assertEqual(invoice.docstatus, 0)  # Ensure the document is saved

        # CEO Approves
        invoice.workflow_state = "Approved by CEO"
        invoice.save()
        print(f"Workflow State after CEO Approves (25000): {invoice.workflow_state}")  # Debug
        self.assertEqual(invoice.workflow_state, "Approved by CEO")
        self.assertEqual(invoice.docstatus, 0)  # Ensure the document is saved

        # Board of Directors Approves
        invoice.reload()  # Reload the document before submitting
        invoice.submit()
        print(f"Workflow State after Board of Directors Approves (25000): {invoice.workflow_state}")  # Debug
        self.assertEqual(invoice.workflow_state, "Approved")
        self.assertEqual(invoice.docstatus, 1)  # Ensure the document is submitted
#        invoice.cancel()
#        invoice.delete()

        # Finance Manager Rejects (Additional Condition for > 20000)
        invoice = self.create_purchase_invoice(25000)
        invoice.insert()
        invoice.workflow_state = "Rejected"
        invoice.save()
        print(f"Workflow State after Finance Manager Rejects (25000): {invoice.workflow_state}")  # Debug
        self.assertEqual(invoice.workflow_state, "Rejected")
        self.assertEqual(invoice.docstatus, 0)  # Ensure the document is saved
#        invoice.delete()

        # CEO Rejects (Additional Condition for > 20000)
        invoice = self.create_purchase_invoice(25000)
        invoice.insert()
        invoice.workflow_state = "Approved by Finance Manager"
        invoice.save()
        invoice.workflow_state = "Rejected"
        invoice.save()
        print(f"Workflow State after CEO Rejects (25000): {invoice.workflow_state}")  # Debug
        self.assertEqual(invoice.workflow_state, "Rejected")
        self.assertEqual(invoice.docstatus, 0)  # Ensure the document is saved
#        invoice.delete()

        # Board of Directors Rejects
        invoice = self.create_purchase_invoice(25000)
        invoice.insert()
        invoice.workflow_state = "Approved by Finance Manager"
        invoice.save()
        invoice.workflow_state = "Approved by CEO"
        invoice.save()
        invoice.workflow_state = "Rejected"
        invoice.save()
        print(f"Workflow State after Board of Directors Rejects (25000): {invoice.workflow_state}")  # Debug
        self.assertEqual(invoice.workflow_state, "Rejected")
        self.assertEqual(invoice.docstatus, 0)  # Ensure the document is saved
#        invoice.delete()

if __name__ == "__main__":
    unittest.main()
