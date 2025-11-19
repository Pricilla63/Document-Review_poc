# import os
# import json
# import glob
# from azure.core.credentials import AzureKeyCredential
# from azure.ai.documentintelligence import DocumentIntelligenceClient
# from dotenv import find_dotenv, load_dotenv

# load_dotenv(find_dotenv())

# endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
# key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

# document_intelligence_client = DocumentIntelligenceClient(
#     endpoint=endpoint, credential=AzureKeyCredential(key)
# )

# # Find all PDF files in current directory AND all subdirectories
# pdf_files = glob.glob("**/*.pdf", recursive=True)

# if not pdf_files:
#     print("❌ No PDF files found in current directory or subdirectories")
#     print("Current working directory:", os.getcwd())
#     print("Please make sure your PDF files are in this directory or its subdirectories")
#     exit()

# print(f"📁 Found {len(pdf_files)} PDF files to process")
# print("Files found:")
# for pdf_file in pdf_files:
#     print(f"  - {pdf_file}")

# # Create output folder if it doesn't exist
# output_folder = "output"
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# successful_files = 0
# failed_files = 0

# for pdf_file in pdf_files:
#     try:
#         print(f"\n🔍 Processing: {pdf_file}")
        
#         with open(pdf_file, "rb") as f:
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
#                 "source_file": pdf_file,
#                 "fields": {}
#             }
            
#             vendor_name = invoice.fields.get("VendorName")
#             if vendor_name:
#                 print(
#                     "Vendor Name: {} has confidence: {}".format(
#                         vendor_name.value_string, vendor_name.confidence
#                     )
#                 )
#                 invoice_dict["fields"]["VendorName"] = {
#                     "value": vendor_name.value_string,
#                     "confidence": vendor_name.confidence
#                 }
            
#             vendor_address = invoice.fields.get("VendorAddress")
#             if vendor_address:
#                 print(
#                     "Vendor Address: {} has confidence: {}".format(
#                         vendor_address.value_address, vendor_address.confidence
#                     )
#                 )
#                 invoice_dict["fields"]["VendorAddress"] = {
#                     "value": str(vendor_address.value_address),
#                     "confidence": vendor_address.confidence
#                 }
            
#             vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
#             if vendor_address_recipient:
#                 print(
#                     "Vendor Address Recipient: {} has confidence: {}".format(
#                         vendor_address_recipient.value_string, vendor_address_recipient.confidence
#                     )
#                 )
#                 invoice_dict["fields"]["VendorAddressRecipient"] = {
#                     "value": vendor_address_recipient.value_string,
#                     "confidence": vendor_address_recipient.confidence
#                 }
            
#             customer_name = invoice.fields.get("CustomerName")
#             if customer_name:
#                 print(
#                     "Customer Name: {} has confidence: {}".format(
#                         customer_name.value_string, customer_name.confidence
#                     )
#                 )
#                 invoice_dict["fields"]["CustomerName"] = {
#                     "value": customer_name.value_string,
#                     "confidence": customer_name.confidence
#                 }
            
#             customer_id = invoice.fields.get("CustomerId")
#             if customer_id:
#                 print(
#                     "Customer Id: {} has confidence: {}".format(
#                         customer_id.value_string, customer_id.confidence
#                     )
#                 )
#                 invoice_dict["fields"]["CustomerId"] = {
#                     "value": customer_id.value_string,
#                     "confidence": customer_id.confidence
#                 }
            
#             customer_address = invoice.fields.get("CustomerAddress")
#             if customer_address:
#                 print(
#                     "Customer Address: {} has confidence: {}".format(
#                         customer_address.value_address, customer_address.confidence
#                     )
#                 )
#                 invoice_dict["fields"]["CustomerAddress"] = {
#                     "value": str(customer_address.value_address),
#                     "confidence": customer_address.confidence
#                 }
            
#             customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
#             if customer_address_recipient:
#                 print(
#                     "Customer Address Recipient: {} has confidence: {}".format(
#                         customer_address_recipient.value_string,
#                         customer_address_recipient.confidence,
#                     )
#                 )
#                 invoice_dict["fields"]["CustomerAddressRecipient"] = {
#                     "value": customer_address_recipient.value_string,
#                     "confidence": customer_address_recipient.confidence
#                 }
            
#             invoice_id = invoice.fields.get("InvoiceId")
#             if invoice_id:
#                 print(
#                     "Invoice Id: {} has confidence: {}".format(
#                         invoice_id.value_string, invoice_id.confidence
#                     )
#                 )
#                 invoice_dict["fields"]["InvoiceId"] = {
#                     "value": invoice_id.value_string,
#                     "confidence": invoice_id.confidence
#                 }
            
#             invoice_date = invoice.fields.get("InvoiceDate")
#             if invoice_date:
#                 print(
#                     "Invoice Date: {} has confidence: {}".format(
#                         invoice_date.value_date, invoice_date.confidence
#                     )
#                 )
#                 invoice_dict["fields"]["InvoiceDate"] = {
#                     "value": str(invoice_date.value_date),
#                     "confidence": invoice_date.confidence
#                 }
            
#             invoice_total = invoice.fields.get("InvoiceTotal")
#             if invoice_total:
#                 print(
#                     "Invoice Total: {} has confidence: {}".format(
#                         invoice_total.value_currency.amount, invoice_total.confidence
#                     )
#                 )
#                 invoice_dict["fields"]["InvoiceTotal"] = {
#                     "value": invoice_total.value_currency.amount,
#                     "currency": invoice_total.value_currency.currency_symbol,
#                     "confidence": invoice_total.confidence
#                 }
            
#             due_date = invoice.fields.get("DueDate")
#             if due_date:
#                 print(
#                     "Due Date: {} has confidence: {}".format(
#                         due_date.value_date, due_date.confidence
#                     )
#                 )
#                 invoice_dict["fields"]["DueDate"] = {
#                     "value": str(due_date.value_date),
#                     "confidence": due_date.confidence
#                 }
            
#             purchase_order = invoice.fields.get("PurchaseOrder")
#             if purchase_order:
#                 print(
#                     "Purchase Order: {} has confidence: {}".format(
#                         purchase_order.value_string, purchase_order.confidence
#                     )
#                 )
#                 invoice_dict["fields"]["PurchaseOrder"] = {
#                     "value": purchase_order.value_string,
#                     "confidence": purchase_order.confidence
#                 }
            
#             billing_address = invoice.fields.get("BillingAddress")
#             if billing_address:
#                 print(
#                     "Billing Address: {} has confidence: {}".format(
#                         billing_address.value_address, billing_address.confidence
#                     )
#                 )
#                 invoice_dict["fields"]["BillingAddress"] = {
#                     "value": str(billing_address.value_address),
#                     "confidence": billing_address.confidence
#                 }
            
#             shipping_address = invoice.fields.get("ShippingAddress")
#             if shipping_address:
#                 print(
#                     "Shipping Address: {} has confidence: {}".format(
#                         shipping_address.value_address, shipping_address.confidence
#                     )
#                 )
#                 invoice_dict["fields"]["ShippingAddress"] = {
#                     "value": str(shipping_address.value_address),
#                     "confidence": shipping_address.confidence
#                 }
            
#             # Add items to the invoice
#             invoice_dict["items"] = []
#             print("Invoice items:")
#             if invoice.fields.get("Items"):
#                 for item_idx, item in enumerate(invoice.fields.get("Items").value_array):
#                     print("...Item #{}".format(item_idx + 1))
#                     item_dict = {"item_number": item_idx + 1}
                    
#                     item_description = item.value_object.get("Description")
#                     if item_description:
#                         print(
#                             "......Description: {} has confidence: {}".format(
#                                 item_description.value_string, item_description.confidence
#                             )
#                         )
#                         item_dict["Description"] = {
#                             "value": item_description.value_string,
#                             "confidence": item_description.confidence
#                         }
                    
#                     item_quantity = item.value_object.get("Quantity")
#                     if item_quantity:
#                         print(
#                             "......Quantity: {} has confidence: {}".format(
#                                 item_quantity.value_number, item_quantity.confidence
#                             )
#                         )
#                         item_dict["Quantity"] = {
#                             "value": item_quantity.value_number,
#                             "confidence": item_quantity.confidence
#                         }
                    
#                     unit_price = item.value_object.get("UnitPrice")
#                     if unit_price:
#                         print(
#                             "......Unit Price: {} has confidence: {}".format(
#                                 unit_price.value_currency.amount, unit_price.confidence
#                             )
#                         )
#                         item_dict["UnitPrice"] = {
#                             "value": unit_price.value_currency.amount,
#                             "currency": unit_price.value_currency.currency_symbol,
#                             "confidence": unit_price.confidence
#                         }
                    
#                     amount = item.value_object.get("Amount")
#                     if amount:
#                         print(
#                             "......Amount: {} has confidence: {}".format(
#                                 amount.value_currency.amount, amount.confidence
#                             )
#                         )
#                         item_dict["Amount"] = {
#                             "value": amount.value_currency.amount,
#                             "currency": amount.value_currency.currency_symbol,
#                             "confidence": amount.confidence
#                         }
                    
#                     invoice_dict["items"].append(item_dict)
            
#             invoice_data.append(invoice_dict)
#             print("----------------------------------------")
        
#         # Create JSON filename based on original PDF name
#         base_name = os.path.splitext(os.path.basename(pdf_file))[0]
#         json_filename = f"{base_name}_extracted.json"
#         json_filepath = os.path.join(output_folder, json_filename)
        
#         # Write to JSON file
#         with open(json_filepath, 'w', encoding='utf-8') as json_file:
#             json.dump(invoice_data, json_file, indent=2, ensure_ascii=False)
        
#         print(f"✅ Saved: {json_filename}")
#         successful_files += 1
        
#     except Exception as e:
#         print(f"❌ Error processing {pdf_file}: {e}")
#         failed_files += 1

# # Print summary
# print("\n" + "="*50)
# print("📊 PROCESSING SUMMARY")
# print(f"✅ Successful: {successful_files} files")
# print(f"❌ Failed: {failed_files} files")
# print(f"📁 Output folder: {output_folder}")
# print("="*50)


import os
import json
import glob
from flask import Flask, request, jsonify
from flask_cors import CORS
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from dotenv import find_dotenv, load_dotenv
import tempfile

load_dotenv(find_dotenv())

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Azure Document Intelligence setup
endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

document_intelligence_client = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# Create output folder if it doesn't exist
output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def extract_invoice_data(file_path):
    """Extract invoice data from a single PDF file"""
    try:
        print(f"🔍 Processing: {file_path}")
        
        with open(file_path, "rb") as f:
            # Try different parameter combinations for different SDK versions
            try:
                # Try the newer SDK syntax first
                poller = document_intelligence_client.begin_analyze_document(
                    "prebuilt-invoice", 
                    body=f,
                    content_type="application/octet-stream"
                )
            except TypeError:
                # Fallback to older syntax
                poller = document_intelligence_client.begin_analyze_document(
                    "prebuilt-invoice", 
                    analyze_request=f,
                    content_type="application/octet-stream"
                )
            
            invoices = poller.result()
        
        invoice_data = []
        
        for idx, invoice in enumerate(invoices.documents):
            print("--------Recognizing invoice #{}--------".format(idx + 1))
            
            invoice_dict = {
                "invoice_number": idx + 1,
                "source_file": os.path.basename(file_path),
                "fields": {}
            }
            
            # Extract vendor information
            vendor_name = invoice.fields.get("VendorName")
            if vendor_name:
                invoice_dict["fields"]["VendorName"] = {
                    "value": vendor_name.value_string,
                    "confidence": vendor_name.confidence
                }
            
            vendor_address = invoice.fields.get("VendorAddress")
            if vendor_address:
                invoice_dict["fields"]["VendorAddress"] = {
                    "value": str(vendor_address.value_address),
                    "confidence": vendor_address.confidence
                }
            
            vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
            if vendor_address_recipient:
                invoice_dict["fields"]["VendorAddressRecipient"] = {
                    "value": vendor_address_recipient.value_string,
                    "confidence": vendor_address_recipient.confidence
                }
            
            # Extract customer information
            customer_name = invoice.fields.get("CustomerName")
            if customer_name:
                invoice_dict["fields"]["CustomerName"] = {
                    "value": customer_name.value_string,
                    "confidence": customer_name.confidence
                }
            
            customer_id = invoice.fields.get("CustomerId")
            if customer_id:
                invoice_dict["fields"]["CustomerId"] = {
                    "value": customer_id.value_string,
                    "confidence": customer_id.confidence
                }
            
            customer_address = invoice.fields.get("CustomerAddress")
            if customer_address:
                invoice_dict["fields"]["CustomerAddress"] = {
                    "value": str(customer_address.value_address),
                    "confidence": customer_address.confidence
                }
            
            customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
            if customer_address_recipient:
                invoice_dict["fields"]["CustomerAddressRecipient"] = {
                    "value": customer_address_recipient.value_string,
                    "confidence": customer_address_recipient.confidence
                }
            
            # Extract invoice details
            invoice_id = invoice.fields.get("InvoiceId")
            if invoice_id:
                invoice_dict["fields"]["InvoiceId"] = {
                    "value": invoice_id.value_string,
                    "confidence": invoice_id.confidence
                }
            
            invoice_date = invoice.fields.get("InvoiceDate")
            if invoice_date:
                invoice_dict["fields"]["InvoiceDate"] = {
                    "value": str(invoice_date.value_date),
                    "confidence": invoice_date.confidence
                }
            
            invoice_total = invoice.fields.get("InvoiceTotal")
            if invoice_total:
                invoice_dict["fields"]["InvoiceTotal"] = {
                    "value": invoice_total.value_currency.amount,
                    "currency": invoice_total.value_currency.currency_symbol,
                    "confidence": invoice_total.confidence
                }
            
            due_date = invoice.fields.get("DueDate")
            if due_date:
                invoice_dict["fields"]["DueDate"] = {
                    "value": str(due_date.value_date),
                    "confidence": due_date.confidence
                }
            
            purchase_order = invoice.fields.get("PurchaseOrder")
            if purchase_order:
                invoice_dict["fields"]["PurchaseOrder"] = {
                    "value": purchase_order.value_string,
                    "confidence": purchase_order.confidence
                }
            
            billing_address = invoice.fields.get("BillingAddress")
            if billing_address:
                invoice_dict["fields"]["BillingAddress"] = {
                    "value": str(billing_address.value_address),
                    "confidence": billing_address.confidence
                }
            
            shipping_address = invoice.fields.get("ShippingAddress")
            if shipping_address:
                invoice_dict["fields"]["ShippingAddress"] = {
                    "value": str(shipping_address.value_address),
                    "confidence": shipping_address.confidence
                }
            
            # Extract line items
            invoice_dict["items"] = []
            if invoice.fields.get("Items"):
                for item_idx, item in enumerate(invoice.fields.get("Items").value_array):
                    item_dict = {"item_number": item_idx + 1}
                    
                    item_description = item.value_object.get("Description")
                    if item_description:
                        item_dict["Description"] = {
                            "value": item_description.value_string,
                            "confidence": item_description.confidence
                        }
                    
                    item_quantity = item.value_object.get("Quantity")
                    if item_quantity:
                        item_dict["Quantity"] = {
                            "value": item_quantity.value_number,
                            "confidence": item_quantity.confidence
                        }
                    
                    unit_price = item.value_object.get("UnitPrice")
                    if unit_price:
                        item_dict["UnitPrice"] = {
                            "value": unit_price.value_currency.amount,
                            "currency": unit_price.value_currency.currency_symbol,
                            "confidence": unit_price.confidence
                        }
                    
                    amount = item.value_object.get("Amount")
                    if amount:
                        item_dict["Amount"] = {
                            "value": amount.value_currency.amount,
                            "currency": amount.value_currency.currency_symbol,
                            "confidence": amount.confidence
                        }
                    
                    invoice_dict["items"].append(item_dict)
            
            invoice_data.append(invoice_dict)
            print("----------------------------------------")
        
        return {
            "success": True,
            "data": invoice_data,
            "message": f"Successfully processed {len(invoice_data)} invoice(s)"
        }
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to process file: {str(e)}"
        }

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "error": "No file provided",
                "message": "Please select a file to upload"
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected",
                "message": "Please select a file to upload"
            }), 400
        
        # Check file extension
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({
                "success": False,
                "error": "Invalid file type",
                "message": "Only PDF files are supported"
            }), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name
        
        try:
            # Process the file
            result = extract_invoice_data(temp_file_path)
            
            # Save to JSON file if processing was successful
            if result["success"] and result["data"]:
                base_name = os.path.splitext(file.filename)[0]
                json_filename = f"{base_name}_extracted.json"
                json_filepath = os.path.join(output_folder, json_filename)
                
                with open(json_filepath, 'w', encoding='utf-8') as json_file:
                    json.dump(result["data"], json_file, indent=2, ensure_ascii=False)
                
                result["saved_file"] = json_filename
            
            return jsonify(result)
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Internal server error during file processing"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Invoice Processing API",
        "version": "1.0.0"
    })

@app.route('/batch-process', methods=['POST'])
def batch_process_files():
    """Process multiple files at once"""
    try:
        if 'files' not in request.files:
            return jsonify({
                "success": False,
                "error": "No files provided",
                "message": "Please select files to upload"
            }), 400
        
        files = request.files.getlist('files')
        
        if not files or files[0].filename == '':
            return jsonify({
                "success": False,
                "error": "No files selected",
                "message": "Please select files to upload"
            }), 400
        
        results = []
        successful_files = 0
        failed_files = 0
        
        for file in files:
            if file.filename.lower().endswith('.pdf'):
                # Save and process each file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                    file.save(temp_file.name)
                    temp_file_path = temp_file.name
                
                try:
                    result = extract_invoice_data(temp_file_path)
                    result["filename"] = file.filename
                    results.append(result)
                    
                    if result["success"]:
                        successful_files += 1
                    else:
                        failed_files += 1
                        
                finally:
                    if os.path.exists(temp_file_path):
                        os.unlink(temp_file_path)
        
        return jsonify({
            "success": True,
            "results": results,
            "summary": {
                "total_files": len(files),
                "successful": successful_files,
                "failed": failed_files
            }
        })
        
    except Exception as e:
        print(f"❌ Batch processing error: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Internal server error during batch processing"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)