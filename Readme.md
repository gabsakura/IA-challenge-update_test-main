# Sensor Monitoring System with Flask and AI Integration

This project is a web application developed with Flask that monitors and visualizes sensor data (temperature, current, and vibration). It features an AI-powered chat interface using Google's Gemini API for data analysis and user interaction.

## Features

- **Real-time Sensor Monitoring**: View sensor data in real-time through an intuitive dashboard
- **Data Visualization**: Interactive charts and graphs for data analysis
- **AI-Powered Analysis**: Integration with Google's Gemini AI for intelligent data interpretation
- **User Authentication**: Secure login and registration system
- **Data Querying**: Filter and analyze data by day, week, month, or year
- **PDF Report Generation**: Generate detailed reports of sensor readings
- **Responsive Design**: Mobile-friendly interface

## Technologies Used

### Backend
- **Flask**: Python web framework
- **SQLite**: Database for storing sensor data
- **Google Gemini AI**: For intelligent data analysis (API key required)
- **Werkzeug**: Password handling and security
- **SQLAlchemy**: Database ORM

### Frontend
- **HTML/CSS/JavaScript**: Frontend development
- **Chart.js**: Data visualization
- **Bootstrap**: Responsive design framework

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sensor-monitoring-system.git
cd sensor-monitoring-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python delete_table.py    # Clear existing data if needed
python create_table.py    # Create the database structure
python populate_data.py   # Populate with sample data
```

5. Configure the Google AI API:
   - Create a `.env` file in the root directory
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```
   > **Note**: For security reasons, the actual API key is not included in this repository. You'll need to obtain your own from the Google Cloud Console.

6. Run the application:
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5001`

## Project Structure

```
├── app.py                  # Main application file
├── AI.py                   # AI integration module
├── AI_folder/             
│   ├── AI_specs.py        # AI configuration
│   └── AI_functions.py    # AI utility functions
├── templates/             
│   ├── dashboard.html     # Main dashboard
│   ├── login.html         # Login page
│   └── components/        # Reusable components
├── static/
│   ├── scripts/           # JavaScript files
│   └── styles/            # CSS files
└── instance/
    └── dados.db           # SQLite database
```

## Database Schema

The `dados` table structure:
- `id`: Primary key
- `temperatura`: Temperature readings
- `corrente`: Current readings
- `vibracao_base`: Base vibration readings
- `vibracao_braco`: Arm vibration readings
- `data_registro`: Timestamp

## API Integration

This project uses Google's Gemini AI API for intelligent data analysis. Due to security concerns, the API key is not included in the repository. To use the AI features:

1. Get an API key from Google Cloud Console
2. Create a `.env` file
3. Add your API key as shown in the installation section

> **Important**: Never commit your API key to version control

## Usage

1. Start the application
2. Register a new user account or login
3. Access the dashboard to view sensor data
4. Use the time range filters to analyze specific periods
5. Interact with the AI assistant for data analysis
6. Generate PDF reports as needed

## Development Notes

- The sample data generator (`populate_data.py`) creates realistic sensor readings within specified ranges:
  - Temperature: 25-47°C
  - Current: 2-6A
  - Vibration: 1-7 units

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Cloud Platform for AI services
- Flask community for the excellent framework
- Contributors and testers

## Screenshots

| Dashboard View | Data Analysis | AI Interface |
|:-------------:|:-------------:|:------------:|
| ![Dashboard](screenshots/dashboard.png) | ![Analysis](screenshots/analysis.png) | ![AI Chat](screenshots/ai_chat.png) |

## Contact

For questions or support, please open an issue in the repository.