from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure the Gemini API
genai.configure(api_key='AIzaSyBGwV0hwIhXw8OdeGBX8PyMbEepxLXeP9k')

def dry_run_code(code, test_case):
    """Perform a dry run of the provided code with a test case."""
    # Set up the model
    model = genai.GenerativeModel('gemini-pro')

    # Prepare the prompt
    prompt = f"""
    Perform a dry run of the following code with the provided test case. Explain each step of execution, with the step and changes in the variables at each step.
    Include variable assignments and their values at each step. If there are any
    errors or potential issues, point them out and also give optimal solution.

    Code:
    {code}

    Test Case:
    {test_case}

    Dry Run Analysis:
    """

    # Generate the response
    response = model.generate_content(prompt)

    return response.text

@app.route('/dry_run', methods=['POST'])
def perform_dry_run():
    data = request.json
    code = data.get('code')
    test_case = data.get('test_case')
    
    if not code or not test_case:
        return jsonify({'error': 'Please provide both code and test case.'}), 400
    
    try:
        result = dry_run_code(code, test_case)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
