"""
AI Code Reviewer - Flask Backend Application
"""
import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from analyzer import CodeAnalyzer

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'py', 'js', 'java', 'cpp', 'c', 'go', 'rs', 'ts', 'jsx', 'tsx', 'rb', 'php', 'swift', 'kt'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize analyzer
analyzer = CodeAnalyzer()


def cleanup_old_uploads(max_age_hours=24):
    """Remove files in upload folder older than max_age_hours"""
    if not os.path.exists(UPLOAD_FOLDER):
        return

    cutoff = datetime.now() - timedelta(hours=max_age_hours)
    for name in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, name)
        if not os.path.isfile(file_path):
            continue

        try:
            modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if modified_time < cutoff:
                os.remove(file_path)
        except OSError:
            continue


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    """Serve favicon to prevent 404 in browser console"""
    return redirect(url_for('static', filename='favicon.svg'))


@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """
    API endpoint to analyze code
    Accepts:
    - code: code text to analyze (from paste)
    - files: multiple files to analyze
    """
    try:
        # Dictionary to store code from various sources
        code_files = {}
        
        # Get code from text area (paste)
        code_text = request.form.get('code', '').strip()
        if code_text:
            code_files['pasted_code.py'] = code_text
        
        # Get uploaded files
        if 'files' in request.files:
            files = request.files.getlist('files')
            
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    raw_content = file.read()
                    try:
                        content = raw_content.decode('utf-8')
                    except UnicodeDecodeError:
                        content = raw_content.decode('utf-8', errors='replace')
                    code_files[filename] = content
        
        # Check if we have any code to analyze
        if not code_files:
            return jsonify({
                'success': False,
                'error': 'Please provide code to analyze (paste or upload files)'
            }), 400
        
        # Analyze the code
        results = analyzer.analyze_multiple_files(code_files)
        
        return jsonify({
            'success': True,
            'data': results
        }), 200
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Analysis error: {error_trace}", flush=True)
        return jsonify({
            'success': False,
            'error': f'Analysis error: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    # Create uploads folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    cleanup_old_uploads(max_age_hours=24)
    
    # Run the Flask app
    print("=" * 60)
    print("AI Code Reviewer is running!")
    print("=" * 60)
    print("\nOpen your browser and navigate to:")
    print("http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='localhost', port=5000)
