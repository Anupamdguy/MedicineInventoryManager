#!/usr/bin/env python
"""
Quick test script for the Medicine Assistant
Run this to test OpenAI integration before full Django integration
"""

import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

def test_openai_connection():
    """Test OpenAI API connection"""
    print("🔍 Testing OpenAI API connection...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your API key:")
        print("OPENAI_API_KEY=sk-your-key-here")
        return False
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # Simple test message
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Connection successful!' if you receive this."}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ SUCCESS: {result}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_medicine_query():
    """Test a sample medicine inventory query"""
    print("\n🧪 Testing medicine inventory query generation...")
    
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    query = "Show me all medicines that are low on stock"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": """You are an SQL expert for a medicine inventory system.
                    Generate a Django ORM query for the given question.
                    Available model: Medicine with fields: name, current_stock, reorder_level"""
                },
                {
                    "role": "user",
                    "content": f"Generate query for: {query}"
                }
            ],
            temperature=0.1
        )
        
        result = response.choices[0].message.content
        print(f"✅ Query generated:\n{result}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_stock_analysis():
    """Test stock analysis generation"""
    print("\n📊 Testing stock analysis generation...")
    
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Mock data
    sample_data = {
        "low_stock_items": [
            {"name": "Paracetamol 500mg", "current_stock": 50, "reorder_level": 200},
            {"name": "Amoxicillin 250mg", "current_stock": 30, "reorder_level": 150}
        ],
        "out_of_stock": [
            {"name": "Ibuprofen 400mg", "category": "Painkiller"}
        ],
        "total_medicines": 150,
        "total_value": 45000.00
    }
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a pharmaceutical inventory analyst. Provide concise, actionable insights."
                },
                {
                    "role": "user",
                    "content": f"Analyze this inventory data and provide recommendations:\n{sample_data}"
                }
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        result = response.choices[0].message.content
        print(f"✅ Analysis generated:")
        print("-" * 60)
        print(result)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def main():
    print("=" * 60)
    print("MEDICINE INVENTORY ASSISTANT - QUICK TEST")
    print("=" * 60)
    
    # Run tests
    tests = [
        ("OpenAI Connection", test_openai_connection),
        ("Medicine Query Generation", test_medicine_query),
        ("Stock Analysis", test_stock_analysis)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} failed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your assistant is ready to integrate.")
        print("\nNext steps:")
        print("1. Copy the assistant files to your Django project")
        print("2. Follow the INTEGRATION_GUIDE.md")
        print("3. Run: python manage.py runserver")
        print("4. Visit: http://localhost:8000/assistant/")
    else:
        print("\n⚠️  Some tests failed. Please check:")
        print("1. Your .env file has the correct OPENAI_API_KEY")
        print("2. You have internet connection")
        print("3. Your API key has sufficient credits")


if __name__ == '__main__':
    main()
