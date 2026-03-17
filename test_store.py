from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_


@pytest.fixture
def order_id():
    """Create a test order for use in tests.
    Finds an available pet dynamically and creates an order for it.
    Returns the order_id for patching.
    """
    # Try to find an available pet by attempting to create an order
    pets_to_try = [0, 2, 1] 
    
    for pet_id in pets_to_try:
        order_data = {"pet_id": pet_id}
        response = api_helpers.post_api_data("/store/order", order_data)
        if response.status_code == 201:
            order = response.json()
            return order['id']
    
    # If no pet is available, skip the test
    pytest.skip("No available pets to create an order")



def test_patch_order_by_id(order_id):
    """Test PATCH request to update order status.
    
    - Uses fixture to create an order
    - Patches the order with new status 'sold'
    - Validates response code is 200
    """
    test_endpoint = f"/store/order/{order_id}"
    update_data = {
        "status": "sold"
    }

    response = api_helpers.patch_api_data(test_endpoint, update_data)

    assert response.status_code == 200

    # Store response body in JSON format
    response_body = response.json()

    # Validate the response message "Order and pet status updated successfully"
    assert_that(response_body['message'], contains_string("Order and pet status updated successfully"))

    # Validate response structure
    assert "message" in response_body
    assert isinstance(response_body['message'], str)
