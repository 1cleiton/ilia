import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaShoppingCart } from 'react-icons/fa';
import Cookies from 'js-cookie';
import { useCart } from '../context/CartContext';

const Header: React.FC = () => {
    const navigate = useNavigate();
    const { getTotalItems, clearCart } = useCart();

    const handleLogout = () => {
        Cookies.remove('authToken');
        clearCart();
        navigate('/login');
    };

    return (
        <header className="bg-blue-700 p-4 shadow-md">
            <div className="max-w-screen-xl mx-auto flex justify-between items-center">
                <h1 className="text-white text-3xl font-extrabold cursor-pointer" onClick={() => navigate('/products')}>
                    Minha Loja
                </h1>

                <nav className="flex items-center space-x-6">
                    <div
                        className="relative cursor-pointer text-white hover:text-blue-200 transition-colors duration-200"
                        onClick={() => navigate('/cart')}
                    >
                        <FaShoppingCart className="h-7 w-7" />
                        {getTotalItems() > 0 && (
                            <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                                {getTotalItems()}
                            </span>
                        )}
                    </div>

                    <button
                        onClick={handleLogout}
                        className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-5 rounded-lg focus:outline-none focus:shadow-outline transition-colors duration-200"
                    >
                        Sair
                    </button>
                </nav>
            </div>
        </header>
    );
};

export default Header;