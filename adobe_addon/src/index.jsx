import React from 'react';
import { createRoot } from 'react-dom/client';
import { AddOnProvider } from '@adobe/add-on-sdk';
import App from './app';

const root = createRoot(document.getElementById('root'));

root.render(
    <React.StrictMode>
        <AddOnProvider>
            <App />
        </AddOnProvider>
    </React.StrictMode>
);