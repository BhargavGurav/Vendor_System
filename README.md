# Vendor System API

Welcome to the Vendor System API! This project is built with Django and provides API endpoints for managing vendors.

## Setup

1. **Clone the Repository**: Clone this repository to your local machine using the following command:

```
git clone https://github.com/BhargavGurav/Vendor_System.git
```


2. **Install Dependencies**: Navigate to the project directory and install the Python dependencies using pip:

```
cd Vendor_System
pip install -r requirements.txt
```


3. **Run Migrations**: Apply the database migrations to create the necessary database schema:
```
python manage.py migrate
```


## Running the Server

To start the Django development server, run the following command:
```
python manage.py runserver
```


By default, the server will start on `http://127.0.0.1:8000/`.

## API Endpoints

### List of Endpoints

- `/vendors/`: [GET] Get a list of all vendors.
- `/vendors/`: [POST] Create a new vendor.       Put all data in json in body (using thunder client in vs code ) input format is given in views file.
- `/vendors/<vendor_id>/`: [GET] Retrieve details of a specific vendor.
- `/vendors/<vendor_id>/`: [PUT] Update details of a specific vendor.
- `/vendors/<vendor_id>/`: [DELETE] Delete a specific vendor.
- `/purchase_orders/`: [GET] Get a list of all purchase orders.
- `/purchase_orders/`: [POST] Create a new purchase order.       Put all data in json in body (using thunder client in vs code ) input format is given in views file.
- `/purchase_orders/<po_id>/`: [GET] Retrieve details of a specific PO.
- `/purchase_orders/<po_id>/`: [PUT] Update details of a specific PO.
- `/purchase_orders/<po_id>/`: [DELETE] Delete a specific PO.
- `/vendors/<vendor_id>/performance/`:[GET, POST] Get performance metrix of the specified vendor
- `/purchase_orders/<po_id>/acknowledge/` [POST] Acknowledges the specified purchase order and recalculate the performance of vendor associated with that purchase order.
### Testing API Endpoints

You can test the API endpoints using Thunder Client, a VS Code extension that provides a convenient way to send HTTP requests.

1. **Install Thunder Client**: Install Thunder Client from the VS Code extensions marketplace.

2. **Start the Server**: Make sure the Django development server is running (`python manage.py runserver`).

3. **Open Thunder Client**: Open VS Code and navigate to the Thunder Client extension.

4. **Send Requests**: Use Thunder Client to send HTTP requests to the API endpoints listed above. You can test various request methods like GET, POST, PUT, and DELETE.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or create a pull request.

## Contact
Feel free to contact 
G-mail : guravbhargav09@gmail.com
Linkedin : https://www.linkedin.com/in/bhargav-gurav-380992224/
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

