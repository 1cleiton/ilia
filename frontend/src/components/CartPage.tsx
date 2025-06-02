import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { FaPlus, FaMinus, FaTrashAlt } from 'react-icons/fa';
import type { CartItem } from '../types/product';
import Cookies from 'js-cookie';

const CartPage: React.FC = () => {
    const { cartItems, addToCart, removeFromCart, removeItem, clearCart } = useCart();
    const navigate = useNavigate();

    const calculateTotal = () => {
        return cartItems.reduce((acc, item) => acc + item.price * item.quantity, 0);
    };

    const calculateItemSubtotal = (item: CartItem): string => {
        return (item.price * item.quantity).toFixed(2).replace('.', ',');
    };

    const handleCheckout = async () => {
        if (cartItems.length === 0) {
            alert('Seu carrinho está vazio. Adicione itens antes de finalizar a compra.');
            return;
        }

        const token = Cookies.get('authToken');
        if (!token) {
            alert('Você precisa estar logado para finalizar a compra.');
            navigate('/login');
            return;
        }

        const orderItems = cartItems.map(item => ({
            id: item.id,
            quantity: item.quantity
        }));

        const payload = {
            items: orderItems
        };

        try {
            const response = await fetch('http://localhost:8001/api/v1/orders/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                alert('Compra finalizada com sucesso! Seu pedido foi enviado.');
                clearCart();
                navigate('/products');
            } else {
                const errorData = await response.json();
                alert(`Erro ao finalizar a compra: ${errorData.detail || response.statusText}`);
                console.error('Erro ao finalizar compra:', errorData);
            }
        } catch (error) {
            alert('Erro de conexão ao tentar finalizar a compra.');
            console.error('Erro de rede:', error);
        }
    };


    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-screen-xl mx-auto bg-white p-6 rounded-lg shadow-md">
                <h1 className="text-4xl font-extrabold text-gray-800 mb-8 text-center">Seu Carrinho</h1>

                {cartItems.length === 0 ? (
                    <div className="text-center py-10">
                        <p className="text-xl text-gray-600 mb-4">Seu carrinho está vazio!</p>
                        <button
                            onClick={() => navigate('/products')}
                            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg focus:outline-none focus:shadow-outline transition-colors duration-200"
                        >
                            Voltar às Compras
                        </button>
                    </div>
                ) : (
                    <div>
                        <div className="hidden md:grid grid-cols-6 gap-4 py-3 px-2 mb-4 font-semibold text-gray-700 border-b border-gray-200">
                            <div className="col-span-2">Produto</div>
                            <div className="text-center">Preço Un.</div>
                            <div className="text-center">Qtd.</div>
                            <div className="text-center">Subtotal</div>
                            <div className="text-center">Ações</div>
                        </div>

                        {cartItems.map((item) => (
                            <div key={item.id} className="grid grid-cols-1 md:grid-cols-6 gap-4 items-center border-b border-gray-200 py-4 px-2 last:border-b-0">
                                <div className="col-span-2 flex items-center space-x-4">
                                    <img src={item.image} alt={item.name} className="w-20 h-20 object-cover rounded-md" />
                                    <span className="font-semibold text-gray-800">{item.name}</span>
                                </div>

                                <div className="text-center text-gray-700 md:block">
                                    R$ {item.price.toFixed(2).replace('.', ',')}
                                </div>

                                <div className="flex items-center justify-center space-x-2 text-gray-700">
                                    <button
                                        onClick={() => removeFromCart(item.id)}
                                        className="p-2 rounded-full bg-gray-200 hover:bg-gray-300 transition-colors duration-200"
                                        aria-label="Diminuir quantidade"
                                    >
                                        <FaMinus className="w-4 h-4" />
                                    </button>
                                    <span className="font-bold text-lg w-8 text-center">{item.quantity}</span>
                                    <button
                                        onClick={() => addToCart(item)} // Passa o item completo para addToCart
                                        className="p-2 rounded-full bg-gray-200 hover:bg-gray-300 transition-colors duration-200"
                                        aria-label="Aumentar quantidade"
                                    >
                                        <FaPlus className="w-4 h-4" />
                                    </button>
                                </div>

                                <div className="text-center text-lg font-bold text-gray-900 md:block">
                                    R$ {calculateItemSubtotal(item)}
                                </div>

                                <div className="text-center">
                                    <button
                                        onClick={() => removeItem(item.id)}
                                        className="p-2 rounded-full bg-red-100 text-red-600 hover:bg-red-200 transition-colors duration-200"
                                        aria-label="Remover item"
                                    >
                                        <FaTrashAlt className="w-5 h-5" />
                                    </button>
                                </div>
                            </div>
                        ))}


                        <div className="mt-8 pt-4 border-t-2 border-gray-300 flex flex-col md:flex-row justify-between items-center">
                            <div className="text-2xl font-bold text-gray-900 mb-4 md:mb-0">
                                Total do Carrinho: R$ {calculateTotal().toFixed(2).replace('.', ',')}
                            </div>
                            <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4">
                                <button
                                    onClick={clearCart}
                                    className="bg-gray-400 hover:bg-gray-500 text-white font-bold py-3 px-6 rounded-lg focus:outline-none focus:shadow-outline transition-colors duration-200 w-full md:w-auto"
                                >
                                    Limpar Carrinho
                                </button>
                                <button
                                    onClick={handleCheckout}
                                    className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg focus:outline-none focus:shadow-outline transition-colors duration-200 w-full md:w-auto"
                                >
                                    Finalizar Compra
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CartPage;