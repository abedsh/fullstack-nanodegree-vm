from app import app

app.secret_key = 'super secret key'
app.run(debug=True, host='0.0.0.0', port=5000)
