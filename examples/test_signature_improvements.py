#!/usr/bin/env python3
"""
Test script for the improved hash signature functions
"""

from fasoarzeka.utils import (
    generate_hash_signature,
    validate_hash_signature,
    create_payment_signature_data,
)


def test_hash_signature_improvements():
    """Test all improvements to the hash signature functions"""
    print("🧪 Testing improved hash signature functions\n")

    # Test data
    secret = "my_secret_key_123"
    amount = "1000"
    merchant_id = "MERCHANT123"
    order_id = "ORDER456"
    callback_url = "https://example.com/callback"
    status_url = "https://example.com/status"
    additional_info = "Test payment"

    # Test 1: Basic signature generation with new interface
    print("✅ Test 1: Basic signature generation")
    try:
        signature1 = generate_hash_signature(
            secret=secret,
            amount=amount,
            merchant_id=merchant_id,
            mapped_order_id=order_id,
        )
        print(f"   Generated signature: {signature1[:20]}...")
        print(f"   Signature length: {len(signature1)} characters")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 2: Backward compatibility with kwargs
    print("\n✅ Test 2: Backward compatibility")
    try:
        signature2 = generate_hash_signature(
            secret=secret, amount=amount, merchantId=merchant_id, mappedOrderId=order_id
        )
        print(f"   Generated signature (kwargs): {signature2[:20]}...")
        print(f"   Same as Test 1: {signature1 == signature2}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 3: Full signature with all parameters
    print("\n✅ Test 3: Full signature with all parameters")
    try:
        signature3 = generate_hash_signature(
            secret=secret,
            amount=amount,
            merchant_id=merchant_id,
            mapped_order_id=order_id,
            link_back_to_calling_website=callback_url,
            link_for_update_status=status_url,
            additional_info=additional_info,
        )
        print(f"   Full signature: {signature3[:20]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 4: Signature validation
    print("\n✅ Test 4: Signature validation")
    try:
        # Valid signature
        is_valid = validate_hash_signature(
            signature=signature1,
            secret=secret,
            amount=amount,
            merchantId=merchant_id,
            mappedOrderId=order_id,
        )
        print(f"   Valid signature validation: {is_valid}")

        # Invalid signature
        is_invalid = validate_hash_signature(
            signature="invalid_signature",
            secret=secret,
            amount=amount,
            merchantId=merchant_id,
            mappedOrderId=order_id,
        )
        print(f"   Invalid signature validation: {is_invalid}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 5: Helper function for payment data
    print("\n✅ Test 5: Payment signature data helper")
    try:
        payment_data = create_payment_signature_data(
            amount=amount,
            merchant_id=merchant_id,
            order_id=order_id,
            callback_url=callback_url,
            status_url=status_url,
            additional_info=additional_info,
        )
        print(f"   Payment data structure: {list(payment_data.keys())}")

        signature4 = generate_hash_signature(secret=secret, **payment_data)
        print(f"   Signature with helper: {signature4[:20]}...")
        print(f"   Same as Test 3: {signature3 == signature4}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 6: Error handling
    print("\n✅ Test 6: Error handling")
    try:
        # Empty secret
        try:
            generate_hash_signature(secret="", amount="1000")
            print("   ❌ Should have raised ValueError for empty secret")
        except ValueError as e:
            print(f"   ✅ Correctly caught empty secret: {e}")

        # None secret
        try:
            generate_hash_signature(secret=None, amount="1000")
            print("   ❌ Should have raised ValueError for None secret")
        except (ValueError, TypeError) as e:
            print(f"   ✅ Correctly caught None secret: {e}")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")

    # Test 7: Custom field order
    print("\n✅ Test 7: Custom field order")
    try:
        custom_order = ["amount", "merchantId", "mappedOrderId"]
        signature5 = generate_hash_signature(
            secret=secret,
            amount=amount,
            merchant_id=merchant_id,
            mapped_order_id=order_id,
            field_order=custom_order,
        )
        print(f"   Custom order signature: {signature5[:20]}...")
        print(f"   Different from default: {signature1 != signature5}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n🎉 All tests completed!")


def test_real_world_scenario():
    """Test a real-world payment scenario"""
    print("\n" + "=" * 50)
    print("🌍 Real-world payment scenario test")
    print("=" * 50)

    # Simulated payment data
    payment_info = {
        "amount": "5000",  # 5000 FCFA
        "merchant_id": "ARZEKA_MERCHANT_001",
        "order_id": "ORD_20251023_001",
        "callback_url": "https://mystore.com/payment/callback",
        "status_url": "https://mystore.com/payment/status",
        "additional_info": "T-shirt purchase",
    }

    secret_key = "SUPER_SECRET_KEY_DONT_SHARE"

    print(f"💰 Payment Amount: {payment_info['amount']} FCFA")
    print(f"🏪 Merchant: {payment_info['merchant_id']}")
    print(f"📋 Order: {payment_info['order_id']}")

    # Step 1: Create payment signature data
    signature_data = create_payment_signature_data(
        amount=payment_info["amount"],
        merchant_id=payment_info["merchant_id"],
        order_id=payment_info["order_id"],
        callback_url=payment_info["callback_url"],
        status_url=payment_info["status_url"],
        additional_info=payment_info["additional_info"],
    )

    # Step 2: Generate signature
    payment_signature = generate_hash_signature(secret=secret_key, **signature_data)

    print(f"🔐 Generated Signature: {payment_signature}")

    # Step 3: Simulate server-side validation
    is_valid = validate_hash_signature(
        signature=payment_signature, secret=secret_key, **signature_data
    )

    print(f"✅ Signature Validation: {'PASSED' if is_valid else 'FAILED'}")

    # Step 4: Test with tampered data (security test)
    tampered_data = signature_data.copy()
    tampered_data["amount"] = "10000"  # Attacker tries to change amount

    is_tampered_valid = validate_hash_signature(
        signature=payment_signature, secret=secret_key, **tampered_data
    )

    print(
        f"🛡️  Tampered Data Validation: {'FAILED (Good!)' if not is_tampered_valid else 'PASSED (Bad!)'}"
    )

    print("\n✨ Real-world scenario test completed!")


if __name__ == "__main__":
    test_hash_signature_improvements()
    test_real_world_scenario()
