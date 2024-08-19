from flask import Flask, request, jsonify
import boto3
import config

app = Flask(__name__)

# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    region_name=config.AWS_REGION,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
)

# Table name from configuration
table = dynamodb.Table(config.TABLE_NAME)

@app.route('/get-item', methods=['GET'])
def get_item():
    try:
        # Retrieve query string parameters
        primaryid = request.args.get('primaryid')
        
        if not primaryid:
            raise ValueError('Primary ID is required')

        # Fetch item from DynamoDB table
        response = table.get_item(
            Key={'primaryid': primaryid}
        )
        item = response.get('Item', {})

        return jsonify(item), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create-item', methods=['POST'])
def create_item():
    try:
        # Retrieve data from request JSON body
        data = request.json
        primaryid = data.get('primaryid')
        name = data.get('name')
        education = data.get('education')
        mail = data.get('mail')

        if not all([primaryid, name, education, mail]):
            raise ValueError('All fields (primaryid, name, education, mail) are required')

        # Create item in DynamoDB table
        table.put_item(
            Item={
                'primaryid': primaryid,
                'name': name,
                'education': education,
                'mail': mail
            }
        )

        return jsonify({'message': 'Item created successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list-items', methods=['GET'])
def list_items():
    try:
        # Scan table to retrieve all items
        response = table.scan()
        items = response.get('Items', [])

        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
