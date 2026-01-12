# Wandrly.ai - Multi-Agent Travel Planner

## Project Documentation

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Features & Capabilities](#features--capabilities)
5. [Architecture & Design Patterns](#architecture--design-patterns)
6. [Data Flow & User Journey](#data-flow--user-journey)
7. [API Integrations](#api-integrations)
8. [Key Components](#key-components)
9. [Error Handling Strategy](#error-handling-strategy)
10. [Setup & Installation](#setup--installation)
11. [Current Limitations](#current-limitations)

---

## Project Overview

**Wandrly.ai** is an AI-powered travel planning application that uses a multi-agent architecture to dynamically generate personalized travel itineraries from natural language input. The system accepts user requests in plain English (e.g., "Plan a 2-day trip to New Delhi starting tomorrow") and returns comprehensive travel plans.

### What It Does

- **Natural Language Processing**: Parses conversational trip descriptions to extract destination, dates, and preferences
- **Weather Forecasting**: Provides daily weather forecasts for the trip dates
- **Points of Interest Discovery**: Finds tourism spots, historic sites, restaurants, and shops
- **Itinerary Generation**: Creates day-by-day activity schedules (morning, afternoon, evening)
- **Transparent AI Reasoning**: Shows which tools were called and why
- **Graceful Error Handling**: Provides fallback itineraries when external services fail

### Example Usage

**User Input**: "Plan a 2-day trip to New Delhi starting tomorrow"

**System Output**:
- Weather forecast for New Delhi (next 2 days)
- 20+ Points of Interest with coordinates and categories
- Day-by-day itinerary with time slots
- AI reasoning showing tool execution

---

## Tech Stack

### Backend
- **FastAPI** - Modern async web framework for building REST APIs
- **Uvicorn** - ASGI server for running FastAPI applications
- **Python 3.10+** - Core programming language

### AI & LLM
- **Google Generative AI (Gemini)** - Large language model for:
  - Dynamic agent planning
  - Tool selection reasoning
  - Itinerary generation
- **Model**: `chat-bison-001`

### External APIs
| API | Purpose | Provider |
|-----|---------|----------|
| **Nominatim** | City geocoding (name → lat/lon) | OpenStreetMap |
| **Overpass API** | Points of Interest retrieval | OpenStreetMap |
| **Open-Meteo** | Weather forecasting | Open-Meteo.com |

### Frontend
- **Streamlit** - Interactive web interface framework
- **Pandas** - Data manipulation and table display

### Data Processing
- **Pydantic** - Data validation and serialization
- **python-dateparser** - Natural language date parsing
- **requests** - HTTP client for API calls
- **python-dotenv** - Environment variable management

---

## Project Structure

```
Wandrly.ai-Multiagent-Travel-planner/
├── main.py                 # FastAPI application entry point
├── agents.py              # LLM-driven agent orchestration
├── tools.py               # External API integrations (POI, Weather)
├── utils.py               # NLP parsing utilities
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── frontend/
│   └── streamlit_app.py    # Streamlit web UI
└── docs/
    └── Design Document - Travel Planning AI agent.docx
```

### Directory Purposes

| Directory/File | Purpose |
|----------------|---------|
| **main.py** | FastAPI REST API with `/plan` endpoint |
| **agents.py** | Multi-agent orchestration and LLM integration |
| **tools.py** | Tool implementations for POI and Weather APIs |
| **utils.py** | Input parsing and transformation utilities |
| **frontend/** | Streamlit-based web interface |
| **docs/** | Design documentation and specifications |
| **requirements.txt** | All Python package dependencies |

---

## Features & Capabilities

### 1. Natural Language Input Processing
- Parses conversational trip descriptions
- Extracts city, start date, end date, and duration
- Handles flexible date formats ("tomorrow", "next Monday", "2025-01-15")
- Supports user preferences and special requirements

**Example Inputs**:
- "Plan a 2-day trip to New Delhi starting tomorrow"
- "I want to visit Paris from January 15 to January 20"
- "3-day vacation in Tokyo starting next week"

### 2. Multi-Agent Architecture
The system uses specialized agents that work together:

| Agent | Responsibility |
|-------|---------------|
| **POI Agent** | Retrieves Points of Interest for destination cities |
| **Weather Agent** | Fetches multi-day weather forecasts |
| **Itinerary Creator** | Generates day-by-day activity plans |
| **LLM Orchestrator** | Decides which tools to invoke based on user request |

### 3. Points of Interest Retrieval
- Fetches tourism, historic, amenity, and shopping locations
- Returns POI name, category, latitude, longitude, and description
- Searches within 10km radius of city center
- Deduplicates results
- Categories: Tourism, Historic, Restaurants, Shops, Parks, Museums

### 4. Weather Forecasting
- Daily weather summaries (Clear, Cloudy, Rain, Snow, etc.)
- Maximum and minimum temperatures
- Weather codes for detailed conditions
- Covers full trip date range
- Uses Open-Meteo API (free, no key required)

### 5. Intelligent Itinerary Generation
- Creates day-by-day schedules
- Allocates time slots (morning, afternoon, evening)
- Considers POI availability and weather conditions
- Incorporates user preferences
- Uses LLM for creative planning
- Fallback itinerary generation if LLM fails

### 6. Error Handling & Resilience
- Graceful fallback when Gemini API is unavailable
- Partial success handling (returns results even if some tools fail)
- Detailed error logging for transparency
- Custom exceptions (POIToolError, WeatherToolError)
- User-friendly error messages in UI

### 7. Transparency & Explainability
- Shows which tools were called in the planning process
- Displays tool execution results and errors
- Expandable reasoning section in UI
- Meta information about the planning process
- Full transparency into AI decision-making

### 8. Interactive Web UI
- Real-time trip planning with spinner feedback
- Weather information display
- Interactive map showing POI locations
- POI details in tabular format
- Day-by-day itinerary table
- AI reasoning expander for transparency
- Error and warning notifications

---

## Architecture & Design Patterns

### 1. Multi-Agent Architecture
Multiple specialized agents handle different domains:
- Each agent is responsible for a specific task
- Agents are orchestrated by a central LLM "planner"
- State is shared across agents
- Agents can be invoked in sequence or parallel

### 2. ReACT (Reasoning and Acting) Pattern
```
Reason → Select Tools → Act → Observe → Repeat
```
- Agent reasons about which tools to use via LLM
- Dynamically decides tool invocation based on context
- Executes tools and processes results
- Iterates based on accumulated state

### 3. Tool/Function Calling Pattern
- Tools are declared with descriptions and parameters
- LLM selects appropriate tools based on user request
- Arguments passed dynamically based on reasoning
- Results integrated into application state
- Transparent tool execution logging

### 4. Fallback Pattern
Ensures service availability even when components fail:
```
Primary: LLM-Generated Plan
    ↓ (if fails)
Fallback: Hardcoded Plan
    ↓ (if fails)
Error: Graceful Degradation
```

### 5. State Aggregation Pattern
- Central state dictionary accumulates results
- Tools write to shared state
- Final state returned as comprehensive result
- Meta information tracks execution path
- Errors collected without blocking success

### 6. Client-Server Architecture
```
Frontend (Streamlit) ←→ HTTP/JSON ←→ Backend (FastAPI)
```
- Loose coupling via REST API
- Independent deployment of frontend/backend
- JSON-based communication

### 7. Composition Pattern
```
Input → Parse → Plan → Execute → Aggregate → Output
```
- Each step outputs feeds next step's input
- Clear separation of concerns
- Testable components

---

## Data Flow & User Journey

### Request-Response Flow

```
1. User Input (Natural Language)
   ↓
2. Streamlit Frontend
   ↓
3. POST /plan → FastAPI Backend
   ↓
4. parse_trip_sentence() [utils.py]
   ↓ Extracts: city, start_date, end_date, preferences
   ↓
5. Gemini API (LLM Planner)
   ↓ Generates dynamic tool execution plan
   ↓
6. Agent Execution (agents.py)
   ├─→ POI_TOOL
   │   └─→ find_pois_osm()
   │       ├─→ Nominatim Geocoding
   │       └─→ Overpass API Query
   │
   ├─→ WEATHER_TOOL
   │   └─→ get_weather_open_meteo()
   │       └─→ Open-Meteo API Request
   │
   └─→ ITINERARY_CREATOR
       └─→ create_itinerary_from_state()
           └─→ Gemini API (generates schedule)
   ↓
7. State Aggregation
   ├─ POI Data
   ├─ Weather Data
   ├─ Itinerary
   ├─ Tools Called Log
   └─ Errors (if any)
   ↓
8. JSON Response
   ↓
9. Streamlit UI Rendering
   ├─ Weather Display
   ├─ POI Map & Table
   ├─ Itinerary Table
   ├─ AI Reasoning Section
   └─ Error Warnings
```

### User Journey Steps

1. **User Describes Trip**: Enters natural language trip description in Streamlit UI
2. **Query Submission**: Clicks "Plan trip" button
3. **Backend Processing**:
   - Query parsed to extract location and dates
   - LLM decides which tools to invoke
   - Tools execute in sequence, building up state
   - Results aggregated with metadata
4. **Result Display**:
   - Weather forecast shown at top
   - POI locations displayed on interactive map
   - Itinerary presented as day-by-day table
   - AI reasoning expanded on demand
5. **Error Handling**: If tools fail, partial results shown with warnings

---

## API Integrations

### 1. Gemini API (Google Generative AI)
**Purpose**: LLM for planning and content generation

- **Endpoint**: Google Generative AI SDK
- **Model**: `chat-bison-001`
- **Authentication**: API key via environment variable
- **Usage**:
  - Tool selection planning
  - Itinerary generation from POI and weather data
- **Fallback**: Hardcoded plan if API fails

### 2. Nominatim API (OpenStreetMap)
**Purpose**: City geocoding (name → lat/lon)

- **Endpoint**: `https://nominatim.openstreetmap.org/search`
- **Method**: GET
- **Rate Limit**: Respectful usage with User-Agent header
- **Input**: City name
- **Output**: Latitude, Longitude

### 3. Overpass API (OpenStreetMap)
**Purpose**: Points of Interest queries

- **Endpoint**: `https://overpass-api.de/api/interpreter`
- **Method**: POST
- **Query Language**: Overpass QL
- **Search Radius**: 10km around city center
- **Categories**:
  - Tourism (tourist attractions, viewpoints, monuments)
  - Historic (archaeological sites, castles, memorials)
  - Amenities (restaurants, cafes, bars)
  - Shops (general retail)
- **Limit**: Configurable POI count per category

### 4. Open-Meteo API
**Purpose**: Weather forecasting

- **Endpoint**: `https://api.open-meteo.com/v1/forecast`
- **Method**: GET
- **Authentication**: None required (free/open)
- **Data Retrieved**:
  - Daily temperature (min/max)
  - Weather codes (0-99 scale)
  - Date range covering full trip
- **Output**: Weather summary strings (e.g., "Clear", "Partly Cloudy")

---

## Key Components

### 1. main.py (FastAPI Application)
**Role**: REST API entry point

```python
@app.post("/plan")
async def plan_trip(request: TripRequest) -> dict
```

- Accepts `TripRequest` with query string
- Delegates to agent orchestration
- Returns structured JSON response with:
  - POI data
  - Weather data
  - Itinerary
  - Tools called
  - Errors

### 2. agents.py (Agent Orchestration)
**Role**: Core LLM integration and agent logic

**Key Functions**:
- `create_react_agent()`: Factory function returning agent callable
- `agent_run()`: Main orchestration loop
  - Parses user input
  - Generates tool execution plan via Gemini
  - Executes tools dynamically
  - Manages state across invocations
- `create_itinerary_from_state()`: Generates personalized itineraries using LLM

**Tool Descriptions** passed to LLM:
```python
{
    "POI_TOOL": "Retrieves points of interest for a given city",
    "WEATHER_TOOL": "Fetches weather forecast for specified dates",
    "ITINERARY_CREATOR": "Creates day-by-day travel itinerary"
}
```

### 3. tools.py (External API Integrations)
**Role**: Tool implementations

**Functions**:
- `find_pois_osm(city: str, num_pois: int) -> list`
  - Geocodes city name
  - Queries Overpass API for POIs
  - Returns structured POI data
  - Raises `POIToolError` on failure

- `get_weather_open_meteo(latitude: float, longitude: float, start_date: str, end_date: str) -> list`
  - Fetches weather forecast
  - Maps weather codes to descriptions
  - Returns daily weather summaries
  - Raises `WeatherToolError` on failure

### 4. utils.py (Input Parsing)
**Role**: Natural language processing

**Function**:
- `parse_trip_sentence(sentence: str) -> dict`
  - Regex-based extraction of:
    - City name
    - Start date
    - End date
    - Trip duration
  - Uses `dateparser` for flexible date parsing
  - Returns structured dictionary

**Example**:
```python
Input: "Plan a 2-day trip to New Delhi starting tomorrow"
Output: {
    "city": "New Delhi",
    "start_date": "2025-12-22",
    "end_date": "2025-12-23",
    "num_days": 2
}
```

### 5. streamlit_app.py (Frontend UI)
**Role**: User interface

**Features**:
- Text input for trip description
- "Plan trip" button
- Results display:
  - Weather summary (text)
  - POI map (Streamlit map component)
  - POI table (pandas DataFrame)
  - Itinerary table (pandas DataFrame)
  - AI reasoning expander (collapsible)
- Error/warning notifications
- Loading spinners

**Configuration**:
```python
page_title="AI Travel Planner"
page_icon="🧭"
layout="wide"
BACKEND_URL = "http://localhost:8000"
```

---

## Error Handling Strategy

### Custom Exceptions
```python
class POIToolError(Exception): pass
class WeatherToolError(Exception): pass
```

### Error Management Levels

1. **Tool-Level Error Handling**
   - Each tool wrapped in try-except
   - Errors caught and logged
   - Custom exceptions raised

2. **Agent-Level Error Handling**
   - Errors collected in `state["errors"]`
   - Tool execution continues despite errors
   - Partial results returned

3. **API-Level Error Handling**
   - HTTPException for FastAPI endpoints
   - 500 Internal Server Error on critical failures
   - Detailed error messages in response

4. **LLM Fallback**
   - Hardcoded plan if Gemini API fails
   - Fallback itinerary if LLM scheduling fails
   - Graceful degradation of service

5. **Frontend Error Display**
   - `st.warning()` for non-critical errors
   - `st.error()` for critical failures
   - Expandable error details in reasoning section

### Error Response Format
```json
{
    "pois": [...],
    "weather": [...],
    "itinerary": [...],
    "tools_called": ["POI_TOOL", "WEATHER_TOOL"],
    "errors": ["POI retrieval failed: Connection timeout"]
}
```

---

## Setup & Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Google Gemini API key

### Installation Steps

1. **Clone the repository** (or navigate to project directory)
   ```bash
   cd /Users/iitjobsinc/Desktop/sNET/hack/Wandrly.ai-Multiagent-Travel-planner
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

   Get your API key from: https://ai.google.dev/

### Running the Application

#### Option 1: Run Backend and Frontend Separately

**Terminal 1 - Backend**:
```bash
python main.py
# Server starts at http://localhost:8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
streamlit run streamlit_app.py
# UI opens at http://localhost:8501
```

#### Option 2: Using Uvicorn
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the API

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/plan" \
  -H "Content-Type: application/json" \
  -d '{"query": "Plan a 2-day trip to New Delhi starting tomorrow"}'
```

**Python Example**:
```python
import requests

response = requests.post(
    "http://localhost:8000/plan",
    json={"query": "Plan a 3-day trip to Paris starting next Monday"}
)
print(response.json())
```

---

## Current Limitations

### Functional Limitations
1. **Single-City Trips Only**: No multi-city routing or complex itineraries
2. **Limited Weather Codes**: Basic mapping of weather codes to descriptions
3. **POI Coverage**: Depends on OpenStreetMap data completeness (varies by region)
4. **No User Accounts**: No authentication or saved trips
5. **No Real-Time Updates**: Static itineraries without dynamic adjustments

### Technical Limitations
1. **Basic Map Visualization**: No tooltips, clustering, or advanced map interactions
2. **Synchronous Processing**: No async task queuing for long-running requests
3. **No Caching**: Repeated queries re-fetch data from external APIs
4. **Single Language**: English-only support
5. **No Mobile Optimization**: Desktop-first UI design

### API Limitations
1. **Gemini API Rate Limits**: Subject to Google's rate limiting
2. **OpenStreetMap Fair Use**: Must respect Nominatim usage policies
3. **Weather Forecast Range**: Limited to ~7 days by Open-Meteo
4. **POI Radius**: Fixed 10km search radius

---

## Future Improvements (from README)

1. **Multi-City Support**: Handle complex multi-destination trips
2. **Enhanced Visualizations**: Interactive maps with POI details on hover
3. **Booking Integration**: Connect with hotel/flight booking APIs
4. **User Profiles**: Save preferences and trip history
5. **Budget Planning**: Cost estimation for trips
6. **Collaborative Planning**: Share and edit trips with others
7. **Mobile App**: Native iOS/Android applications
8. **Real-Time Updates**: Dynamic itinerary adjustments based on weather/events
9. **Multi-Language Support**: Internationalization
10. **Offline Mode**: Cached data for offline access

---

## Summary

**Wandrly.ai** is a sophisticated demonstration of agentic AI architecture applied to travel planning. It combines:

- **LLM Reasoning** (Gemini API) for dynamic tool selection
- **Multi-Agent Pattern** for specialized task handling
- **External API Integration** for real-world data (POI, Weather)
- **Graceful Degradation** for reliability
- **User-Friendly Interface** (Streamlit) for accessibility
- **Transparent AI** for explainability and trust

The project showcases modern AI engineering practices including ReACT patterns, tool calling, state management, and error handling—all while maintaining simplicity and clarity in code organization.

---

**Last Updated**: December 21, 2025
**Project Location**: `/Users/iitjobsinc/Desktop/sNET/hack/Wandrly.ai-Multiagent-Travel-planner`
