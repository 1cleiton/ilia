// src/components/OrderListPage.tsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';

interface Customer {
    id: number;
    name: string;
    email: string;
}

interface OrderItem {
    id: number;
    name: string;
    quantity: number;
    total_price: string;
}

interface Order {
    id: number;
    customer: Customer;
    items: OrderItem[];
    total_price: number;
    status: string;
    created_at: string;
}

const OrderListPage: React.FC = () => {
    const [orders, setOrders] = useState<Order[] | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchOrders = async () => {
            setLoading(true);
            setError(null);

            const token = Cookies.get('authToken');

            if (!token) {
                navigate('/login');
                return;
            }

            try {
                const response = await fetch('http://localhost:8001/api/v1/orders', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${token}`,
                    },
                });

                if (response.ok) {
                    const data: Order[] = await response.json();
                    setOrders(data);
                } else if (response.status === 401 || response.status === 403) {
                    Cookies.remove('authToken');
                    navigate('/login');
                    setError('Sessão expirada ou não autorizada. Faça login novamente.');
                } else {
                    const errorData = await response.json();
                    setError(`Erro ao carregar pedidos: ${errorData.detail || response.statusText}`);
                }
            } catch (err) {
                setError('Erro de conexão ao carregar pedidos.');
                console.error('Erro de rede ao carregar pedidos:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchOrders();
    }, [navigate]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-100">
                <p className="text-xl text-gray-700">Carregando pedidos...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-100">
                <p className="text-xl text-red-600">Erro: {error}</p>
            </div>
        );
    }

    if (!orders || orders.length === 0) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-100">
                <p className="text-xl text-gray-700">Você ainda não fez nenhum pedido.</p>
                <button
                    onClick={() => navigate('/products')}
                    className="ml-4 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline transition-colors duration-200"
                >
                    Ir para Produtos
                </button>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-screen-xl mx-auto bg-white p-6 rounded-lg shadow-md">
                <h1 className="text-4xl font-extrabold text-gray-800 mb-8 text-center">Meus Pedidos</h1>

                <div className="space-y-8">
                    {orders.map((order) => (
                        <div key={order.id} className="border border-gray-200 rounded-lg p-6 shadow-sm">
                            <div className="flex justify-between items-center mb-4 border-b pb-3">
                                <h2 className="text-2xl font-bold text-gray-800">Pedido #{order.id}</h2>
                                <span className={`px-3 py-1 rounded-full text-sm font-semibold
                  ${order.status === 'PENDING' ? 'bg-yellow-100 text-yellow-800' :
                                        order.status === 'COMPLETED' ? 'bg-green-100 text-green-800' :
                                            'bg-gray-100 text-gray-800'}`}>
                                    {order.status}
                                </span>
                            </div>

                            <p className="text-gray-600 mb-2">
                                <span className="font-semibold">Data do Pedido:</span> {new Date(order.created_at).toLocaleString('pt-BR')}
                            </p>
                            <p className="text-gray-600 mb-4">
                                <span className="font-semibold">Total:</span> R$ {order.total_price.toFixed(2).replace('.', ',')}
                            </p>

                            <h3 className="text-xl font-semibold text-gray-700 mb-3">Itens:</h3>
                            <ul className="list-disc pl-5 space-y-2">
                                {order.items.map((item) => (
                                    <li key={item.id} className="text-gray-700">
                                        #{item.id} - {item.name} - Qtd: {item.quantity} - Total: R$ {parseFloat(item.total_price).toFixed(2).replace('.', ',')}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default OrderListPage;