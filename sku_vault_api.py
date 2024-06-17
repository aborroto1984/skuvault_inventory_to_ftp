import requests
from config import EMAIL, PASSWORD
from datetime import datetime


def get_items_inventory():
    tenant_token, user_token = _get_tokens()
    url = "https://app.skuvault.com/api/inventory/getItemQuantities"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "PageNumber": 0,
        "PageSize": 10000,
        "TenantToken": tenant_token,
        "UserToken": user_token,
    }
    response = requests.post(url, json=payload, headers=headers)
    # include only the skus that beging with CM- or WS01
    # for the Availability date from vendor, use today's date
    if response.status_code == 200:
        result = [
            {
                "Manufacturer Part Number": item["Sku"],
                "Manufacturer Unit of Measure": "EA",
                "Manufacturer Plant": "",
                "Available Quantity": item["AvailableQuantity"],
                "Availability date from vendor": datetime.now().strftime("%m/%d/%Y"),
            }
            for item in response.json().get("Items")
            if item["Sku"].startswith("CM-") or item["Sku"] == "WS01"
        ]
        return result


def get_products_inventory():
    tenant_token, user_token = _get_tokens()
    url = "https://app.skuvault.com/api/products/getProducts"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "PageNumber": 0,
        "PageSize": 10000,
        "TenantToken": tenant_token,
        "UserToken": user_token,
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        result = [
            {
                "Manufacturer Part Number": item["Sku"],
                "Manufacturer Unit of Measure": "EA",
                "Manufacturer Plant": "",
                "Available Quantity": item["QuantityAvailable"],
                "Availability date from vendor": datetime.now().strftime("%m/%d/%Y"),
            }
            for item in response.json().get("Products")
            if item["Sku"].startswith("CM-") or item["Sku"] == "WS01"
        ]
        return result


def get_kits_inventory():
    tenant_token, user_token = _get_tokens()
    url = "https://app.skuvault.com/api/inventory/getKitQuantities"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "PageNumber": 0,
        "PageSize": 10000,
        "TenantToken": tenant_token,
        "UserToken": user_token,
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()


def _get_tokens():
    url = "https://app.skuvault.com/api/gettokens"
    payload = {"email": EMAIL, "password": PASSWORD}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        response_json = response.json()
        tenant_token = response_json.get("TenantToken")
        user_token = response_json.get("UserToken")
        return tenant_token, user_token
    return None, None
