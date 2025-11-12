# UI Module

This module scaffolds the FastAPI endpoints for:
- ROI Editor (`roi_editor.py`): Add, list, and delete regions of interest.
- Event Browser (`event_browser.py`): List and add events for demo/testing.
- UI Toggles (`toggles.py`): Enable/disable UI features via API.
- Aggregator (`api.py`): Combines all UI endpoints for easy mounting in the main app.

## Usage
- Mount the `router` from `api.py` in your FastAPI app.
- All endpoints use in-memory stores for demo purposes; replace with persistent storage for production.

## Next Steps
- Add frontend components for ROI editing and event browsing.
- Integrate with main event pipeline and state management.
- Document API schemas and usage examples.
