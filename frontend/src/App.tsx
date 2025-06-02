import { Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import ProductListPage from './components/ProductListPage';
import CartPage from './components/CartPage';
import OrderListPage from './components/OrderListPage';
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
        <Route path="/cart" element={<CartPage />} />
        <Route path="/orders" element={<OrderListPage />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </>
  );
}

export default App;