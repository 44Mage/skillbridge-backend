import google.generativeai as genai

genai.configure(api_key='AIzaSyDLp6-psrjHOKZZToTkeZuezg8IBhB6N0I')

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"AVAILABLE: {m.name}")
except Exception as e:
    print(f"ERROR: {e}")
