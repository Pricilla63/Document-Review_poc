# import os
# import json
# import glob
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from azure.core.credentials import AzureKeyCredential
# from azure.ai.documentintelligence import DocumentIntelligenceClient
# from dotenv import find_dotenv, load_dotenv
# import tempfile

# load_dotenv(find_dotenv())

# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend communication

# # Azure Document Intelligence setup
# endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
# key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

# document_intelligence_client = DocumentIntelligenceClient(
#     endpoint=endpoint, credential=AzureKeyCredential(key)
# )

# # Create output folder if it doesn't exist
# output_folder = "output"
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# def extract_invoice_data(file_path):
#     """Extract invoice data from a single PDF file"""
#     try:
#         print(f"🔍 Processing: {file_path}")
        
#         with open(file_path, "rb") as f:
#             # Try different parameter combinations for different SDK versions
#             try:
#                 # Try the newer SDK syntax first
#                 poller = document_intelligence_client.begin_analyze_document(
#                     "prebuilt-invoice", 
#                     body=f,
#                     content_type="application/octet-stream"
#                 )
#             except TypeError:
#                 # Fallback to older syntax
#                 poller = document_intelligence_client.begin_analyze_document(
#                     "prebuilt-invoice", 
#                     analyze_request=f,
#                     content_type="application/octet-stream"
#                 )
            
#             invoices = poller.result()
        
#         invoice_data = []
        
#         for idx, invoice in enumerate(invoices.documents):
#             print("--------Recognizing invoice #{}--------".format(idx + 1))
            
#             invoice_dict = {
#                 "invoice_number": idx + 1,
#                 "source_file": os.path.basename(file_path),
#                 "fields": {}
#             }
            
#             # Extract vendor information
#             vendor_name = invoice.fields.get("VendorName")
#             if vendor_name:
#                 invoice_dict["fields"]["VendorName"] = {
#                     "value": vendor_name.value_string,
#                     "confidence": vendor_name.confidence
#                 }
            
#             vendor_address = invoice.fields.get("VendorAddress")
#             if vendor_address:
#                 invoice_dict["fields"]["VendorAddress"] = {
#                     "value": str(vendor_address.value_address),
#                     "confidence": vendor_address.confidence
#                 }
            
#             vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
#             if vendor_address_recipient:
#                 invoice_dict["fields"]["VendorAddressRecipient"] = {
#                     "value": vendor_address_recipient.value_string,
#                     "confidence": vendor_address_recipient.confidence
#                 }
            
#             # Extract customer information
#             customer_name = invoice.fields.get("CustomerName")
#             if customer_name:
#                 invoice_dict["fields"]["CustomerName"] = {
#                     "value": customer_name.value_string,
#                     "confidence": customer_name.confidence
#                 }
            
#             customer_id = invoice.fields.get("CustomerId")
#             if customer_id:
#                 invoice_dict["fields"]["CustomerId"] = {
#                     "value": customer_id.value_string,
#                     "confidence": customer_id.confidence
#                 }
            
#             customer_address = invoice.fields.get("CustomerAddress")
#             if customer_address:
#                 invoice_dict["fields"]["CustomerAddress"] = {
#                     "value": str(customer_address.value_address),
#                     "confidence": customer_address.confidence
#                 }
            
#             customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
#             if customer_address_recipient:
#                 invoice_dict["fields"]["CustomerAddressRecipient"] = {
#                     "value": customer_address_recipient.value_string,
#                     "confidence": customer_address_recipient.confidence
#                 }
            
#             # Extract invoice details
#             invoice_id = invoice.fields.get("InvoiceId")
#             if invoice_id:
#                 invoice_dict["fields"]["InvoiceId"] = {
#                     "value": invoice_id.value_string,
#                     "confidence": invoice_id.confidence
#                 }
            
#             invoice_date = invoice.fields.get("InvoiceDate")
#             if invoice_date:
#                 invoice_dict["fields"]["InvoiceDate"] = {
#                     "value": str(invoice_date.value_date),
#                     "confidence": invoice_date.confidence
#                 }
            
#             invoice_total = invoice.fields.get("InvoiceTotal")
#             if invoice_total:
#                 invoice_dict["fields"]["InvoiceTotal"] = {
#                     "value": invoice_total.value_currency.amount,
#                     "currency": invoice_total.value_currency.currency_symbol,
#                     "confidence": invoice_total.confidence
#                 }
            
#             due_date = invoice.fields.get("DueDate")
#             if due_date:
#                 invoice_dict["fields"]["DueDate"] = {
#                     "value": str(due_date.value_date),
#                     "confidence": due_date.confidence
#                 }
            
#             purchase_order = invoice.fields.get("PurchaseOrder")
#             if purchase_order:
#                 invoice_dict["fields"]["PurchaseOrder"] = {
#                     "value": purchase_order.value_string,
#                     "confidence": purchase_order.confidence
#                 }
            
#             billing_address = invoice.fields.get("BillingAddress")
#             if billing_address:
#                 invoice_dict["fields"]["BillingAddress"] = {
#                     "value": str(billing_address.value_address),
#                     "confidence": billing_address.confidence
#                 }
            
#             shipping_address = invoice.fields.get("ShippingAddress")
#             if shipping_address:
#                 invoice_dict["fields"]["ShippingAddress"] = {
#                     "value": str(shipping_address.value_address),
#                     "confidence": shipping_address.confidence
#                 }
            
#             # Extract line items
#             invoice_dict["items"] = []
#             if invoice.fields.get("Items"):
#                 for item_idx, item in enumerate(invoice.fields.get("Items").value_array):
#                     item_dict = {"item_number": item_idx + 1}
                    
#                     item_description = item.value_object.get("Description")
#                     if item_description:
#                         item_dict["Description"] = {
#                             "value": item_description.value_string,
#                             "confidence": item_description.confidence
#                         }
                    
#                     item_quantity = item.value_object.get("Quantity")
#                     if item_quantity:
#                         item_dict["Quantity"] = {
#                             "value": item_quantity.value_number,
#                             "confidence": item_quantity.confidence
#                         }
                    
#                     unit_price = item.value_object.get("UnitPrice")
#                     if unit_price:
#                         item_dict["UnitPrice"] = {
#                             "value": unit_price.value_currency.amount,
#                             "currency": unit_price.value_currency.currency_symbol,
#                             "confidence": unit_price.confidence
#                         }
                    
#                     amount = item.value_object.get("Amount")
#                     if amount:
#                         item_dict["Amount"] = {
#                             "value": amount.value_currency.amount,
#                             "currency": amount.value_currency.currency_symbol,
#                             "confidence": amount.confidence
#                         }
                    
#                     invoice_dict["items"].append(item_dict)
            
#             invoice_data.append(invoice_dict)
#             print("----------------------------------------")
        
#         return {
#             "success": True,
#             "data": invoice_data,
#             "message": f"Successfully processed {len(invoice_data)} invoice(s)"
#         }
        
#     except Exception as e:
#         print(f"❌ Error processing {file_path}: {e}")
#         return {
#             "success": False,
#             "error": str(e),
#             "message": f"Failed to process file: {str(e)}"
#         }

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     """Handle file upload and processing"""
#     try:
#         # Check if file is present in request
#         if 'file' not in request.files:
#             return jsonify({
#                 "success": False,
#                 "error": "No file provided",
#                 "message": "Please select a file to upload"
#             }), 400
        
#         file = request.files['file']
        
#         # Check if file is selected
#         if file.filename == '':
#             return jsonify({
#                 "success": False,
#                 "error": "No file selected",
#                 "message": "Please select a file to upload"
#             }), 400
        
#         # Check file extension
#         if not file.filename.lower().endswith('.pdf'):
#             return jsonify({
#                 "success": False,
#                 "error": "Invalid file type",
#                 "message": "Only PDF files are supported"
#             }), 400
        
#         # Save uploaded file temporarily
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
#             file.save(temp_file.name)
#             temp_file_path = temp_file.name
        
#         try:
#             # Process the file
#             result = extract_invoice_data(temp_file_path)
            
#             # Save to JSON file if processing was successful
#             if result["success"] and result["data"]:
#                 base_name = os.path.splitext(file.filename)[0]
#                 json_filename = f"{base_name}_extracted.json"
#                 json_filepath = os.path.join(output_folder, json_filename)
                
#                 with open(json_filepath, 'w', encoding='utf-8') as json_file:
#                     json.dump(result["data"], json_file, indent=2, ensure_ascii=False)
                
#                 result["saved_file"] = json_filename
            
#             return jsonify(result)
            
#         finally:
#             # Clean up temporary file
#             if os.path.exists(temp_file_path):
#                 os.unlink(temp_file_path)
                
#     except Exception as e:
#         print(f"❌ Upload error: {e}")
#         return jsonify({
#             "success": False,
#             "error": str(e),
#             "message": "Internal server error during file processing"
#         }), 500

# @app.route('/health', methods=['GET'])
# def health_check():
#     """Health check endpoint"""
#     return jsonify({
#         "status": "healthy",
#         "service": "Invoice Processing API",
#         "version": "1.0.0"
#     })

# @app.route('/batch-process', methods=['POST'])
# def batch_process_files():
#     """Process multiple files at once"""
#     try:
#         if 'files' not in request.files:
#             return jsonify({
#                 "success": False,
#                 "error": "No files provided",
#                 "message": "Please select files to upload"
#             }), 400
        
#         files = request.files.getlist('files')
        
#         if not files or files[0].filename == '':
#             return jsonify({
#                 "success": False,
#                 "error": "No files selected",
#                 "message": "Please select files to upload"
#             }), 400
        
#         results = []
#         successful_files = 0
#         failed_files = 0
        
#         for file in files:
#             if file.filename.lower().endswith('.pdf'):
#                 # Save and process each file
#                 with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
#                     file.save(temp_file.name)
#                     temp_file_path = temp_file.name
                
#                 try:
#                     result = extract_invoice_data(temp_file_path)
#                     result["filename"] = file.filename
#                     results.append(result)
                    
#                     if result["success"]:
#                         successful_files += 1
#                     else:
#                         failed_files += 1
                        
#                 finally:
#                     if os.path.exists(temp_file_path):
#                         os.unlink(temp_file_path)
        
#         return jsonify({
#             "success": True,
#             "results": results,
#             "summary": {
#                 "total_files": len(files),
#                 "successful": successful_files,
#                 "failed": failed_files
#             }
#         })
        
#     except Exception as e:
#         print(f"❌ Batch processing error: {e}")
#         return jsonify({
#             "success": False,
#             "error": str(e),
#             "message": "Internal server error during batch processing"
#         }), 500

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)



# import os
# import json
# import glob
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from azure.core.credentials import AzureKeyCredential
# from azure.ai.documentintelligence import DocumentIntelligenceClient
# from dotenv import find_dotenv, load_dotenv
# import tempfile

# load_dotenv(find_dotenv())

# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend communication

# # Azure Document Intelligence setup
# endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
# key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

# document_intelligence_client = DocumentIntelligenceClient(
#     endpoint=endpoint, credential=AzureKeyCredential(key)
# )

# # Create output folder if it doesn't exist - FIXED PATH
# output_folder = os.path.join(os.path.dirname(__file__), "output")
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# def extract_invoice_data(file_path):
#     """Extract invoice data from a single PDF file"""
#     try:
#         print(f"🔍 Processing: {file_path}")
        
#         with open(file_path, "rb") as f:
#             # Try different parameter combinations for different SDK versions
#             try:
#                 # Try the newer SDK syntax first
#                 poller = document_intelligence_client.begin_analyze_document(
#                     "prebuilt-invoice", 
#                     body=f,
#                     content_type="application/octet-stream"
#                 )
#             except TypeError:
#                 # Fallback to older syntax
#                 poller = document_intelligence_client.begin_analyze_document(
#                     "prebuilt-invoice", 
#                     analyze_request=f,
#                     content_type="application/octet-stream"
#                 )
            
#             invoices = poller.result()
        
#         invoice_data = []
        
#         for idx, invoice in enumerate(invoices.documents):
#             print("--------Recognizing invoice #{}--------".format(idx + 1))
            
#             invoice_dict = {
#                 "invoice_number": idx + 1,
#                 "source_file": os.path.basename(file_path),
#                 "fields": {}
#             }
            
#             # Vendor Level Fields
#             vendor_name = invoice.fields.get("VendorName")
#             if vendor_name:
#                 invoice_dict["fields"]["VendorName"] = {
#                     "value": vendor_name.value_string,
#                     "confidence": vendor_name.confidence
#                 }
            
#             vendor_address = invoice.fields.get("VendorAddress")
#             if vendor_address:
#                 invoice_dict["fields"]["VendorAddress"] = {
#                     "value": str(vendor_address.value_address),
#                     "confidence": vendor_address.confidence
#                 }
            
#             vendor_country = invoice.fields.get("VendorCountry")
#             if vendor_country:
#                 invoice_dict["fields"]["VendorCountry"] = {
#                     "value": vendor_country.value_string,
#                     "confidence": vendor_country.confidence
#                 }
            
#             vendor_tax_id = invoice.fields.get("VendorTaxId")
#             if vendor_tax_id:
#                 invoice_dict["fields"]["VendorTaxId"] = {
#                     "value": vendor_tax_id.value_string,
#                     "confidence": vendor_tax_id.confidence
#                 }
            
#             vendor_email = invoice.fields.get("VendorEmail")
#             if vendor_email:
#                 invoice_dict["fields"]["VendorEmail"] = {
#                     "value": vendor_email.value_string,
#                     "confidence": vendor_email.confidence
#                 }
            
#             vendor_phone = invoice.fields.get("VendorPhone")
#             if vendor_phone:
#                 invoice_dict["fields"]["VendorPhone"] = {
#                     "value": vendor_phone.value_string,
#                     "confidence": vendor_phone.confidence
#                 }
            
#             vendor_bank_name = invoice.fields.get("VendorBankName")
#             if vendor_bank_name:
#                 invoice_dict["fields"]["VendorBankName"] = {
#                     "value": vendor_bank_name.value_string,
#                     "confidence": vendor_bank_name.confidence
#                 }
            
#             vendor_bank_account = invoice.fields.get("VendorBankAccount")
#             if vendor_bank_account:
#                 invoice_dict["fields"]["VendorBankAccount"] = {
#                     "value": vendor_bank_account.value_string,
#                     "confidence": vendor_bank_account.confidence
#                 }
            
#             vendor_bank_details = invoice.fields.get("VendorBankDetails")
#             if vendor_bank_details:
#                 invoice_dict["fields"]["VendorBankDetails"] = {
#                     "value": vendor_bank_details.value_string,
#                     "confidence": vendor_bank_details.confidence
#                 }
            
#             vendor_contact_person = invoice.fields.get("VendorContactPerson")
#             if vendor_contact_person:
#                 invoice_dict["fields"]["VendorContactPerson"] = {
#                     "value": vendor_contact_person.value_string,
#                     "confidence": vendor_contact_person.confidence
#                 }
            
#             vendor_website = invoice.fields.get("VendorWebsite")
#             if vendor_website:
#                 invoice_dict["fields"]["VendorWebsite"] = {
#                     "value": vendor_website.value_string,
#                     "confidence": vendor_website.confidence
#                 }
            
#             # Buyer Information Fields
#             customer_name = invoice.fields.get("CustomerName")
#             if customer_name:
#                 invoice_dict["fields"]["CustomerName"] = {
#                     "value": customer_name.value_string,
#                     "confidence": customer_name.confidence
#                 }
            
#             billing_address = invoice.fields.get("BillingAddress")
#             if billing_address:
#                 invoice_dict["fields"]["BillingAddress"] = {
#                     "value": str(billing_address.value_address),
#                     "confidence": billing_address.confidence
#                 }
            
#             shipping_address = invoice.fields.get("ShippingAddress")
#             if shipping_address:
#                 invoice_dict["fields"]["ShippingAddress"] = {
#                     "value": str(shipping_address.value_address),
#                     "confidence": shipping_address.confidence
#                 }
            
#             customer_phone = invoice.fields.get("CustomerPhone")
#             if customer_phone:
#                 invoice_dict["fields"]["CustomerPhone"] = {
#                     "value": customer_phone.value_string,
#                     "confidence": customer_phone.confidence
#                 }
            
#             customer_email = invoice.fields.get("CustomerEmail")
#             if customer_email:
#                 invoice_dict["fields"]["CustomerEmail"] = {
#                     "value": customer_email.value_string,
#                     "confidence": customer_email.confidence
#                 }
            
#             customer_tax_id = invoice.fields.get("CustomerTaxId")
#             if customer_tax_id:
#                 invoice_dict["fields"]["CustomerTaxId"] = {
#                     "value": customer_tax_id.value_string,
#                     "confidence": customer_tax_id.confidence
#                 }
            
#             customer_contact_person = invoice.fields.get("CustomerContactPerson")
#             if customer_contact_person:
#                 invoice_dict["fields"]["CustomerContactPerson"] = {
#                     "value": customer_contact_person.value_string,
#                     "confidence": customer_contact_person.confidence
#                 }
            
#             # Invoice Header Fields
#             invoice_id = invoice.fields.get("InvoiceId")
#             if invoice_id:
#                 invoice_dict["fields"]["InvoiceId"] = {
#                     "value": invoice_id.value_string,
#                     "confidence": invoice_id.confidence
#                 }
            
#             invoice_date = invoice.fields.get("InvoiceDate")
#             if invoice_date:
#                 invoice_dict["fields"]["InvoiceDate"] = {
#                     "value": str(invoice_date.value_date),
#                     "confidence": invoice_date.confidence
#                 }
            
#             due_date = invoice.fields.get("DueDate")
#             if due_date:
#                 invoice_dict["fields"]["DueDate"] = {
#                     "value": str(due_date.value_date),
#                     "confidence": due_date.confidence
#                 }
            
#             invoice_currency = invoice.fields.get("InvoiceCurrency")
#             if invoice_currency:
#                 invoice_dict["fields"]["InvoiceCurrency"] = {
#                     "value": invoice_currency.value_string,
#                     "confidence": invoice_currency.confidence
#                 }
            
#             invoice_type = invoice.fields.get("InvoiceType")
#             if invoice_type:
#                 invoice_dict["fields"]["InvoiceType"] = {
#                     "value": invoice_type.value_string,
#                     "confidence": invoice_type.confidence
#                 }
            
#             purchase_order = invoice.fields.get("PurchaseOrder")
#             if purchase_order:
#                 invoice_dict["fields"]["PurchaseOrder"] = {
#                     "value": purchase_order.value_string,
#                     "confidence": purchase_order.confidence
#                 }
            
#             payment_terms = invoice.fields.get("PaymentTerms")
#             if payment_terms:
#                 invoice_dict["fields"]["PaymentTerms"] = {
#                     "value": payment_terms.value_string,
#                     "confidence": payment_terms.confidence
#                 }
            
#             payment_method = invoice.fields.get("PaymentMethod")
#             if payment_method:
#                 invoice_dict["fields"]["PaymentMethod"] = {
#                     "value": payment_method.value_string,
#                     "confidence": payment_method.confidence
#                 }
            
#             cost_center = invoice.fields.get("CostCenter")
#             if cost_center:
#                 invoice_dict["fields"]["CostCenter"] = {
#                     "value": cost_center.value_string,
#                     "confidence": cost_center.confidence
#                 }
            
#             service_period_start = invoice.fields.get("ServicePeriodStart")
#             if service_period_start:
#                 invoice_dict["fields"]["ServicePeriodStart"] = {
#                     "value": str(service_period_start.value_date),
#                     "confidence": service_period_start.confidence
#                 }
            
#             service_period_end = invoice.fields.get("ServicePeriodEnd")
#             if service_period_end:
#                 invoice_dict["fields"]["ServicePeriodEnd"] = {
#                     "value": str(service_period_end.value_date),
#                     "confidence": service_period_end.confidence
#                 }
            
#             # Line Items
#             invoice_dict["items"] = []
#             if invoice.fields.get("Items"):
#                 for item_idx, item in enumerate(invoice.fields.get("Items").value_array):
#                     item_dict = {"item_number": item_idx + 1}
                    
#                     item_description = item.value_object.get("Description")
#                     if item_description:
#                         item_dict["Description"] = {
#                             "value": item_description.value_string,
#                             "confidence": item_description.confidence
#                         }
                    
#                     item_code = item.value_object.get("ItemCode")
#                     if item_code:
#                         item_dict["ItemCode"] = {
#                             "value": item_code.value_string,
#                             "confidence": item_code.confidence
#                         }
                    
#                     item_quantity = item.value_object.get("Quantity")
#                     if item_quantity:
#                         item_dict["Quantity"] = {
#                             "value": item_quantity.value_number,
#                             "confidence": item_quantity.confidence
#                         }
                    
#                     unit_of_measure = item.value_object.get("UnitOfMeasure")
#                     if unit_of_measure:
#                         item_dict["UnitOfMeasure"] = {
#                             "value": unit_of_measure.value_string,
#                             "confidence": unit_of_measure.confidence
#                         }
                    
#                     unit_price = item.value_object.get("UnitPrice")
#                     if unit_price:
#                         item_dict["UnitPrice"] = {
#                             "value": unit_price.value_currency.amount,
#                             "currency": unit_price.value_currency.currency_symbol,
#                             "confidence": unit_price.confidence
#                         }
                    
#                     discount = item.value_object.get("Discount")
#                     if discount:
#                         item_dict["Discount"] = {
#                             "value": discount.value_number if hasattr(discount, 'value_number') else discount.value_currency.amount,
#                             "confidence": discount.confidence
#                         }
                    
#                     net_amount = item.value_object.get("NetAmount")
#                     if net_amount:
#                         item_dict["NetAmount"] = {
#                             "value": net_amount.value_currency.amount,
#                             "currency": net_amount.value_currency.currency_symbol,
#                             "confidence": net_amount.confidence
#                         }
                    
#                     tax_percentage = item.value_object.get("TaxPercentage")
#                     if tax_percentage:
#                         item_dict["TaxPercentage"] = {
#                             "value": tax_percentage.value_number,
#                             "confidence": tax_percentage.confidence
#                         }
                    
#                     tax_amount = item.value_object.get("TaxAmount")
#                     if tax_amount:
#                         item_dict["TaxAmount"] = {
#                             "value": tax_amount.value_currency.amount,
#                             "currency": tax_amount.value_currency.currency_symbol,
#                             "confidence": tax_amount.confidence
#                         }
                    
#                     gross_amount = item.value_object.get("GrossAmount")
#                     if gross_amount:
#                         item_dict["GrossAmount"] = {
#                             "value": gross_amount.value_currency.amount,
#                             "currency": gross_amount.value_currency.currency_symbol,
#                             "confidence": gross_amount.confidence
#                         }
                    
#                     invoice_dict["items"].append(item_dict)
            
#             # Taxes Fields
#             total_tax = invoice.fields.get("TotalTax")
#             if total_tax:
#                 invoice_dict["fields"]["TotalTax"] = {
#                     "value": total_tax.value_currency.amount,
#                     "currency": total_tax.value_currency.currency_symbol,
#                     "confidence": total_tax.confidence
#                 }
            
#             tax_type = invoice.fields.get("TaxType")
#             if tax_type:
#                 invoice_dict["fields"]["TaxType"] = {
#                     "value": tax_type.value_string,
#                     "confidence": tax_type.confidence
#                 }
            
#             withholding_tax = invoice.fields.get("WithholdingTax")
#             if withholding_tax:
#                 invoice_dict["fields"]["WithholdingTax"] = {
#                     "value": withholding_tax.value_currency.amount,
#                     "currency": withholding_tax.value_currency.currency_symbol,
#                     "confidence": withholding_tax.confidence
#                 }
            
#             # Totals Fields
#             subtotal = invoice.fields.get("Subtotal")
#             if subtotal:
#                 invoice_dict["fields"]["Subtotal"] = {
#                     "value": subtotal.value_currency.amount,
#                     "currency": subtotal.value_currency.currency_symbol,
#                     "confidence": subtotal.confidence
#                 }
            
#             shipping_handling = invoice.fields.get("ShippingHandling")
#             if shipping_handling:
#                 invoice_dict["fields"]["ShippingHandling"] = {
#                     "value": shipping_handling.value_currency.amount,
#                     "currency": shipping_handling.value_currency.currency_symbol,
#                     "confidence": shipping_handling.confidence
#                 }
            
#             surcharges = invoice.fields.get("Surcharges")
#             if surcharges:
#                 invoice_dict["fields"]["Surcharges"] = {
#                     "value": surcharges.value_currency.amount,
#                     "currency": surcharges.value_currency.currency_symbol,
#                     "confidence": surcharges.confidence
#                 }
            
#             invoice_total = invoice.fields.get("InvoiceTotal")
#             if invoice_total:
#                 invoice_dict["fields"]["InvoiceTotal"] = {
#                     "value": invoice_total.value_currency.amount,
#                     "currency": invoice_total.value_currency.currency_symbol,
#                     "confidence": invoice_total.confidence
#                 }
            
#             amount_paid = invoice.fields.get("AmountPaid")
#             if amount_paid:
#                 invoice_dict["fields"]["AmountPaid"] = {
#                     "value": amount_paid.value_currency.amount,
#                     "currency": amount_paid.value_currency.currency_symbol,
#                     "confidence": amount_paid.confidence
#                 }
            
#             amount_due = invoice.fields.get("AmountDue")
#             if amount_due:
#                 invoice_dict["fields"]["AmountDue"] = {
#                     "value": amount_due.value_currency.amount,
#                     "currency": amount_due.value_currency.currency_symbol,
#                     "confidence": amount_due.confidence
#                 }
            
#             # Compliance Fields
#             notes = invoice.fields.get("Notes")
#             if notes:
#                 invoice_dict["fields"]["Notes"] = {
#                     "value": notes.value_string,
#                     "confidence": notes.confidence
#                 }
            
#             qr_code = invoice.fields.get("QRCode")
#             if qr_code:
#                 invoice_dict["fields"]["QRCode"] = {
#                     "value": qr_code.value_string,
#                     "confidence": qr_code.confidence
#                 }
            
#             company_registration = invoice.fields.get("CompanyRegistration")
#             if company_registration:
#                 invoice_dict["fields"]["CompanyRegistration"] = {
#                     "value": company_registration.value_string,
#                     "confidence": company_registration.confidence
#                 }
            
#             # Approval Workflow Fields
#             approval_workflow_id = invoice.fields.get("ApprovalWorkflowId")
#             if approval_workflow_id:
#                 invoice_dict["fields"]["ApprovalWorkflowId"] = {
#                     "value": approval_workflow_id.value_string,
#                     "confidence": approval_workflow_id.confidence
#                 }
            
#             approval_required = invoice.fields.get("ApprovalRequired")
#             if approval_required:
#                 invoice_dict["fields"]["ApprovalRequired"] = {
#                     "value": approval_required.value_string,
#                     "confidence": approval_required.confidence
#                 }
            
#             approver_list = invoice.fields.get("ApproverList")
#             if approver_list:
#                 invoice_dict["fields"]["ApproverList"] = {
#                     "value": approver_list.value_string,
#                     "confidence": approver_list.confidence
#                 }
            
#             approval_status = invoice.fields.get("ApprovalStatus")
#             if approval_status:
#                 invoice_dict["fields"]["ApprovalStatus"] = {
#                     "value": approval_status.value_string,
#                     "confidence": approval_status.confidence
#                 }
            
#             approval_timestamps = invoice.fields.get("ApprovalTimestamps")
#             if approval_timestamps:
#                 invoice_dict["fields"]["ApprovalTimestamps"] = {
#                     "value": approval_timestamps.value_string,
#                     "confidence": approval_timestamps.confidence
#                 }
            
#             invoice_data.append(invoice_dict)
#             print("----------------------------------------")
        
#         return {
#             "success": True,
#             "data": invoice_data,
#             "message": f"Successfully processed {len(invoice_data)} invoice(s)"
#         }
        
#     except Exception as e:
#         print(f"❌ Error processing {file_path}: {e}")
#         return {
#             "success": False,
#             "error": str(e),
#             "message": f"Failed to process file: {str(e)}"
#         }

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     """Handle file upload and processing"""
#     try:
#         # Check if file is present in request
#         if 'file' not in request.files:
#             return jsonify({
#                 "success": False,
#                 "error": "No file provided",
#                 "message": "Please select a file to upload"
#             }), 400
        
#         file = request.files['file']
        
#         # Check if file is selected
#         if file.filename == '':
#             return jsonify({
#                 "success": False,
#                 "error": "No file selected",
#                 "message": "Please select a file to upload"
#             }), 400
        
#         # Check file extension
#         if not file.filename.lower().endswith('.pdf'):
#             return jsonify({
#                 "success": False,
#                 "error": "Invalid file type",
#                 "message": "Only PDF files are supported"
#             }), 400
        
#         # Save uploaded file temporarily
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
#             file.save(temp_file.name)
#             temp_file_path = temp_file.name
        
#         try:
#             # Process the file
#             result = extract_invoice_data(temp_file_path)
            
#             # Save to JSON file if processing was successful
#             if result["success"] and result["data"]:
#                 # Clean filename to remove invalid characters
#                 base_name = os.path.splitext(file.filename)[0]
#                 # Remove any characters that might cause file path issues
#                 safe_base_name = "".join(c for c in base_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
#                 json_filename = f"{safe_base_name}_extracted.json"
#                 json_filepath = os.path.join(output_folder, json_filename)
                
#                 # Ensure output directory exists
#                 os.makedirs(output_folder, exist_ok=True)
                
#                 with open(json_filepath, 'w', encoding='utf-8') as json_file:
#                     json.dump(result["data"], json_file, indent=2, ensure_ascii=False)
                
#                 result["saved_file"] = json_filename
#                 print(f"✅ Saved results to: {json_filepath}")
            
#             return jsonify(result)
            
#         finally:
#             # Clean up temporary file
#             if os.path.exists(temp_file_path):
#                 os.unlink(temp_file_path)
                
#     except Exception as e:
#         print(f"❌ Upload error: {e}")
#         return jsonify({
#             "success": False,
#             "error": str(e),
#             "message": "Internal server error during file processing"
#         }), 500

# @app.route('/health', methods=['GET'])
# def health_check():
#     """Health check endpoint"""
#     return jsonify({
#         "status": "healthy",
#         "service": "Invoice Processing API",
#         "version": "1.0.0"
#     })

# @app.route('/batch-process', methods=['POST'])
# def batch_process_files():
#     """Process multiple files at once"""
#     try:
#         if 'files' not in request.files:
#             return jsonify({
#                 "success": False,
#                 "error": "No files provided",
#                 "message": "Please select files to upload"
#             }), 400
        
#         files = request.files.getlist('files')
        
#         if not files or files[0].filename == '':
#             return jsonify({
#                 "success": False,
#                 "error": "No files selected",
#                 "message": "Please select files to upload"
#             }), 400
        
#         results = []
#         successful_files = 0
#         failed_files = 0
        
#         for file in files:
#             if file.filename.lower().endswith('.pdf'):
#                 # Save and process each file
#                 with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
#                     file.save(temp_file.name)
#                     temp_file_path = temp_file.name
                
#                 try:
#                     result = extract_invoice_data(temp_file_path)
#                     result["filename"] = file.filename
#                     results.append(result)
                    
#                     if result["success"]:
#                         successful_files += 1
#                     else:
#                         failed_files += 1
                        
#                 finally:
#                     if os.path.exists(temp_file_path):
#                         os.unlink(temp_file_path)
        
#         return jsonify({
#             "success": True,
#             "results": results,
#             "summary": {
#                 "total_files": len(files),
#                 "successful": successful_files,
#                 "failed": failed_files
#             }
#         })
        
#     except Exception as e:
#         print(f"❌ Batch processing error: {e}")
#         return jsonify({
#             "success": False,
#             "error": str(e),
#             "message": "Internal server error during batch processing"
#         }), 500

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)




import os
import json
import re
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from openai import AzureOpenAI
from dotenv import find_dotenv, load_dotenv
import tempfile
from datetime import datetime
import fitz  # PyMuPDF
import base64
import time

load_dotenv(find_dotenv())

app = Flask(__name__)
CORS(app)

# Azure Document Intelligence setup
endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

document_intelligence_client = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# Azure OpenAI setup
azure_openai_client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-02-01",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)

# Create output folders
output_folder = "output"
json_output_folder = os.path.join(output_folder, "json_files")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(json_output_folder):
    os.makedirs(json_output_folder)

# All 56 fields definition
ALL_56_FIELDS = [
    # Vendor Level (11)
    "VendorName", "VendorAddress", "VendorCountry", "VendorTaxId",
    "VendorContactEmail", "VendorPhone", "VendorBankName", 
    "VendorBankAccountNumber", "VendorBankDetails", "VendorContactPerson",
    "VendorWebsite",
    # Buyer Information (7)
    "CustomerName", "BillingAddress", "ShippingAddress", "CustomerPhone",
    "CustomerEmail", "CustomerTaxId", "CustomerContactPerson",
    # Invoice Header (11)
    "InvoiceId", "InvoiceDate", "DueDate", "InvoiceCurrency",
    "InvoiceType", "PurchaseOrder", "PaymentTerms", "PaymentMethod",
    "CostCenter", "ServicePeriodStart", "ServicePeriodEnd",
    # Line Items Summary (1)
    "LineItems_Count",
    # Taxes (3)
    "TotalTax", "TaxTypeBreakdown", "WithholdingTax",
    # Totals (6)
    "Subtotal", "ShippingHandling", "Surcharges", "InvoiceTotal",
    "AmountPaid", "AmountDue",
    # Compliance (3)
    "Notes", "QRCode", "CompanyRegistration",
    # Approval Workflow (5)
    "ApprovalWorkflowID", "ApprovalRequired", "ApproverList",
    "ApprovalStatus", "ApprovalTimestamps"
]

# Enhanced Azure Field Mappings
ENHANCED_FIELD_MAPPINGS = {
    # Vendor Level
    "VendorName": "VendorName",
    "VendorAddress": "VendorAddress",
    "VendorTaxId": "VendorTaxId",
    "VendorPhone": "VendorPhone",
    "VendorContactPerson": "VendorAddressRecipient",
    
    # Buyer Information
    "CustomerName": "CustomerName",
    "BillingAddress": "BillingAddress",
    "ShippingAddress": "ShippingAddress",
    "CustomerPhone": "CustomerPhone",
    "CustomerTaxId": "CustomerTaxId",
    "CustomerContactPerson": "CustomerAddressRecipient",
    
    # Invoice Header
    "InvoiceId": "InvoiceId",
    "InvoiceDate": "InvoiceDate",
    "DueDate": "DueDate",
    "PurchaseOrder": "PurchaseOrder",
    "PaymentTerms": "PaymentTerms",
    "ServicePeriodStart": "ServiceStartDate",
    "ServicePeriodEnd": "ServiceEndDate",
    
    # Financials
    "InvoiceTotal": "InvoiceTotal",
    "Subtotal": "SubTotal",
    "TotalTax": "TotalTax",
    "AmountDue": "AmountDue",
    
    # Payment Details
    "VendorBankName": "PaymentDetails",
    "VendorBankAccountNumber": "PaymentDetails",
    "VendorBankDetails": "PaymentDetails",
    "PaymentMethod": "PaymentDetails",
}

# Comprehensive Regex Patterns for all fields
COMPREHENSIVE_REGEX_PATTERNS = {
    "VendorName": [r'(?:From|Vendor|Supplier)[:\s]*([^\n]+)'],
    "VendorAddress": [r'(?:Vendor\s*Address)[:\s]*([^\n]+(?:\n[^\n]+){0,2})'],
    "VendorTaxId": [r'(?:Tax\s*ID|VAT|GST)[\s#:]*([A-Z0-9-]+)'],
    "VendorContactEmail": [r'\b([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b'],
    "VendorPhone": [r'(?:Phone|Tel)[\s:]*([+\d\s\-\(\)]{7,})'],
    "VendorBankName": [r'(?:Bank\s*Name)[\s:]*([A-Za-z0-9\s\.&]+)'],
    "VendorBankAccountNumber": [r'(?:Account\s*Number)[\s:]*([A-Z0-9-]+)'],
    "VendorBankDetails": [r'(?:IBAN)[\s:]*([A-Z0-9-]+)'],
    "VendorContactPerson": [r'(?:Attention|Attn)[\s:]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)'],
    "VendorWebsite": [r'(?:Website)[\s:]*((?:https?://)?[^\s]+\.[a-z]{2,})'],
    
    "CustomerName": [r'(?:To|Bill\s*To|Customer)[\s:]*([^\n]+)'],
    "BillingAddress": [r'(?:Billing\s*Address)[\s:]*([^\n]+(?:\n[^\n]+){0,2})'],
    "ShippingAddress": [r'(?:Shipping\s*Address)[\s:]*([^\n]+(?:\n[^\n]+){0,2})'],
    "CustomerPhone": [r'(?:Customer\s*Phone)[\s:]*([+\d\s\-\(\)]{7,})'],
    "CustomerEmail": [r'(?:Customer\s*Email)[\s:]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'],
    "CustomerTaxId": [r'(?:Customer\s*Tax\s*ID)[\s#:]*([A-Z0-9-]+)'],
    "CustomerContactPerson": [r'(?:Customer\s*Contact)[\s:]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)'],
    
    "InvoiceId": [r'(?:Invoice\s*#|Invoice\s*Number)[\s:]*([A-Z0-9-]+)'],
    "InvoiceDate": [r'(?:Invoice\s*Date|Date)[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'],
    "DueDate": [r'(?:Due\s*Date)[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'],
    "InvoiceCurrency": [r'(?:Currency)[\s:]*([A-Z]{3})'],
    "InvoiceType": [r'(?:Invoice\s*Type)[\s:]*([A-Za-z\s]+)'],
    "PurchaseOrder": [r'(?:PO\s*#|Purchase\s*Order)[\s:]*([A-Z0-9-]+)'],
    "PaymentTerms": [r'(?:Payment\s*Terms)[\s:]*([^\n\r]+)'],
    "PaymentMethod": [r'(?:Payment\s*Method)[\s:]*([A-Za-z\s]+)'],
    "CostCenter": [r'(?:Cost\s*Center)[\s:]*([A-Z0-9-]+)'],
    "ServicePeriodStart": [r'(?:Service\s*Period|From)[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'],
    "ServicePeriodEnd": [r'(?:To|End)[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'],
    
    "TotalTax": [r'(?:Total\s*Tax)[\s:]*\$?([\d,]+\.?\d*)'],
    "WithholdingTax": [r'(?:Withholding\s*Tax)[\s:]*\$?([\d,]+\.?\d*)'],
    
    "Subtotal": [r'(?:Subtotal)[\s:]*\$?([\d,]+\.?\d*)'],
    "ShippingHandling": [r'(?:Shipping|Handling)[\s:]*\$?([\d,]+\.?\d*)'],
    "Surcharges": [r'(?:Surcharge)[\s:]*\$?([\d,]+\.?\d*)'],
    "InvoiceTotal": [r'(?:Invoice\s*Total|Grand\s*Total)[\s:]*\$?([\d,]+\.?\d*)'],
    "AmountPaid": [r'(?:Amount\s*Paid)[\s:]*\$?([\d,]+\.?\d*)'],
    "AmountDue": [r'(?:Amount\s*Due)[\s:]*\$?([\d,]+\.?\d*)'],
    
    "Notes": [r'(?:Notes|Remarks)[\s:]*(.*?)(?=\n\s*\n|\Z)'],
    "QRCode": [r'(?:QR\s*Code)[\s:]*([A-Z0-9]{10,})'],
    "CompanyRegistration": [r'(?:Company\s*Reg\.)[\s:]*([A-Z0-9-]+)'],
}

# =============================================================================
# CORE EXTRACTION FUNCTIONS
# =============================================================================

def extract_text_from_pdf(file_path):
    """Extract raw text from PDF for fallback processing"""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"⚠️ PDF text extraction failed: {e}")
        return ""

def extract_field_value(field):
    """Extract value from Azure Document field with proper type handling"""
    if not field:
        return None
    
    try:
        if hasattr(field, 'value_string') and field.value_string:
            return field.value_string
        elif hasattr(field, 'value_currency') and field.value_currency:
            return {
                "amount": field.value_currency.amount,
                "currency": field.value_currency.currency_symbol,
                "currency_code": field.value_currency.currency_code
            }
        elif hasattr(field, 'value_date') and field.value_date:
            return str(field.value_date)
        elif hasattr(field, 'value_address') and field.value_address:
            address_data = {
                "street_address": getattr(field.value_address, 'street_address', ''),
                "city": getattr(field.value_address, 'city', ''),
                "state": getattr(field.value_address, 'state', ''),
                "postal_code": getattr(field.value_address, 'postal_code', ''),
                "country": getattr(field.value_address, 'country_region', ''),
            }
            return {k: v for k, v in address_data.items() if v}
        elif hasattr(field, 'value_phone_number') and field.value_phone_number:
            return field.value_phone_number
        elif hasattr(field, 'value_number') and field.value_number:
            return field.value_number
        elif hasattr(field, 'value_array') and field.value_array:
            return [extract_field_value(item) for item in field.value_array]
        elif hasattr(field, 'value_object') and field.value_object:
            return {key: extract_field_value(value) for key, value in field.value_object.items()}
    except Exception as e:
        print(f"⚠️ Error extracting field value: {e}")
    
    return None

# =============================================================================
# LINE ITEM EXTRACTION - COMPREHENSIVE IMPLEMENTATION
# =============================================================================

def extract_line_items_enhanced(items_field, text_content=""):
    """Enhanced line item extraction with multiple fallback strategies"""
    line_items = []
    
    # Strategy 1: Azure Document Intelligence Line Items
    if items_field and hasattr(items_field, 'value_array'):
        azure_items = extract_line_items_from_azure(items_field)
        if azure_items:
            line_items.extend(azure_items)
            print(f"✅ Azure extracted {len(azure_items)} line items")
    
    # Strategy 2: If no items from Azure, try text-based extraction
    if not line_items and text_content:
        text_items = extract_line_items_from_text(text_content)
        if text_items:
            line_items.extend(text_items)
            print(f"✅ Text extraction found {len(text_items)} line items")
    
    # Strategy 3: If still no items, try LLM-based extraction
    if not line_items and text_content:
        llm_items = extract_line_items_with_llm(text_content)
        if llm_items:
            line_items.extend(llm_items)
            print(f"✅ LLM extracted {len(llm_items)} line items")
    
    print(f"📊 Total line items extracted: {len(line_items)}")
    return line_items

def extract_line_items_from_azure(items_field):
    """Extract line items from Azure Document Intelligence response"""
    line_items = []
    
    try:
        for idx, item in enumerate(items_field.value_array):
            if hasattr(item, 'value_object'):
                item_data = item.value_object
                line_item = {
                    "item_number": idx + 1,
                    "Description": extract_field_value(item_data.get('Description')),
                    "ItemCode": extract_field_value(item_data.get('ProductCode')),
                    "Quantity": extract_field_value(item_data.get('Quantity')),
                    "UnitOfMeasure": extract_field_value(item_data.get('Unit')),
                    "UnitPrice": extract_field_value(item_data.get('UnitPrice')),
                    "Discount": extract_field_value(item_data.get('Discount')),
                    "NetAmount": extract_field_value(item_data.get('Amount')),
                    "TaxRate": extract_field_value(item_data.get('TaxRate')),
                    "TaxAmount": extract_field_value(item_data.get('TaxAmount')),
                    "GrossAmount": extract_field_value(item_data.get('TotalPrice')),
                }
                # Remove None values and empty fields
                line_item = {k: v for k, v in line_item.items() if v is not None and v != ""}
                if line_item:
                    line_items.append(line_item)
                    
    except Exception as e:
        print(f"⚠️ Error extracting line items from Azure: {e}")
    
    return line_items

def extract_line_items_from_text(text_content):
    """Extract line items from raw text using pattern matching"""
    line_items = []
    
    try:
        lines = text_content.split('\n')
        
        # Table header patterns - more comprehensive
        table_header_patterns = [
            r'description.*qty.*price.*amount',
            r'item.*quantity.*unit.*total',
            r'product.*qty.*rate.*amount',
            r'description.*quantity.*unit price.*total',
            r'item.*description.*amount',
            r'sr.*no.*description.*amount',
            r'no.*description.*quantity.*price',
            r'line.*item.*description.*total',
            r'service.*description.*amount',
            r'charge.*description.*amount',
        ]
        
        # Find table start by looking for headers
        table_start = -1
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            if any(re.search(pattern, line_lower) for pattern in table_header_patterns):
                table_start = i + 1
                print(f"📋 Found table header at line {i}: {line}")
                break
        
        # If no clear header found, look for numbered items
        if table_start == -1:
            for i, line in enumerate(lines):
                if (re.match(r'^\d+\.', line.strip()) or 
                    re.match(r'^item\s*\d+', line.lower().strip()) or
                    re.match(r'^\d+\s+[A-Za-z]', line.strip())):
                    table_start = i
                    break
        
        if table_start == -1:
            print("❌ No line item table found in text")
            return line_items
        
        print(f"🔍 Scanning for line items starting from line {table_start}")
        
        # Extract table rows - more lines to handle multi-line descriptions
        for i in range(table_start, min(table_start + 100, len(lines))):
            line = lines[i].strip()
            if not line:
                continue
                
            # Skip lines that are clearly not line items
            if any(keyword in line.lower() for keyword in [
                'subtotal', 'total', 'tax', 'balance', 'grand total', 
                'amount due', 'thank you', 'terms', 'payment'
            ]):
                print(f"⏹️ Stopping at summary line: {line}")
                break
                
            # Skip header-like lines
            if any(keyword in line.lower() for keyword in [
                'description', 'qty', 'quantity', 'price', 'amount', 
                'unit', 'rate', 'total', 'item no', 'sr no'
            ]):
                continue
            
            # Try to parse as line item
            line_item = parse_line_item_text(line, len(line_items) + 1)
            if line_item and validate_line_item(line_item):
                line_items.append(line_item)
                print(f"   ✅ Line item {len(line_items)}: {line_item.get('Description', 'N/A')[:50]}...")
    
    except Exception as e:
        print(f"⚠️ Error extracting line items from text: {e}")
    
    return line_items

def parse_line_item_text(line_text, item_number):
    """Parse a line of text into line item components"""
    try:
        # Clean the text
        clean_text = re.sub(r'\s+', ' ', line_text.strip())
        
        # Common line item patterns with better matching
        patterns = [
            # Pattern: "1. Description Qty UnitPrice Amount"
            r'^(\d+)\.?\s+(.+?)\s+(\d+\.?\d*)\s+(\d+\.?\d*)\s+(\d+\.?\d*)$',
            # Pattern: "Description Qty UnitPrice Amount"
            r'^(.+?)\s+(\d+\.?\d*)\s+(\d+\.?\d*)\s+(\d+\.?\d*)$',
            # Pattern: "ItemNo Description Amount"
            r'^(\d+)\.?\s+(.+?)\s+([$\d,\.]+)$',
            # Pattern: "Description - Quantity x UnitPrice = Amount"
            r'^(.+?)\s+[-]?\s*(\d+\.?\d*)\s*[x×]\s*([$\d,\.]+)\s*[=]?\s*([$\d,\.]+)$',
            # Pattern: "Description Amount"
            r'^(.+?)\s+([$\d,\.]+)$',
        ]
        
        for pattern in patterns:
            match = re.match(pattern, clean_text)
            if match:
                groups = match.groups()
                line_item = {"item_number": item_number}
                
                if len(groups) >= 5:
                    # Pattern with item no, description, qty, unit price, amount
                    line_item["ItemCode"] = groups[0]
                    line_item["Description"] = groups[1].strip()
                    line_item["Quantity"] = extract_number(groups[2])
                    line_item["UnitPrice"] = extract_currency(groups[3])
                    line_item["NetAmount"] = extract_currency(groups[4])
                elif len(groups) >= 4:
                    # Pattern with description, qty, unit price, amount
                    line_item["Description"] = groups[0].strip()
                    line_item["Quantity"] = extract_number(groups[1])
                    line_item["UnitPrice"] = extract_currency(groups[2])
                    line_item["NetAmount"] = extract_currency(groups[3])
                elif len(groups) >= 3:
                    # Pattern with item no, description, amount
                    if groups[0].isdigit():
                        line_item["ItemCode"] = groups[0]
                        line_item["Description"] = groups[1].strip()
                        line_item["NetAmount"] = extract_currency(groups[2])
                    else:
                        line_item["Description"] = groups[0].strip()
                        line_item["Quantity"] = extract_number(groups[1])
                        line_item["UnitPrice"] = extract_currency(groups[2])
                elif len(groups) >= 2:
                    # Simple pattern with description and amount
                    line_item["Description"] = groups[0].strip()
                    line_item["NetAmount"] = extract_currency(groups[1])
                
                # Calculate missing fields if possible
                if line_item.get("Quantity") and line_item.get("UnitPrice") and not line_item.get("NetAmount"):
                    line_item["NetAmount"] = line_item["Quantity"] * line_item["UnitPrice"]
                
                return line_item
        
        # Fallback: If no pattern matches, treat as description only
        amount = extract_currency_from_text(line_text)
        return {
            "item_number": item_number,
            "Description": clean_text,
            "NetAmount": amount
        }
        
    except Exception as e:
        print(f"⚠️ Error parsing line item text: {e}")
        return None

def extract_line_items_with_llm(text_content):
    """Use LLM to extract line items from complex text"""
    try:
        system_prompt = """
        You are an expert at extracting line items from invoices. Extract all line items and return as JSON array.
        Each line item should have: Description, Quantity, UnitPrice, NetAmount.
        Return ONLY valid JSON, no explanations.
        """
        
        user_prompt = f"""
        Extract line items from this invoice text. Return as JSON array:
        
        {text_content[:6000]}  # Limit text to avoid token limits
        
        Return format:
        [
          {{
            "item_number": 1,
            "Description": "Product or service name",
            "ItemCode": "SKU or code if available",
            "Quantity": 1,
            "UnitOfMeasure": "units/pcs/etc",
            "UnitPrice": 100.00,
            "Discount": 0.00,
            "NetAmount": 100.00,
            "TaxRate": 10.0,
            "TaxAmount": 10.00,
            "GrossAmount": 110.00
          }}
        ]
        For missing fields, use null. Return ONLY JSON.
        """
        
        response = azure_openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=2000
        )
        
        llm_content = response.choices[0].message.content.strip()
        llm_content = re.sub(r'^```json\s*|\s*```$', '', llm_content)
        
        line_items = json.loads(llm_content)
        print(f"🧠 LLM extracted {len(line_items)} line items")
        return line_items
        
    except Exception as e:
        print(f"❌ LLM line item extraction failed: {e}")
        return []

def validate_line_item(line_item):
    """Validate if a line item is meaningful"""
    if not line_item:
        return False
    
    # Must have at least description or amount
    has_description = line_item.get("Description") and len(str(line_item["Description"]).strip()) > 2
    has_amount = line_item.get("NetAmount") is not None
    
    if not has_description and not has_amount:
        return False
    
    # Check if it's actually a total or summary line
    description = str(line_item.get("Description", "")).lower()
    if any(term in description for term in [
        'total', 'subtotal', 'tax', 'balance', 'amount due', 
        'grand total', 'balance due', 'payment', 'thank you'
    ]):
        return False
    
    # Check if description is too generic
    if description in ['', 'description', 'item', 'service', 'product']:
        return False
    
    return True

def extract_number(text):
    """Extract number from text"""
    if text is None:
        return None
    match = re.search(r'(\d+\.?\d*)', str(text))
    return float(match.group(1)) if match else None

def extract_currency(text):
    """Extract currency amount from text"""
    if text is None:
        return None
    # Handle both string and object types
    text_str = str(text)
    match = re.search(r'[\$€£¥]?\s*(\d+[,.]?\d*\.?\d*)', text_str)
    if match:
        return float(match.group(1).replace(',', ''))
    return None

def extract_currency_from_text(text):
    """Extract currency amount from any text"""
    matches = re.findall(r'[\$€£¥]?\s*(\d+[,.]?\d*\.?\d*)', str(text))
    if matches:
        return float(matches[-1].replace(',', ''))  # Take the last amount found
    return None

# =============================================================================
# LINE ITEMS COUNT CALCULATION
# =============================================================================

def calculate_line_items_count(invoice_dict):
    """Calculate and set LineItems_Count field"""
    line_items = invoice_dict.get("items", [])
    line_items_count = len(line_items)
    
    # Always set LineItems_Count, never "na"
    invoice_dict["fields"]["LineItems_Count"] = {
        "value": line_items_count,
        "confidence": 1.0 if line_items_count > 0 else 0.0,
        "method": "Calculated"
    }
    
    print(f"📈 LineItems_Count set to: {line_items_count}")
    return line_items_count

# =============================================================================
# AZURE DOCUMENT INTELLIGENCE EXTRACTION
# =============================================================================

def extract_with_azure_invoice(file_path):
    """Azure Document Intelligence Primary Extraction"""
    try:
        print(f"🔍 Azure DI extraction: {os.path.basename(file_path)}")
        
        with open(file_path, "rb") as f:
            poller = document_intelligence_client.begin_analyze_document(
                "prebuilt-invoice", 
                body=f,
                content_type="application/octet-stream"
            )
            invoices = poller.result()
        
        invoice_data = []
        
        for idx, invoice in enumerate(invoices.documents):
            invoice_dict = {
                "invoice_number": idx + 1,
                "source_file": os.path.basename(file_path),
                "fields": {},
                "items": [],
                "extraction_metadata": {
                    "methods_used": ["AzurePrebuiltInvoice"],
                    "confidence_scores": {},
                    "processing_timestamp": datetime.now().isoformat()
                }
            }
            
            fields = invoice.fields
            
            # Extract mapped fields
            for target_field, source_field in ENHANCED_FIELD_MAPPINGS.items():
                if source_field in fields:
                    field_value = extract_field_value(fields[source_field])
                    if field_value and field_value != "na":
                        invoice_dict["fields"][target_field] = {
                            "value": field_value,
                            "confidence": getattr(fields[source_field], 'confidence', 0.8),
                            "method": "AzurePrebuiltInvoice"
                        }
            
            # Extract line items using enhanced method
            if 'Items' in fields:
                text_content = extract_text_from_pdf(file_path)  # Get text for fallback
                line_items = extract_line_items_enhanced(fields['Items'], text_content)
                invoice_dict["items"] = line_items
            
            invoice_data.append(invoice_dict)
        
        return invoice_data[0] if invoice_data else None
        
    except Exception as e:
        print(f"❌ Azure extraction failed: {e}")
        return None

# =============================================================================
# OPENAI LLM EXTRACTION
# =============================================================================

def extract_with_openai_llm(text_content, file_path=None):
    """Use OpenAI LLM for intelligent field extraction"""
    print("🧠 Using OpenAI LLM for field extraction...")
    
    try:
        system_prompt = """
        You are an expert invoice data extraction specialist. Extract fields from the invoice text.
        Return ONLY valid JSON format with the exact field names. For missing fields, use "na".
        """

        user_prompt = f"""
        Extract invoice fields from this text. Return ONLY JSON:

        {text_content[:8000]}

        Return JSON format with these fields:
        {json.dumps(ALL_56_FIELDS, indent=2)}

        Important: For LineItems_Count, provide the actual number of line items found in the invoice.
        """

        response = azure_openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=3000
        )

        llm_content = response.choices[0].message.content.strip()
        llm_content = re.sub(r'^```json\s*|\s*```$', '', llm_content)
        
        llm_data = json.loads(llm_content)
        print(f"✅ OpenAI LLM extracted {len([v for v in llm_data.values() if v != 'na'])} fields")
        
        return llm_data
        
    except Exception as e:
        print(f"❌ OpenAI LLM extraction failed: {e}")
        return {}

# =============================================================================
# REGEX EXTRACTION
# =============================================================================

def extract_missing_fields_with_regex(text_content, invoice_dict):
    """Extract fields using comprehensive regex patterns"""
    print("🔍 Applying regex extraction for missing fields...")
    
    regex_data = {}
    extracted_count = 0
    
    for field_name, patterns in COMPREHENSIVE_REGEX_PATTERNS.items():
        # Skip if field already exists
        if field_name in invoice_dict.get("fields", {}):
            continue
            
        for pattern in patterns:
            match = re.search(pattern, text_content, re.IGNORECASE | re.MULTILINE)
            if match:
                value = match.group(1).strip() if match.groups() else match.group(0).strip()
                if value and len(value) > 0:
                    regex_data[field_name] = {
                        "value": value,
                        "confidence": 0.7,
                        "method": "Regex"
                    }
                    extracted_count += 1
                    break
    
    print(f"✅ Regex extracted {extracted_count} additional fields")
    return regex_data

# =============================================================================
# INTELLIGENT FIELD FUSION
# =============================================================================

def intelligent_field_fusion(azure_data, llm_data, regex_data):
    """Intelligently fuse data from all extraction sources"""
    print("🔄 Performing intelligent field fusion...")
    
    fused_fields = {}
    confidence_scores = {}
    extraction_methods = {}
    
    for field in ALL_56_FIELDS:
        candidates = []
        
        # Collect candidates from all sources
        if field in azure_data:
            candidates.append(("azure", azure_data[field], 0.9))
        
        if field in llm_data and llm_data[field] != "na":
            # Convert LLM simple values to structured format
            llm_value = {
                "value": llm_data[field],
                "confidence": 0.8,
                "method": "OpenAI_LLM"
            }
            candidates.append(("llm", llm_value, 0.8))
            
        if field in regex_data:
            candidates.append(("regex", regex_data[field], 0.7))
        
        if not candidates:
            fused_fields[field] = {
                "value": "na",
                "confidence": 0.0,
                "method": "NotAvailable"
            }
            continue
        
        # Sort by confidence and select best candidate
        candidates.sort(key=lambda x: x[2], reverse=True)
        best_source, best_value, best_confidence = candidates[0]
        
        fused_fields[field] = best_value
        confidence_scores[field] = best_confidence
        extraction_methods[field] = best_source
    
    return fused_fields, confidence_scores, extraction_methods

# =============================================================================
# DERIVED FIELDS CALCULATION
# =============================================================================

def calculate_derived_fields(invoice_dict, text_content=""):
    """Calculate derived fields from extracted data"""
    print("🔍 Calculating derived fields...")
    
    derived_count = 0
    
    # Calculate tax breakdown from line items
    line_items = invoice_dict.get("items", [])
    if line_items and "TaxTypeBreakdown" not in invoice_dict["fields"]:
        tax_breakdown = {}
        total_tax_from_items = 0.0
        
        for item in line_items:
            tax_amount = item.get("TaxAmount")
            if isinstance(tax_amount, (int, float)) and tax_amount > 0:
                total_tax_from_items += tax_amount
                tax_type = "Sales Tax"
                
                # Try to determine tax type from description
                description = str(item.get("Description", "")).lower()
                if 'vat' in description:
                    tax_type = "VAT"
                elif 'gst' in description:
                    tax_type = "GST"
                
                if tax_type in tax_breakdown:
                    tax_breakdown[tax_type] += tax_amount
                else:
                    tax_breakdown[tax_type] = tax_amount
        
        if tax_breakdown:
            invoice_dict["fields"]["TaxTypeBreakdown"] = {
                "value": tax_breakdown,
                "confidence": 0.7,
                "method": "CalculatedFromItems"
            }
            derived_count += 1
    
    # Set VendorCountry from VendorAddress if available
    if "VendorAddress" in invoice_dict["fields"] and "VendorCountry" not in invoice_dict["fields"]:
        vendor_address = invoice_dict["fields"]["VendorAddress"]["value"]
        if isinstance(vendor_address, dict) and vendor_address.get("country"):
            invoice_dict["fields"]["VendorCountry"] = {
                "value": vendor_address["country"],
                "confidence": invoice_dict["fields"]["VendorAddress"]["confidence"] * 0.9,
                "method": "DerivedFromAddress"
            }
            derived_count += 1
    
    print(f"✅ Derived {derived_count} calculated fields")
    return derived_count

# =============================================================================
# MAIN EXTRACTION FUNCTION
# =============================================================================

def enhanced_extract_invoice_data(file_path):
    """Comprehensive extraction with enhanced line item focus"""
    print(f"🚀 Starting enhanced extraction: {os.path.basename(file_path)}")
    
    # Initialize result structure
    final_result = {
        "invoice_number": 1,
        "source_file": os.path.basename(file_path),
        "fields": {},
        "items": [],  # This will store our line items
        "extraction_metadata": {
            "methods_used": [],
            "confidence_scores": {},
            "processing_timestamp": datetime.now().isoformat(),
            "extraction_strategies": [],
            "line_items_method": "None"
        }
    }
    
    # Extract text for all methods
    text_content = extract_text_from_pdf(file_path)
    
    # STRATEGY 1: Azure Document Intelligence
    azure_data = {}
    azure_items = []
    
    try:
        azure_result = extract_with_azure_invoice(file_path)
        if azure_result:
            azure_data = azure_result.get("fields", {})
            azure_items = azure_result.get("items", [])
            final_result["extraction_metadata"]["methods_used"].append("AzureDocumentIntelligence")
            final_result["extraction_metadata"]["extraction_strategies"].append("AzurePrebuiltInvoice")
            
            if azure_items:
                final_result["extraction_metadata"]["line_items_method"] = "Azure"
                print(f"✅ Azure extracted {len(azure_items)} line items")
    except Exception as e:
        print(f"❌ Azure extraction failed: {e}")
    
    # STRATEGY 2: Extract line items (priority)
    all_line_items = azure_items  # Start with Azure items
    
    # Fallback to text extraction if no Azure items
    if not all_line_items and text_content:
        text_items = extract_line_items_from_text(text_content)
        if text_items:
            all_line_items.extend(text_items)
            final_result["extraction_metadata"]["line_items_method"] = "TextExtraction"
            final_result["extraction_metadata"]["methods_used"].append("TextLineItems")
            print(f"✅ Text extraction found {len(text_items)} line items")
    
    # Final fallback to LLM
    if not all_line_items and text_content:
        llm_items = extract_line_items_with_llm(text_content)
        if llm_items:
            all_line_items.extend(llm_items)
            final_result["extraction_metadata"]["line_items_method"] = "LLM"
            final_result["extraction_metadata"]["methods_used"].append("LLMLineItems")
            print(f"✅ LLM extracted {len(llm_items)} line items")
    
    # Store the line items
    final_result["items"] = all_line_items
    
    # STRATEGY 3: Field extraction from other sources
    llm_data = {}
    if text_content:
        llm_data = extract_with_openai_llm(text_content, file_path)
        if llm_data:
            final_result["extraction_metadata"]["methods_used"].append("OpenAI_LLM_Text")
    
    # STRATEGY 4: Regex extraction
    regex_data = {}
    if text_content:
        regex_data = extract_missing_fields_with_regex(text_content, final_result)
        final_result["extraction_metadata"]["methods_used"].append("EnhancedRegex")
    
    # Fuse all field data
    fused_fields, confidence_scores, extraction_methods = intelligent_field_fusion(
        azure_data, llm_data, regex_data
    )
    
    final_result["fields"] = fused_fields
    final_result["extraction_metadata"]["confidence_scores"] = confidence_scores
    
    # STRATEGY 5: Calculate derived fields including line items count
    calculate_line_items_count(final_result)
    calculate_derived_fields(final_result, text_content)
    
    # STRATEGY 6: Set missing fields to 'na'
    for field in ALL_56_FIELDS:
        if field not in final_result["fields"]:
            final_result["fields"][field] = {
                "value": "na",
                "confidence": 0.0,
                "method": "NotAvailable"
            }
    
    final_result["extraction_metadata"]["extraction_strategies"].append("MissingFieldHandling")
    
    # Calculate extraction statistics
    total_fields = len(ALL_56_FIELDS)
    extracted_fields = len([f for f in final_result["fields"].keys() if final_result["fields"][f]["value"] != "na"])
    extraction_rate = (extracted_fields / total_fields) * 100
    
    line_items_count = len(all_line_items)
    
    print(f"📊 EXTRACTION SUMMARY:")
    print(f"   📈 Fields: {extracted_fields}/{total_fields} ({extraction_rate:.1f}%)")
    print(f"   📦 Line Items: {line_items_count}")
    print(f"   🔧 Line Items Method: {final_result['extraction_metadata']['line_items_method']}")
    print(f"   🎯 Methods: {', '.join(final_result['extraction_metadata']['methods_used'])}")
    
    return [final_result]

# =============================================================================
# FLASK APP AND PROCESSING FUNCTIONS
# =============================================================================

def sanitize_filename(filename):
    """Sanitize filename to be safe for Windows file system"""
    sanitized = re.sub(r'[<>:"/\\|?*#&${}~%]', '_', filename)
    sanitized = re.sub(r'_+', '_', sanitized)
    sanitized = sanitized.strip(' _')
    if len(sanitized) > 200:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:200-len(ext)] + ext
    return sanitized

def save_individual_json(invoice_data, filename):
    """Save individual invoice data as JSON file"""
    try:
        base_name = os.path.splitext(filename)[0]
        safe_base_name = sanitize_filename(base_name)
        json_filename = f"{safe_base_name}_extracted.json"
        json_filepath = os.path.join(json_output_folder, json_filename)
        
        os.makedirs(os.path.dirname(json_filepath), exist_ok=True)
        
        with open(json_filepath, 'w', encoding='utf-8') as json_file:
            json.dump(invoice_data, json_file, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved individual JSON: {json_filename}")
        return json_filename
    except Exception as e:
        print(f"❌ Failed to save JSON for {filename}: {e}")
        return None

def process_all_pdfs_in_folder(folder_path):
    """Process ALL PDF files in a folder and generate individual JSON files"""
    print(f"📁 Processing folder: {folder_path}")
    
    if not os.path.exists(folder_path):
        error_msg = f"Folder not found: {folder_path}"
        print(f"❌ {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "message": "Please create the 'invoices' folder and add PDF files"
        }
    
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        error_msg = f"No PDF files found in {folder_path}"
        print(f"❌ {error_msg}")
        return {
            "success": False,
            "error": "No PDF files found",
            "message": error_msg
        }
    
    print(f"📁 Found {len(pdf_files)} PDF files in folder")
    
    results = []
    successful_files = 0
    failed_files = 0
    json_files_created = []
    
    for pdf_file in pdf_files:
        file_path = os.path.join(folder_path, pdf_file)
        print(f"🔄 Processing: {pdf_file}")
        
        try:
            result_data = enhanced_extract_invoice_data(file_path)
            result = {
                "success": True,
                "data": result_data,
                "filename": pdf_file,
                "message": f"Successfully processed {len(result_data)} invoice(s)"
            }
            
            # Save individual JSON file
            if result_data:
                json_filename = save_individual_json(result_data, pdf_file)
                if json_filename:
                    json_files_created.append(json_filename)
                    result["json_file"] = json_filename
                    successful_files += 1
                    print(f"✅ Success + JSON saved: {pdf_file}")
                else:
                    failed_files += 1
                    print(f"❌ JSON save failed: {pdf_file}")
            else:
                failed_files += 1
                print(f"❌ Processing failed: {pdf_file}")
                
            results.append(result)
                
        except Exception as e:
            print(f"❌ Error processing {pdf_file}: {e}")
            results.append({
                "success": False,
                "error": str(e),
                "filename": pdf_file,
                "message": f"Failed to process {pdf_file}"
            })
            failed_files += 1
    
    # Create Excel from all JSON files
    excel_result = create_excel_from_json_files()
    
    summary = {
        "total_files": len(pdf_files),
        "successful": successful_files,
        "failed": failed_files,
        "json_files_created": len(json_files_created),
        "excel_created": excel_result["success"]
    }
    
    print(f"📊 Processing complete: {summary}")
    
    return {
        "success": True,
        "results": results,
        "json_files": json_files_created,
        "excel_file": excel_result.get("excel_filename"),
        "excel_summary": excel_result.get("summary"),
        "summary": summary
    }

def create_excel_from_json_files():
    """Create single Excel file from all JSON files in the json_output_folder"""
    print(f"📊 Creating Excel from JSON files in: {json_output_folder}")
    
    # Create DataFrame
    rows = []
    json_files = [f for f in os.listdir(json_output_folder) if f.endswith('.json')]
    
    if not json_files:
        print("⚠️ No JSON files found to create Excel")
        return {
            "success": False,
            "error": "No JSON files found",
            "message": "No JSON files were created during processing"
        }
    
    print(f"📁 Found {len(json_files)} JSON files to process")
    
    for json_file in json_files:
        json_path = os.path.join(json_output_folder, json_file)
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                invoice_data = json.load(f)
            
            for invoice in invoice_data:
                row = {"Filename": invoice.get("source_file", json_file)}
                
                # Extract field values
                fields = invoice.get("fields", {})
                for field_name in ALL_56_FIELDS:
                    if field_name in fields:
                        field_data = fields[field_name]
                        value = field_data.get("value", None)
                        if value is not None and value != "na":
                            if isinstance(value, (dict, list)):
                                try:
                                    row[field_name] = json.dumps(value, ensure_ascii=False)
                                except:
                                    row[field_name] = str(value)
                            else:
                                row[field_name] = str(value)
                        else:
                            row[field_name] = "ne" if value == "na" else "ne"
                    else:
                        row[field_name] = "na"
                
                # Add line items count explicitly
                line_items = invoice.get("items", [])
                row["LineItems_Count_Actual"] = len(line_items)
                
                rows.append(row)
                print(f"📝 Added row from {json_file} with {len(line_items)} line items")
                
        except Exception as e:
            print(f"❌ Error processing JSON file {json_file}: {e}")
            row = {"Filename": json_file}
            for field_name in ALL_56_FIELDS:
                row[field_name] = "ne"
            rows.append(row)
    
    if not rows:
        print("⚠️ No data rows to process for Excel")
        return {"success": False, "error": "No data extracted from JSON files"}
    
    df = pd.DataFrame(rows)
    print(f"📊 Created DataFrame with {len(df)} rows and {len(df.columns)} columns")
    
    # Save to Excel
    excel_filename = f"consolidated_invoice_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    excel_filepath = os.path.join(output_folder, excel_filename)
    
    try:
        print(f"💾 Saving consolidated Excel: {excel_filepath}")
        
        with pd.ExcelWriter(excel_filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Extracted_Data', index=False)
            
            worksheet = writer.sheets['Extracted_Data']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
                
        print(f"✅ Consolidated Excel file created: {excel_filepath}")
        
        return {
            "success": True,
            "excel_filename": excel_filename,
            "excel_filepath": excel_filepath,
            "summary": {
                "total_invoices": len(rows),
                "total_fields": len(ALL_56_FIELDS),
                "json_files_processed": len(json_files)
            }
        }
        
    except Exception as e:
        print(f"❌ Excel creation failed: {e}")
        return {"success": False, "error": str(e), "message": "Failed to create Excel file"}

# Flask endpoints
@app.route('/process-folder', methods=['POST'])
def process_folder():
    """Process ALL PDF files in the invoices folder"""
    print("🚀 Received request to process folder")
    try:
        result = process_all_pdfs_in_folder("invoices")
        print(f"✅ Folder processing completed: {result.get('success', False)}")
        return jsonify(result)
    except Exception as e:
        print(f"❌ Folder processing failed: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to process folder"
        }), 500

@app.route('/create-excel-from-json', methods=['POST'])
def create_excel_from_json():
    """Create Excel file from existing JSON files"""
    try:
        result = create_excel_from_json_files()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to create Excel from JSON files"
        }), 500

@app.route('/check-folders', methods=['GET'])
def check_folders():
    """Check if folders exist and show files"""
    folders_info = {
        "pdf_source_folder": {
            "path": "invoices",
            "exists": os.path.exists("invoices"),
            "files": []
        },
        "json_output_folder": {
            "path": json_output_folder,
            "exists": os.path.exists(json_output_folder),
            "files": []
        },
        "output_folder": {
            "path": output_folder,
            "exists": os.path.exists(output_folder),
            "files": []
        }
    }
    
    if folders_info["pdf_source_folder"]["exists"]:
        folders_info["pdf_source_folder"]["files"] = [f for f in os.listdir("invoices") if f.lower().endswith('.pdf')]
    
    if folders_info["json_output_folder"]["exists"]:
        folders_info["json_output_folder"]["files"] = [f for f in os.listdir(json_output_folder) if f.endswith('.json')]
    
    if folders_info["output_folder"]["exists"]:
        folders_info["output_folder"]["files"] = [f for f in os.listdir(output_folder) if f.endswith(('.xlsx', '.csv'))]
    
    return jsonify(folders_info)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Enhanced Invoice Extraction API with Line Items",
        "version": "4.1.0",
        "fields_supported": 56,
        "line_item_extraction": {
            "methods": ["Azure DI", "Text Pattern", "LLM Analysis"],
            "fields_per_item": ["Description", "Quantity", "UnitPrice", "NetAmount", "TaxRate", "TaxAmount", "GrossAmount"]
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Enhanced Invoice Extraction API with Line Items...")
    print("📁 Folder structure:")
    print(f"   - PDF Source: ./invoices/")
    print(f"   - JSON Output: {json_output_folder}")
    print(f"   - Excel Output: {output_folder}")
    print("\n📦 Line Item Extraction Features:")
    print("   - Azure Document Intelligence (Primary)")
    print("   - Text pattern matching (Fallback)")
    print("   - LLM analysis (Complex cases)")
    print("   - Automatic LineItems_Count calculation")
    print("   - Tax breakdown from line items")
    print("\n🎯 Usage:")
    print("   - POST /process-folder - Process all PDFs with enhanced line item extraction")
    print("   - POST /create-excel-from-json - Create Excel from existing JSONs")
    print("   - GET /check-folders - Check folder status")
    
    app.run(debug=True, host='0.0.0.0', port=5000)