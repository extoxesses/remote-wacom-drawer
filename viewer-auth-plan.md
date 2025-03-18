# Viewer Authentication Implementation Plan

## Overview
Update the viewer.html page to support manual WebSocket connection using drawer ID and secret credentials.

## Technical Details

### UI Updates
1. Add input fields for credentials:
```html
<div id="credentials">
    <div>
        <label for="drawerId">Id:</label>
        <input type="text" id="drawerId">
    </div>
    <div>
        <label for="drawerSecret">Secret:</label>
        <input type="text" id="drawerSecret">
    </div>
</div>
```

### JavaScript Implementation
1. Remove hardcoded credentials
2. Add connect button handler:
```javascript
document.getElementById('connectButton').addEventListener('click', () => {
    const drawerId = document.getElementById('drawerId').value;
    const drawerSecret = document.getElementById('drawerSecret').value;
    
    // Store in localStorage for persistence
    localStorage.setItem('authorization', JSON.stringify({
        'api-key': drawerId,
        'api-secret': drawerSecret
    }));
    
    // Connect to server
    socket = connectToServer({
        'api-key': drawerId,
        'api-secret': drawerSecret,
        role: 'drawer'
    });
    
    setSharedConfigurations();
    configViewer(socket, '{{drawer_button}}', '{{eraser_button}}');
});
```

## Implementation Steps

1. Update viewer.html:
   - Replace label elements with input fields for drawerId and drawerSecret
   - Remove automatic WebSocket connection
   - Update connect button click handler
   - Move connection logic into the button click handler

2. Error Handling:
   - Add validation for required fields
   - Display connection status updates to user
   - Handle reconnection attempts properly

## Notes
- Connection is manual via the connect button
- Credentials are stored in localStorage for persistence
- No changes needed to Flask routes
- Existing socket connection and event handling remains unchanged