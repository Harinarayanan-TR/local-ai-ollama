# Frontend - React Chat UI

Modern, responsive ChatGPT-style React application for the Local AI Chat Platform.

## 🎨 Features

- **Dark Modern Theme** - Glassmorphism design
- **Real-time Chat** - Streaming-ready message display
- **Animated Bubbles** - Smooth fade-in animations
- **Responsive Design** - Works on mobile, tablet, desktop
- **Model Selector** - Easy switching between available models
- **Auto Mode Toggle** - Enable/disable intelligent routing
- **Chat History** - Load and display conversation history
- **Session Management** - Secure API key authentication

## 📁 Directory Structure

```
frontend/
├── public/
│   └── index.html           # HTML entry point
├── src/
│   ├── pages/
│   │   ├── LoginPage.js     # Login form
│   │   └── ChatPage.js      # Main chat interface
│   ├── components/
│   │   ├── ChatMessage.js   # Message bubble
│   │   └── Sidebar.js       # Model selector & settings
│   ├── styles/
│   │   ├── index.css        # Global styles
│   │   ├── App.css
│   │   ├── Login.css
│   │   ├── ChatPage.css
│   │   ├── ChatMessage.css
│   │   └── Sidebar.css
│   ├── utils/
│   │   └── api.js           # API client
│   ├── App.js               # Root component
│   └── index.js             # React entry point
├── package.json
└── Dockerfile
```

## 🚀 Getting Started

### Installation

```bash
npm install
```

### Development

```bash
npm start
```

Opens: `http://localhost:3000`

### Production Build

```bash
npm run build
```

Output: `build/` directory

## 🎯 Components

### LoginPage

**Purpose:** API key authentication
**Props:** `onLoginSuccess(sessionId)`

```jsx
<LoginPage onLoginSuccess={(id) => setSessionId(id)} />
```

**Features:**
- Glassmorphic card design
- Password input for API key
- Error message display
- Loading state feedback

### ChatPage

**Purpose:** Main chat interface
**Props:** `sessionId`, `onLogout()`

```jsx
<ChatPage sessionId={sessionId} onLogout={handleLogout} />
```

**Features:**
- Message history loading
- Real-time message sending
- Auto-scroll to latest message
- Model status display
- Model switching
- Auto mode toggle

### ChatMessage

**Purpose:** Individual message display
**Props:** `message` object

```jsx
<ChatMessage message={{
  user: "Hello",
  ai: "Hi there!",
  model: "phi3",
  timestamp: "2024-06-07..."
}} />
```

**Features:**
- User message bubble (blue)
- AI response bubble (dark)
- Model indicator
- Timestamp display

### Sidebar

**Purpose:** Model selection and settings
**Props:** `currentModel`, `autoMode`, callbacks

```jsx
<Sidebar 
  currentModel="phi3"
  autoMode={false}
  onAutoModeToggle={() => {...}}
  onModelSwitch={(model) => {...}}
  onLogout={() => {...}}
  status={status}
/>
```

**Features:**
- Collapsible menu
- Model buttons
- Auto mode checkbox
- Model status indicator
- Logout button

## 🎨 Styling

### Color Scheme

```css
Background: #0d1117 → #161b22 (dark gradient)
Primary: #58a6ff (GitHub blue)
Text: #c9d1d9 (light gray)
Success: #3fb950 (green)
Error: #f85149 (red)
Borders: rgba(48, 54, 61, 0.3)
```

### Responsive Breakpoints

```css
Desktop: > 768px
Mobile: < 768px
```

Sidebar collapses on mobile, chat expands to full width.

## 🔌 API Integration

### api.js Functions

```javascript
login(apiKey)                    // Login
sendMessage(msg, sessionId, ...)  // Send chat message
getStatus()                      // Get model status
switchModel(model, sessionId)    // Switch model
getHistory(sessionId)            // Load history
```

### API Configuration

```javascript
// frontend/src/utils/api.js
const API_BASE_URL = "http://localhost:8000/api";
```

**For Network Access:**
```javascript
const API_BASE_URL = "http://192.168.1.100:8000/api";
```

## 💾 State Management

### LoginPage State

```javascript
const [apiKey, setApiKey] = useState('');
const [error, setError] = useState('');
const [loading, setLoading] = useState(false);
```

### ChatPage State

```javascript
const [messages, setMessages] = useState([]);
const [inputValue, setInputValue] = useState('');
const [loading, setLoading] = useState(false);
const [currentModel, setCurrentModel] = useState('phi3');
const [autoMode, setAutoMode] = useState(false);
const [status, setStatus] = useState(null);
```

## 🎭 Component Flow

```
App
├── LoginPage (before auth)
│   └── Login form
│       └── onLoginSuccess → ChatPage
└── ChatPage (after auth)
    ├── Sidebar
    │   ├── Model selector
    │   ├── Auto mode toggle
    │   ├── Status display
    │   └── Logout
    └── Chat area
        ├── Messages container
        │   └── ChatMessage (list)
        └── Input form
```

## 🔐 Security

### API Key Handling

- Stored in component state (not localStorage)
- Passed in request headers
- Cleared on logout

### CORS

Frontend is CORS-enabled by backend:
```python
# Backend allows all origins (change in production)
CORSMiddleware(allow_origins=["*"])
```

## 📱 Responsive Design

### Mobile Layout
- Sidebar expands as modal at bottom
- Chat takes full width
- Touch-friendly buttons
- Adjusted font sizes

### Desktop Layout
- Sidebar on left (collapsible)
- Chat on right
- Larger component sizes
- Full-width input

## 🎯 User Flow

1. **Login Screen**
   - User enters API key
   - Click "Login"
   
2. **Chat Screen**
   - Chat history loads
   - User types message
   - Select model (optional)
   - Toggle auto mode (optional)
   - Send message
   
3. **Response Display**
   - Message shows in UI
   - Model indicator shown
   - History auto-saves
   - Auto-scroll to latest

4. **Model Management**
   - Click model button to switch
   - Auto mode makes smart selections
   - Status shows current model
   - Logout and session end

## 🚀 Building for Production

### Build Command

```bash
npm run build
```

### Output

```
build/
├── index.html
├── static/
│   ├── js/
│   ├── css/
│   └── media/
└── favicon.ico
```

### Serve Build Locally

```bash
npx serve -s build -l 3000
```

### Docker Deployment

```bash
docker build -t local-ai-frontend .
docker run -p 3000:3000 local-ai-frontend
```

## 🔧 Configuration

### Environment Variables

Create `.env` file:
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_DEBUG=true
```

### Using Environment Variables

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
```

## 📊 Performance

### Optimization Techniques

- Lazy loading messages
- Virtual scrolling (for long history)
- CSS animations (GPU accelerated)
- Minimized re-renders with useCallback
- Code splitting ready

### Load Times

- Initial Load: ~2-3s
- Message Send: ~500ms-2s (depends on model)
- Model Switch: ~200-500ms

## 🐛 Debugging

### Browser Console

All API calls logged:
```javascript
console.log('API Call:', endpoint)
console.error('API Error:', error)
```

### React DevTools

Install extension:
```
Chrome: React Developer Tools
Firefox: React DevTools
```

### Network Tab

Monitor API requests:
- Check response times
- Verify payloads
- Debug CORS issues

## 📝 Common Issues

### "Cannot connect to API"

1. Backend not running
2. Wrong API_BASE_URL
3. CORS blocked

Solution:
```javascript
// Check if backend is accessible
fetch('http://localhost:8000/').then(r => r.json())
```

### "Login failed"

1. Invalid API key
2. Backend error

Check backend logs:
```bash
python -m uvicorn app.main:app --reload
```

### Styling Issues

1. CSS not loading
2. CSS conflicts

Check DevTools → Network tab

## 🌐 Network Access

### Access from Another Device

1. Get your machine IP:
```bash
hostname -I  # Linux/Mac
ipconfig     # Windows
```

2. Update API URL:
```javascript
const API_BASE_URL = "http://192.168.1.100:8000/api";
```

3. Access from phone/other device:
```
http://192.168.1.100:3000
```

---

For full documentation, see main [README.md](../README.md)
