# Visual Task Board - Frontend

Vue.js-based user interface for the Visual Task Board application.

## Technology Stack

- **Framework**: Vue 3
- **State Management**: Vuex 4
- **HTTP Client**: Axios
- **Drag & Drop**: Vue.Draggable
- **Testing**: Jest, Vue Test Utils
- **Code Formatting**: ESLint, Prettier

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Vue components
│   ├── store/          # Vuex store modules
│   ├── services/       # API service layer
│   ├── App.vue         # Root component
│   └── main.js         # Application entry point
├── tests/
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
└── public/             # Static assets
```

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Run Development Server

```bash
npm run serve
```

The application will be available at `http://localhost:8080`

### 3. Build for Production

```bash
npm run build
```

## Testing

Run unit tests:
```bash
npm run test:unit
```

Run with coverage:
```bash
npm run test:coverage
```

## Code Quality

Lint code:
```bash
npm run lint
```

Format code with Prettier:
```bash
npx prettier --write "src/**/*.{js,vue}"
```

## Components

- **BoardList**: Displays all boards and allows creating new boards
- **Board**: Shows a single board with its lists
- **List**: Displays a list with its cards and supports drag & drop
- **Card**: Shows a card and handles click events
- **CardDetail**: Modal for viewing and editing card details
- **AddButton**: Reusable button component for adding items

## State Management

The application uses Vuex for state management with three modules:

- **boards**: Manages board data and operations
- **lists**: Manages list data and operations
- **cards**: Manages card data and operations

## API Integration

All API calls are centralized in `src/services/api.js` using Axios with:
- Request/response interceptors
- Error handling
- Base URL configuration
