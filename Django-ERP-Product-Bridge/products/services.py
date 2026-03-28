import os
import json
import requests
# from decimal import Decimal
from django.conf import settings
from django.db import transaction
from .models import Product

def fetch_products_from_erp():
    """
    Fetches product data from the external ERP API.
    If the API is unreachable or returns empty data,
    it falls back to loading data from a local mock JSON file.
    """
    # ΒΑΛΕ ΕΔΩ ΤΟ ΑΚΡΙΒΕΣ ΟΝΟΜΑ ΠΟΥ ΕΧΕΙΣ ΣΤΟ .ENV ΑΡΧΕΙΟ ΣΟΥ
    url = os.getenv("EXTERNAL_API_URL") 
    
    mock_file_path = os.path.join(settings.BASE_DIR, 'Products', 'mock_products.json')

    try:
        if not url:
            raise ValueError("No API URL found in environment variables.")

        # Κάνουμε το call στο API κατευθείαν (αφού δεν χρειάζεται token)
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Ελέγχει για σφάλματα (π.χ. 404, 500)
        
        api_data = response.json()
        
        # Ελέγχουμε αν το API όντως έφερε προϊόντα (success: true)
        is_success = str(api_data.get("success", "")).lower() == "true" or api_data.get("success") is True
        
        if not is_success:
            # Αν είναι false (π.χ. Κυριακή), πάμε στο fallback!
            raise ValueError("API responded, but returned success: false (Empty data).")
            
        return api_data

    except (requests.exceptions.RequestException, ValueError) as e:
        # FALLBACK: Ενεργοποιείται αν πέσει ο server, λείπει το URL, ή success=false
        print(f"Notice: Loading mock data due to API error/empty data. Reason: {e}")
        
        try:
            with open(mock_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Critical Error: Mock file not found at {mock_file_path}")
            return {"success": False, "data": []}

@transaction.atomic
def sync_products():
    """
    Synchronizes local database products with data fetched from the ERP.
    If no data is received, it safely aborts without deleting existing records.
    It also removes old products from the database that are no longer present in the ERP API.
    """
    response_data = fetch_products_from_erp()
    products_data = response_data.get("data", [])

    # 1. SAFETY CHECK: Abort if no data came from API or Mock file
    if not products_data:
        print("No products found for synchronization. Database remains intact.")
        return 

    # 2. Track incoming IDs to know what to keep
    incoming_ids = []

    for item in products_data:
        try:
            ext_id = int(item["externalId"])
            
            # Save the ID to our "keep" list
            incoming_ids.append(ext_id)

            Product.objects.update_or_create(
                external_id=ext_id,
                defaults={
                    "code": item.get("code", "N/A"),
                    "description": item.get("description", "N/A"),
                    "name": item.get("name", "N/A"),
                    "barcode": item.get("barcode", "N/A"),
                    "retail_price": float(item.get("retailPrice", 0)),
                    "wholesale_price": float(item.get("wholesalePrice", 0)),
                    "discount": float(item.get("discount", 0)),
                }
            )
        except Exception as e:
            print(f"Error saving product {item.get('name')}: {e}")

    # 3. SMART CLEANUP: Delete products that are NOT in the incoming_ids list
    if incoming_ids:
        deleted_count, _ = Product.objects.exclude(external_id__in=incoming_ids).delete()
        
        if deleted_count > 0:
            print(f"Deleted {deleted_count} old products that were removed from the ERP.")