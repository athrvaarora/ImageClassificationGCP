import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist'
  },
  define: {
    'process.env.VITE_API_URL': JSON.stringify(process.env.VITE_API_URL || 'http://localhost:5000')
  },
  server: {
    proxy: {
      '/api': 'http://localhost:5000',
      '/classified_images': 'http://localhost:5000'
    }
  }
});