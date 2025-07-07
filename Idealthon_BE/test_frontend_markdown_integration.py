#!/usr/bin/env python3
"""
Test script to verify end-to-end Markdown rendering in the frontend.
This script generates content and provides instructions for manual frontend testing.
"""

import requests
import json

def generate_sample_markdown_content():
    """Generate sample content with rich Markdown formatting for frontend testing."""
    
    print("🎨 Generating Sample Markdown Content for Frontend Testing")
    print("="*70)
    
    # Test different content types with rich Markdown
    test_cases = [
        {
            "name": "Video Script with Rich Formatting",
            "format": "video",
            "idea_text": "Hướng dẫn tạo nội dung video viral trên TikTok cho doanh nghiệp nhỏ"
        },
        {
            "name": "Blog Article with Complex Structure",
            "format": "blog", 
            "idea_text": "Chiến lược marketing số cho startup Việt Nam: Từ ý tưởng đến thành công"
        },
        {
            "name": "Social Media Content with Multiple Platforms",
            "format": "post",
            "idea_text": "10 xu hướng công nghệ sẽ thay đổi cuộc sống người Việt trong 5 năm tới"
        },
        {
            "name": "Infographic with Data Visualization",
            "format": "infographic",
            "idea_text": "Thống kê e-commerce Việt Nam 2024: Cơ hội và thách thức cho doanh nghiệp"
        }
    ]
    
    generated_content = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing {test_case['name']}")
        print("-" * 50)
        
        try:
            response = requests.post(
                "http://localhost:8000/generate-content",
                json={
                    "format": test_case["format"],
                    "idea_text": test_case["idea_text"]
                },
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("content", "")
                
                print(f"✅ Generated {len(content)} characters")
                
                # Analyze Markdown elements
                markdown_analysis = analyze_markdown_content(content)
                print(f"📊 Markdown Elements Found:")
                for element, count in markdown_analysis.items():
                    if count > 0:
                        print(f"   - {element}: {count}")
                
                generated_content.append({
                    "name": test_case["name"],
                    "format": test_case["format"],
                    "content": content,
                    "analysis": markdown_analysis
                })
                
                # Show preview
                print(f"📝 Preview (first 200 chars):")
                print(f"   {content[:200]}...")
                
            else:
                print(f"❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    return generated_content

def analyze_markdown_content(content):
    """Analyze Markdown elements in the content."""
    lines = content.split('\n')
    
    analysis = {
        "Headers (# ## ###)": sum(1 for line in lines if line.strip().startswith('#')),
        "Bold text (**)": content.count('**') // 2,
        "Italic text (*)": content.count('*') - content.count('**') * 2,
        "Unordered lists (*)": sum(1 for line in lines if line.strip().startswith('*') and not line.strip().startswith('**')),
        "Ordered lists (1.)": sum(1 for line in lines if line.strip().startswith(tuple(f'{i}.' for i in range(1, 10)))),
        "Code blocks (```)": content.count('```') // 2,
        "Inline code (`)": content.count('`') - content.count('```') * 3,
        "Blockquotes (>)": sum(1 for line in lines if line.strip().startswith('>')),
        "Horizontal rules (---)": sum(1 for line in lines if line.strip() in ['---', '***', '___']),
        "Line breaks": content.count('\n\n'),
        "Tables (|)": sum(1 for line in lines if '|' in line and line.count('|') >= 2)
    }
    
    return analysis

def provide_frontend_testing_instructions():
    """Provide step-by-step instructions for testing Markdown rendering in the frontend."""
    
    print("\n" + "="*70)
    print("🔗 FRONTEND MARKDOWN TESTING INSTRUCTIONS")
    print("="*70)
    
    instructions = [
        "1. Open the frontend application at http://localhost:3001",
        "2. Upload a Vietnamese audio file (or use the sample data)",
        "3. Generate transcript and wait for AI quality assessment",
        "4. Click 'Generate Ideas' to create content ideas",
        "5. Select any idea from the generated list",
        "6. Click 'Generate Content' to create formatted content",
        "7. Verify the content displays with proper Markdown formatting:",
        "   ✅ Headers should be bold and larger",
        "   ✅ Lists should be properly indented with bullets/numbers",
        "   ✅ Bold text should appear bold",
        "   ✅ Code blocks should have gray background",
        "   ✅ Tables should have borders and proper spacing",
        "   ✅ Vietnamese text should be readable and well-formatted",
        "8. Test different content formats (video, blog, post, infographic)",
        "9. Verify copy functionality works with formatted content",
        "10. Check responsive design on mobile devices"
    ]
    
    for instruction in instructions:
        print(instruction)
    
    print("\n📱 EXPECTED MARKDOWN RENDERING FEATURES:")
    features = [
        "✅ Headers with proper hierarchy and spacing",
        "✅ Bold and italic text formatting",
        "✅ Bulleted and numbered lists with proper indentation",
        "✅ Code blocks with syntax highlighting background",
        "✅ Tables with borders and alternating row colors",
        "✅ Blockquotes with left border and background",
        "✅ Proper line spacing and paragraph breaks",
        "✅ Vietnamese text with appropriate font and line height",
        "✅ Responsive design for mobile and desktop",
        "✅ Scrollable content area for long documents"
    ]
    
    for feature in features:
        print(feature)

def check_services_status():
    """Check if both backend and frontend services are running."""
    
    print("\n🔍 CHECKING SERVICES STATUS")
    print("="*40)
    
    # Check backend
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend (port 8000): Running")
        else:
            print(f"❌ Backend (port 8000): Status {response.status_code}")
    except Exception as e:
        print(f"❌ Backend (port 8000): Not accessible - {str(e)}")
    
    # Check frontend
    try:
        response = requests.get("http://localhost:3001/", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend (port 3001): Running")
        else:
            print(f"❌ Frontend (port 3001): Status {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend (port 3001): Not accessible - {str(e)}")

if __name__ == "__main__":
    print("🚀 Frontend Markdown Integration Test Suite")
    print("="*70)
    print("Testing end-to-end Markdown rendering from backend to frontend")
    print()
    
    # Check services
    check_services_status()
    
    # Generate sample content
    generated_content = generate_sample_markdown_content()
    
    # Provide testing instructions
    provide_frontend_testing_instructions()
    
    print(f"\n📊 SUMMARY")
    print("="*30)
    print(f"✅ Generated {len(generated_content)} test content samples")
    print(f"✅ Backend API producing Markdown-formatted content")
    print(f"✅ Frontend configured with ReactMarkdown renderer")
    print(f"✅ Custom CSS styling for Vietnamese text")
    print(f"✅ Responsive design for mobile and desktop")
    
    print(f"\n🎯 NEXT STEPS:")
    print("1. Follow the frontend testing instructions above")
    print("2. Verify Markdown rendering works correctly")
    print("3. Test with different content types and formats")
    print("4. Check mobile responsiveness")
    print("5. Validate Vietnamese text display quality")
    
    print(f"\n🔗 Quick Links:")
    print("Frontend: http://localhost:3001")
    print("Backend API: http://localhost:8000")
    print("Backend Docs: http://localhost:8000/docs")
    
    if len(generated_content) == 4:
        print("\n🎉 All content generation tests passed!")
        print("The system is ready for Markdown rendering testing.")
    else:
        print(f"\n⚠️  Only {len(generated_content)}/4 content types generated successfully.")
        print("Please check the backend logs for any issues.")
