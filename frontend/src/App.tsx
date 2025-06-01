import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import ProductListPage from './components/ProductListPage';
import Header from './components/Header';

import './index.css';

function App() {
  return (
    <> { }
      { }
      <Header />

      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/products" element={<ProductListPage />} />
        { }
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </>
  );
}

export default App;